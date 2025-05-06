import os
import secrets
import time
from typing import Any

import pytest
import requests  # type: ignore
from google.protobuf.json_format import ParseDict  # type: ignore
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,  # type: ignore
)


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


def verify_span_recorded(random_string: Any, api_key: Any, base_url: Any) -> Any:
    """Verify the span with the random string was recorded in Okareo."""
    # Wait for data to propagate
    time.sleep(15)

    headers = {"Content-Type": "application/json", "api-key": api_key}

    # Get project ID
    project_response = requests.get(f"{base_url}/v0/projects", headers=headers)

    project_id = project_response.json()[0]["id"]

    # Try a few times with backoff
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            # Query for the span containing our random string
            payload = {
                "limit": 5,
                "filters": [
                    {"field": "input", "operator": "contains", "value": random_string}
                ],
                "project_id": project_id,
            }

            response = requests.post(
                f"{base_url}/v0/find_spans_filter", headers=headers, json=payload
            )

            data = response.json()
            if len(data) > 0:
                print(f"Found span with random string: {random_string}")
                return True

            # If not found and not last attempt, wait longer
            if attempt < max_attempts - 1:
                print(f"Span with {random_string} not found, retrying...")
                time.sleep(10 * (attempt + 1))

        except Exception as e:
            print(f"Error verifying span: {e}")
            if attempt < max_attempts - 1:
                time.sleep(5 * (attempt + 1))

    print(f"Failed to find span with random string: {random_string}")
    return False


def test_traces_endpoint_with_verification(api_key: Any, base_url: Any) -> Any:
    """Test sending trace data to the /traces endpoint with verification."""

    # Generate random identifier for this test
    random_string = generate_random_string()
    print(f"Using random string: {random_string}")

    # Prepare sample trace data with the random string
    sample_data = {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "litellm"}},
                        {
                            "key": "deployment.environment",
                            "value": {"stringValue": "production"},
                        },
                        {"key": "model_id", "value": {"stringValue": "litellm"}},
                    ]
                },
                "scopeSpans": [
                    {
                        "scope": {"name": "litellm"},
                        "spans": [
                            {
                                "traceId": "+Ma464bO5ON9+YlhFsG9Gg==",
                                "spanId": "y1Ygv5dY0jM=",
                                "parentSpanId": "DJfB8MovyNg=",
                                "name": f"litellm_request_{random_string}",  # Include random string in name
                                "kind": 1,
                                "startTimeUnixNano": "1746493671703133952",
                                "endTimeUnixNano": "1746493678456763904",
                                "attributes": [
                                    {
                                        "key": "gen_ai.request.model",
                                        "value": {
                                            "stringValue": "gemini-2.5-pro-exp-03-25"
                                        },
                                    },
                                    {
                                        "key": "llm.request.type",
                                        "value": {"stringValue": "acompletion"},
                                    },
                                    {
                                        "key": "llm.messages",
                                        "value": {
                                            "stringValue": f'[{{"content": "Test message with {random_string}", "role": "user"}}]'
                                        },
                                    },
                                    {
                                        "key": "test_identifier",  # Add dedicated attribute for the random string
                                        "value": {"stringValue": random_string},
                                    },
                                    {
                                        "key": "gen_ai.system",
                                        "value": {"stringValue": "vertex_ai"},
                                    },
                                    {
                                        "key": "gen_ai.response.id",
                                        "value": {
                                            "stringValue": f"chatcmpl-{random_string}"
                                        },
                                    },
                                    {
                                        "key": "llm.usage.total_tokens",
                                        "value": {"intValue": "574"},
                                    },
                                    {
                                        "key": "gen_ai.usage.completion_tokens",
                                        "value": {"intValue": "10"},
                                    },
                                    {
                                        "key": "gen_ai.usage.prompt_tokens",
                                        "value": {"intValue": "1"},
                                    },
                                    {
                                        "key": "SpanAttributes.LLM_PROMPTS.0.content",
                                        "value": {
                                            "stringValue": f"Test with {random_string}"
                                        },
                                    },
                                    {
                                        "key": "SpanAttributes.LLM_COMPLETIONS.0.content",
                                        "value": {
                                            "stringValue": f"Response to {random_string}"
                                        },
                                    },
                                ],
                                "status": {"code": 1},
                                "flags": 256,
                            }
                        ],
                    }
                ],
            }
        ]
    }

    # Convert JSON to protobuf
    trace_request = ExportTraceServiceRequest()
    ParseDict(sample_data, trace_request)

    # Serialize to binary format
    serialized_data = trace_request.SerializeToString()

    # Set up headers
    headers = {"Content-Type": "application/x-protobuf", "api-key": api_key}

    # Send request
    response = requests.post(
        f"{base_url}/v0/traces", headers=headers, data=serialized_data
    )

    # Assert response
    assert (
        response.status_code == 201
    ), f"Expected status code 201, got {response.status_code}: {response.text}"

    # Verify the response data
    try:
        response_data = response.json()
        assert response_data.get("status") == "success"
        assert "message" in response_data
        print(f"Response: {response_data}")
    except ValueError:
        # If response is not JSON, just check status code
        pass

    # Verify the span was recorded in Okareo
    assert verify_span_recorded(
        random_string, api_key, base_url
    ), f"Span with random string '{random_string}' was not found in Okareo"
