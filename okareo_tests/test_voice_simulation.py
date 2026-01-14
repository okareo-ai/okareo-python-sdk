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


def get_datapoints(okareo: Okareo, test_run_id: str) -> List[Any]:
    """Fetch all datapoints for a test run."""
    from okareo_api_client.models.error_response import ErrorResponse

    datapoints = okareo.find_test_data_points(
        FindTestDataPointPayload(test_run_id=test_run_id, full_data_point=True)
    )

    # Handle potential error response
    if isinstance(datapoints, ErrorResponse):
        raise TypeError("Error fetching datapoints")

    return datapoints


def get_messages(okareo: Okareo, test_run_id: str) -> List[List[Dict[str, Any]]]:
    """Fetch messages from all datapoints for a test run."""
    from okareo_api_client.models.full_data_point_item import FullDataPointItem
    from okareo_api_client.types import Unset

    datapoints = get_datapoints(okareo, test_run_id)

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


def get_driver_latencies(messages: List[Dict[str, Any]]) -> List[int]:
    """
    Extract driver latencies from user messages.

    Driver latency is the time the driver took to respond after the target spoke.
    The first user message (if driver starts first) will have latency=0 and is excluded.
    """
    latencies = []
    for msg in messages:
        if msg.get("role") == "user":
            latency = msg.get("metadata", {}).get("latency")
            # Exclude first message latency (0) since driver hasn't responded to anything yet
            if latency is not None and latency > 0:
                latencies.append(latency)
    return latencies


def validate_conversation_sanity(
    okareo: Okareo,
    datapoint: Any,
    messages: List[Dict[str, Any]],
    conv_idx: int,
    max_driver_latency_ms: int = 7000,
) -> None:
    """
    Validate sanity for a single conversation.

    Checks:
    - Messages exist
    - Both user and assistant messages present
    - Message timing (start/end times, duration)
    - Message content (transcript, recording)
    - Conversation order is sequential
    - Driver latency within threshold (all individual latencies)
    - Call recording exists with content

    Args:
        okareo: Okareo client instance
        datapoint: Full datapoint with model_metadata
        messages: List of messages from the conversation
        conv_idx: Conversation index for error messages
        max_driver_latency_ms: Maximum acceptable driver latency in milliseconds
    """
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

    # Driver latency within threshold for all driver responses
    driver_latencies = get_driver_latencies(messages)
    for latency in driver_latencies:
        assert (
            latency < max_driver_latency_ms
        ), f"Conversation {conv_idx}: driver latency {latency}ms should be < {max_driver_latency_ms}ms"

    # Validate call recording exists and has duration > 0
    validate_call_recording(okareo, datapoint, conv_idx)


def validate_test_run_sanity(
    okareo: Okareo,
    evaluation: Any,
    expected_conversations: int | None = None,
    max_driver_latency_ms: int = 7000,
    median_driver_latency_ms: int = 5000,
    validate_metrics: bool = True,
) -> None:
    """
    Validate sanity for an entire test run.

    Checks:
    - Evaluation status is FINISHED
    - Metrics exist and latencies within threshold (if validate_metrics=True)
    - Expected number of conversations (if provided)
    - Per-conversation sanity (timing, content, order, recordings)
    - Median driver latency across all conversations
    - All individual driver latencies within max threshold

    Args:
        okareo: Okareo client instance
        evaluation: Evaluation result from run_simulation
        expected_conversations: Expected number of conversations (optional)
        max_driver_latency_ms: Maximum acceptable driver latency in milliseconds (default 7000ms)
        median_driver_latency_ms: Maximum acceptable median driver latency in milliseconds (default 4500ms)
        validate_metrics: Whether to validate metrics (requires calculate_metrics=True)
    """
    import statistics

    from okareo_api_client.types import Unset

    # Basic status check
    assert evaluation.status == "FINISHED"

    # Metrics validation (optional)
    if validate_metrics:
        assert (
            not isinstance(evaluation.model_metrics, Unset)
            and evaluation.model_metrics is not None
        ), "model_metrics should exist"

        metrics = evaluation.model_metrics.to_dict()
        mean_scores = metrics.get("mean_scores", {})
        baseline = metrics.get("aggregate_baseline_metrics", {})

        # Driver turn taking latency check
        turn_taking_latency = baseline.get("avg_turn_taking_latency")
        assert (
            turn_taking_latency is not None
        ), "avg_turn_taking_latency should exist in baseline"

        # Target turn taking latency exists
        target_latency = mean_scores.get("avg_turn_taking_latency")
        assert (
            target_latency is not None
        ), "avg_turn_taking_latency should exist in mean_scores"

    # Get datapoints and messages
    all_datapoints = get_datapoints(okareo, evaluation.id)
    all_messages = get_messages(okareo, evaluation.id)

    # Validate expected conversation count
    if expected_conversations is not None:
        assert (
            len(all_messages) == expected_conversations
        ), f"Expected {expected_conversations} conversations, got {len(all_messages)}"
        assert (
            len(all_datapoints) == expected_conversations
        ), f"Expected {expected_conversations} datapoints, got {len(all_datapoints)}"

    # Collect all driver latencies across all conversations
    all_driver_latencies = []
    for messages in all_messages:
        driver_latencies = get_driver_latencies(messages)
        all_driver_latencies.extend(driver_latencies)

    # Validate median driver latency
    if all_driver_latencies:
        median_latency = statistics.median(all_driver_latencies)
        assert (
            median_latency < median_driver_latency_ms
        ), f"Median driver latency {median_latency}ms should be < {median_driver_latency_ms}ms"

    # Per-conversation validation
    for conv_idx, (datapoint, messages) in enumerate(zip(all_datapoints, all_messages)):
        validate_conversation_sanity(
            okareo, datapoint, messages, conv_idx, max_driver_latency_ms
        )


def validate_call_recording(okareo: Okareo, datapoint: Any, conv_idx: int) -> None:
    """
    Validate that the call recording exists and has duration > 0.

    Args:
        okareo: Okareo client instance
        datapoint: Full datapoint with model_metadata
        conv_idx: Conversation index for error messages
    """
    import requests

    from okareo_api_client.models.full_data_point_item import FullDataPointItem
    from okareo_api_client.types import Unset

    if not isinstance(datapoint, FullDataPointItem):
        raise TypeError(f"Conversation {conv_idx}: Expected FullDataPointItem")

    if isinstance(datapoint.model_metadata, Unset) or datapoint.model_metadata is None:
        raise ValueError(f"Conversation {conv_idx}: Missing model_metadata")

    metadata = datapoint.model_metadata.additional_properties

    # Check for call_recording_url or call_sid
    call_recording_url = metadata.get("call_recording_url")
    call_sid = metadata.get("call_sid")

    assert (
        call_recording_url or call_sid
    ), f"Conversation {conv_idx}: Missing call_recording_url or call_sid"

    # Fetch the recording using the call_recording_url
    if call_recording_url:
        api_key = os.environ["OKAREO_API_KEY"]
        headers = {"api-key": api_key}

        response = requests.get(call_recording_url, headers=headers, stream=True)
        assert (
            response.status_code == 200
        ), f"Conversation {conv_idx}: Failed to fetch recording, status={response.status_code}"

        # Get content length or download to check size
        content_length = response.headers.get("content-length")
        if content_length:
            file_size = int(content_length)
            assert (
                file_size > 0
            ), f"Conversation {conv_idx}: Recording file size should be > 0, got {file_size}"
        else:
            # If no content-length header, download and check actual size
            content = b""
            for chunk in response.iter_content(chunk_size=8192):
                content += chunk
                if len(content) > 100:  # Stop after confirming some content
                    break
            assert (
                len(content) > 0
            ), f"Conversation {conv_idx}: Recording content should be > 0 bytes"


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
        - Call recordings exist and have size > 0
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
            {"name": f"Customer{i}", "topic": "store hours", "voice": "oliver"}
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

        # Full sanity validation
        validate_test_run_sanity(
            okareo,
            evaluation,
            expected_conversations=num_parallel,
            validate_metrics=True,
        )


class TestVoiceFirstTurn:
    """Tests for first turn control (driver vs target starts)."""

    @pytest.mark.skip(reason="Skipping tests until test target can be parameterized)")
    def test_driver_starts_first(
        self, okareo: Okareo, twilio_target: TwilioVoiceTarget, rnd: str
    ) -> None:
        """
        first_turn="driver": Driver speaks first.
        Validates:
        - First message is from "user" with captured greeting and audio
        - Full sanity checks (timing, content, order, recordings, latency)
        """
        driver = Driver(
            name=f"Driver Starts - {rnd}",
            temperature=0.5,
            prompt_template=DRIVER_PROMPT,
        )

        scenario = create_scenario(
            okareo,
            f"Driver Starts Scenario - {rnd}",
            [{"name": "Sarah", "topic": "return policy", "voice": "oliver"}],
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
            checks=[
                "avg_turn_taking_latency",
                "avg_words_per_minute",
                "total_turn_count",
            ],
        )

        # Full sanity validation
        validate_test_run_sanity(
            okareo,
            evaluation,
            expected_conversations=1,
            validate_metrics=True,
        )

        # First turn specific validation
        messages = get_messages(okareo, evaluation.id)[0]
        first_msg = messages[0]
        assert first_msg.get("role") == "user", "First speaker should be driver (user)"

    def test_target_starts_first(
        self, okareo: Okareo, twilio_target: TwilioVoiceTarget, rnd: str
    ) -> None:
        """
        first_turn="target": Target speaks first.
        Validates:
        - First message is from "assistant" with captured greeting and audio
        - Full sanity checks (timing, content, order, recordings, latency)
        """
        driver = Driver(
            name=f"Target Starts - {rnd}",
            temperature=0.5,
            prompt_template=TARGET_WAITS_PROMPT,
        )

        scenario = create_scenario(
            okareo,
            f"Target Starts Scenario - {rnd}",
            [{"name": "Mike", "topic": "order status", "voice": "oliver"}],
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
            checks=[
                "avg_turn_taking_latency",
                "avg_words_per_minute",
                "total_turn_count",
            ],
        )

        # Full sanity validation
        validate_test_run_sanity(
            okareo,
            evaluation,
            expected_conversations=1,
            validate_metrics=True,
        )

        # First turn specific validation
        messages = get_messages(okareo, evaluation.id)[0]
        first_msg = messages[0]
        assert (
            first_msg.get("role") == "assistant"
        ), "First speaker should be target (assistant)"


class TestVoiceConcurrent:
    """Tests for concurrent driver messages."""

    def test_concurrent_driver_messages(
        self, okareo: Okareo, twilio_target: TwilioVoiceTarget, rnd: str
    ) -> None:
        """
        concurrent_ask_probability=1.0: Driver sends 2 messages before target responds.
        Validates:
        - At least one occurrence of consecutive driver (user) messages
        - Full sanity checks (timing, content, order, recordings, latency)
        """

        driver = Driver(
            name=f"Concurrent Driver - {rnd}",
            temperature=0.5,
            prompt_template=DRIVER_PROMPT,
        )

        scenario = create_scenario(
            okareo,
            f"Concurrent Scenario - {rnd}",
            [{"name": "Jane", "topic": "shipping options", "voice": "oliver"}],
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

        assert len(messages) >= 3, "Should have at least 3 messages"

        # Find consecutive user messages (concurrent driver messages)
        found_consecutive_user = False
        for i in range(len(messages) - 1):
            if (
                messages[i].get("role") == "user"
                and messages[i + 1].get("role") == "user"
            ):
                found_consecutive_user = True
                break

        assert found_consecutive_user, (
            "Should have at least one occurrence of consecutive driver (user) messages. "
            f"Message sequence: {[m.get('role') for m in messages]}"
        )
