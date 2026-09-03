import random
from datetime import datetime
from typing import List, Union
from uuid import UUID

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.checks import CheckOutputType, ModelBasedCheck
from okareo.model_under_test import CustomModel, ModelInvocation
from okareo_api_client.api.default import (
    get_model_under_test_by_name_and_version_v0_models_under_test_name_version_get,
)
from okareo_api_client.models import SeedData
from okareo_api_client.models.model_under_test_response import ModelUnderTestResponse
from okareo_api_client.models.project_response import ProjectResponse
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.test_run_item import TestRunItem
from okareo_api_client.models.test_run_type import TestRunType
from okareo_api_client.types import Unset


@pytest.fixture(scope="module")
def rnd() -> str:
    return f'{random_string(5)} {datetime.now().strftime("%Y%m%d%H%M%S")}'


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


def scratch_project(okareo_client: Okareo, name: str) -> ProjectResponse:
    """A fixed scratch Project, created only the first time it is needed.

    Projects cannot be deleted and their names are unique per organization, so a
    test that mints a new Project every run both piles them up in the gate
    account (the condition `common.default_project_id` exists to work around)
    and, with a fixed name, fails with a 400 on its second run.
    """
    existing = next(
        (item for item in okareo_client.get_projects() if item.name == name), None
    )
    if existing:
        return existing
    return okareo_client.create_project(name=name)


@pytest.fixture(scope="module")
def project_a(okareo_client: Okareo) -> ProjectResponse:
    return scratch_project(okareo_client, "CI - cross-project A")


@pytest.fixture(scope="module")
def project_b(okareo_client: Okareo) -> ProjectResponse:
    return scratch_project(okareo_client, "CI - cross-project B")


def test_get_projects(okareo_client: Okareo) -> None:
    projects = okareo_client.get_projects()
    assert projects
    assert isinstance(projects, List)
    assert len(projects) > 0
    assert projects[0].id
    assert projects[0].name


def test_create_project(rnd: str, okareo_client: Okareo) -> None:
    # A fresh name every run: Project names are unique per organization and a
    # Project cannot be deleted, so a fixed name is a 400 on the second run.
    name = f"CI - Test P_Name {rnd}"
    project = okareo_client.create_project(name=name, tags=["testT1", "testT2"])
    assert project
    assert isinstance(project, ProjectResponse)
    assert project.id
    assert project.name == name
    assert project.tags == ["testT1", "testT2"]

    # keep the picker clean — archiving is the only cleanup a Project has
    okareo_client.archive_project(project.id)


def test_full_eval_cycle_in_new_project(rnd: str, okareo_client: Okareo) -> None:
    # use the same project to not overload the menu

    project = next(
        (
            item
            for item in okareo_client.get_projects()
            if item.name == "CI - test_full_eval_in_new_project"
        ),
        None,
    )

    if not project:
        project = okareo_client.create_project(
            name="CI - test_full_eval_in_new_project"
        )
        assert project.id

    scenario_set_create = ScenarioSetCreate(
        name=f"CI - test_full_eval_in_new_project {rnd}",
        seed_data=[
            SeedData(input_="sample input", result="returns"),
            SeedData(input_="sample input 2", result="pricing"),
        ],
        project_id=project.id,
    )
    response = okareo_client.create_scenario_set(scenario_set_create)

    assert response.project_id == project.id

    class ClassificationModel(CustomModel):
        def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
            prediction = random.choice(["returns", "complains", "pricing"])
            # return a tuple of (actual, overall model response context)
            return ModelInvocation(
                model_prediction=prediction,
                model_output_metadata={"labels": prediction, "confidence": 0.8},
            )

    mut = okareo_client.register_model(
        project_id=project.id,
        name=f"CI - from datetime import datetime {rnd}",
        model=ClassificationModel(name=f"CI - test_full_eval_in_new_project {rnd}"),
    )
    assert mut.mut_id
    assert mut.project_id == project.id

    # use the scenario id from one of the scenario set notebook examples
    assert response.scenario_id is not None
    assert not isinstance(response.scenario_id, Unset)
    test_run_item = mut.run_test(
        scenario=response.scenario_id,
        name=f"CI test_full_eval_in_new_project {rnd}",
        test_run_type=TestRunType.MULTI_CLASS_CLASSIFICATION,
        calculate_metrics=True,
    )

    assert_valid_test_run(
        test_run_item, project.id
    )  # test_run inherits project_id from model

    test_run_get = mut.get_test_run(
        test_run_item.id
    )  # validate roudtrip to retrieve test run

    assert_valid_test_run(test_run_get, project.id)


def assert_valid_test_run(
    test_run_item: TestRunItem, project_id: Union[str, UUID]
) -> None:
    assert test_run_item
    assert test_run_item.id
    assert test_run_item.model_metrics
    assert test_run_item.model_metrics.additional_properties.get("scores_by_label")
    assert test_run_item.project_id == project_id


# --- Cross-Project semantics (project separation, Phase 7) -------------------
#
# These run against a live backend and assert the isolation guarantees, so they
# are meaningful exactly where they run against the project-separation backend:
# the backend's post-deploy `sdk-test-latest` job. They reuse fixed scratch
# Projects (see `scratch_project`) rather than minting new ones per run.


def test_targets_visible_across_projects(
    rnd: str,
    okareo_client: Okareo,
    project_a: ProjectResponse,
) -> None:
    # Targets are org-shared, like Checks and Drivers: a Target registered in
    # one Project resolves by name from any other Project context. The Project
    # named at registration remains the family's home (it stamps where
    # scenario-less live traffic files), not a visibility boundary. This
    # replaces the old G7 isolation assertion, which pinned the pre-org-shared
    # model. Asserted via by-name resolution rather than the org list: the
    # gate account's Target corpus makes the unbounded list exceed Cloud Run's
    # 32 MB response cap (same failure mode the skipped
    # test_omitted_project_resolves_to_default documents for find_test_runs),
    # and by-name resolution is the flow SDK users actually exercise.
    target_name = f"CI iso target {rnd}"

    class EchoModel(CustomModel):
        def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
            return ModelInvocation(model_prediction=str(input_value))

    okareo_client.register_model(
        name=target_name,
        project_id=str(project_a.id),
        model=EchoModel(name=target_name),
    )

    # No Project context on the lookup: the server resolves from the default
    # Project — a different Project than the Target's home. A project-scoped
    # server 404s here; an org-shared one finds the family.
    response = get_model_under_test_by_name_and_version_v0_models_under_test_name_version_get.sync(
        name=target_name,
        version="latest",
        client=okareo_client.client,
        api_key=API_KEY,
    )
    assert isinstance(response, ModelUnderTestResponse)
    assert str(response.name) == target_name
    # The home stays where it was registered — resolution found it, not moved it.
    assert str(response.project_id) == str(project_a.id)


def test_shared_types_visible_from_any_project(
    rnd: str, okareo_client: Okareo, project_a: ProjectResponse
) -> None:
    check_name = f"ci_shared_check_{rnd}".lower()
    okareo_client.set_project(str(project_a.id))
    try:
        okareo_client.create_or_update_check(
            name=check_name,
            description="shared-type visibility check",
            check=ModelBasedCheck(
                prompt_template="Only output True, whatever {model_output} says.",
                check_type=CheckOutputType.PASS_FAIL,
            ),
        )
    finally:
        okareo_client.set_project(None)

    # visible with no Project context (default) — shared org-wide
    names = [c.name for c in okareo_client.get_all_checks()]
    assert check_name in names


@pytest.mark.skip(
    reason="find_test_runs() has no LIMIT, so listing the default Project returns "
    "every run the account has ever made. In the gate account that takes ~55s and "
    "then exceeds Cloud Run's 32 MB response cap, which surfaces as a bare 500. This "
    "assertion needs the unfiltered list — narrowing it would remove the thing under "
    "test — so re-enable once find_test_runs is bounded (limit or time window)."
)
def test_omitted_project_resolves_to_default(okareo_client: Okareo) -> None:
    # The compatibility guarantee: no client-level Project, no per-call value —
    # results are the DEFAULT Project's, not org-wide.
    default_id = next(
        str(p.id) for p in okareo_client.get_projects() if p.name == "Global"
    )
    runs = okareo_client.find_test_runs()
    assert all(r.get("project_id") == default_id for r in runs if r.get("project_id"))


def test_client_level_project_applies_and_per_call_overrides(
    okareo_client: Okareo, project_a: ProjectResponse, project_b: ProjectResponse
) -> None:
    # Both Projects are scratch Projects, deliberately: the per-call override only
    # needs *a different* Project than the client-level one, and reaching for the
    # default Project here would list every run the account has ever made.
    okareo_client.set_project(str(project_a.id))
    try:
        runs_client_level = okareo_client.find_test_runs()
        assert all(
            r.get("project_id") == str(project_a.id)
            for r in runs_client_level
            if r.get("project_id")
        )
        runs_override = okareo_client.find_test_runs(project_id=str(project_b.id))
        assert all(
            r.get("project_id") == str(project_b.id)
            for r in runs_override
            if r.get("project_id")
        )
    finally:
        okareo_client.set_project(None)


def test_archive_round_trip(okareo_client: Okareo) -> None:
    # Works against any backend with Phase 4 deployed; independent of scoping.
    # Its own scratch Project, since it leaves the Project archived.
    project = scratch_project(okareo_client, "CI - archive round trip")

    archived = okareo_client.archive_project(project.id)
    assert archived.additional_properties.get("is_archived") is True

    unarchived = okareo_client.unarchive_project(project.id)
    assert unarchived.additional_properties.get("is_archived") is False

    okareo_client.archive_project(project.id)  # leave the scratch project archived
