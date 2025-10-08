import asyncio
import base64
import io
import json
import logging
import os
import tempfile
import time
import uuid
import wave
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

import numpy as np
import requests
import websockets
from scipy.signal import resample_poly

from okareo import Okareo
from okareo.model_under_test import (
    CustomMultiturnTargetAsync,
    ModelInvocation,
)

logger = logging.getLogger(__name__)


# --------------------- config ----------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY, "Set OPENAI_API_KEY"


API_SR = 24000  # 24 kHz PCM16 mono
CHUNK_MS = 120  # stream in ~120ms chunks


# ---------------- utils: TTS + ASR + WAV + chunking ----------------
def tts_pcm16(text: str, voice: str = "echo", target_sr: int = API_SR) -> bytes:
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini-tts",
        "voice": voice,
        "input": text,
        "response_format": "pcm",
    }
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    native_sr = 24000
    audio = np.frombuffer(r.content, dtype=np.int16)
    if target_sr != native_sr:
        audio = resample_poly(audio, target_sr, native_sr).astype(np.int16)
    return audio.tobytes()


def chunk_bytes(pcm_bytes: bytes, ms: int, sr: int) -> list[bytes]:
    """Split PCM16 mono bytes into ~ms chunks."""
    bytes_per_ms = sr * 2 // 1000  # 2 bytes/sample, mono
    step = max(2, bytes_per_ms * ms)
    return [pcm_bytes[i : i + step] for i in range(0, len(pcm_bytes), step)]


def wav_from_pcm16(pcm_bytes: bytes, sr: int) -> bytes:
    """Wrap raw PCM16 in a WAV container and return bytes."""
    bio = io.BytesIO()
    with wave.open(bio, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm_bytes)
    return bio.getvalue()


async def asr_openai_from_pcm16(
    pcm_bytes: bytes, sr: int, model: str = "gpt-4o-mini-transcribe"
) -> str:
    """Async wrapper around /v1/audio/transcriptions."""
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    wav_bytes = wav_from_pcm16(pcm_bytes, sr)

    def _post() -> requests.Response:
        files = {"file": ("agent.wav", wav_bytes, "audio/wav")}
        data = {"model": model, "response_format": "json", "temperature": "0"}
        return requests.post(url, headers=headers, files=files, data=data, timeout=120)

    resp = await asyncio.to_thread(_post)
    resp.raise_for_status()
    return str(resp.json().get("text", "")).strip()


def save_wav_pcm16(pcm: bytes, sr: int, prefix: str) -> str:
    """Write PCM16 mono @ sr to a temp .wav and return the path."""
    fd, path = tempfile.mkstemp(prefix=prefix, suffix=".wav")
    os.close(fd)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm)
    return path


# ---------------- vendor/protocol abstraction ----------------


class VoiceEdge(ABC):
    """
    Protocol/vendored WSS details live here.
    - connect(): set up WSS and any session state
    - send_pcm(): stream user PCM -> receive agent PCM
    - close(): close socket
    """

    def __init__(self, edge_config: "EdgeConfig"):
        self.edge_config = edge_config
        self.ws: Any = None

    @abstractmethod
    async def connect(self, **kwargs: Any) -> None: ...

    @abstractmethod
    async def send_pcm(
        self, pcm16: bytes, pace_realtime: bool = True, timeout_s: float = 20.0
    ) -> tuple[bytes, Dict[str, Any]]: ...

    @abstractmethod
    async def close(self) -> None: ...

    def is_connected(self) -> bool:
        return self.ws is not None


class EdgeConfig(ABC):
    """Typed build instructions. Creates a new edge each time."""

    sr: int = API_SR
    chunk_ms: int = CHUNK_MS
    api_key: str = ""
    model: str = ""
    instructions: str = "Be brief and helpful."
    output_voice: str = ""

    @abstractmethod
    def create(self) -> VoiceEdge: ...


@dataclass
class OpenAIEdgeConfig(EdgeConfig):
    api_key: str
    model: str = "gpt-realtime"
    sr: int = API_SR
    chunk_ms: int = CHUNK_MS
    instructions: str = "Be brief and helpful."
    output_voice: str = "alloy"

    def create(self) -> VoiceEdge:
        return OpenAIRealtimeEdge(self)


@dataclass
class DeepgramEdgeConfig(EdgeConfig):
    api_key: str
    sr: int = API_SR
    chunk_ms: int = CHUNK_MS
    instructions: str = "Be brief and helpful."
    output_voice: str = "aura-2-thalia-en"

    def create(self) -> VoiceEdge:
        return DeepgramRealtimeEdge(self)

@dataclass
class TwilioEdgeConfig(EdgeConfig):
    """Configuration for Twilio Media Streams integration.
    
    Twilio is just audio transport over phone lines - no LLM involved.
    Audio is mulaw-encoded at 8kHz.
    
    Args:
        account_sid: Twilio Account SID (for verification)
        auth_token: Twilio Auth Token (for verification)
        phone_number: Your Twilio phone number (e.g., +1234567890)
        sr: Sample rate (defaults to 8000 for Twilio)
        chunk_ms: Chunk size in milliseconds
        server_port: Port for the WebSocket server (default 8080)
        use_ngrok: Whether to automatically expose via ngrok (default True for testing)
    """
    account_sid: str = ""
    auth_token: str = ""
    phone_number: str = ""
    sr: int = 8000  # Twilio uses 8kHz
    chunk_ms: int = 20  # Twilio typically uses 20ms chunks
    server_port: int = 8080
    use_ngrok: bool = True
    
    def create(self) -> VoiceEdge:
        return TwilioRealtimeEdge(self)

# ---------------- OpenAI Realtime implementation ----------------
class OpenAIRealtimeEdge(VoiceEdge):
    AUDIO_DONE_TYPES = {
        "response.output_audio.done",
        "response.audio.done",
        "output_audio.done",
    }
    RESP_FINAL_TYPES = {"response.done", "response.completed"}

    def __init__(self, cfg: OpenAIEdgeConfig):
        super().__init__(cfg)
        assert cfg.api_key, "OpenAI API key required"

        self.ws_url = f"wss://api.openai.com/v1/realtime?model={self.edge_config.model}"
        self._connected = False

    async def connect(self, **kwargs: Any) -> None:
        headers = [("Authorization", f"Bearer {self.edge_config.api_key}")]
        self.ws = await websockets.connect(
            self.ws_url, additional_headers=headers, max_size=None
        )
        # swallow a possible first event
        try:
            _ = json.loads(await asyncio.wait_for(self.ws.recv(), timeout=0.3))
        except asyncio.TimeoutError:
            pass

        # Configure session: manual commit & manual response.create
        await self.ws.send(
            json.dumps(
                {
                    "type": "session.update",
                    "session": {
                        "type": "realtime",
                        "model": self.edge_config.model,
                        "output_modalities": ["audio"],
                        "audio": {
                            "input": {
                                "format": {
                                    "type": "audio/pcm",
                                    "rate": self.edge_config.sr,
                                },
                                "turn_detection": {
                                    "type": "semantic_vad",
                                    "create_response": False,
                                    "interrupt_response": True,
                                },
                            },
                            "output": {
                                "format": {
                                    "type": "audio/pcm",
                                    "rate": self.edge_config.sr,
                                },
                                "voice": self.edge_config.output_voice,
                                "speed": 1.0,
                            },
                        },
                        "instructions": self.edge_config.instructions,
                    },
                }
            )
        )
        self._connected = True

    async def send_pcm(
        self, pcm16: bytes, pace_realtime: bool = True, timeout_s: float = 30.0
    ) -> tuple[bytes, Dict[str, Any]]:
        assert self.ws and self._connected, "Call connect() first."

        # Stream audio chunks
        await self._send_audio_chunks(pcm16, pace_realtime)

        # Collect response
        return await self._collect_response(timeout_s)

    async def _send_audio_chunks(self, pcm16: bytes, pace_realtime: bool) -> None:
        """Send audio chunks to OpenAI Realtime API."""
        assert self.ws is not None, "WebSocket not connected"
        chunks = chunk_bytes(pcm16, self.edge_config.chunk_ms, self.edge_config.sr)
        bytes_per_sec = self.edge_config.sr * 2

        for chunk in chunks:
            await self.ws.send(
                json.dumps(
                    {
                        "type": "input_audio_buffer.append",
                        "audio": base64.b64encode(chunk).decode("ascii"),
                    }
                )
            )
            if pace_realtime:
                await asyncio.sleep(max(0.001, len(chunk) / bytes_per_sec))

        await self.ws.send(json.dumps({"type": "input_audio_buffer.commit"}))
        await self.ws.send(json.dumps({"type": "response.create", "response": {}}))

    async def _collect_response(self, timeout_s: float) -> tuple[bytes, Dict[str, Any]]:
        """Collect audio response from OpenAI Realtime API."""
        assert self.ws is not None, "WebSocket not connected"
        audio_buf = bytearray()
        audio_finalized = False
        resp_finalized = False
        started = time.time()
        event_count = 0

        while True:
            if (time.time() - started) > timeout_s:
                break

            evt = json.loads(await asyncio.wait_for(self.ws.recv(), timeout=timeout_s))
            event_count += 1
            event_type = evt.get("type")

            if event_type in (
                "response.output_audio.delta",
                "response.audio.delta",
                "output_audio.delta",
            ):
                b64 = evt.get("delta") or evt.get("audio")
                if b64:
                    audio_buf += base64.b64decode(b64)

            elif event_type in self.AUDIO_DONE_TYPES:
                audio_finalized = True

            elif event_type in self.RESP_FINAL_TYPES:
                resp_finalized = True

            elif event_type == "error":
                logger.error("OpenAI Realtime error: %s", evt)
                resp_finalized = True

            if audio_finalized and resp_finalized:
                break

        return bytes(audio_buf), {"events": event_count}

    async def close(self) -> None:
        if self.ws:
            await self.ws.close()
            self.ws = None
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected


# ---------------- Deepgram VoiceEdge implementation ----------------
class DeepgramRealtimeEdge(VoiceEdge):
    def __init__(self, cfg: DeepgramEdgeConfig):
        super().__init__(cfg)
        assert cfg.api_key, "Deepgram API key required"

        self.ws_url = "wss://agent.deepgram.com/v1/agent/converse"
        self._connected = False
        self._audio_buf = bytearray()
        self._agent_turn_complete = asyncio.Event()
        self._recv_task: Optional[asyncio.Task[None]] = None
        self._stop_recv = asyncio.Event()
        self._keepalive_task: Optional[asyncio.Task[None]] = None
        self._keepalive_stop_event = asyncio.Event()

    async def connect(self, **kwargs: Any) -> None:
        self.ws = await websockets.connect(
            self.ws_url,
            subprotocols=["token", self.edge_config.api_key],  # type: ignore[list-item]
        )
        config_message = {
            "type": "Settings",
            "audio": {
                "input": {
                    "encoding": "linear16",
                    "sample_rate": self.edge_config.sr,
                },
                "output": {
                    "encoding": "linear16",
                    "sample_rate": self.edge_config.sr,
                    "container": "none",
                },
            },
            "agent": {
                "language": "en",
                "listen": {
                    "provider": {
                        "type": "deepgram",
                        "model": "nova-3",
                        "keyterms": ["hello", "goodbye"],
                    }
                },
                "think": {
                    "provider": {
                        "type": "open_ai",
                        "model": "gpt-4o-mini",
                        "temperature": 0.7,
                    },
                    "prompt": self.edge_config.instructions,
                },
                "speak": {
                    "provider": {
                        "type": "deepgram",
                        "model": self.edge_config.output_voice,
                    }
                },
                "greeting": "Hello! How can I help you today?",
            },
        }
        await self.ws.send(json.dumps(config_message))

        # Create keep alive ping
        async def send_keep_alive(stop_event: asyncio.Event) -> None:
            try:
                assert self.ws is not None, "WebSocket not connected"
                while not stop_event.is_set():
                    await asyncio.sleep(5)
                    logger.debug("Keep alive!")
                    await self.ws.send(json.dumps({"type": "KeepAlive"}))
            except websockets.exceptions.ConnectionClosed:
                pass

        self._keepalive_stop_event.clear()
        self._keepalive_task = asyncio.create_task(
            send_keep_alive(self._keepalive_stop_event)
        )

        # start recv loop
        self._stop_recv.clear()
        self._recv_task = asyncio.create_task(self._recv_loop())

        # Wait for greeting
        while not self._agent_turn_complete.is_set():
            await asyncio.sleep(0.05)
        self._agent_turn_complete.clear()
        self._connected = True

    async def _recv_loop(self) -> None:
        try:
            assert self.ws is not None, "WebSocket not connected"
            while not self._stop_recv.is_set():
                raw = await self.ws.recv()
                if isinstance(raw, str):
                    try:
                        logger.debug(raw)
                        evt = json.loads(raw)
                        self._handle_message_event(evt)
                    except json.JSONDecodeError:
                        logger.warning(f"[WARN] non-JSON frame: {raw!r}")
                elif isinstance(raw, bytes):
                    self._audio_buf.extend(raw)

        except websockets.exceptions.ConnectionClosed:
            pass

    def _handle_message_event(self, evt: Dict[str, Any]) -> None:
        etype = evt.get("type")
        if etype == "AgentAudioDone":
            self._agent_turn_complete.set()

    async def send_pcm(
        self,
        pcm16: bytes,
        pace_realtime: bool = True,
        timeout_s: float = 30.0,
        add_silence_ms: int = 400,
    ) -> tuple[bytes, Dict[str, Any]]:
        assert self.ws and self._connected, "Call connect() first."
        self._audio_buf = bytearray()
        self._agent_turn_complete.clear()

        def add_silence(pcm: bytes, sr: int, ms: int = 400) -> bytes:
            return pcm + (b"\x00\x00" * int(sr * ms / 1000))

        pcm16 = add_silence(pcm16, self.edge_config.sr, add_silence_ms)

        chunks = chunk_bytes(pcm16, self.edge_config.chunk_ms, self.edge_config.sr)
        bytes_per_sec = self.edge_config.sr * 2
        for ch in chunks:
            await self.ws.send(ch)
            if pace_realtime:
                await asyncio.sleep(max(0.001, len(ch) / bytes_per_sec))
        # Wait for agent response
        try:
            await asyncio.wait_for(self._agent_turn_complete.wait(), timeout=timeout_s)
        except asyncio.TimeoutError:
            # Deepgram isn't consistently sending the AgentAudioDone event
            logger.warning("Timeout: Agent turn did not complete within timeout")

        pcm_result = bytes(self._audio_buf)
        self._audio_buf = bytearray()
        return pcm_result, {}

    async def close(self) -> None:
        if self.ws:
            self._stop_recv.set()
            self._keepalive_stop_event.set()

            await self.ws.close()

            if self._recv_task:
                await self._recv_task

            if self._keepalive_task:
                await self._keepalive_task

            self.ws = None

        self._connected = False

    def is_connected(self) -> bool:
        return self._connected

# ---------------- Twilio VoiceEdge implementation ----------------
class TwilioRealtimeEdge(VoiceEdge):
    """
    Twilio Media Streams integration for real-time phone audio.
    
    Twilio is just the phone audio transport layer - no LLM involved.
    The actual AI/agent logic runs separately (e.g., OpenAI, Deepgram).
    
    This edge handles:
    1. Receiving WebSocket connection from Twilio
    2. Audio format conversion (mulaw <-> PCM16)
    3. Bidirectional audio streaming
    
    For testing, it can automatically start an aiohttp server + ngrok.
    For production, you'd integrate with your existing server infrastructure.
    """
    
    def __init__(self, cfg: TwilioEdgeConfig):
        super().__init__(cfg)
        self._connected = False
        self._audio_buf = bytearray()
        self._stream_sid: Optional[str] = None
        self._call_sid: Optional[str] = None
        self._recv_task: Optional[asyncio.Task[None]] = None
        self._stop_recv = asyncio.Event()
        self._audio_ready = asyncio.Event()
        self.ws: Optional[Any] = None
        self._server_app: Optional[Any] = None
        self._server_runner: Optional[Any] = None  # Add this
        self._server_task: Optional[asyncio.Task[None]] = None
        self._ngrok_url: Optional[str] = None
        
    def _mulaw_to_pcm16(self, mulaw_bytes: bytes) -> bytes:
        """Convert mulaw audio to PCM16."""
        import audioop
        return audioop.ulaw2lin(mulaw_bytes, 2)
    
    def _pcm16_to_mulaw(self, pcm16_bytes: bytes) -> bytes:
        """Convert PCM16 audio to mulaw."""
        import audioop
        return audioop.lin2ulaw(pcm16_bytes, 2)
    
    def _resample_pcm16(self, pcm_bytes: bytes, from_sr: int, to_sr: int) -> bytes:
        """Resample PCM16 audio."""
        if from_sr == to_sr:
            return pcm_bytes
        
        audio = np.frombuffer(pcm_bytes, dtype=np.int16)
        from math import gcd
        ratio_gcd = gcd(to_sr, from_sr)
        up = to_sr // ratio_gcd
        down = from_sr // ratio_gcd
        resampled = resample_poly(audio, up, down).astype(np.int16)
        return resampled.tobytes()
    
    async def connect(self, websocket: Optional[Any] = None, to_number: Optional[str] = None, **kwargs: Any) -> None:
        """
        Connect to Twilio Media Stream.
        
        Three modes:
        1. Pass existing websocket from your server: connect(websocket=ws)
        2. Auto-start server for incoming calls: connect()
        3. Auto-start server and make outbound call: connect(to_number="+15555551234")
        
        Args:
            websocket: Optional WebSocket from Twilio (if you're running your own server)
            to_number: Phone number to call (for outbound calls, e.g., "+15555551234")
            **kwargs: Additional options
        """
        if websocket:
            # Mode 1: Use provided WebSocket (your own server)
            self.ws = websocket
            self._stop_recv.clear()
            self._recv_task = asyncio.create_task(self._recv_loop())
            
            await asyncio.wait_for(self._wait_for_connected(), timeout=10.0)
            self._connected = True
            logger.info(f"Connected to Twilio Media Stream: {self._stream_sid}")
        else:
            # Mode 2 or 3: Auto-start server
            await self._start_test_server()
            
            # If to_number provided, initiate outbound call
            if to_number:
                await self._initiate_outbound_call(to_number)
    
    async def _initiate_outbound_call(self, to_number: str) -> None:
        """Initiate an outbound call via Twilio API."""
        cfg = self.edge_config
        if not cfg.account_sid or not cfg.auth_token or not cfg.phone_number:
            raise ValueError(
                "Outbound calls require account_sid, auth_token, and phone_number. "
                "Set these in TwilioEdgeConfig."
            )
        
        logger.info(f"Initiating outbound call to {to_number}...")
        
        # Determine the stream URL
        if not self._ngrok_url:
            logger.error("Ngrok URL not available. Cannot make outbound call.")
            raise ValueError("Ngrok tunnel required for outbound calls. Set use_ngrok=True in TwilioEdgeConfig.")
        
        stream_url = self._ngrok_url.replace("https://", "wss://").replace("http://", "ws://")
        stream_url = f"{stream_url}/media-stream"
        
        logger.info(f"Stream URL: {stream_url}")
        
        # Create TwiML with Stream
        twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="{stream_url}" />
    </Connect>
</Response>'''
        
        # Call Twilio API
        try:
            from twilio.rest import Client
        except ImportError:
            raise ImportError(
                "Outbound calls require the twilio package. "
                "Install with: pip install twilio"
            )
        
        client = Client(cfg.account_sid, cfg.auth_token)
        
        # Make the call
        call = client.calls.create(
            twiml=twiml,
            to=to_number,
            from_=cfg.phone_number,
            status_callback_event=['initiated', 'ringing', 'answered', 'completed'],
            status_callback_method='POST'
        )
        
        self._call_sid = call.sid
        logger.info(f"Call initiated: {call.sid}")
        logger.info(f"Calling {to_number}...")
        logger.info("Waiting for call to be answered and stream to connect...")
        logger.info("(This may take 30-60 seconds depending on answer time)")
        
        # Wait for the call to connect and stream to start
        timeout = 60.0  # Increase timeout to 60 seconds
        try:
            await asyncio.wait_for(self._wait_for_connected(), timeout=timeout)
            self._connected = True
            logger.info(f"✅ Call connected! Stream: {self._stream_sid}")
        except asyncio.TimeoutError:
            logger.error(f"❌ Call did not connect within {timeout}s.")
            logger.error("\nPossible issues:")
            logger.error("1. The number did not answer the call")
            logger.error("2. Ngrok free tier is blocking WebSocket connections")
            logger.error("   → Try using ngrok's paid tier or deploy to a public server")
            logger.error("3. Firewall or network issues preventing WebSocket connection")
            logger.error(f"4. Check Twilio call logs: https://console.twilio.com/us1/monitor/logs/calls/{call.sid}")
            
            # Try to get call status
            try:
                call_status = client.calls(call.sid).fetch()
                logger.error(f"   Call status: {call_status.status}")
                logger.error(f"   Call duration: {call_status.duration}")
            except Exception:
                pass
            
            raise TimeoutError(
                f"Call did not connect within {timeout}s. See logs above for troubleshooting."
            )

    async def _start_test_server(self) -> None:
        """Start aiohttp server + ngrok for testing."""
        from aiohttp import web
        
        logger.info("Starting test server for Twilio...")
        
        # Store reference to this edge so handlers can access it
        edge_instance = self
        
        async def voice_webhook(request: Any) -> Any:
            """HTTP webhook that returns TwiML."""
            host = request.host
            protocol = "wss" if edge_instance._ngrok_url and "https" in edge_instance._ngrok_url else "ws"
            stream_url = edge_instance._ngrok_url.replace("https://", "wss://").replace("http://", "ws://") if edge_instance._ngrok_url else f"{protocol}://{host}"
            stream_url = f"{stream_url}/media-stream"
            
            twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="{stream_url}" />
    </Connect>
</Response>'''
            return web.Response(text=twiml, content_type="application/xml")
        
        async def media_stream_handler(request: Any) -> Any:
            """WebSocket handler."""
            ws = web.WebSocketResponse()
            await ws.prepare(request)
            
            logger.info("Twilio Media Stream connected")
            edge_instance.ws = ws
            edge_instance._stop_recv.clear()
            edge_instance._recv_task = asyncio.create_task(edge_instance._recv_loop())
            
            try:
                await asyncio.wait_for(edge_instance._wait_for_connected(), timeout=10.0)
                edge_instance._connected = True
                logger.info(f"Stream ready: {edge_instance._stream_sid}")
                
                # Keep connection alive
                while edge_instance.is_connected():
                    await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Error in media stream: {e}")
            
            return ws
        
        # Create app
        app = web.Application()
        app.router.add_post('/voice', voice_webhook)
        app.router.add_get('/media-stream', media_stream_handler)
        
        self._server_app = app
        
        # Start server in background
        from aiohttp.web_runner import AppRunner, TCPSite
        runner = AppRunner(app)
        await runner.setup()
        site = TCPSite(runner, '0.0.0.0', self.edge_config.server_port)
        await site.start()
        
        # Store runner so we can clean it up later
        self._server_runner = runner
        
        local_url = f"http://localhost:{self.edge_config.server_port}"
        logger.info(f"Server started on {local_url}")
        
        # Start ngrok if enabled
        if self.edge_config.use_ngrok:
            try:
                from pyngrok import ngrok
                
                # Kill any existing tunnels to avoid conflicts
                try:
                    ngrok.kill()
                except Exception:
                    pass
                
                # Start ngrok with explicit configuration
                tunnel = ngrok.connect(
                    self.edge_config.server_port, 
                    "http",
                    bind_tls=True  # Force HTTPS
                )
                self._ngrok_url = tunnel.public_url
                logger.info(f"Public URL (ngrok): {self._ngrok_url}")
                logger.info(f"WebSocket URL: {self._ngrok_url.replace('https://', 'wss://')}/media-stream")
                
                # Give ngrok a moment to fully initialize
                await asyncio.sleep(2)
                
                # Verify tunnel is working and not blocked by free tier
                tunnel_ok = await self._verify_ngrok_tunnel()
                if not tunnel_ok:
                    # Don't raise here, just warn - user might want to proceed anyway
                    logger.warning("")
                    logger.warning("⚠️ Continuing anyway, but outbound calls will likely fail...")
                    logger.warning("")
                
            except ImportError:
                logger.warning("pyngrok not installed. Install with: pip install pyngrok")
                logger.info(f"Configure Twilio webhook to: {local_url}/voice")
            except Exception as e:
                logger.error(f"Could not start ngrok: {e}")
                logger.info(f"Configure Twilio webhook to: {local_url}/voice")
                logger.error("\n⚠️ IMPORTANT: Ngrok free tier may block WebSocket connections with an interstitial page.")
                logger.error("   For outbound calls, consider using ngrok's paid tier or deploy to a public server.")
                raise
        
        if not self.edge_config.use_ngrok:
            logger.info(f"Configure Twilio webhook to: {local_url}/voice")
    
    async def _wait_for_connected(self) -> None:
        """Wait for Twilio 'connected' or 'start' event."""
        while not self._stream_sid:
            await asyncio.sleep(0.05)
    
    async def _recv_loop(self) -> None:
        """Receive messages from Twilio."""
        from aiohttp import web
        
        try:
            assert self.ws is not None
            while not self._stop_recv.is_set():
                msg = await self.ws.receive()
                
                # Check if connection is closed
                if msg.type in (web.WSMsgType.CLOSE, web.WSMsgType.CLOSED, web.WSMsgType.CLOSING):
                    logger.debug("WebSocket closed by peer")
                    break
                
                if msg.type == web.WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {self.ws.exception()}")
                    break
                
                if msg.type == web.WSMsgType.TEXT:
                    try:
                        evt = json.loads(msg.data)
                        await self._handle_twilio_event(evt)
                    except json.JSONDecodeError:
                        logger.warning(f"Non-JSON frame: {msg.data!r}")
                        
        except Exception as e:
            if not self._stop_recv.is_set():
                logger.debug(f"Receive loop ended: {e}")
    
    async def _handle_twilio_event(self, evt: Dict[str, Any]) -> None:
        """Handle Twilio Media Stream events."""
        event_type = evt.get("event")
        
        if event_type == "connected":
            self._stream_sid = evt.get("streamSid")
            logger.debug(f"Stream connected: {self._stream_sid}")
            
        elif event_type == "start":
            start_data = evt.get("start", {})
            self._call_sid = start_data.get("callSid")
            self._stream_sid = start_data.get("streamSid")
            logger.debug(f"Call started: {self._call_sid}")
            
        elif event_type == "media":
            payload = evt.get("media", {})
            mulaw_b64 = payload.get("payload", "")
            
            if mulaw_b64:
                mulaw_bytes = base64.b64decode(mulaw_b64)
                pcm16_bytes = self._mulaw_to_pcm16(mulaw_bytes)
                
                # if self.edge_config.sr != 8000:
                #     pcm16_bytes = self._resample_pcm16(pcm16_bytes, 8000, self.edge_config.sr)
                pcm16_bytes = self._resample_pcm16(pcm16_bytes, 8000, 24000) # TODO clean up configuration/constants
                
                self._audio_buf.extend(pcm16_bytes)
                
        elif event_type == "mark":
            logger.debug(f"Mark received: {evt}")
            self._audio_ready.set()
            
        elif event_type == "stop":
            logger.info("Stream stopped by Twilio")
            self._stop_recv.set()
    
    async def send_pcm(
        self,
        pcm16: bytes,
        pace_realtime: bool = True,
        timeout_s: float = 30.0
    ) -> tuple[bytes, Dict[str, Any]]:
        """Send PCM16 audio to Twilio and receive response."""
        assert self.ws and self._connected, "Call connect() first"
        
        self._audio_buf = bytearray()
        self._audio_ready.clear()
        
        # Resample to 8kHz if needed
        # if self.edge_config.sr != 8000:
        #     pcm16 = self._resample_pcm16(pcm16, self.edge_config.sr, 8000)
        pcm16 = self._resample_pcm16(pcm16, 24000, 8000) # TODO clean up configuration/constants
        
        # Convert to mulaw
        mulaw_bytes = self._pcm16_to_mulaw(pcm16)
        
        # Send chunks
        chunks = chunk_bytes(mulaw_bytes, self.edge_config.chunk_ms, 8000)
        bytes_per_sec = 8000
        
        for chunk in chunks:
            mulaw_b64 = base64.b64encode(chunk).decode("ascii")
            media_msg = {
                "event": "media",
                "streamSid": self._stream_sid,
                "media": {"payload": mulaw_b64}
            }
            await self.ws.send_json(media_msg)
            
            if pace_realtime:
                await asyncio.sleep(max(0.001, len(chunk) / bytes_per_sec))
        
        logger.info(f"Sent {len(chunks)} chunks, first chunk size: {len(chunks[0]) if chunks else 0} bytes")
        # Send mark
        mark_msg = {
            "event": "mark",
            "streamSid": self._stream_sid,
            "mark": {"name": f"end_{uuid.uuid4().hex[:8]}"}
        }
        await self.ws.send_json(mark_msg)
        logger.debug(f"Mark message sent {mark_msg}")
        
        # Wait for response
        try:
            await asyncio.wait_for(self._audio_ready.wait(), timeout=timeout_s)
        except asyncio.TimeoutError:
            logger.warning(f"Timeout waiting for audio after {timeout_s}s")
        
        pcm_result = bytes(self._audio_buf)
        return pcm_result, {
            "stream_sid": self._stream_sid,
            "call_sid": self._call_sid,
            "bytes_received": len(pcm_result)
        }
    
    async def close(self) -> None:
        """Close connection and cleanup."""
        logger.info("Closing Twilio connection...")
        
        # Set connected to False FIRST to unblock media_stream_handler
        self._connected = False
        
        # Close WebSocket
        if self.ws:
            # Signal stop to receive loop
            self._stop_recv.set()
            
            # Send stop message to Twilio
            if self._stream_sid:
                try:
                    stop_msg = {"event": "stop", "streamSid": self._stream_sid}
                    await self.ws.send_json(stop_msg)
                except Exception as e:
                    logger.debug(f"Error sending stop message: {e}")
            
            # Close WebSocket connection (this will unblock the receive loop)
            try:
                await self.ws.close()
            except Exception as e:
                logger.debug(f"Error closing WebSocket: {e}")
            
            # Wait for receive task with short timeout, then cancel if needed
            if self._recv_task:
                try:
                    await asyncio.wait_for(self._recv_task, timeout=0.5)
                except asyncio.TimeoutError:
                    logger.debug("Receive task timed out, cancelling")
                    self._recv_task.cancel()
                    try:
                        await self._recv_task
                    except asyncio.CancelledError:
                        pass
                except Exception as e:
                    logger.debug(f"Error waiting for recv task: {e}")
            
            self.ws = None
        
        # Shutdown aiohttp server BEFORE disconnecting ngrok
        if self._server_runner:
            try:
                logger.debug("Shutting down aiohttp server...")
                await self._server_runner.cleanup()
                logger.info("Server shut down")
            except Exception as e:
                logger.warning(f"Error shutting down server: {e}")
            finally:
                self._server_runner = None
                self._server_app = None
        
        # Disconnect ngrok - kill all tunnels to ensure cleanup
        if self._ngrok_url:
            try:
                from pyngrok import ngrok
                logger.debug("Disconnecting ngrok tunnel...")
                # Kill all tunnels instead of just disconnecting one
                ngrok.kill()
                logger.info("Ngrok tunnels closed")
            except Exception as e:
                logger.debug(f"Error disconnecting ngrok: {e}")
            finally:
                self._ngrok_url = None
        
        logger.info("✅ Cleanup complete")

    def is_connected(self) -> bool:
        return self._connected

    async def _verify_ngrok_tunnel(self) -> bool:
        """
        Verify ngrok tunnel is working for Twilio WebSocket connections.
        Returns True if OK, False if there's an issue (like free tier interstitial).
        """
        if not self._ngrok_url:
            return True  # No ngrok, nothing to check
        
        import aiohttp
        
        try:
            # Test the voice webhook endpoint with POST (as Twilio does)
            print(f"Testing ngrok tunnel: {self._ngrok_url}/voice")
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._ngrok_url}/voice", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    response_text = await response.text()
                    logger.debug(f"Ngrok tunnel test response: status={response.status}, content-type={response.headers.get('content-type', '')}, body={response_text[:100]}...")
                    
                    # If we get HTML back, it's likely the ngrok interstitial page
                    content_type = response.headers.get('content-type', '')
                    is_html = 'text/html' in content_type.lower()
                    
                    if is_html and 'ngrok' in response_text.lower():
                        logger.error("❌ NGROK FREE TIER DETECTED!")
                        logger.error("="*60)
                        logger.error("Ngrok's free tier shows an interstitial warning page that")
                        logger.error("blocks automated WebSocket connections from Twilio.")
                        logger.error("")
                        logger.error("Solutions:")
                        logger.error("1. Upgrade to ngrok's paid tier ($8/month)")
                        logger.error("   → No interstitial page, reliable connections")
                        logger.error("")
                        logger.error("2. Use ngrok authtoken with bypass:")
                        logger.error("   → ngrok config add-authtoken <your-token>")
                        logger.error("   → Some accounts support --authtoken flag")
                        logger.error("")
                        logger.error("3. Deploy to a public server (recommended for production):")
                        logger.error("   → AWS, GCP, Heroku, Railway, etc.")
                        logger.error("")
                        logger.error("4. For testing, use INCOMING calls instead:")
                        logger.error("   → Don't pass to_number to connect()")
                        logger.error("   → Manually call your Twilio number")
                        logger.error("="*60)
                        return False
                    
                    # Check if it's actually returning TwiML
                    if response.status == 200:
                        if 'xml' in content_type.lower() or '<Response>' in response_text:
                            logger.info(f"✅ Ngrok tunnel verified (status: {response.status})")
                            return True
                        else:
                            logger.warning(f"⚠️ Unexpected response from /voice endpoint")
                            logger.warning(f"   Content-Type: {content_type}")
                            logger.warning(f"   First 200 chars: {response_text[:200]}")
                            return False
                    else:
                        logger.warning(f"⚠️ Got HTTP {response.status} from /voice endpoint")
                        return False
                        
        except asyncio.TimeoutError:
            logger.warning("⚠️ Timeout connecting to ngrok tunnel")
            logger.warning("   The tunnel might be slow or not working correctly")
            return False
        except Exception as e:
            logger.warning(f"⚠️ Could not verify ngrok tunnel: {e}")
            logger.warning("   Proceeding anyway, but connection may fail")
            return True  # Don't block on verification errors


# ---------------- RealtimeClient: orchestrates TTS/STT/WAV and delegates to VoiceEdge ----------------
class RealtimeClient:
    """
    - connect(): delegates session setup to VoiceEdge
    - send_utterance(text): TTS -> edge.send_pcm -> save WAVs -> ASR -> return
    - close(): delegates to VoiceEdge
    """

    def __init__(
        self,
        edge: VoiceEdge,
        okareo: Okareo,
        api_sr: int = API_SR,
        chunk_ms: int = CHUNK_MS,
        asr_model: str = "gpt-4o-mini-transcribe",
    ):
        self.edge = edge
        self.okareo = okareo
        self.api_sr = int(api_sr)
        self.chunk_ms = int(chunk_ms)
        self.turn = 0
        self.asr_model = asr_model

    async def connect(self, **edge_kwargs: Any) -> None:
        # For OpenAIRealtimeEdge: pass instructions/output_voice here.
        await self.edge.connect(**edge_kwargs)

    async def close(self) -> None:
        await self.edge.close()

    def _store_wav(self, pcm: bytes, prefix: str) -> str:
        """Upload PCM16 audio data and make it publicly accessible."""
        # Create temporary WAV file from PCM data
        local_path = save_wav_pcm16(pcm, self.api_sr, prefix)

        response = self.okareo.upload_voice(local_path)
        logger.debug(f"Voice file uploaded to {response.file_url}")
        return response.file_url

    async def send_utterance(
        self,
        text: str,
        tts_voice: str = "echo",
        pace_realtime: bool = True,
        timeout_s: float = 60.0,
    ) -> Dict[str, Any]:
        assert self.edge.is_connected(), "Call connect() first."
        turn_id = self.turn + 1

        # 1) TTS -> PCM16
        user_pcm = await asyncio.to_thread(tts_pcm16, text, tts_voice, self.api_sr)
        user_wav_path = self._store_wav(user_pcm, prefix=f"user_turn_{turn_id:03d}_")

        # 2) Stream to edge and collect agent PCM
        agent_pcm, vendor_meta = await self.edge.send_pcm(
            user_pcm, pace_realtime=pace_realtime, timeout_s=timeout_s
        )

        # 3) Save agent WAV
        assistant_wav_path = None
        if agent_pcm:
            assistant_wav_path = self._store_wav(
                agent_pcm, prefix=f"agent_turn_{turn_id:03d}_"
            )

        # 4) Run ASR on agent audio
        agent_asr = ""
        if agent_pcm:
            try:
                agent_asr = await asr_openai_from_pcm16(
                    agent_pcm, self.api_sr, model=self.asr_model
                )
            except Exception:
                logger.exception("[ASR ERR] Failed to transcribe agent audio")

        self.turn = turn_id
        return {
            "turn": turn_id,
            "user_wav_path": user_wav_path,
            "assistant_wav_path": assistant_wav_path,
            "agent_asr": agent_asr,
            "bytes": len(agent_pcm) if agent_pcm else 0,
            "vendor_meta": vendor_meta,
        }


# ---------------- SessionManager: session_id -> RealtimeClient ----------------
class SessionManager:
    def __init__(self, cfg: EdgeConfig, okareo: Okareo):
        self.cfg = cfg
        self.okareo = okareo
        self.sessions: dict[str, RealtimeClient] = {}

    async def start(
        self, session_id: str, **edge_connect_kwargs: Any
    ) -> RealtimeClient:
        c = self.sessions.get(session_id)
        if c is None or not c.edge.is_connected():
            edge = self.cfg.create()  # explicit, typed build
            c = RealtimeClient(edge=edge, okareo=self.okareo)
            await c.connect(**edge_connect_kwargs)
            self.sessions[session_id] = c
        return c

    async def send(
        self, session_id: str, text: str, **send_kwargs: Any
    ) -> Dict[str, Any]:
        c = await self.start(session_id)
        return await c.send_utterance(text, **send_kwargs)

    async def end(self, session_id: str) -> None:
        c = self.sessions.pop(session_id, None)
        if c:
            await c.close()

    async def end_all(self) -> None:
        for sid, c in list(self.sessions.items()):
            try:
                await c.close()
            finally:
                self.sessions.pop(sid, None)


# ---------------- Okareo integration: VoiceMultiturnTarget ----------------


class VoiceMultiturnTarget(CustomMultiturnTargetAsync):
    """
    Configured with a vendor-specific VoiceEdge factory.
    Owns a SessionManager and creates a RealtimeClient per session.
    """

    def __init__(self, name: str, edge_config: EdgeConfig):
        super().__init__(name=name)
        self.cfg = edge_config
        self.sessions: Optional[SessionManager] = None  # Initialize sessions as None

    def set_okareo(self, okareo: Okareo) -> None:
        """Set the Okareo instance and create a SessionManager with it."""
        self.sessions = SessionManager(self.cfg, okareo)

    async def start_session(
        self, scenario_input: Optional[Union[dict, list, str]] = None
    ) -> tuple[Optional[str], Optional[ModelInvocation]]:
        assert self.sessions, "SessionManager not initialized with Okareo instance"
        session_id = str(uuid.uuid4())

        # For OpenAIRealtimeEdge: you can pass output_voice via edge_connect_kwargs
        await self.sessions.start(session_id)
        logger.debug(f"Session started: {session_id}")
        return session_id, None

    async def end_session(self, session_id: str) -> None:
        if self.sessions:
            await self.sessions.end(session_id)

    async def invoke(  # type: ignore[override]
        self,
        messages: list[dict[str, str]],
        scenario_input: Optional[Union[dict, list, str]] = None,
        session_id: Optional[str] = None,
    ) -> ModelInvocation:
        try:
            assert self.sessions, "SessionManager not initialized with Okareo instance"
            assert session_id, "Session ID is required"
            tts_voice = "echo"
            if isinstance(scenario_input, dict):
                tts_voice = scenario_input.get("voice", tts_voice)

            res = await self.sessions.send(
                session_id,
                messages[-1]["content"],
                tts_voice=tts_voice,
            )

            logger.debug(f"user message: {messages[-1]['content']}")
            logger.debug(res)

            return ModelInvocation(
                res.get("agent_asr", ""),
                messages,
                {
                    "user_wav_path": res.get("user_wav_path"),
                    "assistant_wav_path": res.get("assistant_wav_path"),
                },
            )
        except Exception as e:
            import traceback

            traceback.print_exc()
            return ModelInvocation(f"API error: {str(e)}", messages, {"error": str(e)})
