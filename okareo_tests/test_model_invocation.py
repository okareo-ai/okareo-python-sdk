"""How the SDK maps a custom model's ModelInvocation into the Run request it posts."""

import json
from typing import Union

import pytest
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo.model_under_test import CustomModel, ModelInvocation
from okareo_api_client.models import TestRunType

MOCK_UUID = "0156f5d7-4ac4-4568-9d44-24750aa08d1a"
MOCK_HOST = "http://mocked.com"

JSON_SCENARIO = [
    {
        "id": "11111111-1111-4111-8111-111111111111",
        "input": {"query": "user q 1", "user_id": "red", "meta": "meta1"},
        "result": "red",
    },
    {
        "id": "22222222-2222-4222-8222-222222222222",
        "input": {"query": "user q 2", "user_id": "blue", "meta": "meta1"},
        "result": "blue",
    },
    {
        "id": "33333333-3333-4333-8333-333333333333",
        "input": {"query": "user q 3", "user_id": "green", "meta": "meta1"},
        "result": "green",
    },
]


@pytest.fixture
def okareo_client(httpx_mock: HTTPXMock) -> Okareo:
    httpx_mock.add_response(
        json=[
            {
                "id": MOCK_UUID,
                "name": "Global",
                "onboarding_status": "onboarding_status",
                "tags": [],
                "additional_properties": {},
            }
        ],
        status_code=201,
    )
    return Okareo("api-key", MOCK_HOST)


def test_custom_return_invocation(okareo_client: Okareo, httpx_mock: HTTPXMock) -> None:
    test_run_name = "ci_test_custom_return_bc"

    class ClassificationModel(CustomModel):
        def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
            assert isinstance(input_value, dict)

            return ModelInvocation(
                model_prediction=input_value["user_id"],
                model_input=input_value["query"],
                model_output_metadata=input_value["meta"],
            )

    httpx_mock.add_response(
        url=f"{MOCK_HOST}/v0/register_model",
        status_code=201,
        json={
            "id": MOCK_UUID,
            "project_id": MOCK_UUID,
            "version": 1,
            "name": test_run_name,
            "tags": [],
            "time_created": "2026-11-23T00:00:00",
        },
    )
    httpx_mock.add_response(
        url=f"{MOCK_HOST}/v0/scenario_data_points/{MOCK_UUID}",
        status_code=200,
        json=JSON_SCENARIO,
    )
    httpx_mock.add_response(
        url=f"{MOCK_HOST}/v0/test_run",
        status_code=201,
        json={"id": MOCK_UUID, "project_id": MOCK_UUID, "name": test_run_name},
    )

    model_under_test = okareo_client.register_model(
        name=test_run_name,
        model=ClassificationModel(name=test_run_name),
    )
    model_under_test.run_test(
        scenario=MOCK_UUID,
        name=test_run_name,
        test_run_type=TestRunType.MULTI_CLASS_CLASSIFICATION,
        calculate_metrics=True,
    )

    run_request = httpx_mock.get_request(url=f"{MOCK_HOST}/v0/test_run")
    assert run_request is not None
    model_data = json.loads(run_request.content)["model_results"]["model_data"]
    assert model_data == {
        row["id"]: {
            "actual": row["input"]["user_id"],  # type: ignore[index]
            "model_response": row["input"]["meta"],  # type: ignore[index]
            "model_input": row["input"]["query"],  # type: ignore[index]
            "tool_calls": None,
        }
        for row in JSON_SCENARIO
    }
