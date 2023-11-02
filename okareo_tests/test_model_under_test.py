from datetime import datetime

import pytest
from pytest_httpx import HTTPXMock

from okareo import ModelUnderTest, Okareo
from okareo_api_client.models import TestRunItem
from okareo_api_client.models.http_validation_error import HTTPValidationError


def helper_register_model(httpx_mock: HTTPXMock) -> ModelUnderTest:
    fixture = {
        "id": "1",
        "project_id": "1",
        "name": "NotebookModel",
        "tags": ["ci-testing"],
    }
    httpx_mock.add_response(status_code=201, json=fixture)
    okareo = Okareo("api-key", "http://mocked.com")
    return okareo.register_model(name="NotebookModel", tags=["ci-testing"])


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
        registered_model.validate_return_type(HTTPValidationError())

    valid_response = TestRunItem(
        id="test_id",
        project_id="project_id",
        mut_id="mut_id",
        scenario_set_id="scenario_set_id",
    )  # Create a valid TestRunItem instance
    result = registered_model.validate_return_type(valid_response)
    assert result.id == "test_id"
