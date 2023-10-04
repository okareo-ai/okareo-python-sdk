from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo.okareo_api_client.models.http_validation_error import HTTPValidationError


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
