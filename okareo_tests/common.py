import os
import random
import string
from typing import Any, Callable

import pytest

from okareo.common import BASE_URL

API_KEY = os.environ.get("OKAREO_API_KEY", "no-api-key")
PROXY_URL = os.environ.get("PROXY_URL", "http://host.docker.internal:4000")


class OkareoAPIhost:
    def __init__(self, path: str, is_mock: bool) -> None:
        self.path = path
        self.is_mock = is_mock


def integration(func: Callable) -> Any:
    params = [
        OkareoAPIhost("http://mocked.com", True),
        OkareoAPIhost(BASE_URL, False),  # type: ignore
    ]
    return pytest.mark.parametrize("okareo_api", params)(func)


def random_string(length: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


# if unavailable, mock a valid OpenAI API kley
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", f"sk-{random_string(48)}")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


def default_project_id(okareo_client: Any) -> str:
    """The default ("Global") Project's id, selected BY NAME.

    `GET /v0/projects` has no ORDER BY, so `get_projects()[0]` is arbitrary — and the
    gate account accumulates Projects, so [0] is routinely not the default. Fails
    loudly rather than falling back to [0]: a missing Global Project means default
    resolution is broken org-wide and every downstream assertion would mislead.
    """
    projects = okareo_client.get_projects()
    for project in projects:
        if project.name == "Global":
            return str(project.id)
    raise AssertionError(
        "No Project named 'Global' found — default-Project resolution is broken "
        f"for this account. Projects: {[p.name for p in projects]}"
    )
