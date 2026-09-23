"""Live check that dropout does not derail the Driver.

Runs the SAME scenario twice against the same target -- once clean, once with
dropout -- and compares them. The assertions are structural rather than about
wording, because the Driver is an LLM: what must hold is that the turns it does
speak look like the turns of a clean run, that a dropped turn leaves no trace
in the transcript, and that the run still finishes normally.

Opt-in: these dial a real voice target and cost time, so they are skipped
unless ``OKAREO_DROPOUT_LIVE_OFFER_URL`` is set. Against the local stack
(docker + ``scripts/smallwebrtc/agent.py`` on :8081) that is::

    OKAREO_BASE_URL=http://localhost:8000 \\
    OKAREO_DROPOUT_LIVE_OFFER_URL=http://host.docker.internal:8081/api/offer \\
    pytest okareo_tests/test_voice_dropout_behavior.py

The server must already support the ``dropout`` augmentation; until it ships,
point this at a host that has it.
"""

import os
from typing import Any, Dict, List
from uuid import UUID

import pytest
from attrs import define, field
from okareo_tests.common import random_string

from okareo import Okareo
from okareo.augmentations import Augmentation, DropoutAugmentation
from okareo.model_under_test import Driver, Target, VoiceTarget
from okareo_api_client.models.find_test_data_point_payload import (
    FindTestDataPointPayload,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate

OFFER_URL = os.getenv("OKAREO_DROPOUT_LIVE_OFFER_URL")
BASE_URL = os.getenv("OKAREO_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("OKAREO_API_KEY", "")

pytestmark = pytest.mark.skipif(
    not (OFFER_URL and API_KEY),
    reason="live voice run: set OKAREO_DROPOUT_LIVE_OFFER_URL and OKAREO_API_KEY",
)

MAX_TURNS = 4
# Drop every turn from here on, so the comparison is deterministic: turns
# before this must look exactly like a clean run.
DROP_FROM_TURN = 3

DRIVER_PROMPT = (
    "You are a customer calling support. {scenario_input} "
    "Keep every reply to one short sentence."
)


@define
class _SmallWebRTCTarget(VoiceTarget):
    """The local pipecat echo answerer (scripts/smallwebrtc/agent.py)."""

    edge_type = "webrtc"
    offer_url: str = field(default="")

    def params(self) -> dict:
        return {
            "type": "voice",
            "edge_type": "webrtc",
            "platform": "smallwebrtc",
            "offer_url": self.offer_url,
        }


def _run(okareo: Okareo, name: str, augmentation: Any) -> Any:
    scenario = okareo.create_scenario_set(
        ScenarioSetCreate(
            name=f"{name}-scenario",
            seed_data=Okareo.seed_data_from_list(
                [
                    {
                        "input": "Ask how to reset your router.",
                        "result": "The agent explains how to reset the router.",
                    }
                ]
            ),
        )
    )
    return okareo.run_simulation(
        name=name,
        target=Target(
            name="dropout-behavior-echo",
            target=_SmallWebRTCTarget(  # type: ignore[arg-type]
                offer_url=OFFER_URL or ""
            ),
        ),
        driver=Driver(name=f"{name}-driver", prompt_template=DRIVER_PROMPT),
        scenario=scenario,
        max_turns=MAX_TURNS,
        first_turn="driver",
        checks=["avg_turn_taking_latency"],
        augmentation=augmentation,
    )


def _conversation(okareo: Okareo, test_run: Any) -> Dict[str, Any]:
    """The finished conversation: its messages and its dropped turns."""
    rows = okareo.find_test_data_points(
        FindTestDataPointPayload(
            test_run_id=UUID(str(test_run.id)), full_data_point=True
        )
    )
    for row in rows:
        raw: Any = getattr(row, "model_metadata", None)
        # full_data_point rows carry a generated model, not a plain dict.
        meta = raw.to_dict() if hasattr(raw, "to_dict") else raw
        if isinstance(meta, dict) and meta.get("messages"):
            return meta
    raise AssertionError(f"no conversation recorded for run {test_run.id}")


def _driver_lines(meta: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [m for m in meta.get("messages", []) if m.get("role") == "user"]


def _turns_with_driver_speech(meta: Dict[str, Any]) -> List[int]:
    return sorted({m["metadata"]["turn_number"] for m in _driver_lines(meta)})


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(API_KEY, base_path=BASE_URL)


@pytest.fixture(scope="module")
def baseline(okareo: Okareo) -> Dict[str, Any]:
    run = _run(okareo, f"dropout-baseline-{random_string(5)}", None)
    assert run.status == "FINISHED", f"baseline did not finish: {run.status}"
    return _conversation(okareo, run)


@pytest.fixture(scope="module")
def dropped(okareo: Okareo) -> Dict[str, Any]:
    run = _run(
        okareo,
        f"dropout-live-{random_string(5)}",
        Augmentation(
            dropout=DropoutAugmentation(probability=1.0, start_at_turn=DROP_FROM_TURN)
        ),
    )
    assert run.status == "FINISHED", f"dropout run did not finish: {run.status}"
    return _conversation(okareo, run)


def test_the_run_still_reaches_the_turn_limit(dropped: Dict[str, Any]) -> None:
    """Dead air must not end the call early (the silence cutoff must not fire)."""
    assert dropped.get("termination_reason") == "Reached the turn limit"


def test_the_driver_speaks_on_every_turn_before_the_drops(
    baseline: Dict[str, Any], dropped: Dict[str, Any]
) -> None:
    expected = [t for t in _turns_with_driver_speech(baseline) if t < DROP_FROM_TURN]

    assert _turns_with_driver_speech(dropped) == expected


def test_no_driver_speech_survives_a_dropped_turn(dropped: Dict[str, Any]) -> None:
    assert all(t < DROP_FROM_TURN for t in _turns_with_driver_speech(dropped))
    assert dropped.get("dropped_turns")
    assert min(dropped["dropped_turns"]) >= DROP_FROM_TURN


def test_the_transcript_has_no_empty_or_placeholder_rows(
    baseline: Dict[str, Any], dropped: Dict[str, Any]
) -> None:
    for meta in (baseline, dropped):
        assert all((m.get("content") or "").strip() for m in meta["messages"])


def test_the_driver_still_sounds_like_itself(
    baseline: Dict[str, Any], dropped: Dict[str, Any]
) -> None:
    """A rough guard against derailment: the surviving turns are still short,
    single-sentence customer lines rather than confused restarts."""
    kept = [
        m
        for m in _driver_lines(dropped)
        if m["metadata"]["turn_number"] < DROP_FROM_TURN
    ]
    assert kept, "expected the Driver to speak before the drops began"

    base_words = [
        len((m.get("content") or "").split()) for m in _driver_lines(baseline)
    ]
    kept_words = [len((m.get("content") or "").split()) for m in kept]
    baseline_max = max(base_words) if base_words else 0

    # Generous: catches a Driver that starts monologuing, not ordinary variation.
    assert max(kept_words) <= max(baseline_max * 3, 40)


def test_the_target_reply_after_dead_air_is_not_counted_as_slow(
    dropped: Dict[str, Any]
) -> None:
    """A reply into the silence must not be timed as a response, or the
    dead-air wait would inflate every latency metric."""
    for msg in dropped["messages"]:
        if msg.get("role") == "assistant" and msg["metadata"].get(
            "after_driver_dropout"
        ):
            assert msg["metadata"].get("latency") is None
