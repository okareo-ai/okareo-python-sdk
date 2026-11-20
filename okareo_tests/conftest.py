from importlib.metadata import PackageNotFoundError, version
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import pytest

from okareo.common import BASE_URL

LIVE_HOST = urlparse(BASE_URL).hostname


def _pytest_httpx_version() -> Tuple[int, int]:
    try:
        major, minor = version("pytest-httpx").split(".")[:2]
        return int(major), int(minor)
    except (PackageNotFoundError, ValueError):
        return (0, 0)


def _httpx_mock_options(installed: Tuple[int, int]) -> Optional[Dict[str, Any]]:
    """Marker options that keep ``httpx_mock`` behaving the way these tests expect.

    The tests register one response and let it answer several requests, make
    requests nothing was registered for, and send requests for the Okareo API
    to the real server. pytest-httpx 0.30 does all of that by default (with
    the ``non_mocked_hosts`` fixture below). Later releases turned each one
    into an option of the ``httpx_mock`` marker:

    - 0.31: unexpected requests fail the test unless
      ``assert_all_requests_were_expected`` is off, and ``non_mocked_hosts``
      is a marker option instead of a fixture;
    - 0.32: a response answers one request unless
      ``can_send_already_matched_responses`` is on;
    - 0.33: ``should_mock`` replaces ``non_mocked_hosts``.
    """
    if installed < (0, 31):
        return None
    options: Dict[str, Any] = {"assert_all_requests_were_expected": False}
    if installed >= (0, 32):
        options["can_send_already_matched_responses"] = True
    if installed >= (0, 33):
        options["should_mock"] = lambda request: request.url.host != LIVE_HOST
    else:
        options["non_mocked_hosts"] = [LIVE_HOST]
    return options


@pytest.fixture(scope="session")
def non_mocked_hosts() -> list:
    # Read by pytest-httpx 0.30 and earlier; later releases ignore it.
    return [LIVE_HOST]


def pytest_collection_modifyitems(items: List[pytest.Item]) -> None:
    options = _httpx_mock_options(_pytest_httpx_version())
    if options is None:
        return
    for item in items:
        if "httpx_mock" not in getattr(item, "fixturenames", ()):
            continue
        if item.get_closest_marker("httpx_mock") is not None:
            # The test sets its own options.
            continue
        item.add_marker(pytest.mark.httpx_mock(**options))
