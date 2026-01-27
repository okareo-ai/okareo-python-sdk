import base64
import json
import logging
import secrets
import time
import uuid
from typing import Any

import pytest
import requests
from google.protobuf.json_format import ParseDict
from okareo_tests.common import API_KEY, random_string
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,
)

from okareo import Okareo
from okareo.common import BASE_URL

logger = logging.getLogger(__name__)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture(scope="module")
def rnd() -> str:
    """Generate a random string for test isolation."""
    return random_string(5)


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    """Create Okareo client for API interactions."""
    return Okareo(api_key=API_KEY)


@pytest.fixture(scope="module")
def project_id(okareo_client: Okareo) -> str:
    """Get project ID from the first available project."""
    projects = okareo_client.get_projects()
    assert len(projects) > 0, "No projects found"
    return str(projects[0].id)


# ============================================================================
# Helper Functions
# ============================================================================


def create_monitor_with_checks(
    project_id: str,
    monitor_name: str,
    checks: list[str],
) -> dict[str, Any]:
    """Create a monitor (filter) that matches traces and attaches checks.

    Returns:
        Created filter response with filter_group_id
    """
    headers = {"Content-Type": "application/json", "api-key": API_KEY}

    payload = {
        "filters": [
            {"field": "request_model_name", "operator": "contains", "value": "gpt"}
        ],
        "name": monitor_name,
        "description": "Test monitor for trace checks",
        "checks": checks,
        "project_id": project_id,
        "slack_enabled": False,
        "email_enabled": False,
    }

    response = requests.post(f"{BASE_URL}/v0/filters", headers=headers, json=payload)
    assert response.status_code == 201, f"Failed to create monitor: {response.text}"
    return response.json()


def delete_monitor(filter_group_id: str) -> None:
    """Delete a monitor (filter group)."""
    headers = {"Content-Type": "application/json", "api-key": API_KEY}
    response = requests.delete(
        f"{BASE_URL}/v0/filters",
        headers=headers,
        json={"filter_group_id": filter_group_id},
    )
    assert response.status_code in [204, 404], f"Failed to delete monitor: {response.text}"


def build_trace_payload(
    session_id: str,
    num_spans: int = 1,
    test_identifier: str | None = None,
) -> dict[str, Any]:
    """Build an OTEL trace payload with the specified number of GenAI spans.

    Args:
        session_id: Session ID for correlation (becomes context_token)
        num_spans: Number of spans to create
        test_identifier: Optional unique identifier for this test

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
            {"key": "gen_ai.request.model", "value": {"stringValue": "gpt-4"}},
            {"key": "gen_ai.system", "value": {"stringValue": "openai"}},
            {"key": "llm.request.type", "value": {"stringValue": "chat"}},
            {"key": "session.id", "value": {"stringValue": session_id}},
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

        if test_identifier:
            attributes.append(
                {"key": "test_identifier", "value": {"stringValue": test_identifier}}
            )

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
                        {"key": "service.name", "value": {"stringValue": "trace_test"}},
                    ]
                },
                "scopeSpans": [
                    {
                        "scope": {"name": "trace_test"},
                        "spans": spans,
                    }
                ],
            }
        ]
    }


def send_trace(payload: dict[str, Any]) -> requests.Response:
    """Send an OTEL trace to the Okareo traces endpoint."""
    trace_request = ExportTraceServiceRequest()
    ParseDict(payload, trace_request)
    serialized_data = trace_request.SerializeToString()

    headers = {"Content-Type": "application/x-protobuf", "api-key": API_KEY}
    return requests.post(f"{BASE_URL}/v0/traces", headers=headers, data=serialized_data)


def find_datapoints_by_session(
    project_id: str,
    session_id: str,
    expected_count: int,
    max_retries: int = 5,
) -> list[dict[str, Any]]:
    """Find datapoints by session_id (context_token) with retry logic.

    Uses raw HTTP to avoid SDK parsing issues with null checks_metadata.

    Args:
        project_id: Project ID to search in
        session_id: Session ID to filter by (context_token)
        expected_count: Expected number of datapoints
        max_retries: Max retry attempts

    Returns:
        List of datapoint dicts
    """
    headers = {"Content-Type": "application/json", "api-key": API_KEY}
    filters = [{"field": "context_token", "operator": "equal", "value": session_id}]

    datapoints: list[dict[str, Any]] = []
    for attempt in range(max_retries):
        time.sleep(3)
        response = requests.post(
            f"{BASE_URL}/v0/find_datapoints_filter",
            headers=headers,
            json={"limit": 100, "filters": filters, "project_id": project_id},
        )
        if response.status_code == 200:
            datapoints = response.json()
            if len(datapoints) >= expected_count:
                return datapoints
        logger.info(
            f"Retry {attempt + 1}/{max_retries}: found {len(datapoints)} datapoints"
        )

    return datapoints


# ============================================================================
# Tests
# ============================================================================


def test_single_datapoint_with_checks(rnd: str, project_id: str) -> None:
    """Test monitor creation, single span trace, and verify checks executed.

    This tests the sequential (inline) processing path with 1 datapoint.
    """
    test_id = f"single_{rnd}"
    session_id = str(uuid.uuid4())

    checks = ["coherence_summary", "fluency_summary"]

    # Step 1: Create monitor with checks
    logger.info(f"Creating monitor with checks: {checks}")
    monitor = create_monitor_with_checks(
        project_id=project_id,
        monitor_name=f"test_monitor_{test_id}",
        checks=checks,
    )
    filter_group_id = monitor["filter_group_id"]
    logger.info(f"Monitor created: {filter_group_id}")

    try:
        # Step 2: Send single span trace
        logger.info(f"Sending single span trace with session_id={session_id}")
        payload = build_trace_payload(
            session_id=session_id, num_spans=1, test_identifier=test_id
        )
        response = send_trace(payload)

        # Verify response
        assert (
            response.status_code == 201
        ), f"Expected 201, got {response.status_code}: {response.text}"
        response_data = response.json()
        summary = response_data.get("summary", {})

        logger.info(f"Response: {response_data}")

        assert summary.get("status") == "success"
        assert summary.get("spans_processed") == 1
        assert summary.get("datapoints_created") == 1

        # Step 3: Find datapoint and verify checks executed
        logger.info("Finding datapoint and verifying checks...")
        datapoints = find_datapoints_by_session(
            project_id=project_id,
            session_id=session_id,
            expected_count=1,
        )

        assert len(datapoints) == 1, f"Expected 1 datapoint, found {len(datapoints)}"

        datapoint = datapoints[0]
        checks_dict = datapoint.get("checks", {}) or {}
        logger.info(f"Datapoint checks: {list(checks_dict.keys())}")

        # Verify checks were executed
        check_names = set(checks_dict.keys())
        for expected_check in checks:
            assert (
                expected_check in check_names
            ), f"Check '{expected_check}' not found. Found: {check_names}"

        logger.info("SUCCESS: Single datapoint with checks verified")

    finally:
        delete_monitor(filter_group_id)
        logger.info("Monitor deleted")


def test_multi_datapoint_parallel_with_checks(rnd: str, project_id: str) -> None:
    """Test monitor creation, multi-span trace (parallel processing), and verify checks.

    This tests the parallel processing path with multiple datapoints (>=3 spans).
    """
    test_id = f"multi_{rnd}"
    session_id = str(uuid.uuid4())
    num_spans = 5  # Above parallel threshold (>=3)

    checks = ["coherence_summary", "fluency_summary"]

    # Step 1: Create monitor with checks
    logger.info(f"Creating monitor with checks: {checks}")
    monitor = create_monitor_with_checks(
        project_id=project_id,
        monitor_name=f"test_monitor_{test_id}",
        checks=checks,
    )
    filter_group_id = monitor["filter_group_id"]
    logger.info(f"Monitor created: {filter_group_id}")

    try:
        # Step 2: Send multi-span trace (triggers parallel processing)
        logger.info(f"Sending {num_spans} span trace with session_id={session_id}")
        payload = build_trace_payload(
            session_id=session_id, num_spans=num_spans, test_identifier=test_id
        )
        response = send_trace(payload)

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
        datapoints = find_datapoints_by_session(
            project_id=project_id,
            session_id=session_id,
            expected_count=num_spans,
        )

        assert (
            len(datapoints) == num_spans
        ), f"Expected {num_spans} datapoints, found {len(datapoints)}"

        # Verify checks on each datapoint
        for i, datapoint in enumerate(datapoints):
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

    finally:
        delete_monitor(filter_group_id)
        logger.info("Monitor deleted")
