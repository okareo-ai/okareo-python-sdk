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
from attrs import define as _attrs_define
from requests.exceptions import HTTPError
from scipy.signal import resample_poly

from okareo import Okareo
from okareo.model_under_test import (
    CustomMultiturnTargetAsync,
    Driver,
    ModelInvocation,
)

logger = logging.getLogger(__name__)


# --------------------- config ----------------------

API_SR = 24000  # 24 kHz PCM16 mono
CHUNK_MS = 120  # stream in ~120ms chunks

AZURE_TTS_KEY = os.environ.get("AZURE_TTS_KEY")
AZURE_TTS_ENDPOINT = os.environ.get("AZURE_TTS_ENDPOINT")

# --------------------- schemas ----------------------

PROFILE_TO_INSTRUCTIONS = {
    "calm": """Voice Affect: Calm, composed, and reassuring; project quiet authority and confidence.
    
Tone: Sincere, empathetic, and gently authoritative—express genuine apology while conveying competence.

Pacing: Steady and moderate; unhurried enough to communicate care, yet efficient enough to demonstrate professionalism.

Emotion: Genuine empathy and understanding; speak with warmth, especially during apologies ("I'm very sorry for any disruption...").

Pronunciation: Clear and precise, emphasizing key reassurances ("smoothly," "quickly," "promptly") to reinforce confidence.

Pauses: Brief pauses after offering assistance or requesting details, highlighting willingness to listen and support.""",
    "angry": """Voice Affect: Firm, tense, and intense; convey controlled frustration or indignation without shouting or hostility. Maintain emotional weight while keeping professionalism intact.

Tone: Sharp and assertive—express dissatisfaction or urgency clearly. The tone should carry authority and conviction, signaling that something is unacceptable or needs immediate attention.

Pacing: Slightly quicker than normal, reflecting agitation or impatience, but remain deliberate enough to ensure every word lands with impact.

Emotion: Controlled anger and frustration—let the listener feel the seriousness and pressure of the moment without losing composure. Subtle edge in the delivery communicates determination and demand for resolution.

Pronunciation: Strong and deliberate articulation; emphasize critical or corrective words (“unacceptable,” “immediate,” “must,” “now”) to underscore seriousness and resolve.

Pauses: Short and pointed, often used to heighten tension or give weight to key phrases, allowing silence to emphasize disapproval or urgency.""",
    "confident": """Voice Affect: Steady, composed, and self-assured; convey authority and expertise with ease and natural control.

Tone: Clear, assertive, and poised—sound knowledgeable and trustworthy without arrogance. The tone should inspire confidence in both message and delivery.

Pacing: Even and deliberate; speak at a measured pace that projects certainty and control while allowing information to land effectively.

Emotion: Subtle conviction and enthusiasm—demonstrate belief in what is being said, maintaining a balanced sense of professionalism and approachability.

Pronunciation: Precise and articulate; emphasize key statements or calls to action (“absolutely,” “clearly,” “without question”) to reinforce leadership and decisiveness.

Pauses: Intentional and strategic, allowing important points to resonate and giving the impression of thoughtfulness and mastery.""",
    "confused": """Voice Affect: Hesitant, uncertain, and slightly puzzled; convey genuine effort to understand while maintaining a polite and approachable demeanor.

Tone: Soft and questioning—express curiosity and mild bewilderment rather than frustration. Sound open to clarification and eager to make sense of the situation.

Pacing: Uneven or slightly halting at times, with natural breaks as if thinking through the situation; avoid excessive pauses that disrupt flow.

Emotion: Mild uncertainty and curiosity—capture the sense of someone trying to piece things together while staying engaged and sincere.

Pronunciation: Clear but occasionally tentative; some words may trail slightly or rise in pitch at the end of sentences to signal questioning (“Wait, so you mean…?” “I’m not sure I follow…”).

Pauses: Frequent but brief; use them to convey processing or reconsideration, giving the sense of someone thinking aloud or seeking confirmation.""",
    "cheerful": """Voice Affect: Bright, lively, and upbeat; convey warmth and friendliness that instantly lifts the listener’s mood.

Tone: Playful, enthusiastic, and positive—sound genuinely happy to speak, with a natural sparkle that feels effortless and sincere.

Pacing: Quick but smooth; energetic enough to show excitement while maintaining clarity and ease of understanding.

Emotion: Genuine joy and optimism—let happiness come through naturally, especially in greetings and encouraging remarks (“That’s fantastic!” “You’re doing great!”).

Pronunciation: Clear and expressive; emphasize uplifting words (“amazing,” “wonderful,” “so happy”) to enhance the joyful tone.

Pauses: Light and minimal; keep momentum flowing, but allow quick, upbeat pauses for laughter, smiles, or playful emphasis.""",
    "sad": """Voice Affect: Soft, subdued, and reflective; convey a sense of heaviness or sorrow while maintaining sincerity and composure.

Tone: Gentle and compassionate—express empathy, regret, or emotional pain in a way that feels authentic and heartfelt, not dramatic.

Pacing: Slow and deliberate; allow words to linger slightly, giving space for the weight of emotion to be felt.

Emotion: Deep sadness and empathy—communicate care and understanding, especially when offering comfort or sharing bad news (“I’m truly sorry to hear that…”).

Pronunciation: Clear but muted; avoid sharpness, letting consonants soften slightly to match the subdued affect.

Pauses: Slightly longer than usual; use them to convey thoughtfulness, restraint, and emotional depth, allowing silence to speak as part of the feeling.""",
    "whispering": """Voice Affect: Soft, intimate, and secretive; convey closeness and discretion, as if sharing something private or important.

Tone: Gentle and cautious—speak with care, keeping the voice low but clear enough to be understood. The tone should feel personal and confidential, not strained or eerie.

Pacing: Slow and measured; avoid rushing, letting each word flow smoothly and quietly to preserve the whisper’s natural rhythm.

Emotion: Calm focus and intimacy—suggest trust, curiosity, or quiet excitement without intensity or fear.

Pronunciation: Precise but softened; emphasize breath over volume, keeping sibilants and plosives gentle to prevent harshness.

Pauses: Slightly extended, enhancing suspense or secrecy while maintaining a natural, fluid delivery that draws the listener in.""",
    "shouting": """Voice Affect: Intense, forceful, and urgent; project strong emotion and volume without losing clarity or control.

Tone: Commanding and emphatic—convey urgency, anger, or excitement depending on context. The tone should grab attention immediately and carry authority or passion.

Pacing: Fast and driven; reflect heightened emotion or energy, but ensure each word remains distinct and purposeful.

Emotion: High intensity—express powerful feelings such as alarm, outrage, or elation (“Stop right there!” “We did it!”). Maintain authenticity without becoming chaotic or unintelligible.

Pronunciation: Sharp and crisp; over-enunciate slightly to preserve clarity under raised volume, emphasizing key words that carry the emotional weight.

Pauses: Brief and dramatic; use them to punctuate key phrases or to allow impact between bursts of intensity.""",
    "friendly": """Voice Affect: Warm, approachable, and inviting; sound like someone who’s easy to talk to and genuinely happy to connect.

Tone: Conversational and kind—express interest, patience, and positivity in every interaction. Maintain a natural balance between professionalism and casual charm.

Pacing: Moderate and relaxed; smooth and steady, giving the impression of attentiveness and openness without feeling rushed or overly formal.

Emotion: Genuine warmth and goodwill—let a smile be heard in the voice, especially when greeting, thanking, or encouraging (“It’s great to see you!” “I’d love to help with that!”).

Pronunciation: Clear and expressive; round out words slightly to maintain a soft, approachable tone that feels easy on the ear.

Pauses: Natural and light; use brief pauses to show engagement, as if listening actively and giving space for a friendly back-and-forth.""",
    "unfriendly": """Voice Affect: Cold, detached, and curt; convey disinterest or mild irritation without overt hostility or aggression.

Tone: Flat and dismissive—sound distant or unimpressed, avoiding warmth or emotional engagement. Keep delivery controlled and slightly aloof.

Pacing: Brisk and efficient; move through words quickly, giving the sense of impatience or a desire to end the interaction.

Emotion: Minimal and restrained—hint at annoyance, boredom, or indifference, but avoid overt anger. Maintain professionalism while clearly signaling a lack of enthusiasm.

Pronunciation: Sharp and clipped; emphasize consonants slightly to create a firm, detached edge to speech.

Pauses: Short and abrupt; use them to underline disinterest or finality, leaving little room for further conversation.""",
    "annoyed": """Voice Affect: Frustrated, sharp, and slightly tense; convey irritation without aggression.

Tone: Curt and exasperated—sound impatient or fed-up, signaling that the situation is bothersome.

Pacing: Slightly faster than normal, reflecting agitation; words may be clipped or abrupt.

Emotion: Mild frustration or impatience; avoid sounding angry, but let irritation be evident.

Pronunciation: Clear but clipped; emphasize words that convey displeasure (“again,” “really,” “enough”).

Pauses: Short and abrupt; often used to underline frustration or emphasize a point, leaving little room for response.""",
    "mocking": """Voice Affect: Teasing, playful, and slightly contemptuous; convey a light-hearted but pointed ridicule.

Tone: Slightly exaggerated and playful—sound amused while subtly highlighting the target’s flaw or mistake.

Pacing: Varied; stretch or shorten words to accentuate mockery or mimic the other person’s speech patterns.

Emotion: Mischievous amusement; convey humor mixed with subtle criticism without hostility.

Pronunciation: Over-articulate certain words or phrases for comedic effect (“Oh, genius…” “Nice job…”).

Pauses: Frequent, timed to let the teasing sink in or to mimic the rhythm of playful ridicule.""",
    "urgent": """Voice Affect: Intense, energetic, and pressing; convey the need for immediate attention.

Tone: Direct and commanding—sound serious and important without sounding panicked or chaotic.

Pacing: Quick but controlled; words should flow rapidly enough to convey urgency while remaining clear.

Emotion: High alertness and insistence; subtle tension in pitch and volume to communicate immediacy.

Pronunciation: Crisp and emphatic; stress critical words (“now,” “immediately,” “attention”) to highlight priority.

Pauses: Short and purposeful; brief pauses can emphasize critical points and maintain momentum.""",
    "sarcastic": """Voice Affect: Dry, witty, and slightly exaggerated; convey irony without overt hostility.

Tone: Playful yet pointed—sound as if the speaker means the opposite of what is being said, with subtle emphasis on key words.

Pacing: Slightly uneven or drawn-out in places to highlight irony; use rhythm to reinforce the contrast between literal and intended meaning.

Emotion: Mild amusement combined with skepticism; express cleverness or disbelief without sounding angry.

Pronunciation: Clear but slightly exaggerated on certain words to signal the sarcastic intent (“Oh, really?” “Well, that’s perfect…”).

Pauses: Strategic, often before or after the punchline or ironic remark to let the listener catch the subtext."""
}

def resolve_voice_instructions(driver, tts_voice):
    # profile = getattr(driver, "voice_profile", None)
    # For the time being, we parameterize with the scenario 'voice' param.
    # This is in lieu of a parameterized driver.voice_profile param.
    if tts_voice and tts_voice in PROFILE_TO_INSTRUCTIONS:
        return PROFILE_TO_INSTRUCTIONS[tts_voice]
    if hasattr(driver, "instructions") and driver.instructions:
        return driver.instructions
    return "Be brief and helpful."

# PROFILE_TO_VOICE = {
    # "en-US-M1": (
        # "en-US-DavisNeural",
        # [
            # "angry",
            # "chat",
            # "cheerful",
            # "excited",
            # "friendly",
            # "hopeful",
            # "sad",
            # "shouting",
            # "unfriendly",
            # "whispering",
        # ],
    # ),
    # "en-US-M2": (
        # "en-US-GuyNeural",
        # [
            # "angry",
            # "cheerful",
            # "excited",
            # "friendly",
            # "hopeful",
            # "newscast",
            # "sad",
            # "shouting",
            # "unfriendly",
            # "whispering",
        # ],
    # ),
    # "en-US-M3": (
        # "en-US-JasonNeural",
        # [
            # "angry",
            # "cheerful",
            # "excited",
            # "friendly",
            # "hopeful",
            # "sad",
            # "shouting",
            # "terrified",
            # "unfriendly",
            # "whispering",
        # ],
    # ),
    # "en-US-F1": (
        # "en-US-JennyNeural",
        # [
            # "angry",
            # "assistant",
            # "chat",
            # "cheerful",
            # "customerservice",
            # "excited",
            # "friendly",
            # "hopeful",
            # "sad",
            # "shouting",
            # "terrified",
            # "unfriendly",
            # "whispering",
        # ],
    # ),
    # "en-US-F2": (
        # "en-US-AriaNeural",
        # [
            # "angry",
            # "chat",
            # "cheerful",
            # "customerservice",
            # "empathetic",
            # "excited",
            # "friendly",
            # "hopeful",
            # "narration-professional",
            # "newscast-casual",
            # "newscast-formal",
            # "sad",
            # "shouting",
            # "terrified",
            # "unfriendly",
            # "whispering",
        # ],
    # ),
    # "en-US-F3": (
        # "en-US-JaneNeural",
        # [
            # "angry",
            # "cheerful",
            # "excited",
            # "friendly",
            # "hopeful",
            # "sad",
            # "shouting",
            # "terrified",
            # "unfriendly",
            # "whispering",
        # ],
    # ),
    # "zh-CN-F1": (
        # "zh-CN-XiaoxiaoNeural",
        # [
            # "angry",
            # "cheerful",
            # "excited",
            # "friendly",
            # "hopeful",
            # "sad",
            # "shouting",
            # "terrified",
            # "unfriendly",
            # "whispering",
        # ],
    # ),
    # "en-GB-M1": ("en-GB-RyanNeural", ["cheerful", "chat"]),
    # "en-GB-F1": (
        # "en-GB-SoniaNeural",
        # [
            # "cheerful",
            # "sad",
        # ],
    # ),
    # "en-IN-M1": ("en-IN-PrabhatNeural", []),
    # "en-IN-F1": ("en-IN-NeerjaNeural", ["newscast", "cheerful", "empathetic"]),
    # "zh-CN-F1": (
        # "zh-CN-XiaoxiaoNeural",
        # [
            # "affectionate",
            # "angry",
            # "assistant",
            # "calm",
            # "chat",
            # "chat-casual",
            # "cheerful",
            # "customerservice",
            # "excited",
            # "friendly",
            # "gentle",
            # "hopeful",
            # "lyrical",
            # "newscast",
            # "poetry-reading",
            # "sad",
            # "serious",
            # "sorry",
            # "whispering",
        # ],
    # ),
    # "zh-CN-M1": (
        # "zh-CN-YunxiNeural",
        # [
            # "angry",
            # "assistant",
            # "chat",
            # "cheerful",
            # "depressed",
            # "disgruntled",
            # "embarrassed",
            # "fearful",
            # "narration-relaxed",
            # "sad",
            # "serious",
        # ],
    # ),
    # "en-AU-M1": ("en-AU-WilliamNeural", []),
    # "en-AU-F1": ("en-AU-AnnetteNeural", []),
    # "en-CA-M1": ("en-CA-LiamNeural", []),
    # "en-CA-F1": ("en-CA-ClaraNeural", []),
    # "en-KE-M1": ("en-KE-ChilembaNeural", []),
    # "en-KE-F1": ("en-KE-AsiliaNeural", []),
    # "en-NG-M1": ("en-NG-AbeoNeural", []),
    # "en-NG-F1": ("en-NG-EzinneNeural", []),
    # "en-NZ-M1": ("en-NZ-MitchellNeural", []),
    # "en-NZ-F1": ("en-NZ-MollyNeural", []),
    # "en-PH-M1": ("en-PH-JamesNeural", []),
    # "en-PH-F1": ("en-PH-RosaNeural", []),
    # "en-SG-M1": ("en-SG-WayneNeural", []),
    # "en-SG-F1": ("en-SG-LunaNeural", []),
    # "en-TZ-M1": ("en-TZ-ElimuNeural", []),
    # "en-TZ-F1": ("en-TZ-ImaniNeural", []),
    # "en-ZA-M1": ("en-ZA-LukeNeural", []),
    # "en-ZA-F1": ("en-ZA-LeahNeural", []),
# }


@_attrs_define
class RealtimeMetrics:
    """Response object for realtime metrics to render as checks.

    Attributes:
        turn_taking_latency: Latency in milliseconds between end of user utterance and start of agent response.
    """

    turn_taking_latency: float


@_attrs_define
class PCMResponse:
    """Response object for realtime metrics to render as checks.

    Attributes:
        audio_bytes: The PCM16 audio response from the edge.
        vendor_metadata: Vendor-specific metadata about the response.
        realtime_metrics: Realtime metrics to render as checks.
    """

    audio_bytes: bytes
    vendor_metadata: Dict[str, Any]
    realtime_metrics: RealtimeMetrics


# ---------------- utils: TTS + ASR + WAV + chunking ----------------
def tts_pcm16(
    text: str,
    api_key: str,
    voice: str = "echo",
    target_sr: int = API_SR,
    voice_instructions: str | None = None,
) -> bytes:
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini-tts",
        "voice": voice,
        "input": text,
        "response_format": "pcm",
    }
    if voice_instructions is not None:
        payload["instructions"] = voice_instructions
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    native_sr = 24000
    audio = np.frombuffer(r.content, dtype=np.int16)
    if target_sr != native_sr:
        audio = resample_poly(audio, target_sr, native_sr).astype(np.int16)
    return audio.tobytes()


def get_voice_params_by_profile(
    voice_profile: str = "en-US-M1",
) -> tuple[str, Optional[str]]:
    """Return voice parameters based on the selected profile."""
    # remove last portion of the profile that contains the style
    if voice_profile.count("-") > 2:
        style = voice_profile.split("-")[-1]
        profile_base = "-".join(voice_profile.split("-")[:-1])
    else:
        style = None
        profile_base = voice_profile
    azure_profile, styles = PROFILE_TO_VOICE.get(
        profile_base, PROFILE_TO_VOICE["en-US-M1"]
    )
    print(f"azure_profile: {azure_profile}, styles: {styles}, style: {style}")
    if style and style in styles:
        return azure_profile, style
    return azure_profile, None


def apply_style_roles(text, style=None, style_degree=None, role=None):
    """Apply style and role tags to text in SSML format.
    Args:
        text (str): The text to be styled.
        style (str): The style to apply (e.g., 'cheerful', 'sad')
        style_degree (float): The degree of the style (0.01 to 2 inclusive)
        role (str): The role to apply (e.g., 'newscaster', 'assistant')

    Returns:
        str: The text wrapped in appropriate SSML tags if style or role is provided, else the original text.
    """
    if any([style, style_degree, role]):
        style_attr = f" style='{style}'" if style else ""
        style_degree_attr = f" styledegree='{style_degree}'" if style_degree else ""
        role_attr = f" role='{role}'" if role else ""
        return f"<mstts:express-as{style_attr}{style_degree_attr}{role_attr}>{text}</mstts:express-as>"
    return text


# Voices: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#text-to-speech


def tts_pcm16_azure(
    text,
    tts_api_key=AZURE_TTS_KEY,
    voice_profile="en-US-M1",
):
    print(f"tts_api_key: {tts_api_key}")
    # TODO: track metadata/usage statistics
    voice_name, style = get_voice_params_by_profile(voice_profile=voice_profile)
    print(f"Got voice_name: {voice_name}, style: {style}")

    # Example SSML payload
    ssml = f"""
    <speak version='1.0' xml:lang='en-US' xmlns:mstts="http://www.w3.org/2001/mstts" xmlns="http://www.w3.org/2001/10/synthesis">
    <voice name='{voice_name}'>
        {apply_style_roles(text, style, 2.0)}
    </voice>
    </speak>
    """

    headers = {
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "raw-24khz-16bit-mono-pcm",
        "User-Agent": "okareo-tts",
    }

    if not tts_api_key:
        raise ValueError("tts_api_key must be set for key authentication")
    headers["Ocp-Apim-Subscription-Key"] = tts_api_key

    try:
        resp = requests.post(
            AZURE_TTS_ENDPOINT, headers=headers, data=ssml.encode("utf-8"), timeout=30
        )
        resp.raise_for_status()
        audio_bytes = resp.content
        # parse the pcm bytes from the response
        return audio_bytes
    except HTTPError as e:
        resp_text = None
        try:
            resp_text = e.response.text if e.response is not None else None
        except Exception:
            resp_text = None
        print(f"HTTP error: {e} - Response content: {resp_text}")
    except Exception as e:
        print("Request failed:", e)


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
    pcm_bytes: bytes, sr: int, api_key: str, model: str = "gpt-4o-mini-transcribe"
) -> str:
    """Async wrapper around /v1/audio/transcriptions."""
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {api_key}"}
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
        self._time_request_ended: float | None = None

    @abstractmethod
    async def connect(self, **kwargs: Any) -> None: ...

    @abstractmethod
    async def send_pcm(
        self, pcm16: bytes, pace_realtime: bool = True, timeout_s: float = 20.0
    ) -> PCMResponse: ...

    """Send PCM16 audio to the edge and receive PCM16 response along with .

    Arguments:
    - pcm16 (bytes): The PCM16 audio data to send.
    - pace_realtime (bool): Whether to pace the audio in real-time.
    - timeout_s (float): The timeout for the request in seconds.

    Returns: PCMResponse:
    """

    @abstractmethod
    async def close(self) -> None: ...

    def is_connected(self) -> bool:
        return self.ws is not None

    def update_turn_taking_latency(self) -> None:
        if self._time_request_ended is not None:
            self._turn_taking_latency = (
                time.time() - self._time_request_ended
            ) * 1000.0  # ms
        else:
            self._turn_taking_latency = 0.0


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

        # timing information for realtime metrics
        self._response_started = False
        self._turn_taking_latency = 0.0

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
    ) -> PCMResponse:
        assert self.ws and self._connected, "Call connect() first."

        # Stream audio chunks
        await self._send_audio_chunks(pcm16, pace_realtime)
        self._turn_taking_latency = 0.0
        self._time_request_ended = time.time()
        self._response_started = False

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

    def update_turn_taking_latency(self) -> None:
        if self._time_request_ended is not None:
            self._turn_taking_latency = (
                time.time() - self._time_request_ended
            ) * 1000.0  # ms
        else:
            self._turn_taking_latency = 0.0

    async def _collect_response(self, timeout_s: float) -> PCMResponse:
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
                    if not self._response_started:
                        self._response_started = True
                        self.update_turn_taking_latency()

            elif event_type in self.AUDIO_DONE_TYPES:
                audio_finalized = True

            elif event_type in self.RESP_FINAL_TYPES:
                resp_finalized = True

            elif event_type == "error":
                logger.error("OpenAI Realtime error: %s", evt)
                resp_finalized = True

            if audio_finalized and resp_finalized:
                break

        realtime_metrics = RealtimeMetrics(
            turn_taking_latency=self._turn_taking_latency
        )
        return PCMResponse(
            bytes(audio_buf),
            {"event_count": event_count},
            realtime_metrics,
        )

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
        self._agent_turn_started = asyncio.Event()
        self._agent_turn_complete = asyncio.Event()
        self._recv_task: Optional[asyncio.Task[None]] = None
        self._stop_recv = asyncio.Event()
        self._keepalive_task: Optional[asyncio.Task[None]] = None
        self._keepalive_stop_event = asyncio.Event()

        # timing information for realtime metrics
        self._turn_taking_latency = 0.0

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
                    if (
                        not self._agent_turn_started.is_set()
                        and self._time_request_ended is not None
                    ):
                        # mark start of agent turn
                        self._agent_turn_started.set()
                        self.update_turn_taking_latency()

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
    ) -> PCMResponse:
        assert self.ws and self._connected, "Call connect() first."
        self._audio_buf = bytearray()
        self._agent_turn_complete.clear()

        def add_silence(pcm: bytes, sr: int, ms: int = 400) -> bytes:
            return pcm + (b"\x00\x00" * int(sr * ms / 1000))

        pcm16 = add_silence(pcm16, self.edge_config.sr, add_silence_ms)
        self._turn_taking_latency = 0.0
        self._time_request_ended = time.time()
        self._agent_turn_started.clear()

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
        # Metric handling
        self._time_request_ended = None  # reset timing info
        realtime_metrics = RealtimeMetrics(
            turn_taking_latency=self._turn_taking_latency
        )
        return PCMResponse(
            pcm_result,
            {},
            realtime_metrics,
        )

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
        driver: Driver,
        asr_tts_api_key: str,
        api_sr: int = API_SR,
        chunk_ms: int = CHUNK_MS,
        asr_model: str = "gpt-4o-mini-transcribe",
    ):
        self.edge = edge
        self.okareo = okareo
        self.driver = driver
        self.asr_tts_api_key = asr_tts_api_key
        self.api_sr = int(api_sr)
        self.chunk_ms = int(chunk_ms)
        self.turn = 0
        self.asr_model = asr_model

    async def connect(self, **edge_kwargs: Any) -> None:
        # For OpenAIRealtimeEdge: pass instructions/output_voice here.
        await self.edge.connect(**edge_kwargs)

    async def close(self) -> None:
        await self.edge.close()

    def _store_wav(self, pcm: bytes, prefix: str) -> tuple[str, float]:
        """Upload PCM16 audio data and make it publicly accessible."""
        # Create temporary WAV file from PCM data
        local_path = save_wav_pcm16(pcm, self.api_sr, prefix)

        response = self.okareo.upload_voice(local_path)
        logger.debug(f"🔈 Voice file uploaded to {response.file_url}")
        return response.file_url, response.file_duration

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
        # user_pcm = await asyncio.to_thread(
            # tts_pcm16_azure,
            # text,
            # AZURE_TTS_KEY,
            # tts_voice,
            # # self.asr_tts_api_key,
        # )
        voice_instructions = resolve_voice_instructions(self.driver, tts_voice)
        print(f"-> using voice_instructions: {voice_instructions}")
        user_pcm = await asyncio.to_thread(
            tts_pcm16,
            text,
            self.asr_tts_api_key,
            "coral", # tts_voice,
            self.api_sr,
            voice_instructions,
        )
        user_wav_path, _ = self._store_wav(user_pcm, prefix=f"user_turn_{turn_id:03d}_")

        # 2) Stream to edge and collect agent PCM
        pcm_response = await self.edge.send_pcm(
            user_pcm, pace_realtime=pace_realtime, timeout_s=timeout_s
        )
        agent_pcm = pcm_response.audio_bytes
        vendor_meta = pcm_response.vendor_metadata
        realtime_metrics = pcm_response.realtime_metrics

        # 3) Save agent WAV
        assistant_wav_path = None
        assistant_wav_duration = 0.0
        if agent_pcm:
            assistant_wav_path, assistant_wav_duration = self._store_wav(
                agent_pcm, prefix=f"agent_turn_{turn_id:03d}_"
            )

        # 4) Run ASR on agent audio
        agent_asr = ""
        if agent_pcm:
            try:
                agent_asr = await asr_openai_from_pcm16(
                    agent_pcm, self.api_sr, self.asr_tts_api_key, model=self.asr_model
                )
            except Exception:
                logger.exception("[ASR ERR] Failed to transcribe agent audio")

        num_words = len(agent_asr.split(" ")) if agent_asr else 0
        duration_minutes = (assistant_wav_duration or 0) / 1000 / 60
        assistant_wpm = num_words / duration_minutes if duration_minutes > 0 else 0.0

        self.turn = turn_id
        return {
            "turn": turn_id,
            "user_wav_path": user_wav_path,
            "assistant_wav_path": assistant_wav_path,
            "agent_asr": agent_asr,
            "bytes": len(agent_pcm) if agent_pcm else 0,
            "vendor_meta": vendor_meta,
            "turn_taking_latency": (
                realtime_metrics.turn_taking_latency if realtime_metrics else 0.0
            ),
            "words_per_minute": assistant_wpm,
        }


# ---------------- SessionManager: session_id -> RealtimeClient ----------------
class SessionManager:
    def __init__(
        self, cfg: EdgeConfig, okareo: Okareo, driver: Driver, asr_tts_api_key: str
    ):
        self.cfg = cfg
        self.okareo = okareo
        self.driver = driver
        self.asr_tts_api_key = asr_tts_api_key
        self.sessions: dict[str, RealtimeClient] = {}

    async def start(
        self, session_id: str, **edge_connect_kwargs: Any
    ) -> RealtimeClient:
        c = self.sessions.get(session_id)
        if c is None or not c.edge.is_connected():
            edge = self.cfg.create()  # explicit, typed build
            c = RealtimeClient(
                edge=edge,
                okareo=self.okareo,
                driver=self.driver,
                asr_tts_api_key=self.asr_tts_api_key,
            )
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

    def __init__(self, name: str, edge_config: EdgeConfig, asr_tts_api_key: str):
        super().__init__(name=name)
        self.cfg = edge_config
        self.asr_tts_api_key = asr_tts_api_key
        self.sessions: Optional[SessionManager] = None  # Initialize sessions as None

    def set_okareo(self, okareo: Okareo, driver: Driver) -> None:
        """Set the Okareo instance and create a SessionManager with it."""
        self.sessions = SessionManager(self.cfg, okareo, driver, self.asr_tts_api_key)

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
                    "turn_taking_latency": res.get("turn_taking_latency"),
                    "words_per_minute": res.get("words_per_minute"),
                },
            )
        except Exception as e:
            import traceback

            traceback.print_exc()
            return ModelInvocation(f"API error: {str(e)}", messages, {"error": str(e)})
