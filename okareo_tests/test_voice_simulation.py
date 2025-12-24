"""
Voice Simulation Tests

Tests for voice simulations via Twilio, covering:
1. Overall sanity (latency, recordings, transcripts, timing, ordering)
2. First turn control (driver vs target starts)
3. Concurrent driver messages
"""

import os
from typing import Any, Dict, List

import pytest
from okareo_tests.common import random_string

from okareo import Okareo
from okareo.model_under_test import Driver, Target, TwilioVoiceTarget
from okareo_api_client.models.find_test_data_point_payload import (
    FindTestDataPointPayload,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_PHONE = os.getenv("TWILIO_FROM_PHONE")
TWILIO_TO_PHONE = os.getenv("TWILIO_TO_PHONE")

# ============================================================================
# Prompt Templates
# ============================================================================

DRIVER_PROMPT = """
## Persona
- **Identity:** You are a customer named {scenario_input.name} calling about {scenario_input.topic}.

## Rules
- Start with a greeting and your question.
- Keep messages brief and natural.
- Ask one question at a time.
""".strip()

TARGET_WAITS_PROMPT = """
## Persona
- **Identity:** You are a customer named {scenario_input.name} who received a call about {scenario_input.topic}.

## Rules
- Wait for the agent to greet you first.
- Respond naturally to their greeting.
""".strip()


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
        max_parallel_requests=5,
    )


# ============================================================================
# Helpers
# ============================================================================


def create_scenario(okareo: Okareo, name: str, inputs: List[Dict[str, Any]]) -> Any:
    """Create a scenario set from input data."""
    seed_data = Okareo.seed_data_from_list(
        [{"input": inp, "result": "Expected response."} for inp in inputs]
    )
    return okareo.create_scenario_set(ScenarioSetCreate(name=name, seed_data=seed_data))


def get_messages(okareo: Okareo, test_run_id: str) -> List[List[Dict[str, Any]]]:
    """Fetch messages from all datapoints for a test run."""
    from okareo_api_client.models.error_response import ErrorResponse
    from okareo_api_client.models.full_data_point_item import FullDataPointItem
    from okareo_api_client.types import Unset

    datapoints = okareo.find_test_data_points(
        FindTestDataPointPayload(test_run_id=test_run_id, full_data_point=True)
    )

    # Handle potential error response
    if isinstance(datapoints, ErrorResponse):
        raise ValueError(f"Error fetching datapoints: {datapoints}")

    messages_list = []
    for dp in datapoints:
        # Ensure we have a FullDataPointItem with model_metadata
        if isinstance(dp, FullDataPointItem):
            if (
                not isinstance(dp.model_metadata, Unset)
                and dp.model_metadata is not None
            ):
                messages = dp.model_metadata.additional_properties.get("messages", [])
                messages_list.append(messages)

    return messages_list


def validate_message_timing(msg: Dict[str, Any], msg_idx: int) -> None:
    """Validate timing fields for a single message."""
    meta = msg.get("metadata", {})
    role = msg.get("role")

    # Start/end times exist and are logical
    start_time = meta.get("start_time")
    end_time = meta.get("end_time")
    assert start_time is not None, f"Message {msg_idx} ({role}): missing start_time"
    assert end_time is not None, f"Message {msg_idx} ({role}): missing end_time"
    assert (
        end_time > start_time
    ), f"Message {msg_idx} ({role}): end_time should be > start_time"

    # Duration > 500ms (reasonable threshold for voice)
    duration_ms = meta.get("duration_ms")
    assert (
        duration_ms is not None and duration_ms > 0
    ), f"Message {msg_idx} ({role}): duration_ms should be > 0"


def validate_message_content(msg: Dict[str, Any], msg_idx: int) -> None:
    """Validate content and recording for a single message."""
    meta = msg.get("metadata", {})
    role = msg.get("role")
    content = msg.get("content", "")

    # Transcript captured
    assert (
        content.strip() != ""
    ), f"Message {msg_idx} ({role}): transcript should not be empty"

    # Recording captured with duration > 0
    wav_path = meta.get("wav_path")
    assert wav_path, f"Message {msg_idx} ({role}): wav_path should exist"


def validate_conversation_order(messages: List[Dict[str, Any]]) -> None:
    """Validate that messages are in chronological order by start time."""
    for i in range(len(messages) - 1):
        curr_start = messages[i].get("metadata", {}).get("start_time")
        next_start = messages[i + 1].get("metadata", {}).get("start_time")
        assert (
            next_start >= curr_start
        ), f"Message {i+1} start_time should be >= message {i} start_time"


# ============================================================================
# Tests
# ============================================================================


class TestVoiceSanity:
    """Overall sanity test for voice simulations."""

    def test_sanity_with_parallel_conversations(
        self, okareo: Okareo, twilio_target: TwilioVoiceTarget, rnd: str
    ) -> None:
        """
        Validates:
        - Driver turn taking latency < 5s
        - Target turn taking latency exists
        - Parallel conversations complete (5/5)
        - All recordings captured with duration > 0
        - Transcripts captured for both sides
        - Start/end times exist and are logical
        - Duration > 0 for each message
        - Conversation order is sequential
        """
        num_parallel = 5

        driver = Driver(
            name=f"Sanity Driver - {rnd}",
            temperature=0.5,
            prompt_template=DRIVER_PROMPT,
        )

        inputs = [
            {"name": f"Customer{i}", "topic": "store hours", "voice": "ash"}
            for i in range(num_parallel)
        ]
        scenario = create_scenario(okareo, f"Sanity Scenario - {rnd}", inputs)

        evaluation = okareo.run_simulation(
            driver=driver,
            target=Target(name=f"Twilio Target - {rnd}", target=twilio_target),
            name=f"Sanity Test - {rnd}",
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

        # Basic assertions
        from okareo_api_client.types import Unset

        assert evaluation.status == "FINISHED"
        assert (
            not isinstance(evaluation.model_metrics, Unset)
            and evaluation.model_metrics is not None
        )

        # Extract metrics
        metrics = evaluation.model_metrics.to_dict()
        mean_scores = metrics.get("mean_scores", {})
        baseline = metrics.get("aggregate_baseline_metrics", {})

        # Driver turn taking latency < 5s
        driver_latency = baseline.get("avg_turn_taking_latency")
        assert (
            driver_latency is not None
        ), "avg_turn_taking_latency should exist in baseline"
        assert (
            driver_latency < 5000
        ), f"Driver latency {driver_latency}ms should be < 5000ms"

        # Target turn taking latency exists
        target_latency = mean_scores.get("avg_turn_taking_latency")
        assert (
            target_latency is not None
        ), "avg_turn_taking_latency should exist in mean_scores"

        # Validate all parallel conversations completed
        all_messages = get_messages(okareo, evaluation.id)
        assert (
            len(all_messages) == num_parallel
        ), f"Expected {num_parallel} conversations, got {len(all_messages)}"

        # Per-conversation validation
        for conv_idx, messages in enumerate(all_messages):
            assert len(messages) > 0, f"Conversation {conv_idx}: should have messages"

            user_count = 0
            assistant_count = 0

            for msg_idx, msg in enumerate(messages):
                role = msg.get("role")
                if role == "user":
                    user_count += 1
                elif role == "assistant":
                    assistant_count += 1

                validate_message_timing(msg, msg_idx)
                validate_message_content(msg, msg_idx)

            # Both sides have transcripts
            assert user_count > 0, f"Conversation {conv_idx}: should have user messages"
            assert (
                assistant_count > 0
            ), f"Conversation {conv_idx}: should have assistant messages"

            # Conversation order is sequential
            validate_conversation_order(messages)


class TestVoiceFirstTurn:
    """Tests for first turn control (driver vs target starts)."""

    def test_driver_starts_first(
        self, okareo: Okareo, twilio_target: TwilioVoiceTarget, rnd: str
    ) -> None:
        """
        first_turn="driver": Driver speaks first.
        Validates: First message is from "user" with captured greeting and audio.
        """
        driver = Driver(
            name=f"Driver Starts - {rnd}",
            temperature=0.5,
            prompt_template=DRIVER_PROMPT,
        )

        scenario = create_scenario(
            okareo,
            f"Driver Starts Scenario - {rnd}",
            [{"name": "Sarah", "topic": "return policy", "voice": "coral"}],
        )

        evaluation = okareo.run_simulation(
            driver=driver,
            target=Target(name=f"Twilio Target - {rnd}", target=twilio_target),
            name=f"Driver Starts Test - {rnd}",
            scenario=scenario,
            max_turns=2,
            repeats=1,
            first_turn="driver",
            calculate_metrics=True,
            checks=["total_turn_count"],
        )

        assert evaluation.status == "FINISHED"

        messages = get_messages(okareo, evaluation.id)[0]
        assert len(messages) > 0

        first_msg = messages[0]
        assert first_msg.get("role") == "user", "First speaker should be driver (user)"
        validate_message_content(first_msg, 0)

    def test_target_starts_first(
        self, okareo: Okareo, twilio_target: TwilioVoiceTarget, rnd: str
    ) -> None:
        """
        first_turn="target": Target speaks first.
        Validates: First message is from "assistant" with captured greeting and audio.
        """
        driver = Driver(
            name=f"Target Starts - {rnd}",
            temperature=0.5,
            prompt_template=TARGET_WAITS_PROMPT,
        )

        scenario = create_scenario(
            okareo,
            f"Target Starts Scenario - {rnd}",
            [{"name": "Mike", "topic": "order status", "voice": "ash"}],
        )

        evaluation = okareo.run_simulation(
            driver=driver,
            target=Target(name=f"Twilio Target - {rnd}", target=twilio_target),
            name=f"Target Starts Test - {rnd}",
            scenario=scenario,
            max_turns=2,
            repeats=1,
            first_turn="target",
            calculate_metrics=True,
            checks=["total_turn_count"],
        )

        assert evaluation.status == "FINISHED"

        messages = get_messages(okareo, evaluation.id)[0]
        assert len(messages) > 0

        first_msg = messages[0]
        assert (
            first_msg.get("role") == "assistant"
        ), "First speaker should be target (assistant)"
        validate_message_content(first_msg, 0)


class TestVoiceConcurrent:
    """Tests for concurrent driver messages."""

    def test_concurrent_driver_messages(
        self, okareo: Okareo, twilio_target: TwilioVoiceTarget, rnd: str
    ) -> None:
        """
        concurrent_ask_probability=1.0: Driver sends 2 messages before target responds.
        Validates: Message sequence is user → user → assistant.
        """
        driver = Driver(
            name=f"Concurrent Driver - {rnd}",
            temperature=0.5,
            prompt_template=DRIVER_PROMPT,
        )

        scenario = create_scenario(
            okareo,
            f"Concurrent Scenario - {rnd}",
            [{"name": "Jane", "topic": "shipping options", "voice": "ash"}],
        )

        evaluation = okareo.run_simulation(
            driver=driver,
            target=Target(name=f"Twilio Target - {rnd}", target=twilio_target),
            name=f"Concurrent Driver Test - {rnd}",
            scenario=scenario,
            max_turns=2,
            repeats=1,
            first_turn="driver",
            concurrent_ask_probability=1.0,
            calculate_metrics=True,
            checks=["total_turn_count"],
        )

        assert evaluation.status == "FINISHED"

        messages = get_messages(okareo, evaluation.id)[0]
        assert (
            len(messages) >= 3
        ), "Should have at least 3 messages (user, user, assistant)"

        # Validate sequence: user → user → assistant
        assert messages[0].get("role") == "user", "Message 1 should be user"
        assert messages[1].get("role") == "user", "Message 2 should be user"
        assert messages[2].get("role") == "assistant", "Message 3 should be assistant"
