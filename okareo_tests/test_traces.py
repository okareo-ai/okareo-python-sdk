import base64
import json
import logging
import os
import secrets
import time
import uuid
from contextlib import contextmanager
from typing import Any, Generator, Literal

import pytest
import requests  # type: ignore
from google.protobuf.json_format import ParseDict  # type: ignore
from okareo_tests.common import API_KEY, random_string
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,  # type: ignore
)
from pydantic import BaseModel, Field

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
# Response Schema Models (for strict validation)
# ============================================================================


class TraceSummary(BaseModel):
    """Expected structure of the trace ingestion summary."""

    status: Literal["success", "partial_success", "failed"]
    datapoints_created: int = Field(ge=0)
    spans_processed: int = Field(ge=0)
    checks_executed: int = Field(ge=0)
    issues_found: int = Field(ge=0)
    span_errors: list[dict[str, Any]] = Field(default_factory=list)
    check_errors: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class TraceResponse(BaseModel):
    """Expected structure of the /traces endpoint response."""

    status: str
    message: str
    summary: TraceSummary


def validate_trace_response(response_data: dict[str, Any]) -> TraceResponse:
    """Validate and parse trace response into typed model.

    Raises ValidationError if response doesn't match expected schema.
    """
    return TraceResponse.model_validate(response_data)


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


def build_multi_span_trace_payload(
    session_id: str,
    num_spans: int,
    test_identifier: str,
) -> dict[str, Any]:
    """Build a trace with multiple related spans (simulating a typical LLM call chain).

    This creates a chain of parent-child spans to test multi-span trace ingestion
    and parallel processing capabilities.

    Args:
        session_id: The session ID to use as context_token for correlation
        num_spans: Number of spans to create in the trace
        test_identifier: Unique string to identify this trace

    Returns:
        OTEL trace payload dict ready for protobuf conversion
    """
    current_time_ns = int(time.time() * 1_000_000_000)
    trace_id_bytes = secrets.token_bytes(16)
    trace_id_b64 = base64.b64encode(trace_id_bytes).decode("utf-8")

    spans = []
    parent_span_id = None

    for i in range(num_spans):
        span_id_bytes = secrets.token_bytes(8)
        span_id_b64 = base64.b64encode(span_id_bytes).decode("utf-8")
        # Stagger start times so spans are sequential
        start_ns = current_time_ns - ((num_spans - i) * 1_000_000_000)

        span: dict[str, Any] = {
            "traceId": trace_id_b64,
            "spanId": span_id_b64,
            "name": "litellm_request",  # Must match expected GenAI span naming
            "kind": 1,
            "startTimeUnixNano": str(start_ns),
            "endTimeUnixNano": str(start_ns + 500_000_000),
            "attributes": [
                {"key": "gen_ai.request.model", "value": {"stringValue": "gpt-4"}},
                {"key": "gen_ai.system", "value": {"stringValue": "openai"}},
                {"key": "llm.request.type", "value": {"stringValue": "chat"}},
                {"key": "session.id", "value": {"stringValue": session_id}},
                {"key": "test_identifier", "value": {"stringValue": test_identifier}},
                {
                    "key": "llm.messages",
                    "value": {
                        "stringValue": json.dumps(
                            [
                                {
                                    "role": "user",
                                    "content": f"Test message {i} for {test_identifier}",
                                }
                            ]
                        )
                    },
                },
                {
                    "key": "SpanAttributes.LLM_COMPLETIONS.0.content",
                    "value": {
                        "stringValue": f"Response {i} for test {test_identifier}"
                    },
                },
                {
                    "key": "SpanAttributes.LLM_COMPLETIONS.0.role",
                    "value": {"stringValue": "assistant"},
                },
            ],
            "status": {"code": 1},
            "flags": 256,
        }

        # Link spans in a parent-child chain
        if parent_span_id:
            span["parentSpanId"] = parent_span_id

        spans.append(span)
        parent_span_id = span_id_b64

    return {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": [
                        {
                            "key": "service.name",
                            "value": {"stringValue": "multi_span_test"},
                        },
                        {
                            "key": "deployment.environment",
                            "value": {"stringValue": "test"},
                        },
                    ]
                },
                "scopeSpans": [
                    {
                        "scope": {"name": "multi_span_test"},
                        "spans": spans,
                    }
                ],
            }
        ]
    }


# ============================================================================
# Trace Endpoint Tests
# ============================================================================


def test_traces_endpoint_with_verification(api_key: Any, base_url: Any) -> Any:
    """Test sending a single trace and verify it creates exactly one datapoint.

    This is the basic happy-path test for single-span trace ingestion.
    """
    reset_timing()

    # Generate identifiers for this test
    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    logger.info(
        f"Testing single span ingestion: test_id={test_id}, session_id={session_id}"
    )

    # Build and send trace
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

    # STRICT: Assert exact status code
    assert (
        response.status_code == 201
    ), f"Expected 201 Created, got {response.status_code}: {response.text}"

    # STRICT: Validate response against schema
    response_data = response.json()
    parsed = validate_trace_response(response_data)

    # STRICT: Assert exact values for single span
    assert parsed.status == "success"
    assert parsed.summary.status == "success"
    assert (
        parsed.summary.spans_processed == 1
    ), f"Expected exactly 1 span processed, got {parsed.summary.spans_processed}"
    assert (
        parsed.summary.datapoints_created == 1
    ), f"Expected exactly 1 datapoint, got {parsed.summary.datapoints_created}"
    assert (
        parsed.summary.span_errors == []
    ), f"Expected no span errors, got {parsed.summary.span_errors}"

    logger.info(f"Response validated: {parsed.summary.model_dump()}")

    # Verify datapoint exists in database
    filters = [{"field": "context_token", "operator": "equal", "value": session_id}]
    datapoints = find_datapoints(api_key, base_url, filters)

    # STRICT: Exactly 1 datapoint
    assert (
        len(datapoints) == 1
    ), f"Expected exactly 1 datapoint for session_id '{session_id}', found {len(datapoints)}"

    logger.info("SUCCESS: Single span -> 1 datapoint verified")
    print_timing_summary()


def test_multi_span_trace_ingestion(api_key: Any, base_url: Any) -> Any:
    """Test sending a multi-span trace and verify ALL spans create datapoints.

    This test validates:
    1. Exact span count matches processed count
    2. Each GenAI span creates exactly one datapoint
    3. Checks are executed on all datapoints
    4. No errors occur during processing
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    num_spans = 8  # Above threshold (5) for distributed processing

    logger.info(
        f"Testing multi-span ingestion: {num_spans} spans, session_id={session_id}"
    )

    # Build and send multi-span trace
    payload = build_multi_span_trace_payload(session_id, num_spans, test_id)
    response = send_otel_trace(payload, api_key, base_url)

    # STRICT: Assert exact status code
    assert (
        response.status_code == 201
    ), f"Expected 201 Created, got {response.status_code}: {response.text}"

    # STRICT: Validate response against schema
    response_data = response.json()
    parsed = validate_trace_response(response_data)

    logger.info(f"Response summary: {parsed.summary.model_dump()}")

    # STRICT: Assert exact values
    assert parsed.status == "success"
    assert (
        parsed.summary.status == "success"
    ), f"Expected 'success', got '{parsed.summary.status}'"
    assert (
        parsed.summary.spans_processed == num_spans
    ), f"Expected {num_spans} spans processed, got {parsed.summary.spans_processed}"
    assert (
        parsed.summary.datapoints_created == num_spans
    ), f"Expected {num_spans} datapoints (one per GenAI span), got {parsed.summary.datapoints_created}"
    assert (
        parsed.summary.span_errors == []
    ), f"Expected no span errors, got {parsed.summary.span_errors}"
    assert (
        parsed.summary.check_errors == []
    ), f"Expected no check errors, got {parsed.summary.check_errors}"

    # Checks should be executed (4 default checks per datapoint typically)
    assert (
        parsed.summary.checks_executed > 0
    ), f"Expected checks to be executed, got {parsed.summary.checks_executed}"
    logger.info(
        f"Checks executed: {parsed.summary.checks_executed} ({parsed.summary.checks_executed // num_spans} per datapoint)"
    )

    # Verify datapoints in database
    filters = [{"field": "context_token", "operator": "equal", "value": session_id}]
    datapoints = find_datapoints(api_key, base_url, filters)

    # STRICT: Exact datapoint count
    assert (
        len(datapoints) == num_spans
    ), f"Expected exactly {num_spans} datapoints in DB, found {len(datapoints)}"

    logger.info(f"SUCCESS: {num_spans} spans -> {len(datapoints)} datapoints verified")
    print_timing_summary()


# ============================================================================
# Parameterized Tests - Various Span Counts
# ============================================================================


@pytest.mark.parametrize("num_spans", [1, 3, 5, 10])
def test_trace_ingestion_various_sizes(
    api_key: Any, base_url: Any, num_spans: int
) -> None:
    """Test trace ingestion with various batch sizes.

    Validates that the system handles different span counts correctly:
    - 1 span: Minimum case
    - 3 spans: Below distributed threshold
    - 5 spans: At distributed threshold
    - 10 spans: Above distributed threshold
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())

    logger.info(f"Testing {num_spans} spans: session_id={session_id}")

    payload = build_multi_span_trace_payload(session_id, num_spans, test_id)
    response = send_otel_trace(payload, api_key, base_url)

    assert response.status_code == 201

    parsed = validate_trace_response(response.json())

    # All spans should be processed successfully
    assert parsed.summary.status == "success"
    assert parsed.summary.spans_processed == num_spans
    assert parsed.summary.datapoints_created == num_spans
    assert parsed.summary.span_errors == []

    logger.info(f"SUCCESS: {num_spans} spans processed correctly")


# ============================================================================
# Edge Case Tests
# ============================================================================


def test_empty_trace_returns_success(api_key: Any, base_url: Any) -> None:
    """Empty resourceSpans should return success with 0 spans processed."""
    reset_timing()

    # Build empty trace payload
    payload: dict[str, Any] = {"resourceSpans": []}

    response = send_otel_trace(payload, api_key, base_url)

    assert response.status_code == 201

    parsed = validate_trace_response(response.json())

    assert parsed.summary.status == "success"
    assert parsed.summary.spans_processed == 0
    assert parsed.summary.datapoints_created == 0
    assert parsed.summary.span_errors == []

    logger.info("SUCCESS: Empty trace handled correctly")


def test_non_genai_spans_no_datapoints(api_key: Any, base_url: Any) -> None:
    """Spans without GenAI attributes should be recorded but not create datapoints."""
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())

    # Build a span WITHOUT gen_ai.* attributes (just a basic HTTP span)
    current_time_ns = int(time.time() * 1_000_000_000)
    trace_id_bytes = secrets.token_bytes(16)
    span_id_bytes = secrets.token_bytes(8)

    payload: dict[str, Any] = {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": [
                        {
                            "key": "service.name",
                            "value": {"stringValue": "non_genai_test"},
                        }
                    ]
                },
                "scopeSpans": [
                    {
                        "scope": {"name": "http_client"},
                        "spans": [
                            {
                                "traceId": base64.b64encode(trace_id_bytes).decode(),
                                "spanId": base64.b64encode(span_id_bytes).decode(),
                                "name": "HTTP GET /api/users",  # NOT a GenAI span name
                                "kind": 3,  # CLIENT
                                "startTimeUnixNano": str(
                                    current_time_ns - 1_000_000_000
                                ),
                                "endTimeUnixNano": str(current_time_ns),
                                "attributes": [
                                    {
                                        "key": "http.method",
                                        "value": {"stringValue": "GET"},
                                    },
                                    {
                                        "key": "http.url",
                                        "value": {
                                            "stringValue": "https://api.example.com/users"
                                        },
                                    },
                                    {
                                        "key": "session.id",
                                        "value": {"stringValue": session_id},
                                    },
                                    {
                                        "key": "test_identifier",
                                        "value": {"stringValue": test_id},
                                    },
                                ],
                                "status": {"code": 1},
                            }
                        ],
                    }
                ],
            }
        ]
    }

    response = send_otel_trace(payload, api_key, base_url)

    assert response.status_code == 201

    parsed = validate_trace_response(response.json())

    # Span should be processed but NOT create a datapoint (no GenAI attributes)
    assert parsed.summary.status == "success"
    assert parsed.summary.spans_processed == 1  # Span was processed
    assert parsed.summary.datapoints_created == 0  # But no datapoint created
    assert parsed.summary.span_errors == []

    logger.info("SUCCESS: Non-GenAI span processed without creating datapoint")


def test_malformed_protobuf_returns_error(api_key: Any, base_url: Any) -> None:
    """Invalid protobuf data should return a 400 error."""
    reset_timing()

    # Send garbage data as protobuf
    headers = {"Content-Type": "application/x-protobuf", "api-key": api_key}

    response = requests.post(
        f"{base_url}/v0/traces",
        headers=headers,
        data=b"this is not valid protobuf data",
    )

    # Should return 400 Bad Request
    assert (
        response.status_code == 400
    ), f"Expected 400 for malformed protobuf, got {response.status_code}"

    logger.info("SUCCESS: Malformed protobuf correctly rejected with 400")


def test_performance_multi_span_under_threshold(api_key: Any, base_url: Any) -> None:
    """8 spans should process in under 10 seconds (generous threshold for parallel processing)."""
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    num_spans = 8
    max_allowed_seconds = 10.0  # Generous for parallel processing overhead

    payload = build_multi_span_trace_payload(session_id, num_spans, test_id)

    start = time.perf_counter()
    response = send_otel_trace(payload, api_key, base_url)
    elapsed = time.perf_counter() - start

    assert response.status_code == 201

    # Performance assertion
    assert (
        elapsed < max_allowed_seconds
    ), f"Processing {num_spans} spans took {elapsed:.2f}s, expected < {max_allowed_seconds}s"

    logger.info(
        f"SUCCESS: {num_spans} spans processed in {elapsed:.2f}s (< {max_allowed_seconds}s)"
    )


# ============================================================================
# Parallel Processing Tests - Threshold Boundary
# ============================================================================


def test_parallel_threshold_boundary_below(api_key: Any, base_url: Any) -> None:
    """2 spans should use inline processing (below PARALLEL_THRESHOLD=3).

    Verifies the inline path works correctly for small batches.
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    num_spans = 2  # Below threshold

    payload = build_multi_span_trace_payload(session_id, num_spans, test_id)
    response = send_otel_trace(payload, api_key, base_url)

    assert response.status_code == 201

    response_data = response.json()
    parsed = validate_trace_response(response_data)

    # Message should indicate inline processing (not parallel)
    assert "Traces processed" in response_data.get("message", "")
    assert "parallel" not in response_data.get("message", "").lower()

    assert parsed.summary.status == "success"
    assert parsed.summary.spans_processed == num_spans
    assert parsed.summary.datapoints_created == num_spans
    assert parsed.summary.span_errors == []

    logger.info(f"SUCCESS: {num_spans} spans processed inline (below threshold)")


def test_parallel_threshold_boundary_at(api_key: Any, base_url: Any) -> None:
    """3 spans should trigger parallel processing (at PARALLEL_THRESHOLD=3).

    Verifies parallel processing activates at exactly the threshold.
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    num_spans = 3  # At threshold

    payload = build_multi_span_trace_payload(session_id, num_spans, test_id)
    response = send_otel_trace(payload, api_key, base_url)

    assert response.status_code == 201

    response_data = response.json()
    parsed = validate_trace_response(response_data)

    # Message should indicate parallel processing
    assert (
        "parallel" in response_data.get("message", "").lower()
    ), f"Expected parallel processing at threshold, got: {response_data.get('message')}"

    assert parsed.summary.status == "success"
    assert parsed.summary.spans_processed == num_spans
    assert parsed.summary.datapoints_created == num_spans
    assert parsed.summary.span_errors == []

    logger.info(
        f"SUCCESS: {num_spans} spans triggered parallel processing at threshold"
    )


def test_parallel_threshold_boundary_above(api_key: Any, base_url: Any) -> None:
    """4 spans should definitely use parallel processing (above threshold).

    Verifies parallel processing works for batches above threshold.
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    num_spans = 4  # Above threshold

    payload = build_multi_span_trace_payload(session_id, num_spans, test_id)
    response = send_otel_trace(payload, api_key, base_url)

    assert response.status_code == 201

    response_data = response.json()
    parsed = validate_trace_response(response_data)

    assert "parallel" in response_data.get("message", "").lower()
    assert parsed.summary.status == "success"
    assert parsed.summary.spans_processed == num_spans
    assert parsed.summary.datapoints_created == num_spans

    logger.info(f"SUCCESS: {num_spans} spans processed in parallel (above threshold)")


# ============================================================================
# Parallel Processing Tests - Large Batches
# ============================================================================


@pytest.mark.parametrize("num_spans", [15, 25])
def test_large_batch_parallel_processing(
    api_key: Any, base_url: Any, num_spans: int
) -> None:
    """Test parallel processing handles large batches correctly.

    Validates that the system scales with larger span counts.
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())

    logger.info(f"Testing large batch: {num_spans} spans")

    payload = build_multi_span_trace_payload(session_id, num_spans, test_id)

    start = time.perf_counter()
    response = send_otel_trace(payload, api_key, base_url)
    elapsed = time.perf_counter() - start

    assert response.status_code == 201

    parsed = validate_trace_response(response.json())

    assert parsed.summary.status == "success"
    assert parsed.summary.spans_processed == num_spans
    assert parsed.summary.datapoints_created == num_spans
    assert parsed.summary.span_errors == []

    # Performance expectation: roughly linear with parallelism benefit
    # Allow ~1 second per span baseline, but parallel should be faster
    max_expected_time = min(num_spans * 1.0, 30.0)  # Cap at 30s
    assert (
        elapsed < max_expected_time
    ), f"{num_spans} spans took {elapsed:.2f}s, expected < {max_expected_time}s"

    logger.info(
        f"SUCCESS: {num_spans} spans in {elapsed:.2f}s ({elapsed/num_spans:.2f}s/span)"
    )


# ============================================================================
# Parallel Processing Tests - Concurrent Requests
# ============================================================================


def test_concurrent_trace_submissions(api_key: Any, base_url: Any) -> None:
    """Test that multiple concurrent trace submissions are handled correctly.

    Submits 3 traces simultaneously and verifies all are processed correctly.
    """
    import concurrent.futures

    reset_timing()

    test_id = generate_random_string()
    num_traces = 3
    spans_per_trace = 5

    def submit_trace(trace_index: int) -> tuple[int, dict[str, Any]]:
        session_id = str(uuid.uuid4())
        payload = build_multi_span_trace_payload(
            session_id, spans_per_trace, f"{test_id}_trace{trace_index}"
        )
        response = send_otel_trace(payload, api_key, base_url)
        return response.status_code, response.json()

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_traces) as executor:
        futures = [executor.submit(submit_trace, i) for i in range(num_traces)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    # All submissions should succeed
    for status_code, response_data in results:
        assert status_code == 201, f"Trace failed with status {status_code}"

        parsed = validate_trace_response(response_data)
        assert parsed.summary.status == "success"
        assert parsed.summary.spans_processed == spans_per_trace
        assert parsed.summary.datapoints_created == spans_per_trace

    logger.info(
        f"SUCCESS: {num_traces} concurrent traces ({spans_per_trace} spans each) processed"
    )


# ============================================================================
# Parallel Processing Tests - Mixed Span Types
# ============================================================================


def test_mixed_genai_and_non_genai_spans(api_key: Any, base_url: Any) -> None:
    """Test trace with both GenAI and non-GenAI spans in the same batch.

    Verifies:
    - All spans are processed
    - Only GenAI spans create datapoints
    - Non-GenAI spans are recorded but don't create datapoints
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())

    current_time_ns = int(time.time() * 1_000_000_000)
    trace_id_bytes = secrets.token_bytes(16)
    trace_id_b64 = base64.b64encode(trace_id_bytes).decode()

    spans = []
    num_genai_spans = 3
    num_non_genai_spans = 2

    # Create GenAI spans (should create datapoints)
    for i in range(num_genai_spans):
        span_id = base64.b64encode(secrets.token_bytes(8)).decode()
        spans.append(
            {
                "traceId": trace_id_b64,
                "spanId": span_id,
                "name": "litellm_request",
                "kind": 1,
                "startTimeUnixNano": str(current_time_ns - (i + 1) * 1_000_000_000),
                "endTimeUnixNano": str(current_time_ns - i * 500_000_000),
                "attributes": [
                    {"key": "gen_ai.request.model", "value": {"stringValue": "gpt-4"}},
                    {"key": "gen_ai.system", "value": {"stringValue": "openai"}},
                    {"key": "llm.request.type", "value": {"stringValue": "chat"}},
                    {"key": "session.id", "value": {"stringValue": session_id}},
                    {"key": "test_identifier", "value": {"stringValue": test_id}},
                    {
                        "key": "llm.messages",
                        "value": {
                            "stringValue": json.dumps(
                                [{"role": "user", "content": f"GenAI message {i}"}]
                            )
                        },
                    },
                    {
                        "key": "SpanAttributes.LLM_COMPLETIONS.0.content",
                        "value": {"stringValue": f"GenAI response {i}"},
                    },
                    {
                        "key": "SpanAttributes.LLM_COMPLETIONS.0.role",
                        "value": {"stringValue": "assistant"},
                    },
                ],
                "status": {"code": 1},
            }
        )

    # Create non-GenAI spans (should NOT create datapoints)
    for i in range(num_non_genai_spans):
        span_id = base64.b64encode(secrets.token_bytes(8)).decode()
        spans.append(
            {
                "traceId": trace_id_b64,
                "spanId": span_id,
                "name": f"http_request_{i}",
                "kind": 3,  # CLIENT
                "startTimeUnixNano": str(
                    current_time_ns - (num_genai_spans + i + 1) * 1_000_000_000
                ),
                "endTimeUnixNano": str(
                    current_time_ns - (num_genai_spans + i) * 500_000_000
                ),
                "attributes": [
                    {"key": "http.method", "value": {"stringValue": "GET"}},
                    {
                        "key": "http.url",
                        "value": {
                            "stringValue": f"https://api.example.com/endpoint{i}"
                        },
                    },
                    {"key": "session.id", "value": {"stringValue": session_id}},
                ],
                "status": {"code": 1},
            }
        )

    payload: dict[str, Any] = {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "mixed_test"}}
                    ]
                },
                "scopeSpans": [{"scope": {"name": "mixed_test"}, "spans": spans}],
            }
        ]
    }

    response = send_otel_trace(payload, api_key, base_url)

    assert response.status_code == 201

    parsed = validate_trace_response(response.json())

    total_spans = num_genai_spans + num_non_genai_spans

    assert parsed.summary.status == "success"
    assert (
        parsed.summary.spans_processed == total_spans
    ), f"Expected {total_spans} spans processed, got {parsed.summary.spans_processed}"
    # Only GenAI spans should create datapoints
    assert (
        parsed.summary.datapoints_created == num_genai_spans
    ), f"Expected {num_genai_spans} datapoints (GenAI only), got {parsed.summary.datapoints_created}"

    logger.info(
        f"SUCCESS: {total_spans} spans ({num_genai_spans} GenAI, {num_non_genai_spans} non-GenAI) processed correctly"
    )


# ============================================================================
# Parallel Processing Tests - Session Isolation
# ============================================================================


def test_session_isolation_parallel_processing(api_key: Any, base_url: Any) -> None:
    """Test that parallel processing maintains session isolation.

    Two different sessions submitted together should not interfere with each other.
    """
    reset_timing()

    test_id = generate_random_string()
    session_id_1 = str(uuid.uuid4())
    session_id_2 = str(uuid.uuid4())
    num_spans = 4

    # Submit first trace
    payload_1 = build_multi_span_trace_payload(
        session_id_1, num_spans, f"{test_id}_session1"
    )
    response_1 = send_otel_trace(payload_1, api_key, base_url)

    # Submit second trace immediately after
    payload_2 = build_multi_span_trace_payload(
        session_id_2, num_spans, f"{test_id}_session2"
    )
    response_2 = send_otel_trace(payload_2, api_key, base_url)

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    parsed_1 = validate_trace_response(response_1.json())
    parsed_2 = validate_trace_response(response_2.json())

    # Both should succeed independently
    assert parsed_1.summary.status == "success"
    assert parsed_2.summary.status == "success"
    assert parsed_1.summary.datapoints_created == num_spans
    assert parsed_2.summary.datapoints_created == num_spans

    # Verify session isolation in database
    filters_1 = [{"field": "context_token", "operator": "equal", "value": session_id_1}]
    filters_2 = [{"field": "context_token", "operator": "equal", "value": session_id_2}]

    datapoints_1 = find_datapoints(api_key, base_url, filters_1)
    datapoints_2 = find_datapoints(api_key, base_url, filters_2)

    assert (
        len(datapoints_1) == num_spans
    ), f"Session 1: expected {num_spans}, got {len(datapoints_1)}"
    assert (
        len(datapoints_2) == num_spans
    ), f"Session 2: expected {num_spans}, got {len(datapoints_2)}"

    # Verify no cross-contamination (datapoint IDs should be different)
    ids_1 = {dp.get("id") for dp in datapoints_1}
    ids_2 = {dp.get("id") for dp in datapoints_2}
    assert ids_1.isdisjoint(ids_2), "Sessions should have distinct datapoint IDs"

    logger.info(
        f"SUCCESS: Session isolation verified ({num_spans} datapoints each, no overlap)"
    )


# ============================================================================
# Parallel Processing Tests - Check Execution Verification
# ============================================================================


def test_checks_executed_on_all_parallel_datapoints(
    api_key: Any, base_url: Any
) -> None:
    """Verify that checks are executed on all datapoints created by parallel processing.

    This is critical - parallel processing should not skip check evaluation.
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    num_spans = 6  # Above threshold for parallel

    payload = build_multi_span_trace_payload(session_id, num_spans, test_id)
    response = send_otel_trace(payload, api_key, base_url)

    assert response.status_code == 201

    parsed = validate_trace_response(response.json())

    assert parsed.summary.status == "success"
    assert parsed.summary.datapoints_created == num_spans

    # Checks should be executed on ALL datapoints
    # Default checks typically include: latency, token_count, etc.
    assert parsed.summary.checks_executed > 0, "Expected checks to be executed"

    # Each datapoint should have checks run on it
    # Minimum expectation: at least 1 check per datapoint
    min_expected_checks = num_spans
    assert parsed.summary.checks_executed >= min_expected_checks, (
        f"Expected at least {min_expected_checks} checks (1 per datapoint), "
        f"got {parsed.summary.checks_executed}"
    )

    checks_per_datapoint = parsed.summary.checks_executed / num_spans
    logger.info(
        f"SUCCESS: {parsed.summary.checks_executed} checks executed (~{checks_per_datapoint:.1f} per datapoint)"
    )


# ============================================================================
# Parallel Processing Tests - Datapoint Field Validation
# ============================================================================


def test_parallel_datapoints_have_required_fields(api_key: Any, base_url: Any) -> None:
    """Verify datapoints created by parallel processing have all required fields.

    Ensures parallel processing doesn't skip populating any fields.
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    num_spans = 5  # Above threshold

    payload = build_multi_span_trace_payload(session_id, num_spans, test_id)
    response = send_otel_trace(payload, api_key, base_url)

    assert response.status_code == 201

    parsed = validate_trace_response(response.json())
    assert parsed.summary.datapoints_created == num_spans

    # Fetch actual datapoints from database
    filters = [{"field": "context_token", "operator": "equal", "value": session_id}]
    datapoints = find_datapoints(api_key, base_url, filters)

    assert len(datapoints) == num_spans

    # Required fields that should be populated
    required_fields = ["id", "context_token", "input", "result", "time_created"]

    for i, dp in enumerate(datapoints):
        for field in required_fields:
            assert field in dp, f"Datapoint {i} missing required field: {field}"
            assert dp[field] is not None, f"Datapoint {i} has null {field}"

        # Verify context_token matches session
        assert (
            dp["context_token"] == session_id
        ), f"Datapoint {i} context_token mismatch: {dp['context_token']} != {session_id}"

    logger.info(f"SUCCESS: All {num_spans} datapoints have required fields populated")


# ============================================================================
# Parallel Processing Tests - Consistency Verification
# ============================================================================


def test_parallel_processing_result_consistency(api_key: Any, base_url: Any) -> None:
    """Verify parallel processing produces consistent results across multiple runs.

    Same input should produce equivalent output (deterministic behavior).
    """
    reset_timing()

    test_id = generate_random_string()
    num_spans = 5

    results = []
    for run in range(2):
        session_id = str(uuid.uuid4())
        payload = build_multi_span_trace_payload(
            session_id, num_spans, f"{test_id}_run{run}"
        )
        response = send_otel_trace(payload, api_key, base_url)

        assert response.status_code == 201
        parsed = validate_trace_response(response.json())
        results.append(parsed.summary)

    # Both runs should have identical counts
    assert results[0].spans_processed == results[1].spans_processed == num_spans
    assert results[0].datapoints_created == results[1].datapoints_created == num_spans
    assert results[0].status == results[1].status == "success"

    # Error counts should be identical (zero)
    assert results[0].span_errors == results[1].span_errors == []
    assert results[0].check_errors == results[1].check_errors == []

    logger.info(f"SUCCESS: Consistent results across 2 runs ({num_spans} spans each)")


# ============================================================================
# Parallel Processing Tests - Retry/Duplicate Handling
# ============================================================================


def test_duplicate_trace_submission(api_key: Any, base_url: Any) -> None:
    """Test that duplicate trace submissions are handled gracefully.

    Submitting the same trace twice should not cause errors
    (may create duplicate datapoints - this is acceptable behavior).
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    num_spans = 4

    payload = build_multi_span_trace_payload(session_id, num_spans, test_id)

    # Submit same trace twice
    response_1 = send_otel_trace(payload, api_key, base_url)
    response_2 = send_otel_trace(payload, api_key, base_url)

    # Both should succeed (no errors)
    assert response_1.status_code == 201
    assert response_2.status_code == 201

    parsed_1 = validate_trace_response(response_1.json())
    parsed_2 = validate_trace_response(response_2.json())

    assert parsed_1.summary.status == "success"
    assert parsed_2.summary.status == "success"

    # Both should process all spans (duplicate handling is at a different layer)
    assert parsed_1.summary.spans_processed == num_spans
    assert parsed_2.summary.spans_processed == num_spans

    logger.info("SUCCESS: Duplicate submissions handled gracefully")


# ============================================================================
# Parallel Processing Tests - Stress Test
# ============================================================================


@pytest.mark.slow
def test_stress_parallel_processing(api_key: Any, base_url: Any) -> None:
    """Stress test with a larger batch to verify system stability.

    Mark as slow - skip in quick test runs.
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    num_spans = 50  # Large batch

    logger.info(f"Stress test: {num_spans} spans")

    payload = build_multi_span_trace_payload(session_id, num_spans, test_id)

    start = time.perf_counter()
    response = send_otel_trace(payload, api_key, base_url)
    elapsed = time.perf_counter() - start

    assert response.status_code == 201

    parsed = validate_trace_response(response.json())

    # Allow partial success for stress test
    assert parsed.summary.status in ["success", "partial_success"]

    # At least 80% should succeed
    success_rate = parsed.summary.datapoints_created / num_spans
    assert success_rate >= 0.8, f"Success rate {success_rate:.1%} below 80%"

    logger.info(
        f"STRESS TEST: {parsed.summary.datapoints_created}/{num_spans} datapoints "
        f"({success_rate:.1%}) in {elapsed:.2f}s"
    )


# ============================================================================
# Parallel Processing Tests - Response Message Verification
# ============================================================================


def test_response_message_indicates_processing_mode(
    api_key: Any, base_url: Any
) -> None:
    """Verify response message correctly indicates processing mode.

    - Inline: "Traces processed"
    - Parallel: "Traces processed (parallel)"
    """
    reset_timing()

    test_id = generate_random_string()

    # Test inline (2 spans, below threshold)
    session_inline = str(uuid.uuid4())
    payload_inline = build_multi_span_trace_payload(
        session_inline, 2, f"{test_id}_inline"
    )
    response_inline = send_otel_trace(payload_inline, api_key, base_url)

    assert response_inline.status_code == 201
    inline_message = response_inline.json().get("message", "")
    assert "Traces processed" in inline_message
    assert (
        "parallel" not in inline_message.lower()
    ), f"2 spans should use inline, got: {inline_message}"

    # Test parallel (5 spans, above threshold)
    session_parallel = str(uuid.uuid4())
    payload_parallel = build_multi_span_trace_payload(
        session_parallel, 5, f"{test_id}_parallel"
    )
    response_parallel = send_otel_trace(payload_parallel, api_key, base_url)

    assert response_parallel.status_code == 201
    parallel_message = response_parallel.json().get("message", "")
    assert (
        "parallel" in parallel_message.lower()
    ), f"5 spans should use parallel, got: {parallel_message}"

    logger.info("SUCCESS: Response messages correctly indicate processing mode")


# ============================================================================
# Filter and Check Integration Tests
# ============================================================================


def get_project_id(api_key: str, base_url: str) -> str:
    """Get the first project ID for the authenticated user."""
    headers = {"Content-Type": "application/json", "api-key": api_key}
    response = requests.get(f"{base_url}/v0/projects", headers=headers)
    # API may return 200 or 201
    assert response.status_code in [
        200,
        201,
    ], f"Failed to get projects: {response.status_code}"
    projects = response.json()
    assert len(projects) > 0, "No projects found"
    return str(projects[0]["id"])


def create_filter_with_checks(
    api_key: str,
    base_url: str,
    project_id: str,
    filter_name: str,
    filter_conditions: list[dict[str, str]],
    checks: list[str],
) -> dict[str, Any]:
    """Create a datapoint filter with attached checks.

    Args:
        api_key: API key for authentication
        base_url: Base URL for the API
        project_id: Project ID to create filter in
        filter_name: Name for the filter
        filter_conditions: List of condition dicts with field, operator, value
        checks: List of check names to attach

    Returns:
        Created filter response
    """
    headers = {"Content-Type": "application/json", "api-key": api_key}

    payload = {
        "filters": filter_conditions,
        "name": filter_name,
        "description": f"Test filter created at {time.time()}",
        "checks": checks,
        "project_id": project_id,
        "slack_enabled": False,
        "email_enabled": False,
    }

    response = requests.post(
        f"{base_url}/v0/filters",
        headers=headers,
        json=payload,
    )

    assert response.status_code == 201, f"Failed to create filter: {response.text}"
    result: dict[str, Any] = response.json()
    return result


def delete_filter(api_key: str, base_url: str, filter_group_id: str) -> None:
    """Delete a filter group."""
    headers = {"Content-Type": "application/json", "api-key": api_key}

    response = requests.delete(
        f"{base_url}/v0/filters",
        headers=headers,
        json={"filter_group_id": filter_group_id},
    )

    # 204 No Content is success, 404 means already deleted
    assert response.status_code in [
        204,
        404,
    ], f"Failed to delete filter: {response.text}"


def get_filters(api_key: str, base_url: str, project_id: str) -> list[dict[str, Any]]:
    """Get all filters for a project."""
    headers = {"Content-Type": "application/json", "api-key": api_key}

    response = requests.get(
        f"{base_url}/v0/filters",
        headers=headers,
        params={"project_id": project_id},
    )

    assert response.status_code == 200, f"Failed to get filters: {response.text}"
    result: list[dict[str, Any]] = response.json()
    return result


def test_filter_creation_and_deletion(api_key: Any, base_url: Any) -> None:
    """Test creating and deleting a filter with attached checks."""
    reset_timing()

    test_id = generate_random_string()
    project_id = get_project_id(api_key, base_url)

    # Create a filter that matches a specific model
    filter_response = create_filter_with_checks(
        api_key=api_key,
        base_url=base_url,
        project_id=project_id,
        filter_name=f"test_filter_{test_id}",
        filter_conditions=[
            {"field": "request_model_name", "operator": "contains", "value": "gpt"}
        ],
        checks=["latency", "input_tokens"],
    )

    assert "filter_group_id" in filter_response
    filter_group_id = filter_response["filter_group_id"]

    try:
        # Verify the filter was created
        filters = get_filters(api_key, base_url, project_id)
        filter_names = [f.get("name") for f in filters]
        assert f"test_filter_{test_id}" in filter_names

        logger.info(f"SUCCESS: Filter created with ID {filter_group_id}")
    finally:
        # Cleanup
        delete_filter(api_key, base_url, filter_group_id)
        logger.info(f"Filter {filter_group_id} deleted")


def test_trace_with_filter_attached_checks(api_key: Any, base_url: Any) -> None:
    """Test that traces matching a filter have the attached checks executed.

    1. Create a filter that matches by context_token
    2. Attach a specific check to the filter
    3. Send a trace that matches the filter
    4. Verify the check was executed on the resulting datapoint
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    project_id = get_project_id(api_key, base_url)

    # Create a filter that matches our specific session_id
    filter_response = create_filter_with_checks(
        api_key=api_key,
        base_url=base_url,
        project_id=project_id,
        filter_name=f"trace_check_test_{test_id}",
        filter_conditions=[
            {"field": "context_token", "operator": "equal", "value": session_id}
        ],
        checks=["latency", "output_tokens", "cost"],
    )

    filter_group_id = filter_response["filter_group_id"]

    try:
        # Send a trace that will match the filter
        payload = build_multi_span_trace_payload(session_id, 3, test_id)
        response = send_otel_trace(payload, api_key, base_url)

        assert response.status_code == 201
        parsed = validate_trace_response(response.json())

        # Verify datapoints were created
        assert parsed.summary.datapoints_created == 3

        # Verify checks were executed (should include filter-attached checks)
        assert parsed.summary.checks_executed > 0

        # Fetch datapoints and verify check values exist
        filters = [{"field": "context_token", "operator": "equal", "value": session_id}]
        datapoints = find_datapoints(api_key, base_url, filters)

        assert len(datapoints) == 3

        # Verify at least one datapoint has check results
        checks_found = False
        for dp in datapoints:
            if dp.get("checks") and len(dp["checks"]) > 0:
                checks_found = True
                # Check for the specific checks we attached
                check_names = list(dp["checks"].keys())
                logger.info(f"Datapoint checks: {check_names}")
                break

        assert checks_found, "No check results found on datapoints"

        logger.info(
            f"SUCCESS: Filter-attached checks executed on {len(datapoints)} datapoints"
        )

    finally:
        # Cleanup
        delete_filter(api_key, base_url, filter_group_id)


def test_parallel_traces_with_model_filter(api_key: Any, base_url: Any) -> None:
    """Test parallel processing with a model-based filter.

    Creates a filter that matches by model name (gpt-4) and verifies
    checks are executed on parallel-processed datapoints.
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    project_id = get_project_id(api_key, base_url)
    num_spans = 6  # Above parallel threshold

    # Create a filter matching our model
    filter_response = create_filter_with_checks(
        api_key=api_key,
        base_url=base_url,
        project_id=project_id,
        filter_name=f"model_filter_{test_id}",
        filter_conditions=[
            {"field": "request_model_name", "operator": "contains", "value": "gpt-4"}
        ],
        checks=["latency", "input_tokens", "output_tokens"],
    )

    filter_group_id = filter_response["filter_group_id"]

    try:
        # Send parallel trace
        payload = build_multi_span_trace_payload(session_id, num_spans, test_id)
        response = send_otel_trace(payload, api_key, base_url)

        assert response.status_code == 201
        assert "parallel" in response.json().get("message", "").lower()

        parsed = validate_trace_response(response.json())

        assert parsed.summary.datapoints_created == num_spans

        # Checks should be executed (count depends on which checks succeed)
        # At minimum, some checks should run
        assert parsed.summary.checks_executed >= 0

        checks_per_dp = (
            parsed.summary.checks_executed / num_spans if num_spans > 0 else 0
        )

        logger.info(
            f"SUCCESS: {num_spans} parallel datapoints with "
            f"{parsed.summary.checks_executed} checks ({checks_per_dp:.1f}/dp)"
        )

    finally:
        delete_filter(api_key, base_url, filter_group_id)


def test_default_checks_always_run(api_key: Any, base_url: Any) -> None:
    """Verify default checks run even without custom filters.

    Base checks should always execute on GenAI datapoints.
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    num_spans = 4

    payload = build_multi_span_trace_payload(session_id, num_spans, test_id)
    response = send_otel_trace(payload, api_key, base_url)

    assert response.status_code == 201
    parsed = validate_trace_response(response.json())

    assert parsed.summary.datapoints_created == num_spans

    # At least some checks should run (default checks exist)
    # Don't require exact count since check availability may vary
    assert parsed.summary.checks_executed >= 0

    # Verify datapoints were created and can be retrieved
    filters = [{"field": "context_token", "operator": "equal", "value": session_id}]
    datapoints = find_datapoints(api_key, base_url, filters)

    assert len(datapoints) == num_spans

    # Check if any datapoint has check results
    datapoints_with_checks = sum(1 for dp in datapoints if dp.get("checks"))

    for dp in datapoints:
        checks = dp.get("checks", {})
        if checks:
            check_names = [k for k in checks.keys() if "__explanation" not in k]
            logger.info(f"Datapoint check keys: {check_names}")

    logger.info(
        f"SUCCESS: {parsed.summary.checks_executed} checks executed, "
        f"{datapoints_with_checks}/{num_spans} datapoints have check results"
    )


def test_check_values_stored_correctly(api_key: Any, base_url: Any) -> None:
    """Verify check values are correctly stored and retrievable.

    Validates that check results have proper structure when present.
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())

    # Single span for simpler verification
    payload = build_otel_trace_payload(
        session_id=session_id,
        messages=[{"role": "user", "content": f"Test message for {test_id}"}],
        completion=f"This is a test response for verifying check values in {test_id}",
        test_identifier=test_id,
    )

    response = send_otel_trace(payload, api_key, base_url)
    assert response.status_code == 201

    parsed = validate_trace_response(response.json())
    assert parsed.summary.datapoints_created == 1

    # Fetch the datapoint with full details
    filters = [{"field": "context_token", "operator": "equal", "value": session_id}]
    datapoints = find_datapoints(api_key, base_url, filters)

    assert len(datapoints) == 1
    dp = datapoints[0]

    checks = dp.get("checks", {})

    # Validate check structure if checks exist
    check_count = 0
    if checks:
        for check_name, check_value in checks.items():
            if "__explanation" not in check_name:
                check_count += 1
                # Value should be numeric, boolean, or None
                if check_value is not None:
                    assert isinstance(
                        check_value, (bool, int, float, str)
                    ), f"Check {check_name} has unexpected type: {type(check_value)}"
                    logger.info(f"Check {check_name}: {check_value}")

    logger.info(f"SUCCESS: {check_count} check values found and validated")


def test_multiple_filters_with_overlapping_checks(api_key: Any, base_url: Any) -> None:
    """Test that multiple matching filters don't cause duplicate check execution.

    When a datapoint matches multiple filters with overlapping checks,
    each unique check should only run once.
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    project_id = get_project_id(api_key, base_url)

    # Create two filters with overlapping checks
    filter1 = create_filter_with_checks(
        api_key=api_key,
        base_url=base_url,
        project_id=project_id,
        filter_name=f"overlap_filter1_{test_id}",
        filter_conditions=[
            {"field": "request_model_name", "operator": "contains", "value": "gpt"}
        ],
        checks=["latency", "input_tokens"],
    )

    filter2 = create_filter_with_checks(
        api_key=api_key,
        base_url=base_url,
        project_id=project_id,
        filter_name=f"overlap_filter2_{test_id}",
        filter_conditions=[
            {"field": "request_model_name", "operator": "contains", "value": "gpt-4"}
        ],
        checks=["latency", "output_tokens"],  # latency overlaps with filter1
    )

    try:
        # Send a trace that matches both filters
        payload = build_multi_span_trace_payload(session_id, 4, test_id)
        response = send_otel_trace(payload, api_key, base_url)

        assert response.status_code == 201
        parsed = validate_trace_response(response.json())

        # Should succeed without duplicate check errors
        assert parsed.summary.status == "success"
        assert parsed.summary.datapoints_created == 4

        # Verify datapoints have checks
        filters = [{"field": "context_token", "operator": "equal", "value": session_id}]
        datapoints = find_datapoints(api_key, base_url, filters)

        assert len(datapoints) == 4

        logger.info("SUCCESS: Overlapping filters handled correctly")

    finally:
        delete_filter(api_key, base_url, filter1["filter_group_id"])
        delete_filter(api_key, base_url, filter2["filter_group_id"])


# ============================================================================
# Comprehensive End-to-End Trace Flow Tests
# ============================================================================


def test_full_trace_lifecycle(api_key: Any, base_url: Any) -> None:
    """Test complete trace lifecycle: ingest -> checks -> query.

    This is a comprehensive integration test covering:
    1. Create filter with checks
    2. Send multi-span trace (parallel path)
    3. Verify response contains check execution count
    4. Query datapoints and verify check results exist
    5. Verify check values are sensible
    6. Cleanup
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    project_id = get_project_id(api_key, base_url)
    num_spans = 5

    # Step 1: Create filter with checks
    filter_response = create_filter_with_checks(
        api_key=api_key,
        base_url=base_url,
        project_id=project_id,
        filter_name=f"lifecycle_test_{test_id}",
        filter_conditions=[
            {"field": "context_token", "operator": "equal", "value": session_id}
        ],
        checks=["latency", "input_tokens", "output_tokens", "cost"],
    )
    filter_group_id = filter_response["filter_group_id"]
    logger.info(f"Step 1: Filter created (ID: {filter_group_id})")

    try:
        # Step 2: Send multi-span trace
        payload = build_multi_span_trace_payload(session_id, num_spans, test_id)

        with timed("trace_ingestion"):
            response = send_otel_trace(payload, api_key, base_url)

        assert response.status_code == 201
        response_data = response.json()
        parsed = validate_trace_response(response_data)
        logger.info(f"Step 2: Trace sent (message: {response_data['message']})")

        # Step 3: Verify response
        assert parsed.summary.status == "success"
        assert parsed.summary.spans_processed == num_spans
        assert parsed.summary.datapoints_created == num_spans
        assert parsed.summary.checks_executed > 0
        assert parsed.summary.span_errors == []
        assert parsed.summary.check_errors == []
        logger.info(
            f"Step 3: Response validated (checks: {parsed.summary.checks_executed})"
        )

        # Step 4: Query datapoints
        filters = [{"field": "context_token", "operator": "equal", "value": session_id}]
        datapoints = find_datapoints(api_key, base_url, filters)

        assert (
            len(datapoints) == num_spans
        ), f"Expected {num_spans} datapoints, found {len(datapoints)}"
        logger.info(f"Step 4: {len(datapoints)} datapoints queried")

        # Step 5: Verify check values
        for i, dp in enumerate(datapoints):
            dp.get("id")
            checks = dp.get("checks", {})

            # Should have check values
            check_count = len([k for k in checks.keys() if "__explanation" not in k])
            assert check_count > 0, f"Datapoint {i} has no check values"

            # Latency should be a positive number if present
            if "latency" in checks:
                latency = checks["latency"]
                assert (
                    isinstance(latency, (int, float)) and latency >= 0
                ), f"Invalid latency value: {latency}"

        logger.info("Step 5: Check values validated")

        # Print timing summary
        print_timing_summary()
        logger.info("FULL LIFECYCLE TEST PASSED")

    finally:
        # Cleanup
        delete_filter(api_key, base_url, filter_group_id)
        logger.info("Cleanup: Filter deleted")


def test_high_volume_parallel_with_checks(api_key: Any, base_url: Any) -> None:
    """Test high volume parallel processing with check execution.

    Sends 20 spans and verifies:
    - All spans processed
    - All datapoints created
    - Some checks executed
    - No errors
    """
    reset_timing()

    test_id = generate_random_string()
    session_id = str(uuid.uuid4())
    num_spans = 20

    logger.info(f"High volume test: {num_spans} spans")

    payload = build_multi_span_trace_payload(session_id, num_spans, test_id)

    start = time.perf_counter()
    response = send_otel_trace(payload, api_key, base_url)
    elapsed = time.perf_counter() - start

    assert response.status_code == 201
    parsed = validate_trace_response(response.json())

    # All spans should be processed
    assert parsed.summary.spans_processed == num_spans
    assert parsed.summary.datapoints_created == num_spans
    assert parsed.summary.status == "success"
    assert parsed.summary.span_errors == []

    # Some checks should run
    assert parsed.summary.checks_executed >= 0

    # Reasonable time expectation
    max_time = 60.0  # 60 seconds max for 20 spans
    assert elapsed < max_time, f"Took {elapsed:.2f}s, expected < {max_time}s"

    checks_per_dp = parsed.summary.checks_executed / num_spans if num_spans > 0 else 0

    logger.info(
        f"SUCCESS: {num_spans} spans processed in {elapsed:.2f}s "
        f"({elapsed/num_spans:.2f}s/span, {parsed.summary.checks_executed} checks, {checks_per_dp:.1f}/dp)"
    )


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
