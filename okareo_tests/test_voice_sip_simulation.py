"""
Voice SIP Simulation Tests

Mirrors test_voice_simulation.py but dials a SIP URI instead of a PSTN number.
The target is a Twilio SIP Domain pointed at the same TwiML/webhook as the
existing PSTN voice agent — so the agent code is identical; only the transport
is SIP. This validates the SIP target end-to-end against a real agent.

Env (each field is target-scoped — CI maps the blue/prod variant per job):
  TWILIO_TO_SIP_URI       ←  secrets.TWILIO_{BLUE,PROD}_TARGET_SIP_URI
  TWILIO_TO_SIP_USERNAME  ←  secrets.TWILIO_{BLUE,PROD}_TARGET_SIP_USERNAME
  TWILIO_TO_SIP_PASSWORD  ←  secrets.TWILIO_{BLUE,PROD}_TARGET_SIP_PASSWORD

Auth fields are kept separate from the URI so the same shape extends to
non-digest auth modes (certs, bearer tokens, IP-ACL-only) without re-encoding
the URI. Each field is independently optional; only TWILIO_TO_SIP_URI is
required to enable the suite.
"""

import os

import pytest
from okareo_tests.common import random_string

# Reuse the platform-agnostic validators + helpers from the PSTN suite.
from okareo_tests.test_voice_simulation import (
    DRIVER_PROMPT,
    TARGET_WAITS_PROMPT,
    create_scenario,
    get_messages,
    validate_test_run_sanity,
)

from okareo import Okareo
from okareo.model_under_test import Driver, SipTarget, Target

TWILIO_TO_SIP_URI = os.getenv("TWILIO_TO_SIP_URI")
TWILIO_TO_SIP_USERNAME = os.getenv("TWILIO_TO_SIP_USERNAME")
TWILIO_TO_SIP_PASSWORD = os.getenv("TWILIO_TO_SIP_PASSWORD")

pytestmark = pytest.mark.skipif(
    not TWILIO_TO_SIP_URI,
    reason="TWILIO_TO_SIP_URI not set — provision a Twilio SIP Domain "
    "(or map TWILIO_{BLUE,PROD}_TARGET_SIP_URI in CI) to enable",
)


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
def sip_target() -> SipTarget:
    """A SIP target pointing at the env-configured Twilio SIP Domain URI.

    Same agent the PSTN tests reach (TWILIO_TO_PHONE) — the Twilio SIP Domain's
    Voice URL is configured to the same TwiML/webhook. We're testing the SIP
    transport against an unchanged agent.
    """
    assert TWILIO_TO_SIP_URI is not None  # pytestmark already gated
    return SipTarget(
        sip_uri=TWILIO_TO_SIP_URI,
        sip_username=TWILIO_TO_SIP_USERNAME,
        sip_password=TWILIO_TO_SIP_PASSWORD,
        max_parallel_requests=5,
    )


# ============================================================================
# Tests — direct mirrors of test_voice_simulation.py
# ============================================================================


class TestVoiceSipSanity:
    """Sanity test for SIP-targeted voice simulations.

    Mirrors TestVoiceSanity::test_sanity_with_parallel_conversations; the only
    change is the target type (SipTarget vs TwilioVoiceTarget). All assertion
    invariants are transport-agnostic.
    """

    def test_sanity_with_parallel_conversations(
        self, okareo: Okareo, sip_target: SipTarget, rnd: str
    ) -> None:
        num_parallel = 5

        driver = Driver(
            name=f"SIP Sanity Driver - {rnd}",
            temperature=0.5,
            prompt_template=DRIVER_PROMPT,
        )

        inputs = [
            {"name": f"Customer{i}", "topic": "store hours", "voice": "oscar"}
            for i in range(num_parallel)
        ]
        scenario = create_scenario(okareo, f"SIP Sanity Scenario - {rnd}", inputs)

        evaluation = okareo.run_simulation(
            driver=driver,
            target=Target(name=f"SIP Target - {rnd}", target=sip_target),
            name=f"SIP Sanity Test - {rnd}",
            scenario=scenario,
            max_turns=3,
            repeats=1,
            first_turn="driver",
            calculate_metrics=True,
            checks=[
                "avg_turn_taking_latency",
                "avg_words_per_minute",
                "total_turn_count",
            ],
        )

        validate_test_run_sanity(
            okareo,
            evaluation,
            expected_conversations=num_parallel,
            validate_metrics=True,
        )


class TestVoiceSipFirstTurn:
    """First-turn control over SIP. Mirrors TestVoiceFirstTurn."""

    def test_target_starts_first(
        self, okareo: Okareo, sip_target: SipTarget, rnd: str
    ) -> None:
        driver = Driver(
            name=f"SIP Target Starts - {rnd}",
            temperature=0.5,
            prompt_template=TARGET_WAITS_PROMPT,
        )
        scenario = create_scenario(
            okareo,
            f"SIP Target Starts Scenario - {rnd}",
            [{"name": "Mike", "topic": "order status", "voice": "oscar"}],
        )

        evaluation = okareo.run_simulation(
            driver=driver,
            target=Target(name=f"SIP Target - {rnd}", target=sip_target),
            name=f"SIP Target Starts Test - {rnd}",
            scenario=scenario,
            max_turns=2,
            repeats=1,
            first_turn="target",
            calculate_metrics=True,
            checks=[
                "avg_turn_taking_latency",
                "avg_words_per_minute",
                "total_turn_count",
            ],
        )

        validate_test_run_sanity(
            okareo,
            evaluation,
            expected_conversations=1,
            validate_metrics=True,
        )

        messages = get_messages(okareo, evaluation.id)[0]
        first_msg = messages[0]
        assert (
            first_msg.get("role") == "assistant"
        ), "First speaker should be target (assistant)"


class TestVoiceSipConcurrent:
    """Concurrent driver messages over SIP. Mirrors TestVoiceConcurrent."""

    def test_concurrent_driver_messages(
        self, okareo: Okareo, sip_target: SipTarget, rnd: str
    ) -> None:
        driver = Driver(
            name=f"SIP Concurrent Driver - {rnd}",
            temperature=0.5,
            prompt_template=DRIVER_PROMPT,
        )
        scenario = create_scenario(
            okareo,
            f"SIP Concurrent Scenario - {rnd}",
            [{"name": "Jane", "topic": "shipping options", "voice": "oscar"}],
        )

        evaluation = okareo.run_simulation(
            driver=driver,
            target=Target(name=f"SIP Target - {rnd}", target=sip_target),
            name=f"SIP Concurrent Driver Test - {rnd}",
            scenario=scenario,
            max_turns=2,
            repeats=1,
            first_turn="driver",
            concurrent_ask_probability=1.0,
            turn_transition_time=50,
            calculate_metrics=True,
            checks=["avg_words_per_minute"],
        )

        assert evaluation.id is not None, "Evaluation should have an ID"

        messages_list = get_messages(okareo, evaluation.id)
        assert messages_list, "No message lists returned"
        messages = messages_list[0]
        user_messages = [m for m in messages if m.get("role") == "user"]
        assert len(user_messages) >= 2, (
            f"concurrent_ask_probability=1.0 should produce at least 2 driver messages. "
            f"Got {len(user_messages)} user messages."
        )
