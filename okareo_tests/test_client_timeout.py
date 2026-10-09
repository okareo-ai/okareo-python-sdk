"""`Okareo(..., timeout=...)` reaches every request; without it there is no timeout."""

import socket
import time
from typing import Iterator

import httpx
import pytest
from pytest_httpx import HTTPXMock

from okareo import Okareo

GLOBAL_PROJECT_RESPONSE = [
    {
        "id": "0156f5d7-4ac4-4568-9d44-24750aa08d1a",
        "name": "Global",
        "onboarding_status": "onboarding_status",
        "tags": [],
        "additional_properties": {},
    }
]


@pytest.fixture
def silent_server() -> Iterator[str]:
    """The URL of a local server that accepts connections and never answers.

    It listens and never calls accept(): the kernel completes the handshake for a
    connection in the listen backlog, so the request goes out and no reply comes.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen(8)
    host, port = server.getsockname()
    try:
        yield f"http://{host}:{port}"
    finally:
        server.close()


def test_timeout_applies_to_the_constructors_own_request(silent_server: str) -> None:
    started = time.monotonic()

    with pytest.raises(httpx.TimeoutException):
        Okareo("foo", base_path=silent_server, timeout=0.5)

    assert time.monotonic() - started < 2.5


def test_timeout_is_set_on_the_client(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json=GLOBAL_PROJECT_RESPONSE, status_code=201)

    okareo = Okareo("foo", "http://mocked.com", timeout=12.5)

    assert okareo.client.get_httpx_client().timeout == httpx.Timeout(12.5)


def test_no_timeout_by_default(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json=GLOBAL_PROJECT_RESPONSE, status_code=201)

    okareo = Okareo("foo", "http://mocked.com")

    assert okareo.client.get_httpx_client().timeout == httpx.Timeout(None)
