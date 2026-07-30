"""End-to-end simulation against a native WebRTC voice target (M1).

This is the SDK-level counterpart to the server-side unit/integration tests in
okareo_server (``app/tests/test_webrtc_edge_unit.py``). It drives the *public*
path a customer would use -- create a scenario, run a simulation against a
voice target with ``edge_type="webrtc"``, and assert real datapoints come back
-- so it exercises API -> orchestrator -> VoiceTarget -> RealtimeClient ->
WebRTCEdge -> LiveKit, which the server-side spikes bypass.

Requires a server that has the ``edge_type="webrtc"`` support (M1) deployed or
running locally. Point at it with ``BASE_URL``.

Run:
    export OKAREO_API_KEY=...            # Okareo project key
    export RETELL_API_KEY=... RETELL_AGENT_ID=...
    export BASE_URL=http://localhost:8000
    pytest okareo_tests/test_webrtc_target_e2e.py -v -s

The test SKIPS (never fails) when any credential is absent, so it is safe in a
CI job without secrets.
"""

import os
from typing import Any, Dict, List

import pytest
from okareo_tests.common import random_string

from okareo import Okareo
from okareo.model_under_test import (
    Driver,
    SmallWebRTCTarget,
    Target,
    WebRTCVoiceTarget,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate

# --------------------------------------------------------------------------
# Credentials / gating
# --------------------------------------------------------------------------

OKAREO_API_KEY = os.environ.get("OKAREO_API_KEY")
RETELL_API_KEY = os.environ.get("RETELL_API_KEY")
RETELL_AGENT_ID = os.environ.get("RETELL_AGENT_ID")
BASE_URL = os.environ.get("BASE_URL", "https://api.okareo.com")

# Unconditionally skipped in the build: each WebRTC e2e simulation needs live
# provider credentials AND a reachable agent, which are not yet provisioned in
# CI. This is applied INSTEAD of the per-class ``requires_*_creds`` skipif (which
# would otherwise report a misleading "missing env var" reason in CI). To
# re-enable once creds + an agent exist, swap ``@_NEEDS_LIVE_SETUP`` back to the
# per-class ``@requires_*_creds`` marker defined below.
_NEEDS_LIVE_SETUP = pytest.mark.skip(
    reason="Credentials and a live agent must be set up before enabling in the build."
)

requires_webrtc_creds = pytest.mark.skipif(
    not (OKAREO_API_KEY and RETELL_API_KEY and RETELL_AGENT_ID),
    reason="needs OKAREO_API_KEY + RETELL_API_KEY + RETELL_AGENT_ID",
)


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

DRIVER_PROMPT = (
    "You are a caller speaking to a voice agent on the phone. "
    "Keep every turn to one short sentence. "
    "Ask about {scenario_input.topic}, then respond naturally."
)


def _messages(datapoint: Any) -> List[Dict[str, Any]]:
    """Pull the conversation turns off a datapoint.

    Voice simulations put the turn list on
    ``model_metadata.additional_properties["messages"]`` (same path
    ``test_voice_simulation.get_messages`` uses).
    """
    metadata = getattr(datapoint, "model_metadata", None)
    props = getattr(metadata, "additional_properties", None) if metadata else None
    if isinstance(props, dict):
        messages = props.get("messages", [])
        if isinstance(messages, list):
            return [m for m in messages if isinstance(m, dict)]
    return []


def _assistant_turns(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [m for m in messages if m.get("role") == "assistant"]


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------


@_NEEDS_LIVE_SETUP
class TestWebRTCSimulationE2E:
    """Full simulation against a live Retell agent over native WebRTC."""

    def test_webrtc_simulation_produces_transcribed_datapoints(self) -> None:
        assert OKAREO_API_KEY and RETELL_AGENT_ID  # narrowed by the skipif
        okareo = Okareo(api_key=OKAREO_API_KEY, base_path=BASE_URL)
        rnd = random_string(5)

        scenario = okareo.create_scenario_set(
            ScenarioSetCreate(
                name=f"WebRTC E2E Scenario - {rnd}",
                seed_data=Okareo.seed_data_from_list(
                    [
                        {
                            "input": {"topic": "checking on an appointment"},
                            "result": "Agent responds and the call completes.",
                        }
                    ]
                ),
            )
        )

        target = WebRTCVoiceTarget(
            platform="retell",
            agent_id=RETELL_AGENT_ID,
            max_parallel_requests=1,
        )

        driver = Driver(
            name=f"WebRTC E2E Driver - {rnd}",
            temperature=0.6,
            prompt_template=DRIVER_PROMPT,
        )

        evaluation = okareo.run_simulation(
            driver=driver,
            target=Target(name=f"WebRTC Target - {rnd}", target=target),
            name=f"WebRTC E2E - {rnd}",
            scenario=scenario,
            max_turns=3,
            repeats=1,
            # Retell greets first, so let the target open the conversation.
            first_turn="target",
            calculate_metrics=True,
            # Multi-turn simulations require >=1 check. Deliberately DETERMINISTIC
            # checks only -- model-based ones (task_completed, behavior_adherence)
            # invoke an LLM judge, which is unrelated to what this test proves and
            # fails locally when the configured Vertex model is unavailable.
            # Both of these also exercise the driver-timing metadata the edge
            # derives from its computed playback-complete ("mark") timestamp.
            checks=["latency", "time_to_first_audio"],
            # Retell's secret rides the shared "voice" key, same as the other
            # hosted providers -- this is what the orchestrator validates.
            api_keys={"voice": RETELL_API_KEY},
        )

        print(f"\nrun status: {evaluation.status}", flush=True)
        assert evaluation is not None
        assert getattr(evaluation, "id", None), "no test run id returned"

        # get_datapoints lives in the voice-sim test module, not common.
        from okareo_tests.test_voice_simulation import get_datapoints

        datapoints = get_datapoints(okareo, evaluation.id)
        assert datapoints, "simulation produced no datapoints"

        # The whole point of M1: the agent was reached over WebRTC and its
        # speech came back transcribed (Deepgram streaming ASR on the edge).
        all_assistant: List[Dict[str, Any]] = []
        for dp in datapoints:
            all_assistant.extend(_assistant_turns(_messages(dp)))

        assert all_assistant, "no assistant turns -- agent never spoke"
        transcribed = [m for m in all_assistant if (m.get("content") or "").strip()]
        assert transcribed, (
            "assistant turns had empty transcripts -- streaming ASR did not "
            "attach text to the target utterances"
        )
        print(
            f"assistant turns: {len(all_assistant)}, transcribed: {len(transcribed)}",
            flush=True,
        )

        # Twilio parity: ONE merged whole-call recording, not just per-utterance
        # segments (segments drop inter-utterance gaps and cannot show overlap).
        recordings = []
        for dp in datapoints:
            props = (
                getattr(
                    getattr(dp, "model_metadata", None), "additional_properties", {}
                )
                or {}
            )
            if props.get("call_recording_url"):
                recordings.append(
                    {
                        "url": props["call_recording_url"],
                        "channels": props.get("call_recording_channels"),
                        "source": props.get("call_recording_source"),
                        "format": "wav",
                    }
                )
        assert recordings, (
            "no call_recording_url on any datapoint -- whole-call recording parity "
            "with the Twilio edge is missing"
        )
        for rec in recordings:
            print(
                f"call_recording: {rec.get('channels')}ch {rec.get('format')} "
                f"from {rec.get('source')} -> {str(rec.get('url'))[:60]}...",
                flush=True,
            )
            assert rec.get("url"), "call_recording has no url"
        for m in transcribed[:3]:
            print(f"  agent: {m.get('content')!r}", flush=True)

    def test_invalid_platform_is_rejected(self) -> None:
        """Server-side per-platform validation should reject a bad platform."""
        assert OKAREO_API_KEY
        okareo = Okareo(api_key=OKAREO_API_KEY, base_path=BASE_URL)
        rnd = random_string(5)
        scenario = okareo.create_scenario_set(
            ScenarioSetCreate(
                name=f"WebRTC Bad Platform - {rnd}",
                seed_data=Okareo.seed_data_from_list(
                    [{"input": {"topic": "x"}, "result": "y"}]
                ),
            )
        )
        target = WebRTCVoiceTarget(platform="not-a-platform", agent_id="a")

        with pytest.raises(Exception) as exc:
            okareo.run_simulation(
                driver=Driver(
                    name=f"WebRTC Bad Driver - {rnd}",
                    temperature=0.6,
                    prompt_template=DRIVER_PROMPT,
                ),
                target=Target(name=f"WebRTC Bad - {rnd}", target=target),
                name=f"WebRTC Bad - {rnd}",
                scenario=scenario,
                max_turns=1,
                repeats=1,
                first_turn="target",
                checks=["latency"],  # deterministic; no LLM judge
                api_keys={"voice": RETELL_API_KEY},
            )
        # Assert on the ACTUAL reason -- without this the test would pass on any
        # error (e.g. a missing-checks validation error) and prove nothing.
        message = str(exc.value).lower()
        assert "platform" in message, f"expected a platform rejection, got: {exc.value}"
        print(f"\nrejected as expected: {exc.value}", flush=True)


LIVEKIT_URL = os.environ.get("LIVEKIT_URL")
LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET")

requires_livekit_creds = pytest.mark.skipif(
    not (OKAREO_API_KEY and LIVEKIT_URL and LIVEKIT_API_KEY and LIVEKIT_API_SECRET),
    reason="needs OKAREO_API_KEY + LIVEKIT_URL/API_KEY/API_SECRET (and a running agent)",
)


@_NEEDS_LIVE_SETUP
class TestLiveKitDirectSimulationE2E:
    """LiveKit direct exercises the LOCAL-MIX recording path.

    Retell records server-side, so that e2e validates the *vendor* branch. A
    LiveKit room has no vendor recording at all, so this is the only end-to-end
    check of Okareo's own dual-channel mix -- the callee-agnostic path that
    also covers Daily-direct and Pipecat OSS.
    """

    def test_livekit_simulation_stores_local_dual_channel_mix(self) -> None:
        import uuid as _uuid

        assert OKAREO_API_KEY
        okareo = Okareo(api_key=OKAREO_API_KEY, base_path=BASE_URL)
        rnd = random_string(5)

        scenario = okareo.create_scenario_set(
            ScenarioSetCreate(
                name=f"LiveKit E2E Scenario - {rnd}",
                seed_data=Okareo.seed_data_from_list(
                    [
                        {
                            "input": {"topic": "the weather today"},
                            "result": "Agent responds.",
                        }
                    ]
                ),
            )
        )
        target = WebRTCVoiceTarget(
            platform="livekit",
            livekit_url=LIVEKIT_URL,
            livekit_api_key=LIVEKIT_API_KEY,
            livekit_api_secret=LIVEKIT_API_SECRET,
            room_name=f"okareo-e2e-{_uuid.uuid4().hex[:8]}",
            max_parallel_requests=1,
        )
        evaluation = okareo.run_simulation(
            driver=Driver(
                name=f"LiveKit E2E Driver - {rnd}",
                temperature=0.6,
                prompt_template=DRIVER_PROMPT,
            ),
            target=Target(name=f"LiveKit Target - {rnd}", target=target),
            name=f"LiveKit E2E - {rnd}",
            scenario=scenario,
            max_turns=2,
            repeats=1,
            first_turn="driver",  # our own agent does not greet first
            calculate_metrics=True,
            checks=["latency"],
        )
        print(f"\nrun status: {evaluation.status}", flush=True)

        from okareo_tests.test_voice_simulation import get_datapoints

        datapoints = get_datapoints(okareo, evaluation.id)
        assert datapoints, "simulation produced no datapoints"

        found = []
        for dp in datapoints:
            props = (
                getattr(
                    getattr(dp, "model_metadata", None), "additional_properties", {}
                )
                or {}
            )
            if props.get("call_recording_url"):
                found.append(props)
        assert found, "no call_recording_url -- local mix did not produce a recording"

        for props in found:
            print(
                f"recording: {props.get('call_recording_channels')}ch from "
                f"{props.get('call_recording_source')} -> "
                f"{str(props.get('call_recording_url'))[:60]}...",
                flush=True,
            )
            # No vendor recording exists for a bare LiveKit room, so this MUST
            # be Okareo's own mix -- and it must be dual-channel.
            assert props.get("call_recording_source") == "okareo_local_mix"
            assert props.get("call_recording_channels") == 2


# ---------------------------------------------------------------------------
# M2 live e2e for Daily direct
# ---------------------------------------------------------------------------

DAILY_ROOM_URL = os.environ.get("DAILY_ROOM_URL")
DAILY_MEETING_TOKEN = os.environ.get("DAILY_MEETING_TOKEN")

requires_daily_creds = pytest.mark.skipif(
    not (OKAREO_API_KEY and DAILY_ROOM_URL),
    reason="needs OKAREO_API_KEY + DAILY_ROOM_URL (and an agent in that room)",
)


def _assistant_transcripts(datapoints: List[Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for dp in datapoints:
        for m in _assistant_turns(_messages(dp)):
            if (m.get("content") or "").strip():
                out.append(m)
    return out


def _recording_props(datapoints: List[Any]) -> List[Dict[str, Any]]:
    recs: List[Dict[str, Any]] = []
    for dp in datapoints:
        props = (
            getattr(getattr(dp, "model_metadata", None), "additional_properties", {})
            or {}
        )
        if props.get("call_recording_url"):
            recs.append(props)
    return recs


@_NEEDS_LIVE_SETUP
class TestDailyDirectSimulationE2E:
    """Daily direct: like LiveKit, no vendor recording -> LOCAL-MIX path."""

    def test_daily_simulation_produces_transcribed_datapoints(self) -> None:
        assert OKAREO_API_KEY
        okareo = Okareo(api_key=OKAREO_API_KEY, base_path=BASE_URL)
        rnd = random_string(5)
        scenario = okareo.create_scenario_set(
            ScenarioSetCreate(
                name=f"Daily E2E Scenario - {rnd}",
                seed_data=Okareo.seed_data_from_list(
                    [
                        {
                            "input": {"topic": "the weather today"},
                            "result": "Agent responds.",
                        }
                    ]
                ),
            )
        )
        target = WebRTCVoiceTarget(
            platform="daily",
            room_url=DAILY_ROOM_URL,
            meeting_token=DAILY_MEETING_TOKEN,
            max_parallel_requests=1,
        )
        evaluation = okareo.run_simulation(
            driver=Driver(
                name=f"Daily E2E Driver - {rnd}",
                temperature=0.6,
                prompt_template=DRIVER_PROMPT,
            ),
            target=Target(name=f"Daily Target - {rnd}", target=target),
            name=f"Daily E2E - {rnd}",
            scenario=scenario,
            max_turns=2,
            repeats=1,
            first_turn="driver",  # our own agent typically does not greet first
            calculate_metrics=True,
            checks=["latency"],
        )
        print(f"\nrun status: {evaluation.status}", flush=True)

        from okareo_tests.test_voice_simulation import get_datapoints

        datapoints = get_datapoints(okareo, evaluation.id)
        assert datapoints, "simulation produced no datapoints"
        assert _assistant_transcripts(datapoints), "agent never spoke / no transcript"

        recs = _recording_props(datapoints)
        assert recs, "no call_recording_url -- local mix did not produce a recording"
        for rec in recs:
            print(
                f"recording: {rec.get('call_recording_channels')}ch from "
                f"{rec.get('call_recording_source')}",
                flush=True,
            )
            # Daily direct has no vendor recording -> Okareo's own dual-channel mix.
            assert rec.get("call_recording_source") == "okareo_local_mix"
            assert rec.get("call_recording_channels") == 2


# ---------------------------------------------------------------------------
# M3 generic WebRTC (offerer) -- against a self-hosted SmallWebRTC agent
# ---------------------------------------------------------------------------

GENERIC_OFFER_URL = os.environ.get("GENERIC_OFFER_URL")

requires_generic_creds = pytest.mark.skipif(
    not (OKAREO_API_KEY and GENERIC_OFFER_URL),
    reason="needs OKAREO_API_KEY + GENERIC_OFFER_URL (a SmallWebRTC /api/offer)",
)


@_NEEDS_LIVE_SETUP
class TestSmallWebRTCSimulationE2E:
    """Full simulation against a self-hosted generic WebRTC agent (Okareo is the
    offerer). No vendor SFU/secret: we POST an SDP offer to ``offer_url`` and
    connect peer-to-peer. The Rung-1 harness echoes audio, so the assistant
    turns transcribe back the driver's own speech -- enough to prove the whole
    public path (API -> orchestrator -> WebRTCEdge -> aiortc offerer -> agent)."""

    def test_smallwebrtc_produces_transcribed_datapoints(self) -> None:
        assert OKAREO_API_KEY and GENERIC_OFFER_URL
        okareo = Okareo(api_key=OKAREO_API_KEY, base_path=BASE_URL)
        rnd = random_string(5)
        scenario = okareo.create_scenario_set(
            ScenarioSetCreate(
                name=f"SmallWebRTC E2E Scenario - {rnd}",
                seed_data=Okareo.seed_data_from_list(
                    [
                        {
                            "input": {"topic": "scheduling a dentist appointment"},
                            "result": "Agent responds.",
                        }
                    ]
                ),
            )
        )
        target = SmallWebRTCTarget(
            offer_url=GENERIC_OFFER_URL,
            max_parallel_requests=1,
        )
        evaluation = okareo.run_simulation(
            driver=Driver(
                name=f"SmallWebRTC E2E Driver - {rnd}",
                temperature=0.6,
                prompt_template=DRIVER_PROMPT,
            ),
            target=Target(name=f"SmallWebRTC Target - {rnd}", target=target),
            name=f"SmallWebRTC E2E - {rnd}",
            scenario=scenario,
            max_turns=2,
            repeats=1,
            first_turn="driver",  # a bare/echo agent does not greet
            calculate_metrics=True,
            checks=["latency"],
            # SmallWebRTC carries no api_keys["voice"] secret.
        )
        print(f"\nrun status: {evaluation.status}", flush=True)
        assert getattr(evaluation, "id", None), "no test run id"

        from okareo_tests.test_voice_simulation import get_datapoints

        datapoints = get_datapoints(okareo, evaluation.id)
        assert datapoints, "simulation produced no datapoints"
        assert _assistant_transcripts(datapoints), "agent never spoke / no transcript"

        recs = _recording_props(datapoints)
        assert recs, "no call_recording_url"
        for rec in recs:
            print(
                f"recording: {rec.get('call_recording_channels')}ch from "
                f"{rec.get('call_recording_source')}",
                flush=True,
            )
            # Generic peer has no vendor recording -> Okareo local mix.
            assert rec.get("call_recording_source") == "okareo_local_mix"
