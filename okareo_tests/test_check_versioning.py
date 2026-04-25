"""Integration tests for check versioning (M8 backend).

All check-endpoint calls use raw httpx via okareo.client.get_httpx_client().
Existing Okareo SDK methods are used for run_test / find_test_data_points.
Tags are out of scope for this pass.
"""

from typing import Any, Union, cast
from uuid import UUID

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.checks import CheckOutputType, ModelBasedCheck
from okareo.model_under_test import CustomModel, ModelInvocation
from okareo_api_client.models.find_test_data_point_payload import (
    FindTestDataPointPayload,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_type import TestRunType


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(10)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


# ---- helpers ----------------------------------------------------------------


def _headers(okareo: Okareo) -> dict[str, str]:
    return {"api-key": okareo.api_key, "Content-Type": "application/json"}


def _create_check(
    okareo: Okareo,
    name: str,
    description: str = "test check",
    prompt_template: str = "Return True if the model_output has more than 3 words. Output: {model_output}",
    check_type: str = "pass_fail",
) -> dict[str, Any]:
    body = {
        "name": name,
        "description": description,
        "check_config": {
            "prompt_template": prompt_template,
            "type": check_type,
        },
    }
    resp = okareo.client.get_httpx_client().request(
        method="post",
        url="/v0/check_create_or_update",
        json=body,
        headers=_headers(okareo),
    )
    assert (
        resp.status_code == 200
    ), f"Create check failed {resp.status_code}: {resp.text}"
    return cast(dict[str, Any], resp.json())


def _get_check(okareo: Okareo, check_id: str) -> dict[str, Any]:
    resp = okareo.client.get_httpx_client().request(
        method="get",
        url=f"/v0/check/{check_id}",
        headers=_headers(okareo),
    )
    assert resp.status_code in (
        200,
        201,
    ), f"Get check failed {resp.status_code}: {resp.text}"
    return cast(dict[str, Any], resp.json())


def _get_all_checks(okareo: Okareo, all_versions: bool = False) -> list[dict[str, Any]]:
    url = "/v0/checks"
    if all_versions:
        url += "?all-versions=true"
    resp = okareo.client.get_httpx_client().request(
        method="get",
        url=url,
        headers=_headers(okareo),
    )
    assert resp.status_code in (
        200,
        201,
    ), f"Get all checks failed {resp.status_code}: {resp.text}"
    return cast(list[dict[str, Any]], resp.json())


def _delete_check(okareo: Okareo, check_id: str, check_name: str) -> None:
    resp = okareo.client.get_httpx_client().request(
        method="delete",
        url=f"/v0/check/{check_id}",
        data={"name": check_name},
        headers={"api-key": okareo.api_key},
    )
    assert (
        resp.status_code == 204
    ), f"Delete check failed {resp.status_code}: {resp.text}"


# ---- Group 1: Version fields on responses -----------------------------------


class TestVersionFieldsOnResponses:
    def test_create_check_returns_version_1(self, okareo: Okareo, rnd: str) -> None:
        name = f"ver-create-v1-{rnd}"
        check = _create_check(okareo, name)
        try:
            assert check["version"] == 1
        finally:
            _delete_check(okareo, check["id"], name)

    def test_get_check_includes_version(self, okareo: Okareo, rnd: str) -> None:
        name = f"ver-get-single-{rnd}"
        created = _create_check(okareo, name)
        try:
            fetched = _get_check(okareo, created["id"])
            assert "version" in fetched
            assert fetched["version"] == 1
        finally:
            _delete_check(okareo, created["id"], name)

    def test_get_all_checks_version_on_custom_check(
        self, okareo: Okareo, rnd: str
    ) -> None:
        name = f"ver-list-custom-{rnd}"
        created = _create_check(okareo, name)
        try:
            all_checks = _get_all_checks(okareo)
            match = [c for c in all_checks if c["id"] == created["id"]]
            assert (
                len(match) == 1
            ), f"Custom check not found in list by id={created['id']}"
            assert match[0]["version"] is not None
        finally:
            _delete_check(okareo, created["id"], name)


# ---- Group 2: Versioning behavior -------------------------------------------


class TestVersioningBehavior:
    def test_config_change_creates_new_version(self, okareo: Okareo, rnd: str) -> None:
        name = f"ver-bump-{rnd}"
        v1 = _create_check(okareo, name)
        v1_id = v1["id"]
        try:
            v2 = _create_check(
                okareo,
                name,
                prompt_template="Return True if model_output is valid JSON. Output: {model_output}",
            )
            assert v2["version"] == 2
            assert v2["id"] != v1_id
        finally:
            _delete_check(okareo, v1_id, name)

    def test_same_config_returns_existing_version(
        self, okareo: Okareo, rnd: str
    ) -> None:
        name = f"ver-no-bump-same-{rnd}"
        v1 = _create_check(okareo, name, prompt_template="Same prompt {model_output}")
        try:
            v1_again = _create_check(
                okareo, name, prompt_template="Same prompt {model_output}"
            )
            assert v1_again["id"] == v1["id"]
            assert v1_again["version"] == v1["version"]
        finally:
            _delete_check(okareo, v1["id"], name)

    def test_description_only_change_no_new_version(
        self, okareo: Okareo, rnd: str
    ) -> None:
        name = f"ver-desc-only-{rnd}"
        v1 = _create_check(okareo, name, description="original description")
        try:
            updated = _create_check(okareo, name, description="updated description")
            assert updated["id"] == v1["id"]
            assert updated["version"] == v1["version"]
        finally:
            _delete_check(okareo, v1["id"], name)


# ---- Group 3: Version history -----------------------------------------------


class TestVersionHistory:
    def test_get_all_checks_default_returns_latest_only(
        self, okareo: Okareo, rnd: str
    ) -> None:
        name = f"ver-hist-latest-{rnd}"
        v1 = _create_check(okareo, name)
        v1_id = v1["id"]
        v2 = _create_check(
            okareo,
            name,
            prompt_template="Different config for v2 {model_output}",
        )
        try:
            all_checks = _get_all_checks(okareo, all_versions=False)
            matches = [c for c in all_checks if c["name"] == name]
            assert (
                len(matches) == 1
            ), f"Expected 1 entry for '{name}', got {len(matches)}"
            assert matches[0]["id"] == v2["id"]
        finally:
            _delete_check(okareo, v1_id, name)

    def test_get_all_checks_all_versions_returns_history(
        self, okareo: Okareo, rnd: str
    ) -> None:
        name = f"ver-hist-all-{rnd}"
        v1 = _create_check(okareo, name)
        v1_id = v1["id"]
        _create_check(
            okareo,
            name,
            prompt_template="Different config for v2 history {model_output}",
        )
        try:
            all_checks = _get_all_checks(okareo, all_versions=True)
            matches = [c for c in all_checks if c["name"] == name]
            assert (
                len(matches) == 2
            ), f"Expected 2 entries for '{name}', got {len(matches)}"
            versions = {c["version"] for c in matches}
            assert versions == {1, 2}
        finally:
            _delete_check(okareo, v1_id, name)


# ---- Group 4: Delete archives all versions ----------------------------------


class TestDeleteArchivesAllVersions:
    def test_delete_archives_all_versions(self, okareo: Okareo, rnd: str) -> None:
        name = f"ver-del-all-{rnd}"
        v1 = _create_check(okareo, name)
        v1_id = v1["id"]
        _create_check(
            okareo,
            name,
            prompt_template="Different config for v2 delete {model_output}",
        )
        _delete_check(okareo, v1_id, name)

        all_checks = _get_all_checks(okareo, all_versions=True)
        matches = [c for c in all_checks if c["name"] == name]
        assert len(matches) == 0, f"Expected 0 entries after delete, got {len(matches)}"

    def test_deleted_check_name_reusable(self, okareo: Okareo, rnd: str) -> None:
        name = f"ver-del-reuse-{rnd}"
        original = _create_check(okareo, name)
        _delete_check(okareo, original["id"], name)

        reused = _create_check(
            okareo, name, prompt_template="Reused name check {model_output}"
        )
        try:
            assert reused["version"] == 1
            assert reused["id"] != original["id"]
        finally:
            _delete_check(okareo, reused["id"], name)


# ---- Group 5: UUID-based check selection in runs ----------------------------


@pytest.fixture(scope="module")
def versioning_scenario(rnd: str, okareo: Okareo) -> Any:
    return okareo.create_scenario_set(
        ScenarioSetCreate(
            name=f"check-ver-scenario-{rnd}",
            seed_data=[
                SeedData(
                    input_="The quick brown fox jumps over the lazy dog",
                    result="A fox jumps over a dog",
                ),
                SeedData(
                    input_="Python is a popular programming language",
                    result="Python is popular",
                ),
            ],
        )
    )


class TestUuidCheckSelection:
    def test_run_test_with_check_uuid(
        self, okareo: Okareo, rnd: str, versioning_scenario: Any
    ) -> None:
        check_name = f"ver-uuid-run-{rnd}"
        check = okareo.create_or_update_check(
            name=check_name,
            description="Check for UUID run test",
            check=ModelBasedCheck(
                prompt_template="Return True if the model_output is not empty. Output: {model_output}",
                check_type=CheckOutputType.PASS_FAIL,
            ),
        )
        try:
            mut = okareo.register_model(
                name=f"ver-uuid-model-{rnd}",
                model=_SimpleModel(name=f"ver-uuid-model-{rnd}"),
            )
            run = mut.run_test(
                name=f"ver-uuid-run-{rnd}",
                scenario=versioning_scenario,
                test_run_type=TestRunType.NL_GENERATION,
                checks=[str(check.id)],
            )
            assert run.id is not None

            tdps = okareo.find_test_data_points(
                FindTestDataPointPayload(test_run_id=run.id, full_data_point=True)
            )
            assert isinstance(tdps, list)
            assert len(tdps) > 0

            check_id_str = str(check.id)
            for tdp in tdps:
                cv_list = None
                if hasattr(tdp, "check_values") and tdp.check_values is not None:
                    cv_list = tdp.check_values
                elif hasattr(tdp, "additional_properties"):
                    cv_list = tdp.additional_properties.get("check_values")

                if cv_list is not None:
                    for cv in cv_list:
                        cv_data = cv if isinstance(cv, dict) else cv.to_dict()
                        if cv_data.get("name") == check_name:
                            assert (
                                cv_data["check_id"] == check_id_str
                            ), f"Expected check_id={check_id_str} but got {cv_data['check_id']}"
        finally:
            okareo.delete_check(cast(UUID, check.id), cast(str, check.name))

    def test_run_test_with_pinned_version(
        self, okareo: Okareo, rnd: str, versioning_scenario: Any
    ) -> None:
        check_name = f"ver-pinned-{rnd}"
        v1 = okareo.create_or_update_check(
            name=check_name,
            description="Pinned v1",
            check=ModelBasedCheck(
                prompt_template="Return True if model_output has more than 1 word. Output: {model_output}",
                check_type=CheckOutputType.PASS_FAIL,
            ),
        )
        v1_id = str(v1.id)

        okareo.create_or_update_check(
            name=check_name,
            description="Pinned v2",
            check=ModelBasedCheck(
                prompt_template="Return True if model_output is valid JSON. Output: {model_output}",
                check_type=CheckOutputType.PASS_FAIL,
            ),
        )
        try:
            mut = okareo.register_model(
                name=f"ver-pinned-model-{rnd}",
                model=_SimpleModel(name=f"ver-pinned-model-{rnd}"),
            )
            run = mut.run_test(
                name=f"ver-pinned-run-{rnd}",
                scenario=versioning_scenario,
                test_run_type=TestRunType.NL_GENERATION,
                checks=[v1_id],
            )

            tdps = okareo.find_test_data_points(
                FindTestDataPointPayload(test_run_id=run.id, full_data_point=True)
            )
            assert isinstance(tdps, list)
            assert len(tdps) > 0

            for tdp in tdps:
                check_values = None
                if hasattr(tdp, "check_values") and tdp.check_values is not None:
                    check_values = tdp.check_values
                elif hasattr(tdp, "additional_properties"):
                    check_values = tdp.additional_properties.get("check_values")

                if check_values is not None:
                    for cv in check_values:
                        cv_data = cv if isinstance(cv, dict) else cv.to_dict()
                        if cv_data.get("name") == check_name:
                            assert (
                                cv_data["check_id"] == v1_id
                            ), f"Expected check_id={v1_id} (v1) but got {cv_data['check_id']}"
        finally:
            okareo.delete_check(cast(UUID, v1.id), cast(str, v1.name))


# ---- internal model for Group 5 tests ---------------------------------------


class _SimpleModel(CustomModel):
    def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
        return ModelInvocation(
            model_prediction=f"Summary: {str(input_value)[:30]}",
            model_input=input_value,
        )
