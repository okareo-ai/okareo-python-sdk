from datetime import datetime
from typing import Union

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import CustomModel, ModelInvocation
from okareo_api_client.models import ScenarioSetResponse, TestRunType
from okareo_api_client.models.datapoint_search import DatapointSearch
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate

today_with_time = datetime.now().strftime("%m-%d %H:%M:%S")
rnd_str = random_string(5)
unique_key = f"{rnd_str} {today_with_time}"
create_scenario_name = f"ci_json_test_create_scenarios {unique_key}"


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


JSON_SCENARIO = [
    {
        "input": {"query": "user q 1", "user_id": "red", "meta": "meta1"},
        "result": "red",
    },
    {
        "input": {"query": "user q 2", "user_id": "blue", "meta": "meta1"},
        "result": "blue",
    },
    {
        "input": {"query": "user q 3", "user_id": "green", "meta": "meta1"},
        "result": "green",
    },
]  # type: ignore
SCENARIO_USERID = [scenario["input"]["user_id"] for scenario in JSON_SCENARIO]  # type: ignore
SCENARIO_QUERY = [scenario["input"]["query"] for scenario in JSON_SCENARIO]  # type: ignore
SCENARIO_META = [scenario["input"]["meta"] for scenario in JSON_SCENARIO]  # type: ignore


JSON_SEED = Okareo.seed_data_from_list(JSON_SCENARIO)  # type: ignore


@pytest.fixture(scope="module")
def create_scenario_set(okareo_client: Okareo) -> ScenarioSetResponse:
    scenario_set_create = ScenarioSetCreate(
        name=create_scenario_name,
        seed_data=JSON_SEED,
    )
    scenario = okareo_client.create_scenario_set(scenario_set_create)
    return scenario


# BC test for custom model removed as it has been phased out of SDK and docs


def test_custom_return_invocation(
    okareo_client: Okareo, create_scenario_set: ScenarioSetResponse
) -> None:
    test_run_name = f"ci_test_custom_return_bc {unique_key}"

    class ClassificationModel(CustomModel):
        def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
            assert isinstance(input_value, dict)

            return ModelInvocation(
                model_prediction=input_value["user_id"],
                model_input=input_value["query"],
                model_output_metadata=input_value["meta"],
            )

    model_under_test = okareo_client.register_model(
        name=test_run_name,
        model=ClassificationModel(name=test_run_name),
    )

    test_run = model_under_test.run_test(
        scenario=create_scenario_set,
        name=test_run_name,
        test_run_type=TestRunType.MULTI_CLASS_CLASSIFICATION,
        calculate_metrics=True,
    )

    assert test_run.id
    assert test_run.model_metrics
    metrics_dict = test_run.model_metrics.to_dict()
    assert metrics_dict["weighted_average"] is not None
    assert metrics_dict["weighted_average"]["f1"] == 1

    dp = okareo_client.find_datapoints(DatapointSearch(test_run_id=test_run.id))
    assert isinstance(dp, list)
    assert len(dp) == 3
    for d in dp:
        assert d.input_ in SCENARIO_QUERY
        assert d.result in SCENARIO_USERID
