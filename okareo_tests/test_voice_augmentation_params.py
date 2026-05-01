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
from typing import Any, Dict

import pytest
from okareo_tests.common import random_string

from okareo import Okareo
from okareo.augmentations import (
    Augmentation,
    BackchannelAugmentation,
    BargeInAugmentation,
    CAPAugmentation,
    DirectedSpeechAugmentation,
    NoiseAugmentation,
    SecondarySpeakerAugmentation,
)
from okareo.model_under_test import Driver, Target, TwilioVoiceTarget
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
        ),
    ),
    "backchannel": Augmentation(
        backchannel=BackchannelAugmentation(
            probability=0.5,
            utterance="yeah",
            min_offset_ms=500,
            max_offset_ms=2000,
        ),
    ),
    "barge_in": Augmentation(
        barge_in=BargeInAugmentation(
            probability=0.3,
            replacement_text="wait a second",
            min_offset_ms=500,
            max_offset_ms=2000,
        ),
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
        checks=["avg_turn_taking_latency"],
    )

    assert isinstance(evaluation, TestRunItem), (
        f"{aug_name}: expected TestRunItem, got {type(evaluation)}"
    )
    assert evaluation.id is not None, (
        f"{aug_name}: test run should have an ID"
    )
    assert evaluation.status == "FINISHED", (
        f"{aug_name}: expected FINISHED, got {evaluation.status}"
    )

    sim_params = extract_sim_params(evaluation)
    assert "augmentation" in sim_params, (
        f"{aug_name}: simulation_params should contain 'augmentation'"
    )
    aug_payload = sim_params["augmentation"]
    assert aug_name in aug_payload, (
        f"{aug_name}: augmentation payload should contain key '{aug_name}', "
        f"got {list(aug_payload.keys())}"
    )

    expected = aug_config.to_dict()[aug_name]
    actual = aug_payload[aug_name]
    for param_key, param_value in expected.items():
        assert param_key in actual, (
            f"{aug_name}.{param_key}: missing from server response"
        )
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
