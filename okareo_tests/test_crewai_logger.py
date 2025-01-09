import json
from typing import Any

from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.crewai_logger import CrewAILogger
from okareo_api_client.models.datapoint_search import DatapointSearch


def get_logger_config() -> dict[str, Any]:
    logger_config = {
        "api_key": API_KEY,
        "tags": ["crewai-test"],
        "context_token": random_string(10),
    }
    return logger_config


def test_crewai_logger() -> None:
    logger_config = get_logger_config()
    CrewAILogger(logger_config)

    from opentelemetry import trace

    tracer = trace.get_tracer("crewai.telemetry")
    with tracer.start_as_current_span("test_span") as span:
        span.set_attribute(
            "test_attribute",
            json.dumps(
                {
                    "agent": "test_agent",
                    "message": "This is a test message",
                    "timestamp": "2024-03-14T12:00:00Z",
                    "metadata": {"task_id": "123456", "priority": "high"},
                }
            ),
        )

    okareo = Okareo(api_key=API_KEY)
    dp = okareo.find_datapoints(
        DatapointSearch(context_token=logger_config["context_token"])
    )

    assert isinstance(dp, list)


def test_create_group() -> Any:
    okareo = Okareo(api_key=API_KEY)
    group_name = f"test_group_{random_string(5)}"
    tags = ["test", "crewai"]
    group = okareo.create_group(name=group_name, tags=tags)
    assert isinstance(group, dict)
    assert group.get("name") == group_name
    assert set(group.get("tags", [])) == set(tags)


def test_add_model_to_group() -> Any:
    okareo = Okareo(api_key=API_KEY)
    group_name = f"test_group_{random_string(5)}"
    group = okareo.create_group(name=group_name)
    model = okareo.register_model(name=f"test_model_{random_string(5)}")
    result = okareo.add_model_to_group(group, model)
    assert isinstance(result, dict)


def test_create_trace_eval() -> Any:
    okareo = Okareo(api_key=API_KEY)
    group_name = f"test_group_{random_string(5)}"
    group = okareo.create_group(name=group_name)
    okareo.create_trace_eval(group, "context_token")
