"""Live tests of the SDK's lookup of a Check by name and version (`get_check`).

Each test uses a unique randomized name and deletes the Checks it creates. Marked `live`: they call a real
Okareo backend and skip when OKAREO_API_KEY is unset.
"""

from typing import Any, Optional, cast
from uuid import UUID

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.checks import CheckOutputType, ModelBasedCheck

pytestmark = pytest.mark.live


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(10)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


# ---- helpers ----------------------------------------------------------------


def _sdk_check(
    okareo: Okareo,
    name: str,
    prompt_template: str = "Return True if the model_output has more than 3 words. Output: {model_output}",
    description: str = "test check",
    tags: Optional[list[str]] = None,
) -> Any:
    """Create a check via the SDK and return the EvaluatorDetailedResponse."""
    kwargs: dict[str, Any] = {
        "name": name,
        "description": description,
        "check": ModelBasedCheck(
            prompt_template=prompt_template,
            check_type=CheckOutputType.PASS_FAIL,
        ),
    }
    if tags is not None:
        kwargs["tags"] = tags
    return okareo.create_or_update_check(**kwargs)


# ---- get_check by name / version --------------------------------------------


class TestSDKGetCheckByName:
    def test_get_check_by_name_returns_latest(self, okareo: Okareo, rnd: str) -> None:
        name = f"sdk-getchk-latest-{rnd}"
        v1 = _sdk_check(okareo, name)
        v1_id = str(v1.id)
        v2 = _sdk_check(
            okareo,
            name,
            prompt_template="SDK get_check latest v2 {model_output}",
        )
        try:
            fetched = okareo.get_check(name)
            assert str(fetched.id) == str(v2.id)
            assert fetched.version == 2
        finally:
            okareo.delete_check(UUID(v1_id), name)

    def test_get_check_by_name_and_version(self, okareo: Okareo, rnd: str) -> None:
        name = f"sdk-getchk-pinned-{rnd}"
        v1 = _sdk_check(okareo, name)
        v1_id = str(v1.id)
        _sdk_check(
            okareo,
            name,
            prompt_template="SDK get_check pinned v2 {model_output}",
        )
        try:
            fetched = okareo.get_check(name, version=1)
            assert str(fetched.id) == v1_id
            assert fetched.version == 1
        finally:
            okareo.delete_check(UUID(v1_id), name)

    def test_get_check_by_name_with_latest_string(
        self, okareo: Okareo, rnd: str
    ) -> None:
        name = f"sdk-getchk-latest-str-{rnd}"
        v1 = _sdk_check(okareo, name)
        v1_id = str(v1.id)
        v2 = _sdk_check(
            okareo,
            name,
            prompt_template="SDK get_check latest string v2 {model_output}",
        )
        try:
            fetched = okareo.get_check(name, version="latest")
            assert str(fetched.id) == str(v2.id)
            assert fetched.version == 2
        finally:
            okareo.delete_check(UUID(v1_id), name)

    def test_get_check_by_name_not_found(self, okareo: Okareo, rnd: str) -> None:
        with pytest.raises(ValueError, match="No check found"):
            okareo.get_check(f"nonexistent-check-{rnd}")

    def test_get_check_by_name_version_not_found(
        self, okareo: Okareo, rnd: str
    ) -> None:
        name = f"sdk-getchk-badver-{rnd}"
        created = _sdk_check(okareo, name)
        try:
            with pytest.raises(ValueError, match="version 99"):
                okareo.get_check(name, version=99)
        finally:
            okareo.delete_check(cast(UUID, created.id), name)
