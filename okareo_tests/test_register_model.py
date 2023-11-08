from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo.model_under_test import OpenAIModel


def test_register_model(httpx_mock: HTTPXMock) -> None:
    fixture = {
        "id": "1",
        "project_id": "1",
        "name": "NotebookModel",
        "tags": ["ci-testing"],
    }
    httpx_mock.add_response(status_code=201, json=fixture)
    okareo = Okareo("api-key", "http://mocked.com")
    mut = okareo.register_model(
        OpenAIModel(
            name="NotebookModel",
            model_id="",
            temperature=-1,
        ),
        tags=["ci-testing"],
    )
    assert mut
