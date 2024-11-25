import random
from datetime import datetime
from typing import List, Union

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import CustomModel, ModelInvocation
from okareo_api_client.models import SeedData
from okareo_api_client.models.project_response import ProjectResponse
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.test_run_item import TestRunItem
from okareo_api_client.models.test_run_type import TestRunType


@pytest.fixture(scope="module")
def rnd() -> str:
    return f'{random_string(5)} {datetime.now().strftime("%Y%m%d%H%M%S")}'


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


def test_create_project(okareo_client: Okareo) -> None:
    project = okareo_client.create_project(
        name="CI - Test P_Name", tags=["testT1", "testT2"]
    )
    assert project
    assert isinstance(project, ProjectResponse)
    assert project.id
    assert project.name == "CI - Test P_Name"
    assert project.tags == ["testT1", "testT2"]


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
    assert isinstance(response.scenario_id, str)
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


def assert_valid_test_run(test_run_item: TestRunItem, project_id: str) -> None:
    assert test_run_item
    assert test_run_item.id
    assert test_run_item.model_metrics
    assert test_run_item.model_metrics.additional_properties.get("scores_by_label")
    assert test_run_item.project_id == project_id
