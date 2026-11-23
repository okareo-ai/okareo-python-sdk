"""One live test per group of SDK client methods: the call works against a real Okareo backend and its
answer parses. Groups: Projects, Scenarios, Targets, Runs with their datapoints, and a Simulation with a
Driver and a custom multiturn Target.

These tests are part of the live set: every test marked `live`, which also covers the custom Target tests
in test_integration_model_under_test.py, the Check lookups in test_check_versioning.py and the audio helpers
in test_audio_file_upload.py. `pytest -m live` runs only that set, `pytest -m "not live"` leaves it out, and
it skips when OKAREO_API_KEY is unset. Each test deletes what it creates through the `created` fixture, uses
a unique name, and calls no LLM.
"""

from typing import Any, List, Optional, Union

import pytest
from okareo_tests.common import API_KEY, random_string
from okareo_tests.live_artifacts import LiveArtifacts

from okareo import Okareo
from okareo.model_under_test import (
    CustomModel,
    CustomMultiturnTarget,
    Driver,
    GenerationModel,
    ModelInvocation,
    Target,
)
from okareo_api_client.models.datapoint_search import DatapointSearch
from okareo_api_client.models.find_test_data_point_payload import (
    FindTestDataPointPayload,
)
from okareo_api_client.models.full_data_point_item import FullDataPointItem
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_type import TestRunType

# The SDK client does not bound a blocking Run, so each test carries its own limit.
pytestmark = [pytest.mark.live, pytest.mark.timeout(300)]


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


def unique_name(kind: str) -> str:
    return f"ci-live-{kind}-{random_string(8)}"


def test_projects_list_includes_the_default_project(okareo: Okareo) -> None:
    projects = okareo.get_projects()

    assert projects
    assert all(project.id and project.name for project in projects)
    assert "Global" in [project.name for project in projects]


def test_scenario_is_created_read_back_and_deleted(
    okareo: Okareo, created: LiveArtifacts
) -> None:
    name = unique_name("scenario")
    rows = [
        SeedData(input_="What time do you open?", result="9am"),
        SeedData(input_={"question": "Do you deliver?"}, result="yes"),
    ]

    scenario = okareo.create_scenario_set(ScenarioSetCreate(name=name, seed_data=rows))
    created.scenario(scenario.scenario_id, name)

    assert scenario.name == name
    read_back = okareo.get_scenario_data_points(str(scenario.scenario_id))
    assert [(row.input_, row.result) for row in read_back] == [
        (row.input_, row.result) for row in rows
    ]


def test_target_is_registered_read_back_and_deleted(
    okareo: Okareo, created: LiveArtifacts
) -> None:
    name = unique_name("target")

    # Registering a generation Target stores its config; no model is called.
    registered = okareo.register_model(
        name=name,
        model=GenerationModel(system_prompt_template=f"Summarize: {name}"),
        update=True,
    )
    created.target(registered.mut_id)

    assert registered.version == 1
    fetched = okareo.get_model(name)
    assert fetched.mut_id == registered.mut_id
    assert fetched.version == 1


class FirstWord(CustomModel):
    def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
        return ModelInvocation(
            model_prediction=str(input_value).split(" ")[0],
            model_input=input_value,
        )


def test_run_of_a_custom_model_stores_one_datapoint_per_row(
    okareo: Okareo, created: LiveArtifacts
) -> None:
    name = unique_name("run")
    scenario = okareo.create_scenario_set(
        ScenarioSetCreate(
            name=name,
            seed_data=[
                SeedData(input_="red apple", result="red"),
                SeedData(input_="green leaf", result="green"),
            ],
        )
    )
    created.scenario(scenario.scenario_id, name)
    target = okareo.register_model(name=name, model=FirstWord(name=name))
    created.target(target.mut_id)

    run = target.run_test(
        scenario=scenario,
        name=name,
        test_run_type=TestRunType.MULTI_CLASS_CLASSIFICATION,
        calculate_metrics=True,
    )
    created.run(run.id)

    assert run.status == "FINISHED"
    datapoints = okareo.find_datapoints(DatapointSearch(test_run_id=run.id))
    assert sorted((point.input_, point.result) for point in datapoints) == [
        ("green leaf", "green"),
        ("red apple", "red"),
    ]


class EchoTarget(CustomMultiturnTarget):
    def invoke(
        self,
        messages: List[dict[str, str]],
        scenario_input: Optional[Union[dict, list, str]] = None,
        session_id: Optional[str] = None,
    ) -> ModelInvocation:
        last = messages[-1]["content"] if messages else ""
        return ModelInvocation(f"echo: {last}", messages, {})


def test_simulation_reaches_a_custom_multiturn_target_in_the_test_process(
    okareo: Okareo, created: LiveArtifacts
) -> None:
    name = unique_name("simulation")
    scenario = okareo.create_scenario_set(
        ScenarioSetCreate(
            name=name,
            seed_data=[
                SeedData(
                    input_="Ask about opening hours.", result="The Target answers."
                )
            ],
        )
    )
    created.scenario(scenario.scenario_id, name)
    target = Target(name=name, target=EchoTarget(name=name))
    created.target(okareo.create_or_update_target(target).id)
    # With steps the Driver is scripted, so no Driver model runs.
    driver = Driver(
        name=name,
        steps=[
            {"message": "What time do you open?"},
            {"end_conversation": "Thanks, goodbye."},
        ],
    )
    created.driver(okareo.create_or_update_driver(driver).id)

    # run_simulation upserts the Target and the Driver by name, so it reuses the two registered above.
    run = okareo.run_simulation(
        name=name,
        scenario=scenario,
        target=target,
        driver=driver,
        max_turns=2,
        repeats=1,
        first_turn="driver",
        checks=["levenshtein_distance"],
    )
    created.run(run.id)

    assert run.status == "FINISHED"
    conversations = okareo.find_test_data_points(
        FindTestDataPointPayload(test_run_id=run.id, full_data_point=True)
    )
    assert len(conversations) == 1
    conversation = conversations[0]
    assert isinstance(conversation, FullDataPointItem)
    turns: Any = conversation.metric_value.additional_properties["generation_output"]
    assert "echo: What time do you open?" in [turn.get("content") for turn in turns]
