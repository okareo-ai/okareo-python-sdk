"""
Voice Augmentation Parameter Tests

End-to-end tests that run one simulation per augmentation type with
explicitly non-default parameters, verify that simulation_params
roundtrips correctly on the completed test run, and confirm the
simulation finishes without error.

Each test uses max_turns=1, repeats=1, and a single-datapoint scenario
to minimize per-sim runtime.
"""

import os
from typing import Any, Dict, List
from uuid import UUID

import pytest
from okareo_tests.common import random_string

from okareo import Okareo
from okareo.augmentations import (
    Augmentation,
    BackchannelAugmentation,
    BargeInAugmentation,
    CAPAugmentation,
    DirectedSpeechAugmentation,
    DropoutAugmentation,
    NoiseAugmentation,
    SecondarySpeakerAugmentation,
)
from okareo.model_under_test import Driver, Target, TwilioVoiceTarget
from okareo_api_client.models.find_test_data_point_payload import (
    FindTestDataPointPayload,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.test_run_item import TestRunItem
from okareo_api_client.types import Unset

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_PHONE = os.getenv("TWILIO_FROM_PHONE")
TWILIO_TO_PHONE = os.getenv("TWILIO_TO_PHONE")

DRIVER_PROMPT = """
## Persona
- **Identity:** You are {scenario_input.name} calling about {scenario_input.topic}.

## Rules
- EVERY MESSAGE MUST BE THREE WORDS OR FEWER.
- Ask one question at a time.
- Never elaborate.
""".strip()

AUGMENTATION_CONFIGS: Dict[str, Augmentation] = {
    "cap": Augmentation(
        cap=CAPAugmentation(probability=0.7, pause_ms=2000),
    ),
    "directed_speech": Augmentation(
        directed_speech=DirectedSpeechAugmentation(
            probability=0.5,
            prompt="You are testing directed speech augmentation.",
            lpf_cutoff_hz=600,
            gain_db=-12.0,
            start_at_turn=2,
        ),
    ),
    "noise": Augmentation(
        noise=NoiseAugmentation(
            probability=0.5,
            profile="traffic",
            snr_db=15,
        ),
    ),
    "secondary_speaker": Augmentation(
        secondary_speaker=SecondarySpeakerAugmentation(
            probability=0.4,
            voice="oscar",
            prompt="You are a bystander making small talk.",
            lpf_cutoff_hz=600,
            gain_db=-12.0,
            inter_speaker_pause_ms=2000,
            start_at_turn=2,
        ),
    ),
    "backchannel": Augmentation(
        backchannel=BackchannelAugmentation(
            probability=0.5,
            utterance="yeah",
            min_offset_ms=500,
            max_offset_ms=2000,
            start_at_turn=2,
        ),
    ),
    "barge_in": Augmentation(
        barge_in=BargeInAugmentation(
            probability=0.3,
            prompt="Interrupt and ask to be put on hold.",
            replacement_text="wait a second",
            min_offset_ms=500,
            max_offset_ms=2000,
            start_at_turn=2,
        ),
    ),
    "dropout": Augmentation(
        dropout=DropoutAugmentation(probability=0.2, start_at_turn=2),
    ),
}


# ============================================================================
# Fixtures
# ============================================================================


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
                "input": {"name": "Alex", "topic": "store hours", "voice": "oscar"},
                "result": "Expected response.",
            }
        ]
    )
    return okareo.create_scenario_set(
        ScenarioSetCreate(name=f"Aug Params Scenario - {rnd}", seed_data=seed_data)
    )


@pytest.fixture(scope="module")
def driver(rnd: str) -> Driver:
    return Driver(
        name=f"Aug Params Driver - {rnd}",
        temperature=0.5,
        prompt_template=DRIVER_PROMPT,
    )


# ============================================================================
# Helpers
# ============================================================================


def extract_sim_params(test_run: TestRunItem) -> Dict[str, Any]:
    """Extract simulation_params as a plain dict from a TestRunItem."""
    sim_params = test_run.simulation_params
    if isinstance(sim_params, Unset) or sim_params is None:
        return {}
    return sim_params.to_dict()


def run_and_verify_augmentation(
    okareo: Okareo,
    twilio_target: TwilioVoiceTarget,
    scenario: Any,
    driver: Driver,
    rnd: str,
    aug_name: str,
    aug_config: Augmentation,
) -> None:
    """Run a simulation with the given augmentation and verify roundtrip."""
    evaluation = okareo.run_simulation(
        driver=driver,
        target=Target(
            name=f"Aug Target {aug_name} - {rnd}",
            target=twilio_target,
        ),
        name=f"Aug Test {aug_name} - {rnd}",
        scenario=scenario,
        max_turns=1,
        repeats=1,
        first_turn="target",
        calculate_metrics=True,
        augmentation=aug_config,
        checks=["time_to_first_audio"],
    )

    assert isinstance(
        evaluation, TestRunItem
    ), f"{aug_name}: expected TestRunItem, got {type(evaluation)}"
    assert evaluation.id is not None, f"{aug_name}: test run should have an ID"
    assert (
        evaluation.status == "FINISHED"
    ), f"{aug_name}: expected FINISHED, got {evaluation.status}"

    sim_params = extract_sim_params(evaluation)
    assert (
        "augmentation" in sim_params
    ), f"{aug_name}: simulation_params should contain 'augmentation'"
    aug_payload = sim_params["augmentation"]
    assert aug_name in aug_payload, (
        f"{aug_name}: augmentation payload should contain key '{aug_name}', "
        f"got {list(aug_payload.keys())}"
    )

    expected = aug_config.to_dict()[aug_name]
    actual = aug_payload[aug_name]
    for param_key, param_value in expected.items():
        assert (
            param_key in actual
        ), f"{aug_name}.{param_key}: missing from server response"
        assert actual[param_key] == param_value, (
            f"{aug_name}.{param_key}: expected {param_value}, "
            f"got {actual[param_key]}"
        )


# ============================================================================
# Tests
# ============================================================================


class TestAugmentationParams:
    """Run one sim per augmentation type, verify params roundtrip and completion."""

    @pytest.mark.parametrize("aug_name", list(AUGMENTATION_CONFIGS.keys()))
    def test_augmentation_roundtrip(
        self,
        okareo: Okareo,
        twilio_target: TwilioVoiceTarget,
        scenario: Any,
        driver: Driver,
        rnd: str,
        aug_name: str,
    ) -> None:
        run_and_verify_augmentation(
            okareo,
            twilio_target,
            scenario,
            driver,
            rnd,
            aug_name,
            AUGMENTATION_CONFIGS[aug_name],
        )


# ============================================================================
# Behavior: dropout actually drops the turns it says it will
# ============================================================================


def _conversation(okareo: Okareo, test_run: TestRunItem) -> Dict[str, Any]:
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


def _driver_turns(meta: Dict[str, Any]) -> List[int]:
    return sorted(
        {
            m["metadata"]["turn_number"]
            for m in meta.get("messages", [])
            if m.get("role") == "user"
        }
    )


class TestDropoutBehavior:
    """A roundtrip proves the config arrived; this proves it took effect."""

    def test_dropout_silences_the_driver_from_its_start_turn(
        self,
        okareo: Okareo,
        twilio_target: TwilioVoiceTarget,
        scenario: Any,
        driver: Driver,
        rnd: str,
    ) -> None:
        start_at_turn = 2
        evaluation = okareo.run_simulation(
            driver=driver,
            target=Target(
                name=f"Dropout Behavior Target - {rnd}", target=twilio_target
            ),
            name=f"Dropout Behavior - {rnd}",
            scenario=scenario,
            max_turns=3,
            repeats=1,
            first_turn="target",
            augmentation=Augmentation(
                dropout=DropoutAugmentation(
                    probability=1.0, start_at_turn=start_at_turn
                )
            ),
            checks=["avg_turn_taking_latency"],
        )
        assert (
            evaluation.status == "FINISHED"
        ), f"expected FINISHED, got {evaluation.status}"

        meta = _conversation(okareo, evaluation)

        # The start turn was dropped, and nothing before it ...
        dropped = meta.get("dropped_turns") or []
        assert dropped, "expected dropped_turns to be recorded on the datapoint"
        assert min(dropped) >= start_at_turn
        assert start_at_turn in dropped

        # ... the Driver said nothing on any turn that was dropped ...
        #
        # Not "nothing from the start turn on": a turn is only dropped when the
        # Target spoke on the turn before it. Once both sides are silent the
        # Driver's turn is the only thing that can revive the call, so it is
        # left alone -- and against an agent that waits rather than re-prompts
        # the Driver comes back on the next turn, which is correct.
        assert set(_driver_turns(meta)).isdisjoint(dropped)

        # ... the dead air did not end the call early (a Driver that says
        # goodbye on its own is fine; the silence cutoff firing is not) ...
        assert meta.get("termination_reason") not in {
            "No response from the Target",
            "Ended early after an error",
            "Connection disconnected",
            "Target disconnected before the conversation started",
        }

        # ... and a dropped turn left no empty row behind. A keypress is
        # exempt: it is a ``user`` row carrying the send_dtmf call with
        # ``content: null``, and the IVR testtarget asks for keypad input.
        spoken = [m for m in meta["messages"] if not m.get("tool_calls")]
        assert all((m.get("content") or "").strip() for m in spoken)
