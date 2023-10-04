from pytest_httpx import HTTPXMock

from okareo import Okareo


def test_can_instantiate() -> None:
    Okareo("api-key")


def test_returns_json(httpx_mock: HTTPXMock) -> None:
    fixture = [{"hash": "ff64e2c", "time_created": "2023-09-28T08:47:29.637000Z"}]
    httpx_mock.add_response(json=fixture)
    okareo = Okareo("api-key")
    generations = okareo.get_generations()
    assert generations == fixture
