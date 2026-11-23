import os
from typing import Iterator
from urllib.parse import urlparse

import pytest
from okareo_tests.common import API_KEY
from okareo_tests.live_artifacts import LiveArtifacts

from okareo.common import BASE_URL

LIVE_MARKER_HELP = (
    "live: calls a real Okareo backend; skipped when OKAREO_API_KEY is unset. "
    "Select the set with `-m live`, leave it out with `-m 'not live'`."
)


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", LIVE_MARKER_HELP)


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    if os.environ.get("OKAREO_API_KEY"):
        return
    skip = pytest.mark.skip(reason="live test: OKAREO_API_KEY is not set")
    for item in items:
        if item.get_closest_marker("live") is not None:
            item.add_marker(skip)


@pytest.fixture(scope="session")
def non_mocked_hosts() -> list:
    return [urlparse(BASE_URL).hostname]


@pytest.fixture
def created() -> Iterator[LiveArtifacts]:
    """What a live test made; deleted after the test, whether it passed or failed.

    A removal that fails is reported as its own error, beside the test's result.
    """
    artifacts = LiveArtifacts(api_key=API_KEY)
    yield artifacts
    failures = artifacts.remove_all()
    if failures:
        pytest.fail("Cleanup failed:\n" + "\n".join(failures))
