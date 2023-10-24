import uuid
from urllib.parse import urlparse

import pytest
from okareo_tests.common import API_KEY, OkareoAPIhost, integration
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo.common import BASE_URL
from okareo_api_client.models.http_validation_error import HTTPValidationError
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.types import UNSET


@pytest.fixture
def non_mocked_hosts() -> list:
    return [urlparse(BASE_URL).hostname]


def test_can_instantiate() -> None:
    Okareo("api-key")


@integration
def test_returns_json(httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost) -> None:
    fixture = [{"hash": "ff64e2c", "time_created": "2023-09-28T08:47:29.637000+00:00"}]
    print("okareo_api", okareo_api)
    if okareo_api.is_mock:
        httpx_mock.add_response(json=fixture)

    print("DEBUG INFO", API_KEY, okareo_api.path)
    okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)
    generations = okareo.get_generations()
    assert generations
    assert not isinstance(generations, HTTPValidationError)
    if okareo_api.is_mock:
        assert [g.to_dict() for g in generations] == fixture
    else:
        assert len(generations) > 0


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
        httpx_mock.add_response(json=mock_response, status_code=201)

    okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)
    scenario_request = ScenarioSetCreate(
        name="test_scenario",
        seed_data=[],
        number_examples=10,
        project_id="project_id" if okareo_api.is_mock else UNSET,
    )
    scenario_response = okareo.create_scenario_set(scenario_request)

    if okareo_api.is_mock:
        assert scenario_response.scenario_id == "scenario_id"
    else:
        assert scenario_response.scenario_id
        uuid.UUID(scenario_response.scenario_id)
    assert scenario_response.name == "test_scenario"


@integration
def test_error_handling(httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost) -> None:
    # Mocking an error response
    if okareo_api.is_mock:
        httpx_mock.add_response(json={"detail": "Some error"}, status_code=400)

    okareo = Okareo("wrong-api-key", base_path=okareo_api.path)

    # Expecting the method to raise an exception
    if okareo_api.is_mock:
        with pytest.raises(Exception, match="Unexpected"):
            okareo.get_generations()
