"""Dropout must not derail the Driver, checked end to end over a real call.

Runs the SAME scenario twice against the same target -- once clean, once with
dropout -- and compares them. The assertions are structural rather than about
wording, because the Driver is an LLM: what must hold is that the turns it does
speak look like the turns of a clean run, that a dropped turn leaves no trace in
the transcript, and that the run still finishes normally.

Target: the Twilio testtarget, as the rest of the voice suite uses. Dials
TWILIO_TO_PHONE, whose webhook points at okareo_server's
``/v0/voice/twilio/testtarget``.

Requires (same as test_voice_augmentation_params.py):
  OKAREO_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_PHONE,
  TWILIO_TO_PHONE

Against a local server, point the client at it and make sure the number's
webhook reaches that server (e.g. via ngrok)::

    OKAREO_BASE_URL=http://localhost:8000 pytest \
        okareo_tests/test_voice_dropout_behavior.py

Two calls, so it is skipped unless the Twilio credentials are present.
"""

import os
from typing import Any, Dict, List
from uuid import UUID

import pytest
from okareo_tests.common import random_string

from okareo import Okareo
from okareo.augmentations import Augmentation, DropoutAugmentation
from okareo.model_under_test import Driver, Target, TwilioVoiceTarget
from okareo_api_client.models.find_test_data_point_payload import (
    FindTestDataPointPayload,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_PHONE = os.getenv("TWILIO_FROM_PHONE")
TWILIO_TO_PHONE = os.getenv("TWILIO_TO_PHONE")

pytestmark = pytest.mark.skipif(
    not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_TO_PHONE),
    reason="live voice run: needs TWILIO_ACCOUNT_SID/AUTH_TOKEN/TO_PHONE",
)

# Endings that would mean dropout broke the call rather than merely silencing
# a turn. A Driver that says goodbye on its own is fine.
BAD_ENDINGS = {
    "No response from the Target",
    "Ended early after an error",
    "Connection disconnected",
    "Target disconnected before the conversation started",
}

MAX_TURNS = 4
# Drop every Driver turn from here on, so the comparison is deterministic: the
# turns before it must look like a clean run, and none after it may speak.
DROP_FROM_TURN = 3

DRIVER_PROMPT = """
## Persona
- **Identity:** You are {scenario_input.name} calling about {scenario_input.topic}.

## Rules
- EVERY MESSAGE MUST BE THREE WORDS OR FEWER.
- Ask one question at a time.
- Never elaborate.
""".strip()


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=os.environ["OKAREO_API_KEY"])


@pytest.fixture(scope="module")
def twilio_target() -> TwilioVoiceTarget:
    assert TWILIO_ACCOUNT_SID is not None, "TWILIO_ACCOUNT_SID must be set"
    assert TWILIO_AUTH_TOKEN is not None, "TWILIO_AUTH_TOKEN must be set"
    return TwilioVoiceTarget(
        account_sid=TWILIO_ACCOUNT_SID,
        auth_token=TWILIO_AUTH_TOKEN,
        from_phone_number=TWILIO_FROM_PHONE,
        to_phone_number=TWILIO_TO_PHONE,
    )


@pytest.fixture(scope="module")
def scenario(okareo: Okareo, rnd: str) -> Any:
    seed_data = Okareo.seed_data_from_list(
        [
            {
                "input": {"name": "Alex", "topic": "store hours"},
                "result": "Expected response.",
            }
        ]
    )
    return okareo.create_scenario_set(
        ScenarioSetCreate(
            name=f"Dropout Behavior Scenario - {rnd}", seed_data=seed_data
        )
    )


@pytest.fixture(scope="module")
def driver(rnd: str) -> Driver:
    return Driver(
        name=f"Dropout Behavior Driver - {rnd}",
        temperature=0.5,
        prompt_template=DRIVER_PROMPT,
    )


def _run(
    okareo: Okareo,
    twilio_target: TwilioVoiceTarget,
    scenario: Any,
    driver: Driver,
    rnd: str,
    name: str,
    augmentation: Any,
) -> Any:
    evaluation = okareo.run_simulation(
        driver=driver,
        target=Target(name=f"Dropout {name} Target - {rnd}", target=twilio_target),
        name=f"Dropout {name} - {rnd}",
        scenario=scenario,
        max_turns=MAX_TURNS,
        repeats=1,
        first_turn="target",
        augmentation=augmentation,
        checks=["avg_turn_taking_latency"],
    )
    assert (
        evaluation.status == "FINISHED"
    ), f"{name}: expected FINISHED, got {evaluation.status}"
    return evaluation


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
def baseline(
    okareo: Okareo,
    twilio_target: TwilioVoiceTarget,
    scenario: Any,
    driver: Driver,
    rnd: str,
) -> Dict[str, Any]:
    run = _run(okareo, twilio_target, scenario, driver, rnd, "Baseline", None)
    return _conversation(okareo, run)


@pytest.fixture(scope="module")
def dropped(
    okareo: Okareo,
    twilio_target: TwilioVoiceTarget,
    scenario: Any,
    driver: Driver,
    rnd: str,
) -> Dict[str, Any]:
    run = _run(
        okareo,
        twilio_target,
        scenario,
        driver,
        rnd,
        "Dropout",
        Augmentation(
            dropout=DropoutAugmentation(probability=1.0, start_at_turn=DROP_FROM_TURN)
        ),
    )
    return _conversation(okareo, run)


class TestDropoutDoesNotDerailTheDriver:
    def test_dead_air_does_not_end_the_call(self, dropped: Dict[str, Any]) -> None:
        """The silence cutoff must not fire on turns the Driver dropped."""
        assert dropped.get("termination_reason") not in BAD_ENDINGS

    def test_the_driver_speaks_on_every_turn_before_the_drops(
        self, baseline: Dict[str, Any], dropped: Dict[str, Any]
    ) -> None:
        expected = [
            t for t in _turns_with_driver_speech(baseline) if t < DROP_FROM_TURN
        ]

        assert _turns_with_driver_speech(dropped) == expected

    def test_no_driver_speech_survives_a_dropped_turn(
        self, dropped: Dict[str, Any]
    ) -> None:
        assert all(t < DROP_FROM_TURN for t in _turns_with_driver_speech(dropped))
        assert dropped.get("dropped_turns")
        assert min(dropped["dropped_turns"]) >= DROP_FROM_TURN

    def test_the_transcript_has_no_empty_or_placeholder_rows(
        self, baseline: Dict[str, Any], dropped: Dict[str, Any]
    ) -> None:
        """A dropped turn must leave no row behind. A keypress is exempt: it
        is recorded as a ``user`` row carrying the ``send_dtmf`` call with
        ``content: null``, answered by a ``tool`` row -- the IVR testtarget
        asks for keypad input, so real runs contain them."""
        for meta in (baseline, dropped):
            spoken = [m for m in meta["messages"] if not m.get("tool_calls")]
            assert all((m.get("content") or "").strip() for m in spoken)

    def test_the_driver_still_sounds_like_itself(
        self, baseline: Dict[str, Any], dropped: Dict[str, Any]
    ) -> None:
        """A rough guard against derailment: the surviving turns are still the
        short persona lines of a clean run, not confused restarts."""
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

        # Generous: catches a Driver that starts monologuing, not ordinary
        # variation between two LLM runs.
        assert max(kept_words) <= max(baseline_max * 3, 40)

    def test_the_target_reply_after_dead_air_is_not_counted_as_slow(
        self, dropped: Dict[str, Any]
    ) -> None:
        """A reply into the silence must not be timed as a response, or the
        dead-air wait would inflate every latency metric."""
        for msg in dropped["messages"]:
            if msg.get("role") == "assistant" and msg["metadata"].get(
                "after_driver_dropout"
            ):
                assert msg["metadata"].get("latency") is None
