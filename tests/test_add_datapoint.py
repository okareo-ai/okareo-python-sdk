from datetime import datetime

from pytest_httpx import HTTPXMock

from okareo import ModelUnderTest, Okareo


def helper_register_model(httpx_mock: HTTPXMock) -> ModelUnderTest:
    fixture = {
        "id": "1",
        "project_id": "1",
        "name": "NotebookModel",
        "tags": ["ci-testing"],
    }
    httpx_mock.add_response(status_code=201, json=fixture)
    okareo = Okareo("api-key")
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
