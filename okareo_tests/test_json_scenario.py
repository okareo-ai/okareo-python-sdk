import json
import os
from datetime import datetime
from typing import Union

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import (
    CohereModel,
    CustomModel,
    GenerationModel,
    ModelInvocation,
)
from okareo_api_client.models import ScenarioSetResponse, ScenarioType, TestRunType
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.test_run_item_model_metrics import TestRunItemModelMetrics

today_with_time = datetime.now().strftime("%m-%d %H:%M:%S")
rnd_str = random_string(5)
unique_key = f"{rnd_str} {today_with_time}"
upload_scenario_name = f"ci_json_test_upload_scenario_set {unique_key}"
create_scenario_name = f"ci_json_test_create_scenarios {unique_key}"
generate_scenario_name = f"ci_json_test_generate_scenarios {unique_key}"


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    print(API_KEY)
    return Okareo(api_key=API_KEY)


@pytest.fixture(scope="module")
def uploaded_scenario_set(okareo_client: Okareo) -> ScenarioSetResponse:
    file_path = os.path.join(os.path.dirname(__file__), "json_scenario.jsonl")
    scenario: ScenarioSetResponse = okareo_client.upload_scenario_set(
        file_path=file_path, scenario_name=upload_scenario_name
    )

    return scenario


def validate_scenario_set(
    uploaded_scenario_set: ScenarioSetResponse, name: str, okareo_client: Okareo
) -> None:
    assert uploaded_scenario_set is not None
    assert uploaded_scenario_set.name == name
    assert uploaded_scenario_set.scenario_id
    assert uploaded_scenario_set.project_id
    assert uploaded_scenario_set.time_created

    scenario_dps = okareo_client.get_scenario_data_points(
        uploaded_scenario_set.scenario_id
    )
    assert scenario_dps
    assert len(scenario_dps) == 3
    for dp in scenario_dps:
        input_ = dp.to_dict()["input"]
        assert input_
        assert input_["query"]
        assert input_["meta"]
        assert input_["user_id"]


def test_upload_scenario_set(
    uploaded_scenario_set: ScenarioSetResponse, okareo_client: Okareo
) -> None:
    validate_scenario_set(uploaded_scenario_set, upload_scenario_name, okareo_client)


JSON_SEED = Okareo.seed_data_from_list(
    [
        {
            "input": {"query": "user q 1", "user_id": "1", "meta": "meta1"},
            "result": ["red"],
        },
        {
            "input": {"query": "user q 2", "user_id": "2", "meta": "meta1"},
            "result": ["blue"],
        },
        {
            "input": {"query": "user q 3", "user_id": "3", "meta": "meta1"},
            "result": ["green"],
        },
    ]
)


def test_create_scenario_set(okareo_client: Okareo) -> None:
    scenario_set_create = ScenarioSetCreate(
        name=create_scenario_name,
        seed_data=JSON_SEED,
    )
    scenario = okareo_client.create_scenario_set(scenario_set_create)
    validate_scenario_set(scenario, create_scenario_name, okareo_client)


def test_download_scenario_set(
    uploaded_scenario_set: ScenarioSetResponse, okareo_client: Okareo
) -> None:
    response_file = okareo_client.download_scenario_set(
        uploaded_scenario_set, upload_scenario_name
    )
    with open(response_file.name) as scenario_file:
        for line in scenario_file:
            assert json.loads(line)["input"]["query"] != ""
            assert json.loads(line)["input"]["user_id"] != ""
            assert json.loads(line)["input"]["meta"] != ""
            assert json.loads(line)["result"] != ""
    os.remove(upload_scenario_name)


@pytest.fixture(scope="module")
def generate_scenarios(
    okareo_client: Okareo, uploaded_scenario_set: ScenarioSetResponse
) -> ScenarioSetResponse:
    assert isinstance(uploaded_scenario_set.scenario_id, str)
    questions: ScenarioSetResponse = okareo_client.generate_scenarios(
        source_scenario=uploaded_scenario_set.scenario_id,
        name=generate_scenario_name,
        number_examples=2,
        generation_type=ScenarioType.REPHRASE_INVARIANT,
    )
    return questions


# todo fix this
def not_test_generate_scenarios(generate_scenarios: ScenarioSetResponse) -> None:
    assert generate_scenarios is not None
    assert generate_scenarios.name == generate_scenario_name
    assert generate_scenarios.scenario_id
    assert generate_scenarios.project_id
    assert generate_scenarios.time_created


JSON_CLASSIFICATION = Okareo.seed_data_from_list(
    [
        {
            "input": {"query": "user q 1", "user_id": "1", "meta": "meta1"},
            "result": "red",  # result has to be a single label (not a list)
        },
        {
            "input": {"query": "user q 2", "user_id": "2", "meta": "meta2"},
            "result": "blue",
        },
        {
            "input": {"query": "user q 3", "user_id": "3", "meta": "meta3"},
            "result": "green",
        },
    ]
)


def test_classification_cohere(okareo_client: Okareo) -> None:
    test_run_name = f"ci_json_test_classification_cohere {today_with_time}"

    scenario_set_create = ScenarioSetCreate(
        name=test_run_name,
        seed_data=JSON_CLASSIFICATION,
    )
    scenario = okareo_client.create_scenario_set(scenario_set_create)
    validate_scenario_set(scenario, test_run_name, okareo_client)

    mut = okareo_client.register_model(
        name=test_run_name,
        model=CohereModel(
            model_id="e2b2964d-d741-41e5-a3b7-b363202be88c-ft",
            model_type="classify",
        ),
    )

    run_resp = mut.run_test(
        name=test_run_name,
        scenario=scenario,
        api_key=os.environ["COHERE_API_KEY"],
        test_run_type=TestRunType.MULTI_CLASS_CLASSIFICATION,
        calculate_metrics=True,
    )
    assert run_resp.name == test_run_name


def test_classification_openai(okareo_client: Okareo) -> None:
    test_run_name = f"ci_json_test_classification_openai {today_with_time}"

    scenario_set_create = ScenarioSetCreate(
        name=test_run_name,
        seed_data=JSON_CLASSIFICATION,
    )
    scenario = okareo_client.create_scenario_set(scenario_set_create)
    validate_scenario_set(scenario, test_run_name, okareo_client)

    mut = okareo_client.register_model(
        name=test_run_name,
        model=GenerationModel(
            model_id="gpt-4.1-mini",
            temperature=0,
            system_prompt_template="Classify this by label equal to one of (red,blue,green): {scenario_input} label:\n",
            user_prompt_template=None,
        ),
    )

    run_resp = mut.run_test(
        name=test_run_name,
        scenario=scenario,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.MULTI_CLASS_CLASSIFICATION,
        calculate_metrics=True,
    )
    assert run_resp.name == test_run_name


def test_custom_retrieval(
    okareo_client: Okareo, uploaded_scenario_set: ScenarioSetResponse
) -> None:
    class RetrievalModel(CustomModel):
        def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
            assert isinstance(input_value, dict)
            assert input_value["query"]
            assert input_value["meta"]
            assert input_value["user_id"]

            return ModelInvocation(
                model_prediction=[
                    {
                        "id": "red",
                        "score": 1,
                        "label": "red",
                        "metadata": input_value["meta"],
                    }
                ],
                model_output_metadata={"meta": input_value["meta"]},
            )

    model_under_test = okareo_client.register_model(
        name=f"ci_json_vectordb_retrieval test {rnd_str}",
        model=RetrievalModel(name="ci_custom_retrieval_json"),
    )

    test_run_name = f"ci_json_test_custom_retrieval {today_with_time}"

    retrieval_test_run = model_under_test.run_test(
        scenario=uploaded_scenario_set,
        name=test_run_name,
        test_run_type=TestRunType.INFORMATION_RETRIEVAL,
        calculate_metrics=True,
    )

    assert retrieval_test_run.id
    assert retrieval_test_run.model_metrics
    metrics_dict = retrieval_test_run.model_metrics.to_dict()
    assert metrics_dict["Accuracy@k"]


def test_generation_openai(
    okareo_client: Okareo, uploaded_scenario_set: ScenarioSetResponse
) -> None:
    test_run_name = f"ci_json_test_generation_openai {today_with_time}"

    mut = okareo_client.register_model(
        name=test_run_name,
        model=GenerationModel(
            model_id="gpt-4.1-mini",
            temperature=0,
            system_prompt_template="Do system stuff with JSON: {scenario_input.query} and {scenario_input.meta} \n",
            user_prompt_template="Do user stuff with JSON: {scenario_input.user_id} \n",
        ),
    )

    run_resp = mut.run_test(
        name=test_run_name,
        scenario=uploaded_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        checks=["consistency_summary", "compression_ratio", "levenshtein_distance"],
    )
    assert run_resp.name == test_run_name
    assert isinstance(run_resp.model_metrics, TestRunItemModelMetrics)
    metrics_dict = run_resp.model_metrics.to_dict()
    assert metrics_dict["mean_scores"] is not None
    assert metrics_dict["scores_by_row"] is not None
