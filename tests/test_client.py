from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo_api_client.api_config import HTTPException


def test_can_instantiate() -> None:
    Okareo("api-key")


def test_returns_json(httpx_mock: HTTPXMock) -> None:
    fixture = [{"hash": "ff64e2c", "time_created": "2023-09-28T08:47:29.637000+00:00"}]
    httpx_mock.add_response(json=fixture)
    okareo = Okareo("api-key")
    generations = okareo.get_generations()
    assert generations
    assert not isinstance(generations, HTTPException)
    assert [g.dict() for g in generations] == fixture
