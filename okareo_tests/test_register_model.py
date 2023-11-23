from pytest_httpx import HTTPXMock

from okareo import Okareo


def test_register_model(httpx_mock: HTTPXMock) -> None:
    fixture = {
        "id": "1",
        "project_id": "1",
        "name": "NotebookModel",
        "tags": ["ci-testing"],
        "time_created": "foo",
    }
    httpx_mock.add_response(status_code=201, json=fixture)
    okareo = Okareo("api-key", "http://mocked.com")
    mut = okareo.register_model(name="NotebookModel", tags=["ci-testing"])
    assert mut
