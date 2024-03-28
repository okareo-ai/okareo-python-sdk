from typing import List

import pytest
from okareo_tests.common import API_KEY

from okareo import Okareo


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


def test_get_projects(okareo_client: Okareo) -> None:
    projects = okareo_client.get_projects()
    assert projects
    assert isinstance(projects, List)
    assert len(projects) > 0
    assert projects[0].id
    assert projects[0].name
