import pytest
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo_api_client.models.http_validation_error import HTTPValidationError
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate


def test_can_instantiate() -> None:
    Okareo("api-key")


def test_returns_json(httpx_mock: HTTPXMock) -> None:
    fixture = [{"hash": "ff64e2c", "time_created": "2023-09-28T08:47:29.637000+00:00"}]
    httpx_mock.add_response(json=fixture)
    okareo = Okareo("api-key")
    generations = okareo.get_generations()
    assert generations
    assert not isinstance(generations, HTTPValidationError)
    assert [g.to_dict() for g in generations] == fixture


def test_create_scenario_set(httpx_mock: HTTPXMock) -> None:
    # Mocking a successful response
    mock_response = {
        "scenario_id": "scenario_id",
        "name": "test_scenario",
        "project_id": "test_id",
        "type": "test_type",
        "time_created": "2023-10-20T13:51:57.334956",
        # ... any other fields ...
    }

    httpx_mock.add_response(json=mock_response, status_code=201)

    okareo = Okareo("api-key")
    scenario_request = ScenarioSetCreate(
        name="test_scenario", seed_data=[], number_examples=10, project_id="project_id"
    )
    scenario_response = okareo.create_scenario_set(scenario_request)

    assert scenario_response.scenario_id == "scenario_id"
    assert scenario_response.name == "test_scenario"


def test_error_handling(httpx_mock: HTTPXMock) -> None:
    # Mocking an error response
    httpx_mock.add_response(json={"detail": "Some error"}, status_code=400)

    okareo = Okareo("api-key")

    # Expecting the method to raise an exception
    with pytest.raises(Exception, match="Unexpected"):
        okareo.get_generations()
