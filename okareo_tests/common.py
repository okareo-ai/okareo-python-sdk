import os
from typing import Any, Callable

import pytest

from okareo.common import BASE_URL

API_KEY = os.environ.get("API_KEY", "no-api-key")


class OkareoAPIhost:
    def __init__(self, path: str, is_mock: bool) -> None:
        self.path = path
        self.is_mock = is_mock


def integration(func: Callable) -> Any:
    params = [
        OkareoAPIhost("http://mocked.com", True),
        OkareoAPIhost(BASE_URL, False),
    ]
    return pytest.mark.parametrize("okareo_api", params)(func)
