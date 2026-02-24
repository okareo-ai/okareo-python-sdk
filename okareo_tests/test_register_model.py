import uuid

from pytest_httpx import HTTPXMock

from okareo import Okareo

MOCK_UUID_1 = str(uuid.uuid4())
MOCK_UUID_2 = str(uuid.uuid4())


def test_register_model(httpx_mock: HTTPXMock) -> None:
    fixture = {
        "id": MOCK_UUID_1,
        "project_id": MOCK_UUID_2,
        "version": 1,
        "name": "NotebookModel",
        "tags": ["ci-testing"],
        "time_created": "foo",
    }
    httpx_mock.add_response(
        json=[
            {
                "id": MOCK_UUID_1,
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
