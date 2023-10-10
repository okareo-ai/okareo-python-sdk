from datetime import datetime

from pytest_httpx import HTTPXMock

from okareo import Okareo


def test_add_datapoint(httpx_mock: HTTPXMock) -> None:
    fixture = {"id": "1", "project_id": "1", "mut_id": "1"}
    httpx_mock.add_response(status_code=201, json=fixture)
    okareo = Okareo("api-key")
    dp = okareo.add_data_point(
        mut_id=1,
        project_id=1,
        input_obj={"input": "value"},
        result_obj={"result": "value"},
        feedback=0,
        context_token="SOME_CONTEXT_TOKEN",
        input_datetime=str(datetime.now()),
        result_datetime=str(datetime.now()),
        tags=["ci-testing"],
    )
    assert dp
