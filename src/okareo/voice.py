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
        logger.debug(f"🔈 Voice file uploaded to {response.file_url}")
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
        logger.debug(f"✅ Session started: {session_id}")
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
