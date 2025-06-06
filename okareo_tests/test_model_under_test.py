import os
from datetime import datetime
from typing import Optional
from unittest.mock import Mock

import pytest
from okareo_tests.common import API_KEY, OkareoAPIhost, integration, random_string
from pytest_httpx import HTTPXMock

from okareo import ModelUnderTest, Okareo
from okareo.error import TestRunError
from okareo.model_under_test import CohereModel, OpenAIModel, PineconeDb
from okareo_api_client.models import SeedData
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.test_run_type import TestRunType

GLOBAL_PROJECT_RESPONSE = [
    {
        "id": "0156f5d7-4ac4-4568-9d44-24750aa08d1a",
        "name": "Global",
        "onboarding_status": "onboarding_status",
        "tags": [],
        "additional_properties": {},
    }
]


def helper_register_model(httpx_mock: HTTPXMock) -> ModelUnderTest:
    httpx_mock.add_response(
        json=GLOBAL_PROJECT_RESPONSE,
        status_code=201,
    )
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
        httpx_mock.add_response(
            json=GLOBAL_PROJECT_RESPONSE,
            status_code=201,
        )
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
        httpx_mock.add_response(
            json=GLOBAL_PROJECT_RESPONSE,
            status_code=201,
        )
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

    if okareo_api.is_mock:
        httpx_mock.add_response(
            json=GLOBAL_PROJECT_RESPONSE,
            status_code=201,
        )
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
            status_code=201,
            json={
                "id": "test-run-item-id",
                "name": "CI run test",
                "input": "",
                "result": "",
                "project_id": "",
                "mut_id": "",
                "scenario_set_id": "",
            },
        )

    okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)

    # generate scenario and return results in one call
    scenario_set_create = ScenarioSetCreate(
        name=f"my test scenario set {random_string(10)}",
        seed_data=[
            SeedData(input_="example question or statement", result="example result")
        ],
    )
    response = okareo.create_scenario_set(scenario_set_create)
    response.scenario_id

    mut = okareo.register_model(
        name=mut_fixture["name"],
        tags=mut_fixture["tags"],
        model=OpenAIModel(
            model_id="gpt-4o-mini",
            temperature=1,
            system_prompt_template="system_prompt_template",
        ),
    )

    # use the scenario id from one of the scenario set notebook examples
    test_run_item = mut.run_test(
        scenario=response, name="CI run test", api_key=os.environ["OPENAI_API_KEY"]
    )
    assert test_run_item.name == "CI run test"


@integration
def test_mut_test_run_with_id(httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost) -> None:
    mut_fixture = get_mut_fixture()

    if okareo_api.is_mock:
        httpx_mock.add_response(
            json=GLOBAL_PROJECT_RESPONSE,
            status_code=201,
        )

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
            status_code=201,
            json={
                "id": "test-run-item-id",
                "name": "CI run test",
                "input": "",
                "result": "",
                "project_id": "",
                "mut_id": "",
                "scenario_set_id": "",
            },
        )

    okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)
    # generate scenario and return results in one call
    scenario_set_create = ScenarioSetCreate(
        name=f"my test scenario set {random_string(10)}",
        seed_data=[
            SeedData(input_="example question or statement", result="example result")
        ],
    )
    response = okareo.create_scenario_set(scenario_set_create)

    mut = okareo.register_model(
        name=mut_fixture["name"],
        tags=mut_fixture["tags"],
        model=OpenAIModel(
            model_id="gpt-4o-mini",
            temperature=1,
            system_prompt_template="system_prompt_template",
        ),
    )

    # use the scenario id from one of the scenario set notebook examples
    assert isinstance(response.scenario_id, str)
    test_run_item = mut.run_test(
        scenario=response.scenario_id,
        name="CI run test",
        api_key=os.environ["OPENAI_API_KEY"],
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


def test_missing_api_key_test_run_modelv2(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        json=GLOBAL_PROJECT_RESPONSE,
        status_code=201,
    )
    httpx_mock.add_response(status_code=201, json=get_mut_fixture())
    okareo = Okareo("api-key", "http://mocked.com")
    mut = okareo.register_model(
        name="complex model test",
        model=[
            CohereModel(model_id="foo", model_type="embed"),
            PineconeDb(index_name="bar", region="baz", project_id="fooz"),
        ],
    )

    with pytest.raises(TestRunError):
        mut.run_test(
            name="quick test",
            scenario=Mock(),
            calculate_metrics=True,
            test_run_type=TestRunType.INFORMATION_RETRIEVAL,
            api_keys={"cohere": "foo"},
        )


def test_missing_vector_db_key_test_run_modelv2(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        json=GLOBAL_PROJECT_RESPONSE,
        status_code=201,
    )
    httpx_mock.add_response(status_code=201, json=get_mut_fixture())
    okareo = Okareo("api-key", "http://mocked.com")
    mut = okareo.register_model(
        name="complex model test",
        model=[
            CohereModel(model_id="foo", model_type="embed"),
        ],
    )

    with pytest.raises(TestRunError):
        mut.run_test(
            name="quick test",
            scenario=Mock(),
            calculate_metrics=True,
            test_run_type=TestRunType.INFORMATION_RETRIEVAL,
            api_keys={"cohere": "foo"},
        )
