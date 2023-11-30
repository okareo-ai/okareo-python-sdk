import random
from datetime import datetime
from typing import Optional, Tuple
from unittest.mock import Mock

import pytest
from okareo_tests.common import API_KEY, OkareoAPIhost, integration, random_string
from pytest_httpx import HTTPXMock

from okareo import ModelUnderTest, Okareo
from okareo.error import MissingApiKeyError, MissingVectorDbError
from okareo.model_under_test import CohereModel, PineconeDb
from okareo_api_client.models import SeedData, TestRunItem
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.test_run_type import TestRunType


def helper_register_model(httpx_mock: HTTPXMock) -> ModelUnderTest:
    fixture = get_mut_fixture("NotebookModel")
    httpx_mock.add_response(status_code=201, json=fixture)
    okareo = Okareo("api-key", "http://mocked.com")
    return okareo.register_model(name="NotebookModel", tags=["ci-testing"])


def get_mut_fixture(name: Optional[str] = None) -> dict:
    rnd_str = random_string(5)
    return {
        "id": "1",
        "project_id": "1",
        "name": name if name else f"CI-Test-Model-{rnd_str}",
        "tags": ["ci-testing"],
        "time_created": "foo",
    }


@integration
def test_register_model(httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost) -> None:
    fixture = get_mut_fixture()
    if okareo_api.is_mock:
        httpx_mock.add_response(status_code=201, json=fixture)

    okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)
    mut = okareo.register_model(name=fixture["name"], tags=fixture["tags"])
    assert mut.name == fixture["name"]


@integration
def test_add_datapoint_optional_integration(
    httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost
) -> None:
    fixture = get_mut_fixture()
    if okareo_api.is_mock:
        httpx_mock.add_response(status_code=201, json=fixture)

    okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)
    mut = okareo.register_model(name=fixture["name"], tags=fixture["tags"])
    dp = mut.add_data_point(
        feedback=0,
        context_token="SOME_CONTEXT_TOKEN",
    )
    assert dp


@integration
def test_mut_test_run(httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost) -> None:
    mut_fixture = get_mut_fixture()
    okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)

    if okareo_api.is_mock:
        httpx_mock.add_response(
            status_code=201,
            json={
                "scenario_id": "scenario-id",
                "project_id": "project-id",
                "time_created": str(datetime.now()),
                "type": "REPHRASE_INVARIANT",
            },
        )
        httpx_mock.add_response(status_code=201, json=mut_fixture)
        httpx_mock.add_response(
            status_code=200,
            json=[
                {
                    "id": "test-run-item-id",
                    "name": "CI run test",
                    "input": "",
                    "result": "",
                }
            ],
        )
        # add test run
        httpx_mock.add_response(
            status_code=201,
            json={
                "id": "test-run-id",
                "project_id": "",
                "mut_id": "",
                "scenario_set_id": "",
                "name": "CI run test",
            },
        )

    # generate scenario and return results in one call
    scenario_set_create = ScenarioSetCreate(
        name="my test scenario set",
        number_examples=1,
        seed_data=[
            SeedData(input_="example question or statement", result="example result")
        ],
    )
    response = okareo.create_scenario_set(scenario_set_create)
    scenario_id = response.scenario_id

    def call_model(input_: str) -> Tuple[str, dict]:
        actual = random.choice(["returns", "complains", "pricing"])
        # return a tuple of (actual, overall model response context)
        return actual, {"labels": actual, "confidence": 0.8}

    # this will return a model if it already exists or create a new one if it doesn't
    mut = okareo.register_model(name=mut_fixture["name"], tags=mut_fixture["tags"])

    # use the scenario id from one of the scenario set notebook examples
    test_run_item = mut.run_test(
        scenario_id=scenario_id, model_invoker=call_model, test_run_name="CI run test"
    )
    assert test_run_item.name == "CI run test"


def test_add_datapoint(httpx_mock: HTTPXMock) -> None:
    registered_model = helper_register_model(httpx_mock)
    fixture = {"id": "1", "project_id": "1", "mut_id": "1"}
    httpx_mock.add_response(status_code=201, json=fixture)
    dp = registered_model.add_data_point(
        input_obj={"input": "value"},
        result_obj={"result": "value"},
        feedback=0,
        context_token="SOME_CONTEXT_TOKEN",
        input_datetime=str(datetime.now()),
        result_datetime=str(datetime.now()),
        tags=["ci-testing"],
    )
    assert dp


def test_add_datapoint_only_context_and_feedback(httpx_mock: HTTPXMock) -> None:
    registered_model = helper_register_model(httpx_mock)
    fixture = {"id": "1", "project_id": "1", "mut_id": "1"}
    httpx_mock.add_response(status_code=201, json=fixture)
    dp = registered_model.add_data_point(
        feedback=0,
        context_token="SOME_CONTEXT_TOKEN",
    )
    assert dp


def test_get_test_run(httpx_mock: HTTPXMock) -> None:
    registered_model = helper_register_model(httpx_mock)

    # Mocking response for the get_test_run_v0_test_runs_test_run_id_get API call
    httpx_mock.add_response(
        status_code=201,
        json={
            "id": "test_id",
            "project_id": "project_id",
            "mut_id": "mut_id",
            "scenario_set_id": "scenario_set_id",
        },
    )

    result = registered_model.get_test_run("test_run_id")
    assert result


def test_validate_return_type(httpx_mock: HTTPXMock) -> None:
    registered_model = helper_register_model(httpx_mock)

    with pytest.raises(TypeError, match="Empty response from Okareo API"):
        registered_model.validate_return_type(None)

    with pytest.raises(TypeError):
        registered_model.validate_return_type(None)

    valid_response = TestRunItem(
        id="test_id",
        project_id="project_id",
        mut_id="mut_id",
        scenario_set_id="scenario_set_id",
    )  # Create a valid TestRunItem instance
    result = registered_model.validate_return_type(valid_response)
    assert result.id == "test_id"


def test_missing_api_key_test_run_modelv2(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(status_code=201, json=get_mut_fixture())
    okareo = Okareo("api-key", "http://mocked.com")
    mut = okareo.register_model(
        name="complex model test",
        model=[
            CohereModel(model_id="foo", model_type="embed"),
            PineconeDb(index_name="bar", region="baz", project_id="fooz"),
        ],
    )

    with pytest.raises(MissingApiKeyError):
        mut.run_test_v2(
            name="quick test",
            scenario=Mock(),
            calculate_metrics=True,
            test_run_type=TestRunType.INFORMATION_RETRIEVAL,
            api_keys={"cohere": "foo"},
        )


def test_missing_vector_db_key_test_run_modelv2(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(status_code=201, json=get_mut_fixture())
    okareo = Okareo("api-key", "http://mocked.com")
    mut = okareo.register_model(
        name="complex model test",
        model=[
            CohereModel(model_id="foo", model_type="embed"),
        ],
    )

    with pytest.raises(MissingVectorDbError):
        mut.run_test_v2(
            name="quick test",
            scenario=Mock(),
            calculate_metrics=True,
            test_run_type=TestRunType.INFORMATION_RETRIEVAL,
            api_keys={"cohere": "foo"},
        )
