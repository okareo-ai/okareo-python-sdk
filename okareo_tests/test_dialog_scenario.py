import os
from datetime import datetime

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import GenerationModel
from okareo_api_client.models import ScenarioSetResponse, TestRunType
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.test_run_item_model_metrics import TestRunItemModelMetrics

today_with_time = datetime.now().strftime("%m-%d %H:%M:%S")
rnd_str = random_string(5)
unique_key = f"{rnd_str} {today_with_time}"
create_scenario_name = f"ci_test_dialog_scenarios {unique_key}"


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


def validate_scenario_set(
    scenario_set_validated: ScenarioSetResponse, name: str, okareo_client: Okareo
) -> None:
    assert scenario_set_validated is not None
    assert scenario_set_validated.name == name
    assert scenario_set_validated.scenario_id
    assert scenario_set_validated.project_id
    assert scenario_set_validated.time_created

    scenario_dps = okareo_client.get_scenario_data_points(
        scenario_set_validated.scenario_id
    )
    assert scenario_dps
    assert len(scenario_dps) == 1
    for dp in scenario_dps:
        input_ = dp.to_dict()["input"]
        assert input_
        assert input_[0]["role"] == "system"
        assert input_[1]["role"] == "user"
        assert input_[2]["role"] == "assistant"
        assert input_[3]["role"] == "function"


JSON_DAILOG = Okareo.seed_data_from_list(
    [
        {
            "input": [
                {"role": "system", "content": "You are super genious mind reader!"},
                {
                    "role": "user",
                    "content": (
                        "I want to know the temperature in location i'm thinking of ... "
                        + "figure out the location and temperature!"
                    ),
                },
                {"role": "assistant", "content": "I can help you with that!"},
                {
                    "role": "function",
                    "name": "get_temp",
                    "content": "Error from server (NotFound)",
                },
            ],
            "result": {"role": "assistant", "content": "Oops!"},
        },
    ]
)


@pytest.fixture(scope="module")
def create_scenario_set(okareo_client: Okareo) -> ScenarioSetResponse:
    scenario_set_create = ScenarioSetCreate(
        name=create_scenario_name,
        seed_data=JSON_DAILOG,
    )
    scenario = okareo_client.create_scenario_set(scenario_set_create)
    return scenario


def test_create_scenario_set(
    okareo_client: Okareo, create_scenario_set: ScenarioSetResponse
) -> None:
    validate_scenario_set(create_scenario_set, create_scenario_name, okareo_client)


def test_dialog_input(
    okareo_client: Okareo, create_scenario_set: ScenarioSetResponse
) -> None:
    test_run_name = f"ci_test_dialog_scenarios_openai {unique_key}"

    mut = okareo_client.register_model(
        name=test_run_name,
        model=GenerationModel(
            model_id="gpt-4.1-mini",
            temperature=0,
            dialog_template="{scenario_input}",
        ),
    )

    run_resp = mut.run_test(
        name=test_run_name,
        scenario=create_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        checks=["compression_ratio", "levenshtein_distance"],
    )
    assert run_resp.name == test_run_name
    assert isinstance(run_resp.model_metrics, TestRunItemModelMetrics)
    metrics_dict = run_resp.model_metrics.to_dict()
    assert metrics_dict["mean_scores"] is not None
    assert metrics_dict["scores_by_row"] is not None


DAILOG_TEMPLATE = """
[
    {
        "role": "{scenario_input.0.role}",
        "content": "{scenario_input.0.content}"
    },
    {
        "role": "{scenario_input.2.role}",
        "content": "{scenario_input.2.content}"
    }
]
"""


def test_dialog_template(
    okareo_client: Okareo, create_scenario_set: ScenarioSetResponse
) -> None:
    test_run_name = f"ci_test_dialog_template_openai {unique_key}"

    mut = okareo_client.register_model(
        name=test_run_name,
        model=GenerationModel(
            model_id="gpt-4.1-mini",
            temperature=0,
            dialog_template=DAILOG_TEMPLATE,
        ),
    )

    run_resp = mut.run_test(
        name=test_run_name,
        scenario=create_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        checks=["compression_ratio", "levenshtein_distance"],
    )
    assert run_resp.name == test_run_name
    assert isinstance(run_resp.model_metrics, TestRunItemModelMetrics)
    metrics_dict = run_resp.model_metrics.to_dict()
    assert metrics_dict["mean_scores"] is not None
    assert metrics_dict["scores_by_row"] is not None
