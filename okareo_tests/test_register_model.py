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
    httpx_mock.add_response(status_code=201, json=fixture)
    okareo = Okareo("api-key", "http://mocked.com")
    mut = okareo.register_model(name="NotebookModel", tags=["ci-testing"])
    assert mut
