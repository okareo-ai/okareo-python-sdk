from urllib.parse import urlparse

import pytest

from okareo.common import BASE_URL


@pytest.fixture(scope="session")
def non_mocked_hosts() -> list:
    return [urlparse(BASE_URL).hostname]
