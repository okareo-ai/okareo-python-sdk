import os
import uuid
from datetime import datetime

import pytest
from okareo_tests.common import API_KEY, OkareoAPIhost, integration
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.scenario_set_generate import ScenarioSetGenerate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.types import UNSET


def test_can_instantiate() -> None:
    Okareo(API_KEY)


@pytest.fixture
def okareo_client(httpx_mock: HTTPXMock) -> Okareo:
    httpx_mock.add_response(
        json=[
            {
                "id": "0156f5d7-4ac4-4568-9d44-24750aa08d1a",
                "name": "Global",
                "onboarding_status": "onboarding_status",
                "tags": [],
                "additional_properties": {},
            }
        ],
        status_code=201,
    )
    return Okareo("foo", "http://mocked.com")


@integration
def test_create_scenario_set(httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost) -> None:
    # Mocking a successful response
    mock_response = {
        "scenario_id": "scenario_id",
        "name": "test_scenario",
        "project_id": "test_id",
        "type": "test_type",
        "time_created": "2023-10-20T13:51:57.334956",
        # ... any other fields ...
    }

    if okareo_api.is_mock:
        httpx_mock.add_response(
            json=[
                {
                    "id": "0156f5d7-4ac4-4568-9d44-24750aa08d1a",
                    "name": "Global",
                    "onboarding_status": "onboarding_status",
                    "tags": [],
                    "additional_properties": {},
                }
            ],
            status_code=201,
        )
        httpx_mock.add_response(json=mock_response, status_code=201)

    okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)
    scenario_request = ScenarioSetCreate(
        name="test_scenario",
        seed_data=[SeedData(input_="foo", result="bar")],
        project_id="project_id" if okareo_api.is_mock else UNSET,
    )
    scenario_response = okareo.create_scenario_set(scenario_request)

    if okareo_api.is_mock:
        assert scenario_response.scenario_id == "scenario_id"
    else:
        assert scenario_response.scenario_id
        uuid.UUID(scenario_response.scenario_id)
    assert scenario_response.name == "test_scenario"


def test_register_model_raises_on_validation_error(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(json={"wrong": "response format"}, status_code=200)
    with pytest.raises(Exception, match="Unexpected status code"):
        okareo_client.register_model("this should fail", project_id="42")


def test_register_model_raises_on_empty_response(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(status_code=422)
    with pytest.raises(Exception, match="Expecting value"):
        okareo_client.register_model("this should fail", project_id="42")


def test_create_scenario_set_raises_on_validation_error(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(json={"wrong": "response format"}, status_code=200)

    seed_data = [
        SeedData(input_="are you able to set up in aws?", result="capabilities"),
    ]
    scenario_set_create = ScenarioSetCreate(
        name="my test scenario set x",
        seed_data=seed_data,
    )
    with pytest.raises(Exception, match="Unexpected"):
        okareo_client.create_scenario_set(create_request=scenario_set_create)


def test_upload_scenario_set(okareo_client: Okareo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        json={
            "scenario_id": "created-id",
            "project_id": "new-project-id",
            "time_created": datetime.now().isoformat(),
            "type": "seed",
        },
        status_code=200,
    )
    okareo_client.upload_scenario_set(
        scenario_name="my-test-scenario-1",
        file_path=os.path.join(os.path.dirname(__file__), "webbizz_class_seed.jsonl"),
    )


def test_generate_scenario_set(okareo_client: Okareo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        json={
            "scenario_id": "created-id",
            "project_id": "new-project-id",
            "time_created": datetime.now().isoformat(),
            "type": "seed",
        },
        status_code=201,
    )

    okareo_client.generate_scenario_set(
        ScenarioSetGenerate(
            source_scenario_id="just-a-random-scenario-id",
            name="my generation foo",
            number_examples=22,
        )
    )


def test_get_scenario_data_points(okareo_client: Okareo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json={}, status_code=200)
    okareo_client.get_scenario_data_points(scenario_id="scenario-id")


def test_get_all_checks(okareo_client: Okareo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json={}, status_code=201)
    okareo_client.get_all_checks()
