"""End-to-end verification of the WebRTC concurrency + parity fixes (okareo_server PR #1033).

``test_webrtc_target_e2e.py`` proves each platform works at concurrency 1.
This module proves the claims that PR actually made:

  1. **Within-run concurrency** (P2): a run with ``max_parallel_requests > 1``
     executes WebRTC conversations concurrently, each with its own isolated
     target (distinct rooms/peer connections, no shared state).
  2. **Per-conversation identity** (P0/P1/P3): every datapoint carries its own
     ``call_sid`` (Retell: the vendor call id; others: the conversation's
     session id) and its own whole-call recording -- no cross-talk, no shared
     room.
  3. **Augmentation behavior** (P0): supported augmentations (noise) run on
     WebRTC; unsupported ones (backchannel, needs ``send_injection``) are
     dropped GRACEFULLY -- the run completes instead of failing.
  4. **DTMF honesty** (P0): a WebRTC transcript never contains a fabricated
     ``DTMF:`` marker (the tool is withheld from DTMF-incapable targets).

Like its sibling module, this drives the *public* customer path (SDK ->
API -> orchestrator -> VoiceTarget -> WebRTCEdge -> media), so it needs a
live server that holds the voice credentials (driver LLM, Cartesia TTS,
Deepgram STT). The SmallWebRTC tests are the default runnable set: the
answerer is the self-hosted echo agent in
``okareo_server/scripts/smallwebrtc/agent.py`` -- no vendor account at all.

Run (SmallWebRTC, no vendor creds):
    # 1. the echo answerer (in okareo_server, conda env `poetry`):
    python okareo_server/scripts/smallwebrtc/agent.py -t webrtc --host 0.0.0.0 --port 8081

    # 2. the tests, against a server with the PR deployed:
    export OKAREO_API_KEY=...
    export BASE_URL=http://localhost:8000        # or the dev-sandbox URL
    # local server is Dockerized -> reach the answerer via host.docker.internal
    export GENERIC_OFFER_URL=http://host.docker.internal:8081/api/offer
    pytest okareo_tests/test_webrtc_parity_e2e.py -v -s

Run (Retell, hosted agent -- exercises vendor-side call ids + recording fetch):
    export RETELL_API_KEY=... RETELL_AGENT_ID=...
    pytest okareo_tests/test_webrtc_parity_e2e.py -v -s -k retell

Every test SKIPS (never fails) when its credentials are absent, so the module
is safe to collect in a CI job without secrets.
"""

import os
import time
from typing import Any, Dict, List, Union
from uuid import UUID

import pytest
from okareo_tests.common import random_string
from okareo_tests.test_webrtc_target_e2e import (
    DRIVER_PROMPT,
    _assistant_turns,
    _messages,
)

from okareo import Okareo
from okareo.augmentations import (
    Augmentation,
    BackchannelAugmentation,
    NoiseAugmentation,
)
from okareo.model_under_test import (
    Driver,
    SmallWebRTCTarget,
    Target,
    WebRTCVoiceTarget,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate

OKAREO_API_KEY = os.environ.get("OKAREO_API_KEY")
BASE_URL = os.environ.get("BASE_URL", "https://api.okareo.com")
GENERIC_OFFER_URL = os.environ.get("GENERIC_OFFER_URL")
RETELL_API_KEY = os.environ.get("RETELL_API_KEY")
RETELL_AGENT_ID = os.environ.get("RETELL_AGENT_ID")

requires_smallwebrtc = pytest.mark.skipif(
    not (OKAREO_API_KEY and GENERIC_OFFER_URL),
    reason="needs OKAREO_API_KEY + GENERIC_OFFER_URL (the echo answerer's /api/offer)",
)
requires_retell = pytest.mark.skipif(
    not (OKAREO_API_KEY and RETELL_API_KEY and RETELL_AGENT_ID),
    reason="needs OKAREO_API_KEY + RETELL_API_KEY + RETELL_AGENT_ID",
)

# Three one-topic rows: with max_parallel_requests=3, all three conversations
# should be in flight at once.
CONCURRENT_TOPICS = [
    "scheduling a dentist appointment",
    "asking about store opening hours",
    "checking the status of an order",
]


def _seed(topics: List[str]) -> list:
    return Okareo.seed_data_from_list(
        [{"input": {"topic": t}, "result": "Agent responds."} for t in topics]
    )


def _props(datapoint: Any) -> Dict[str, Any]:
    metadata = getattr(datapoint, "model_metadata", None)
    props = getattr(metadata, "additional_properties", None) if metadata else None
    return props if isinstance(props, dict) else {}


def _get_datapoints(okareo: Okareo, run_id: Union[str, UUID]) -> list:
    from okareo_tests.test_voice_simulation import get_datapoints

    return get_datapoints(okareo, run_id)


def _assert_per_conversation_isolation(datapoints: list, expected: int) -> None:
    """The heart of the concurrency claims: N conversations -> N distinct
    call identities and N distinct recordings. A shared room / shared target
    would collapse these (same room-derived id, or cross-talk recordings)."""
    assert (
        len(datapoints) == expected
    ), f"expected {expected} datapoints, got {len(datapoints)}"

    call_sids = [_props(dp).get("call_sid") for dp in datapoints]
    assert all(
        call_sids
    ), f"every WebRTC datapoint must carry a call_sid (P3); got {call_sids}"
    assert (
        len(set(call_sids)) == expected
    ), f"call_sids must be distinct per conversation; got {call_sids}"

    recordings = [_props(dp).get("call_recording_url") for dp in datapoints]
    assert all(recordings), "every conversation must store a whole-call recording"
    assert len(set(recordings)) == expected, "recordings must be per-conversation"

    for dp in datapoints:
        assistant = _assistant_turns(_messages(dp))
        assert assistant, "a conversation produced no assistant turns"
        assert any(
            (m.get("content") or "").strip() for m in assistant
        ), "assistant turns were not transcribed"


def _assert_no_fabricated_dtmf(datapoints: list) -> None:
    """P0: the send_dtmf tool is withheld from DTMF-incapable targets, and the
    transcript marker is only written for tones that actually played -- so a
    WebRTC transcript must never contain a `DTMF:` line."""
    for dp in datapoints:
        for message in _messages(dp):
            content = message.get("content") or ""
            assert not content.startswith(
                "DTMF:"
            ), f"fabricated DTMF marker in a WebRTC transcript: {content!r}"


@requires_smallwebrtc
class TestSmallWebRTCConcurrency:
    """P2: max_parallel_requests > 1 actually runs conversations concurrently."""

    def test_three_concurrent_conversations_are_isolated_and_overlap(self) -> None:
        assert OKAREO_API_KEY and GENERIC_OFFER_URL
        offer_url: str = GENERIC_OFFER_URL
        okareo = Okareo(api_key=OKAREO_API_KEY, base_path=BASE_URL)
        rnd = random_string(5)

        def _run(topics: List[str], parallel: int, label: str) -> tuple:
            scenario = okareo.create_scenario_set(
                ScenarioSetCreate(
                    name=f"WebRTC Conc Scenario {label} - {rnd}",
                    seed_data=_seed(topics),
                )
            )
            started = time.monotonic()
            evaluation = okareo.run_simulation(
                driver=Driver(
                    name=f"WebRTC Conc Driver {label} - {rnd}",
                    temperature=0.6,
                    prompt_template=DRIVER_PROMPT,
                ),
                target=Target(
                    name=f"WebRTC Conc Target {label} - {rnd}",
                    target=SmallWebRTCTarget(
                        offer_url=offer_url,
                        max_parallel_requests=parallel,
                    ),
                ),
                name=f"WebRTC Conc {label} - {rnd}",
                scenario=scenario,
                max_turns=2,
                repeats=1,
                first_turn="driver",  # the echo agent does not greet
                calculate_metrics=True,
                checks=["latency"],
            )
            elapsed = time.monotonic() - started
            assert getattr(evaluation, "id", None), "no test run id"
            return evaluation, elapsed

        # Baseline: one conversation, so the concurrency assertion below has a
        # same-session, same-agent yardstick.
        baseline_eval, baseline_s = _run(CONCURRENT_TOPICS[:1], parallel=1, label="1x")
        baseline_dps = _get_datapoints(okareo, baseline_eval.id)
        _assert_per_conversation_isolation(baseline_dps, expected=1)

        concurrent_eval, concurrent_s = _run(CONCURRENT_TOPICS, parallel=3, label="3x")
        datapoints = _get_datapoints(okareo, concurrent_eval.id)

        _assert_per_conversation_isolation(datapoints, expected=3)
        _assert_no_fabricated_dtmf(datapoints)

        # Wall-clock proof the calls overlapped: serial execution of 3
        # conversations costs >= 3x one conversation; concurrent execution
        # should land near 1x. 2.25x splits the difference with margin for
        # per-conversation setup jitter -- the pre-P2 serial runner sat at
        # ~3x and fails this loudly.
        print(
            f"\nbaseline(1 conv): {baseline_s:.1f}s, "
            f"concurrent(3 convs): {concurrent_s:.1f}s "
            f"(ratio {concurrent_s / baseline_s:.2f}x)",
            flush=True,
        )
        assert concurrent_s < 2.25 * baseline_s, (
            f"3 conversations took {concurrent_s:.1f}s vs {baseline_s:.1f}s for 1 "
            "-- they appear to have run serially (the P2 gate is not in effect "
            "on this server)"
        )


@requires_smallwebrtc
class TestSmallWebRTCAugmentations:
    """P0: supported augmentations run; unsupported ones degrade gracefully."""

    def _simulate(self, okareo: Okareo, augmentation: Augmentation, label: str) -> list:
        offer_url = GENERIC_OFFER_URL
        assert offer_url  # narrowed by the class-level skipif
        rnd = random_string(5)
        scenario = okareo.create_scenario_set(
            ScenarioSetCreate(
                name=f"WebRTC Aug Scenario {label} - {rnd}",
                seed_data=_seed(CONCURRENT_TOPICS[:1]),
            )
        )
        evaluation = okareo.run_simulation(
            driver=Driver(
                name=f"WebRTC Aug Driver {label} - {rnd}",
                temperature=0.6,
                prompt_template=DRIVER_PROMPT,
            ),
            target=Target(
                name=f"WebRTC Aug Target {label} - {rnd}",
                target=SmallWebRTCTarget(offer_url=offer_url, max_parallel_requests=1),
            ),
            name=f"WebRTC Aug {label} - {rnd}",
            scenario=scenario,
            max_turns=2,
            repeats=1,
            first_turn="driver",
            calculate_metrics=True,
            checks=["latency"],
            augmentation=augmentation,
        )
        assert getattr(evaluation, "id", None), "no test run id"
        return _get_datapoints(okareo, evaluation.id)

    def test_noise_augmentation_runs_on_webrtc(self) -> None:
        """Noise needs no edge capability (pure on_pcm) -- the run must
        complete with transcribed datapoints and a recording. Definitive
        proof the noise is audible lives in the recording itself; here we
        prove the augmented pipeline works end to end on this edge."""
        assert OKAREO_API_KEY
        okareo = Okareo(api_key=OKAREO_API_KEY, base_path=BASE_URL)
        datapoints = self._simulate(
            okareo,
            Augmentation(
                noise=NoiseAugmentation(probability=1.0, profile="cafeteria", snr_db=10)
            ),
            label="noise",
        )
        _assert_per_conversation_isolation(datapoints, expected=1)

    def test_unsupported_backchannel_degrades_gracefully(self) -> None:
        """Backchannel requires send_injection, which the WebRTC edge does not
        have yet: the strategy must be DROPPED (server logs a warning naming
        it) and the run must still complete normally -- not fail, and not
        fabricate any injected/DTMF artifacts in the transcript."""
        assert OKAREO_API_KEY
        okareo = Okareo(api_key=OKAREO_API_KEY, base_path=BASE_URL)
        datapoints = self._simulate(
            okareo,
            Augmentation(backchannel=BackchannelAugmentation(probability=1.0)),
            label="backchannel",
        )
        _assert_per_conversation_isolation(datapoints, expected=1)
        _assert_no_fabricated_dtmf(datapoints)


@requires_retell
class TestRetellConcurrency:
    """P2 + P3 against a hosted vendor: each concurrent conversation gets its
    own create-web-call, and the datapoint's call_sid IS Retell's call id --
    so distinct call_sids are direct proof of per-conversation vendor calls."""

    def test_concurrent_retell_calls_get_distinct_vendor_call_ids(self) -> None:
        assert OKAREO_API_KEY and RETELL_API_KEY and RETELL_AGENT_ID
        okareo = Okareo(api_key=OKAREO_API_KEY, base_path=BASE_URL)
        rnd = random_string(5)
        scenario = okareo.create_scenario_set(
            ScenarioSetCreate(
                name=f"Retell Conc Scenario - {rnd}",
                seed_data=_seed(CONCURRENT_TOPICS[:2]),
            )
        )
        evaluation = okareo.run_simulation(
            driver=Driver(
                name=f"Retell Conc Driver - {rnd}",
                temperature=0.6,
                prompt_template=DRIVER_PROMPT,
            ),
            target=Target(
                name=f"Retell Conc Target - {rnd}",
                target=WebRTCVoiceTarget(
                    platform="retell",
                    agent_id=RETELL_AGENT_ID,
                    max_parallel_requests=2,
                ),
            ),
            name=f"Retell Conc E2E - {rnd}",
            scenario=scenario,
            max_turns=3,
            repeats=1,
            first_turn="target",  # Retell agents greet
            calculate_metrics=True,
            checks=["latency"],
            api_keys={"voice": RETELL_API_KEY},
        )
        assert getattr(evaluation, "id", None), "no test run id"
        datapoints = _get_datapoints(okareo, evaluation.id)

        _assert_per_conversation_isolation(datapoints, expected=2)
        _assert_no_fabricated_dtmf(datapoints)

        # Retell call ids are `call_...`; both datapoints carrying one proves
        # the vendor id propagated (P3) AND that two separate web calls were
        # created (per-conversation acquire), not one shared session.
        call_sids = [_props(dp).get("call_sid") for dp in datapoints]
        assert all(
            isinstance(sid, str) and sid.startswith("call_") for sid in call_sids
        ), f"expected Retell call ids ('call_...') as call_sids, got {call_sids}"

        # Retell records server-side; the edge downloads + rehosts it, so the
        # recording source should be the vendor, not the local-mix fallback.
        sources = {_props(dp).get("call_recording_source") for dp in datapoints}
        assert sources == {
            "retell"
        }, f"expected vendor ('retell') recordings, got sources={sources}"


# --------------------------------------------------------------------------
# Daily REST mode (Tier 3 -> automated: needs the bot-per-room watcher)
# --------------------------------------------------------------------------

DAILY_API_KEY = os.environ.get("DAILY_API_KEY")

requires_daily_rest = pytest.mark.skipif(
    not (OKAREO_API_KEY and DAILY_API_KEY),
    reason=(
        "needs OKAREO_API_KEY + DAILY_API_KEY -- and the bot-per-room watcher "
        "running: python okareo_server/scripts/daily/room_watcher.py"
    ),
)


def _daily_okareo_rooms(api_key: str) -> List[str]:
    """Names of okareo-sim-* rooms currently existing on the Daily account."""
    import httpx

    response = httpx.get(
        "https://api.daily.co/v1/rooms?limit=100",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json().get("data", [])
    return [
        room["name"]
        for room in data
        if isinstance(room, dict)
        and str(room.get("name", "")).startswith("okareo-sim-")
    ]


@requires_daily_rest
class TestDailyRestConcurrency:
    """P1 REST mode + P2 concurrency against real Daily infrastructure.

    PREREQUISITE: ``scripts/daily/room_watcher.py`` must be running with the
    same DAILY_API_KEY -- Okareo creates a fresh ``okareo-sim-*`` room per
    conversation (no ``room_url`` on the target selects REST mode) and the
    watcher spawns an echo agent into each one. Proves: per-conversation room
    creation, concurrent isolation, and room cleanup at release.
    """

    def test_two_concurrent_rest_rooms_are_isolated_and_cleaned_up(self) -> None:
        assert OKAREO_API_KEY and DAILY_API_KEY
        okareo = Okareo(api_key=OKAREO_API_KEY, base_path=BASE_URL)
        rnd = random_string(5)
        scenario = okareo.create_scenario_set(
            ScenarioSetCreate(
                name=f"Daily REST Conc Scenario - {rnd}",
                seed_data=_seed(CONCURRENT_TOPICS[:2]),
            )
        )
        evaluation = okareo.run_simulation(
            driver=Driver(
                name=f"Daily REST Conc Driver - {rnd}",
                temperature=0.6,
                prompt_template=DRIVER_PROMPT,
            ),
            target=Target(
                name=f"Daily REST Conc Target - {rnd}",
                # No room_url: REST mode -- Okareo creates a room per
                # conversation with the key below; the watcher answers them.
                target=WebRTCVoiceTarget(platform="daily", max_parallel_requests=2),
            ),
            name=f"Daily REST Conc E2E - {rnd}",
            scenario=scenario,
            max_turns=2,
            repeats=1,
            first_turn="driver",  # the echo agent does not greet
            calculate_metrics=True,
            checks=["latency"],
            api_keys={"voice": DAILY_API_KEY},
        )
        assert getattr(evaluation, "id", None), "no test run id"
        datapoints = _get_datapoints(okareo, evaluation.id)

        _assert_per_conversation_isolation(datapoints, expected=2)
        _assert_no_fabricated_dtmf(datapoints)

        # Daily direct/REST has no vendor recording -> Okareo's local mix.
        sources = {_props(dp).get("call_recording_source") for dp in datapoints}
        assert sources == {"okareo_local_mix"}, f"unexpected sources: {sources}"

        # release() deletes each REST-created room (exp is only the backstop
        # for crashed workers). Poll briefly: deletion is per-conversation
        # teardown and can trail the run's finalize by a moment.
        leftovers = _daily_okareo_rooms(DAILY_API_KEY)
        for _ in range(4):
            if not leftovers:
                break
            time.sleep(2)
            leftovers = _daily_okareo_rooms(DAILY_API_KEY)
        assert not leftovers, (
            f"okareo-sim rooms not deleted at release: {leftovers} "
            "(their exp will reap them, but eager cleanup is the contract)"
        )


# --------------------------------------------------------------------------
# LiveKit direct (Tier 3 -> automated: needs creds + the agent worker)
# --------------------------------------------------------------------------

LIVEKIT_URL = os.environ.get("LIVEKIT_URL")
LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET")

requires_livekit = pytest.mark.skipif(
    not (OKAREO_API_KEY and LIVEKIT_URL and LIVEKIT_API_KEY and LIVEKIT_API_SECRET),
    reason=(
        "needs OKAREO_API_KEY + LIVEKIT_URL/LIVEKIT_API_KEY/LIVEKIT_API_SECRET "
        "-- and the agent worker running: python scripts/livekit/agent.py dev "
        "(auto-dispatches into every new room; needs OPENAI_API_KEY)"
    ),
)


@requires_livekit
class TestLiveKitDirectConcurrency:
    """#1026's templated room name at concurrency 3, against a live agent.

    PREREQUISITE: ``scripts/livekit/agent.py dev`` -- a livekit-agents worker
    with automatic dispatch, so it joins every ``okareo-sim-*`` room the
    template mints. LiveKit creates rooms on first join, so unlike Daily no
    broker/watcher is needed: the template IS the per-conversation isolation.
    """

    def test_three_concurrent_templated_rooms_are_isolated(self) -> None:
        assert OKAREO_API_KEY and LIVEKIT_URL
        assert LIVEKIT_API_KEY and LIVEKIT_API_SECRET
        okareo = Okareo(api_key=OKAREO_API_KEY, base_path=BASE_URL)
        rnd = random_string(5)
        scenario = okareo.create_scenario_set(
            ScenarioSetCreate(
                name=f"LiveKit Conc Scenario - {rnd}",
                seed_data=_seed(CONCURRENT_TOPICS),
            )
        )
        evaluation = okareo.run_simulation(
            driver=Driver(
                name=f"LiveKit Conc Driver - {rnd}",
                temperature=0.6,
                prompt_template=DRIVER_PROMPT,
            ),
            target=Target(
                name=f"LiveKit Conc Target - {rnd}",
                target=WebRTCVoiceTarget(
                    platform="livekit",
                    livekit_url=LIVEKIT_URL,
                    livekit_api_key=LIVEKIT_API_KEY,
                    livekit_api_secret=LIVEKIT_API_SECRET,
                    # The load-bearing part: a STATIC name here would put all
                    # three conversations in ONE room (the pre-#1026 bug).
                    room_name="okareo-sim-{scenario_row_run_guid}",
                    max_parallel_requests=3,
                ),
            ),
            name=f"LiveKit Conc E2E - {rnd}",
            scenario=scenario,
            max_turns=2,
            repeats=1,
            first_turn="target",  # the livekit agent greets first
            calculate_metrics=True,
            checks=["latency"],
        )
        assert getattr(evaluation, "id", None), "no test run id"
        datapoints = _get_datapoints(okareo, evaluation.id)

        _assert_per_conversation_isolation(datapoints, expected=3)
        _assert_no_fabricated_dtmf(datapoints)

        # Local mix (LiveKit direct produces no vendor recording).
        sources = {_props(dp).get("call_recording_source") for dp in datapoints}
        assert sources == {"okareo_local_mix"}, f"unexpected sources: {sources}"
