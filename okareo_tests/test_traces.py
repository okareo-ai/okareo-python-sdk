import base64
import json
import logging
import os
import secrets
import time
import uuid
from contextlib import contextmanager
from typing import Any, Generator

import pytest
import requests  # type: ignore
from google.protobuf.json_format import ParseDict  # type: ignore
from okareo_tests.common import API_KEY, random_string
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,  # type: ignore
)

from okareo import Okareo
from okareo.model_under_test import (
    CustomMultiturnTarget,
    Driver,
    ModelInvocation,
    Target,
    TwilioVoiceTarget,
)
from okareo_api_client.models import ScenarioSetCreate, SeedData
from okareo_api_client.models.find_test_data_point_payload import (
    FindTestDataPointPayload,
)
from okareo_api_client.models.test_run_type import TestRunType

logger = logging.getLogger(__name__)

# ============================================================================
# Timing Utilities
# ============================================================================

_timing_results: dict[str, list[float]] = {}


@contextmanager
def timed(operation: str) -> Generator[None, None, None]:
    """Context manager to time an operation and store results."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        if operation not in _timing_results:
            _timing_results[operation] = []
        _timing_results[operation].append(elapsed)
        logger.debug(f"⏱️  {operation}: {elapsed:.3f}s")


def print_timing_summary() -> None:
    """Print a summary of all timed operations."""
    logger.info(f"\n{'=' * 60}")
    logger.info("TIMING SUMMARY")
    logger.info("=" * 60)

    # Sort by total time descending
    sorted_ops = sorted(_timing_results.items(), key=lambda x: sum(x[1]), reverse=True)

    for operation, times in sorted_ops:
        total = sum(times)
        count = len(times)
        avg = total / count if count > 0 else 0
        logger.info(f"{operation}:")
        logger.info(f"  Total: {total:.3f}s | Count: {count} | Avg: {avg:.3f}s")

    logger.info(f"{'=' * 60}\n")


def reset_timing() -> None:
    """Reset timing results."""
    _timing_results.clear()


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "NOT SET")
BASE_URL = os.environ.get("BASE_URL", "https://api.okareo.com")

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM_PHONE = os.environ.get("TWILIO_FROM_PHONE")
TWILIO_TO_PHONE = os.environ.get("TWILIO_TO_PHONE")


@pytest.fixture
def api_key():  # type: ignore
    """Get API key from environment variable."""
    api_key = os.environ.get("OKAREO_API_KEY")
    if not api_key:
        pytest.skip("OKAREO_API_KEY environment variable not set")
    return api_key


@pytest.fixture
def base_url():  # type: ignore
    """Get base URL from environment variable or use default."""
    return os.environ.get("BASE_URL", "https://api.okareo.com")


def generate_random_string():  # type: ignore
    """Generate a unique random string for testing."""
    return f"trace_test_{secrets.token_hex(8)}"


def find_datapoints(
    api_key: Any, base_url: Any, filters: list[dict[str, str]], wait: int = 15
) -> list[dict[str, Any]]:
    """Find datapoints using /v0/find_datapoints_filter. Retries 3x with backoff."""
    if wait > 0:
        time.sleep(wait)

    headers = {"Content-Type": "application/json", "api-key": api_key}

    with timed("GET /v0/projects"):
        project_id = requests.get(f"{base_url}/v0/projects", headers=headers).json()[0][
            "id"
        ]

    for attempt in range(3):
        with timed("POST /v0/find_datapoints_filter"):
            response = requests.post(
                f"{base_url}/v0/find_datapoints_filter",
                headers=headers,
                json={"limit": 20, "filters": filters, "project_id": project_id},
            )
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                logger.debug(f"find_datapoints: found {len(data)} datapoints")
                return data
        attempt_num = attempt + 1
        logger.debug(
            f"find_datapoints attempt {attempt_num}: {response.status_code}, retrying..."
        )
        time.sleep(10 * (attempt + 1))

    return []


def build_otel_trace_payload(
    session_id: str,
    messages: list[dict[str, str]],
    completion: str,
    test_identifier: str | None = None,
    service_name: str = "okareo_test",
    model_name: str = "gpt-4",
    system_name: str = "openai",
) -> dict[str, Any]:
    """Build an OTEL trace payload with the given conversation data.

    Args:
        session_id: The session ID to use as context_token for correlation
        messages: List of message dicts (excluding the final assistant response)
        completion: The assistant's completion/response
        test_identifier: Optional unique string to identify this trace
        service_name: Service name for the trace (default: okareo_test)
        model_name: Model name (default: gpt-4)
        system_name: AI system name (default: openai)

    Returns:
        OTEL trace payload dict ready for protobuf conversion
    """
    current_time_ns = int(time.time() * 1_000_000_000)
    start_time_ns = current_time_ns - (30 * 1_000_000_000)

    trace_id_bytes = secrets.token_bytes(16)
    span_id_bytes = secrets.token_bytes(8)
    trace_id_b64 = base64.b64encode(trace_id_bytes).decode("utf-8")
    span_id_b64 = base64.b64encode(span_id_bytes).decode("utf-8")

    attributes = [
        {"key": "gen_ai.request.model", "value": {"stringValue": model_name}},
        {"key": "llm.request.type", "value": {"stringValue": "chat"}},
        {"key": "llm.messages", "value": {"stringValue": json.dumps(messages)}},
        {"key": "session.id", "value": {"stringValue": session_id}},
        {"key": "gen_ai.system", "value": {"stringValue": system_name}},
        {
            "key": "SpanAttributes.LLM_COMPLETIONS.0.content",
            "value": {"stringValue": completion},
        },
        {
            "key": "SpanAttributes.LLM_COMPLETIONS.0.role",
            "value": {"stringValue": "assistant"},
        },
    ]

    if test_identifier:
        attributes.append(
            {"key": "test_identifier", "value": {"stringValue": test_identifier}}
        )

    return {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": service_name}},
                        {
                            "key": "deployment.environment",
                            "value": {"stringValue": "test"},
                        },
                    ]
                },
                "scopeSpans": [
                    {
                        "scope": {"name": service_name},
                        "spans": [
                            {
                                "traceId": trace_id_b64,
                                "spanId": span_id_b64,
                                "name": "litellm_request",
                                "kind": 1,
                                "startTimeUnixNano": str(start_time_ns),
                                "endTimeUnixNano": str(current_time_ns),
                                "attributes": attributes,
                                "status": {"code": 1},
                                "flags": 256,
                            }
                        ],
                    }
                ],
            }
        ]
    }


def send_otel_trace(
    payload: dict[str, Any], api_key: str, base_url: str
) -> requests.Response:
    """Send an OTEL trace to the Okareo traces endpoint."""
    trace_request = ExportTraceServiceRequest()
    ParseDict(payload, trace_request)
    serialized_data = trace_request.SerializeToString()

    headers = {"Content-Type": "application/x-protobuf", "api-key": api_key}
    with timed("POST /v0/traces"):
        response = requests.post(
            f"{base_url}/v0/traces", headers=headers, data=serialized_data
        )
    return response


# ============================================================================
# Trace Endpoint Tests
# ============================================================================


def test_traces_endpoint_with_verification(api_key: Any, base_url: Any) -> Any:
    """Test sending trace data to the /traces endpoint with verification."""
    reset_timing()  # Reset timing for this test

    # Generate identifiers for this test
    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    logger.debug(f"Using test_id: {test_id}, session_id: {session_id}")

    # Build and send trace using shared utilities
    messages = [{"role": "user", "content": f"Test message with {test_id}"}]
    completion = f"Response to {test_id}"

    payload = build_otel_trace_payload(
        session_id=session_id,
        messages=messages,
        completion=completion,
        test_identifier=test_id,
        service_name="litellm",
        model_name="gemini-2.5-pro-exp-03-25",
        system_name="vertex_ai",
    )

    response = send_otel_trace(payload, api_key, base_url)

    # Assert response
    assert (
        response.status_code == 201
    ), f"Expected status code 201, got {response.status_code}: {response.text}"

    # Verify the response data
    try:
        response_data = response.json()
        assert response_data.get("status") == "success"
        assert "message" in response_data
        logger.debug(f"Response: {response_data}")
    except ValueError:
        # If response is not JSON, just check status code
        pass

    # Verify the span was recorded in Okareo
    filters = [{"field": "context_token", "operator": "equal", "value": session_id}]
    datapoints = find_datapoints(api_key, base_url, filters)
    assert (
        len(datapoints) > 0
    ), f"Span with session_id '{session_id}' was not found in Okareo"
    logger.info(f"Found {len(datapoints)} datapoint(s) with session_id: {session_id}")
    print_timing_summary()


# ============================================================================
# Simulation-Trace Consistency Tests
# ============================================================================


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    """Create an Okareo client for testing."""
    return Okareo(api_key=API_KEY)


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


@pytest.fixture(scope="module")
def twilio_target() -> TwilioVoiceTarget:
    if not all(
        [TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_PHONE, TWILIO_TO_PHONE]
    ):
        pytest.skip("Twilio environment variables not set")
    return TwilioVoiceTarget(
        account_sid=TWILIO_ACCOUNT_SID,  # type: ignore
        auth_token=TWILIO_AUTH_TOKEN,  # type: ignore
        from_phone_number=TWILIO_FROM_PHONE,
        to_phone_number=TWILIO_TO_PHONE,
    )


class ControlledMultiturnTarget(CustomMultiturnTarget):
    """A custom multiturn target that returns predefined responses.

    This gives us full control over:
    - session_id (context_token) returned from start_session
    - responses returned from invoke
    """

    def __init__(self, name: str, responses: list[str], session_id: str):
        super().__init__(name=name)
        self.responses = responses
        self.controlled_session_id = session_id
        self.turn_index = 0

    def start_session(
        self, scenario_input: str | None = None
    ) -> tuple[str | None, ModelInvocation | None]:
        """Return our controlled session_id."""
        return self.controlled_session_id, None

    def end_session(self, session_id: str) -> None:
        pass

    def invoke(
        self,
        messages: list[dict[str, str]],
        scenario_input: Any = None,
        session_id: str | None = None,
    ) -> ModelInvocation:
        """Return the next response in sequence."""
        if self.turn_index < len(self.responses):
            response = self.responses[self.turn_index]
            self.turn_index += 1
        else:
            response = "Conversation complete."
        return ModelInvocation(response, messages, {"turn": self.turn_index})


def run_trace_consistency_test(
    api_key: str,
    base_url: str,
    okareo_client: Okareo,
    simulation_eval: Any,
    simulation_session_id: str,
    test_id: str,
) -> None:
    # Get the simulation datapoints to see the actual conversation
    with timed("find_test_data_points (simulation)"):
        tdps = okareo_client.find_test_data_points(
            FindTestDataPointPayload(
                test_run_id=simulation_eval.id, full_data_point=True
            )
        )
    assert isinstance(tdps, list) and len(tdps) > 0

    # Extract the message history from the simulation
    tdp = tdps[0]
    generation_output = tdp.metric_value.additional_properties.get(  # type: ignore
        "generation_output", []
    )
    logger.debug(f"Simulation conversation: {json.dumps(generation_output, indent=2)}")

    # Prepare message data for traces
    trace_messages = generation_output[:-1] if generation_output else []
    final_response = (
        generation_output[-1].get("content", "") if generation_output else ""
    )

    # =========================================================================
    # Test 1: MATCHING trace (same session_id, same conversation)
    # =========================================================================
    logger.info(f"\n{'=' * 60}")
    logger.info("TEST 1: MATCHING TRACE")
    logger.info("=" * 60)

    matching_trace_payload = build_otel_trace_payload(
        session_id=simulation_session_id,
        messages=trace_messages,
        completion=final_response,
        test_identifier=f"{test_id}_matching",
    )

    response = send_otel_trace(matching_trace_payload, api_key, base_url)
    assert (
        response.status_code == 201
    ), f"Failed to send matching trace: {response.text}"
    logger.info(f"Sent matching trace with session_id: {simulation_session_id}")

    # =========================================================================
    # Test 2: MISMATCHED trace (different session_id, truncated user messages)
    # =========================================================================
    logger.info(f"\n{'=' * 60}")
    logger.info("TEST 2: MISMATCHED TRACE")
    logger.info("=" * 60)

    # Use a different session_id for the mismatched trace so it links to the same simulation
    # but creates a separate trace datapoint we can evaluate independently
    str(uuid.uuid4())

    # Build mismatched messages (truncated user messages)
    mismatched_messages = []
    for msg in trace_messages:
        if msg.get("role") == "user":
            original = msg.get("content", "")
            truncated = original[15:] if len(original) > 15 else original[:5]
            mismatched_messages.append({"role": "user", "content": truncated})
        else:
            mismatched_messages.append(msg)

    # Log the difference
    if trace_messages and mismatched_messages:
        first_sim_user: dict[str, Any] = next(
            (m for m in trace_messages if m.get("role") == "user"), {}
        )
        first_mismatch_user: dict[str, Any] = next(
            (m for m in mismatched_messages if m.get("role") == "user"), {}
        )
        logger.debug(f"Simulation user message: '{first_sim_user.get('content', '')}'")
        logger.debug(
            f"Trace user message (truncated): '{first_mismatch_user.get('content', '')}'"
        )

    # We need to link the mismatched trace to the same simulation
    # The simulation_trace_consistency check uses context_token to find the simulation
    # So we need to use the simulation_session_id for the mismatched trace too
    # But to distinguish the traces, we'll send them and then filter by test_identifier
    mismatched_trace_payload = build_otel_trace_payload(
        session_id=simulation_session_id,  # Same session to link to simulation
        messages=mismatched_messages,
        completion=final_response,
        test_identifier=f"{test_id}_mismatched",
    )

    response = send_otel_trace(mismatched_trace_payload, api_key, base_url)
    assert (
        response.status_code == 201
    ), f"Failed to send mismatched trace: {response.text}"
    logger.info(f"Sent mismatched trace with session_id: {simulation_session_id}")

    # =========================================================================
    # Wait for trace ingestion and find all trace datapoints
    # =========================================================================
    filters = [
        {"field": "context_token", "operator": "equal", "value": simulation_session_id}
    ]
    trace_datapoints = find_datapoints(api_key, base_url, filters)

    # Filter to only OTEL-ingested datapoints (source != "Okareo")
    trace_only = [dp for dp in trace_datapoints if dp.get("source") != "Okareo"]
    logger.info(
        f"Trace datapoints found: {len(trace_only)} (total with same context_token: {len(trace_datapoints)})"
    )
    assert (
        len(trace_only) >= 2
    ), f"Expected at least 2 trace datapoints, found {len(trace_only)}"

    datapoint_ids: list[str] = [str(dp.get("id")) for dp in trace_only if dp.get("id")]
    logger.debug(f"Datapoint IDs: {datapoint_ids}")

    # =========================================================================
    # Evaluate all trace datapoints together
    # =========================================================================
    logger.info(f"\n{'=' * 60}")
    logger.info("EVALUATING ALL TRACES")
    logger.info("=" * 60)

    with timed("evaluate (simulation_trace_consistency)"):
        check_eval = okareo_client.evaluate(
            name=f"Trace Consistency Eval - {test_id}",
            test_run_type=TestRunType.NL_GENERATION,
            datapoint_ids=datapoint_ids,
            checks=["simulation_trace_consistency"],
        )

    assert (
        check_eval.status == "FINISHED"
    ), f"Evaluation failed: {check_eval.failure_message}"
    logger.info(f"Evaluation completed: {check_eval.app_link}")

    # Verify we get one pass (matching) and one fail (mismatched)
    with timed("find_test_data_points (evaluation)"):
        eval_tdps = okareo_client.find_test_data_points(
            FindTestDataPointPayload(test_run_id=check_eval.id, full_data_point=True)
        )
    assert isinstance(eval_tdps, list) and len(eval_tdps) >= 2

    pass_count = 0
    fail_count = 0
    for eval_tdp in eval_tdps:
        checks = eval_tdp.checks if eval_tdp.checks else {}  # type: ignore
        consistency_score = checks.get("simulation_trace_consistency")
        explanation = checks.get("simulation_trace_consistency__explanation", "")
        logger.debug(f"simulation_trace_consistency score: {consistency_score}")
        if explanation:
            logger.debug(f"Explanation: {explanation}")
        if consistency_score is True:
            pass_count += 1
        elif consistency_score is False:
            fail_count += 1

    logger.info(f"Results: {pass_count} passed, {fail_count} failed")
    assert (
        pass_count >= 1
    ), f"Expected at least 1 pass (matching trace), got {pass_count}"
    assert (
        fail_count >= 1
    ), f"Expected at least 1 fail (mismatched trace), got {fail_count}"

    logger.info(
        "PASS: Got expected mix of matching (pass) and mismatched (fail) results"
    )


def test_simulation_trace_consistency_matching_and_mismatching(
    api_key: str, base_url: str, okareo_client: Okareo, rnd: str
) -> None:
    """Test simulation_trace_consistency check with both MATCHING and MISMATCHING traces.

    This test runs a single simulation and sends two different traces:
    1. A MATCHING trace (same conversation) - expects check to PASS (score=True)
    2. A MISMATCHED trace (truncated user messages) - expects check to FAIL (score=False)
    """
    reset_timing()
    test_id = generate_random_string()
    simulation_session_id = str(uuid.uuid4())

    # Define controlled responses that the target will return
    target_responses = [
        "Hello! I'm your weather assistant. How can I help you today?",
        "It's currently sunny and 72°F. Perfect weather for outdoor activities!",
    ]

    # Create controlled target with known session_id
    custom_target = ControlledMultiturnTarget(
        name=f"trace_consistency_target_{rnd}",
        responses=target_responses,
        session_id=simulation_session_id,
    )

    target = Target(
        name=f"Trace Consistency Target {rnd}",
        target=custom_target,
    )

    driver = Driver(
        name=f"Trace Consistency Driver {rnd}",
        temperature=0,
    )

    # Create scenario
    seeds = [
        SeedData(
            input_="Ask about the weather forecast for today.",
            result="Weather information response",
        )
    ]

    with timed("create_scenario_set"):
        scenario = okareo_client.create_scenario_set(
            ScenarioSetCreate(
                name=f"Trace Consistency Scenario - {test_id}",
                seed_data=seeds,
            )
        )

    # Run simulation - this creates datapoints with context_token = simulation_session_id
    with timed("run_simulation"):
        simulation_eval = okareo_client.run_simulation(
            target=target,
            driver=driver,
            scenario=scenario,
            name=f"Trace Consistency Sim - {test_id}",
            max_turns=2,
            repeats=1,
            first_turn="driver",
            checks=["behavior_adherence"],
        )

    assert (
        simulation_eval.status == "FINISHED"
    ), f"Simulation failed: {simulation_eval.failure_message}"
    logger.info(f"Simulation completed with session_id: {simulation_session_id}")

    run_trace_consistency_test(
        api_key,
        base_url,
        okareo_client,
        simulation_eval,
        simulation_session_id,
        test_id,
    )
    print_timing_summary()


def test_voice_simulation_trace_consistency_matching_and_mismatching(
    api_key: str,
    base_url: str,
    okareo_client: Okareo,
    twilio_target: TwilioVoiceTarget,
    rnd: str,
) -> None:
    """Test simulation_trace_consistency check with a voice simulation."""
    reset_timing()
    test_id = generate_random_string()

    driver = Driver(
        name=f"Voice Trace Driver - {rnd}",
        temperature=0.5,
        prompt_template="You are a customer asking about store hours. Keep it brief.",
    )

    seed_data = Okareo.seed_data_from_list(
        [{"input": {"topic": "store hours"}, "result": "Store hours response"}]
    )

    with timed("create_scenario_set"):
        scenario = okareo_client.create_scenario_set(
            ScenarioSetCreate(
                name=f"Voice Trace Scenario - {test_id}",
                seed_data=seed_data,
            )
        )

    with timed("run_voice_simulation"):
        simulation_eval = okareo_client.run_simulation(
            driver=driver,
            target=Target(name=f"Voice Trace Target - {rnd}", target=twilio_target),
            name=f"Voice Trace Sim - {test_id}",
            scenario=scenario,
            max_turns=1,
            repeats=1,
            first_turn="target",
            checks=["behavior_adherence"],
        )

    assert (
        simulation_eval.status == "FINISHED"
    ), f"Voice simulation failed: {simulation_eval.failure_message}"

    # Get context_token from the simulation datapoint using find_datapoints (returns DatapointListItem)
    filters = [
        {"field": "test_run_id", "operator": "equal", "value": simulation_eval.id}
    ]
    datapoints = find_datapoints(api_key, base_url, filters, wait=0)
    assert len(datapoints) > 0, "No datapoints found for voice simulation"
    simulation_session_id = datapoints[0].get("context_token")
    assert simulation_session_id, "No context_token found in voice simulation datapoint"
    logger.info(f"Voice simulation completed with session_id: {simulation_session_id}")

    run_trace_consistency_test(
        api_key,
        base_url,
        okareo_client,
        simulation_eval,
        simulation_session_id,
        test_id,
    )
    print_timing_summary()


# ============================================================================
# Parallel Processing Tests
# ============================================================================


def build_multi_span_trace_payload(
    session_id: str,
    num_spans: int,
    test_identifier: str,
    model_name: str = "gpt-4",
) -> dict[str, Any]:
    """Build an OTEL trace payload with multiple GenAI spans.

    Args:
        session_id: Session ID for correlation (becomes context_token)
        num_spans: Number of spans to create in the trace
        test_identifier: Unique identifier for this test
        model_name: Model name for the spans

    Returns:
        OTEL trace payload dict ready for protobuf conversion
    """
    current_time_ns = int(time.time() * 1_000_000_000)
    trace_id_bytes = secrets.token_bytes(16)
    trace_id_b64 = base64.b64encode(trace_id_bytes).decode("utf-8")

    spans = []
    for i in range(num_spans):
        span_id_bytes = secrets.token_bytes(8)
        span_id_b64 = base64.b64encode(span_id_bytes).decode("utf-8")
        start_ns = current_time_ns - ((num_spans - i) * 1_000_000_000)

        attributes = [
            {"key": "gen_ai.request.model", "value": {"stringValue": model_name}},
            {"key": "gen_ai.system", "value": {"stringValue": "openai"}},
            {"key": "llm.request.type", "value": {"stringValue": "chat"}},
            {"key": "session.id", "value": {"stringValue": session_id}},
            {"key": "test_identifier", "value": {"stringValue": test_identifier}},
            {
                "key": "llm.messages",
                "value": {
                    "stringValue": json.dumps(
                        [{"role": "user", "content": f"Test message {i}"}]
                    )
                },
            },
            {
                "key": "SpanAttributes.LLM_COMPLETIONS.0.content",
                "value": {"stringValue": f"This is a helpful response to message {i}."},
            },
            {
                "key": "SpanAttributes.LLM_COMPLETIONS.0.role",
                "value": {"stringValue": "assistant"},
            },
        ]

        span = {
            "traceId": trace_id_b64,
            "spanId": span_id_b64,
            "name": "litellm_request",
            "kind": 1,
            "startTimeUnixNano": str(start_ns),
            "endTimeUnixNano": str(start_ns + 500_000_000),
            "attributes": attributes,
            "status": {"code": 1},
            "flags": 256,
        }
        spans.append(span)

    return {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "parallel_test"}},
                    ]
                },
                "scopeSpans": [
                    {
                        "scope": {"name": "parallel_test"},
                        "spans": spans,
                    }
                ],
            }
        ]
    }


def create_monitor_with_checks(
    api_key: str,
    base_url: str,
    project_id: str,
    monitor_name: str,
    checks: list[str],
) -> dict[str, Any]:
    """Create a monitor (filter) that matches traces and attaches checks."""
    headers = {"Content-Type": "application/json", "api-key": api_key}

    payload = {
        "filters": [
            {"field": "request_model_name", "operator": "contains", "value": "gpt"}
        ],
        "name": monitor_name,
        "description": "Test monitor for parallel trace checks",
        "checks": checks,
        "project_id": project_id,
        "slack_enabled": False,
        "email_enabled": False,
    }

    response = requests.post(f"{base_url}/v0/filters", headers=headers, json=payload)
    assert response.status_code == 201, f"Failed to create monitor: {response.text}"
    return response.json()


def delete_monitor(api_key: str, base_url: str, filter_group_id: str) -> None:
    """Delete a monitor (filter group)."""
    headers = {"Content-Type": "application/json", "api-key": api_key}
    response = requests.delete(
        f"{base_url}/v0/filters",
        headers=headers,
        json={"filter_group_id": filter_group_id},
    )
    assert response.status_code in [204, 404], f"Failed to delete monitor: {response.text}"


def get_project_id(api_key: str, base_url: str) -> str:
    """Get the first project ID for the authenticated user."""
    headers = {"Content-Type": "application/json", "api-key": api_key}
    response = requests.get(f"{base_url}/v0/projects", headers=headers)
    assert response.status_code in [200, 201], f"Failed to get projects: {response.status_code}"
    projects = response.json()
    assert len(projects) > 0, "No projects found"
    return str(projects[0]["id"])


def test_parallel_trace_processing_with_checks(api_key: str, base_url: str) -> None:
    """Test parallel processing of multiple spans in a single trace with monitor checks.

    This test:
    1. Creates a monitor with checks (coherence_summary, fluency_summary)
    2. Sends a single trace with 5 spans (triggers parallel processing >= 3 threshold)
    3. Verifies all 5 datapoints are created
    4. Verifies checks are executed on all datapoints
    """
    reset_timing()
    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    num_spans = 5  # Above parallel threshold (>=3)

    project_id = get_project_id(api_key, base_url)

    checks = ["coherence_summary", "fluency_summary"]

    # Step 1: Create monitor with checks
    logger.info(f"Creating monitor with checks: {checks}")
    monitor = create_monitor_with_checks(
        api_key=api_key,
        base_url=base_url,
        project_id=project_id,
        monitor_name=f"parallel_test_monitor_{test_id}",
        checks=checks,
    )
    filter_group_id = monitor["filter_group_id"]
    logger.info(f"Monitor created: {filter_group_id}")

    try:
        # Step 2: Send multi-span trace (triggers parallel processing)
        logger.info(f"Sending {num_spans} span trace with session_id={session_id}")
        payload = build_multi_span_trace_payload(
            session_id=session_id,
            num_spans=num_spans,
            test_identifier=test_id,
        )
        response = send_otel_trace(payload, api_key, base_url)

        # Verify response
        assert (
            response.status_code == 201
        ), f"Expected 201, got {response.status_code}: {response.text}"
        response_data = response.json()
        summary = response_data.get("summary", {})

        logger.info(f"Response: {response_data}")

        assert summary.get("status") == "success"
        assert summary.get("spans_processed") == num_spans
        assert summary.get("datapoints_created") == num_spans

        # Verify parallel processing was used
        message = response_data.get("message", "")
        assert (
            "parallel" in message.lower()
        ), f"Expected parallel processing, message: {message}"
        logger.info(f"Parallel processing confirmed: {message}")

        # Step 3: Find all datapoints and verify checks executed on each
        logger.info("Finding datapoints and verifying checks...")
        filters = [{"field": "context_token", "operator": "equal", "value": session_id}]
        datapoints = find_datapoints(api_key, base_url, filters, wait=5)

        assert (
            len(datapoints) >= num_spans
        ), f"Expected at least {num_spans} datapoints, found {len(datapoints)}"

        # Verify checks on each datapoint
        for i, datapoint in enumerate(datapoints[:num_spans]):
            checks_dict = datapoint.get("checks", {}) or {}
            check_names = set(checks_dict.keys())
            logger.info(f"Datapoint {i+1} checks: {list(check_names)}")

            for expected_check in checks:
                assert expected_check in check_names, (
                    f"Check '{expected_check}' not found in datapoint {i+1}. Found: {check_names}"
                )

        logger.info(
            f"SUCCESS: {num_spans} datapoints with checks verified (parallel processing)"
        )
        print_timing_summary()

    finally:
        delete_monitor(api_key, base_url, filter_group_id)
        logger.info("Monitor deleted")
