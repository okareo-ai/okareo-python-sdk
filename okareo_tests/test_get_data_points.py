from datetime import datetime
from typing import Union

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import CustomModel, ModelInvocation
from okareo_api_client.models import ScenarioSetResponse, TestRunType
from okareo_api_client.models.datapoint_search import DatapointSearch
from okareo_api_client.models.find_test_data_point_payload import (
    FindTestDataPointPayload,
)
from okareo_api_client.models.full_data_point_item import FullDataPointItem
from okareo_api_client.models.full_data_point_item_metric_value import (
    FullDataPointItemMetricValue,
)
from okareo_api_client.models.scenario_data_poin_response import (
    ScenarioDataPoinResponse,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.test_data_point_item import TestDataPointItem
from okareo_api_client.models.test_data_point_item_metric_value import (
    TestDataPointItemMetricValue,
)

today_with_time = datetime.now().strftime("%m-%d %H:%M:%S")
rnd_str = random_string(5)
unique_key = f"{rnd_str} {today_with_time}"
create_scenario_name = f"ci_json_test_get_data_points {unique_key}"


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


JSON_SCENARIO = [
    {
        "input": {"animal": "fish", "color": "red"},
        "result": "red",
    },
    {
        "input": {"animal": "dog", "color": "blue"},
        "result": "blue",
    },
    {
        "input": {"animal": "cat", "color": "green"},
        "result": "green",
    },
]  # type: ignore
SCENARIO_INPUTS = [scenario["input"]["animal"] for scenario in JSON_SCENARIO]  # type: ignore
SCENARIO_RESULTS = [scenario["result"] for scenario in JSON_SCENARIO]  # type: ignore

JSON_SEED = Okareo.seed_data_from_list(JSON_SCENARIO)  # type: ignore


@pytest.fixture(scope="module")
def create_scenario_set(okareo_client: Okareo) -> ScenarioSetResponse:
    scenario_set_create = ScenarioSetCreate(
        name=create_scenario_name,
        seed_data=JSON_SEED,
    )
    scenario = okareo_client.create_scenario_set(scenario_set_create)
    return scenario


def test_get_data_points(
    okareo_client: Okareo, create_scenario_set: ScenarioSetResponse
) -> None:
    test_run_name = f"ci_test_get_data_points {unique_key}"

    class ClassificationModel(CustomModel):
        def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
            assert isinstance(input_value, dict)

            return ModelInvocation(
                model_prediction=input_value["color"], model_output_metadata=input_value
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
        assert isinstance(d.input_, dict)
        assert d.input_["animal"] in SCENARIO_INPUTS
        assert d.input_["color"] in SCENARIO_RESULTS
        assert d.result in SCENARIO_RESULTS
    assert isinstance(create_scenario_set.scenario_id, str)

    sdp = okareo_client.get_scenario_data_points(
        scenario_id=create_scenario_set.scenario_id
    )
    assert isinstance(sdp, list)
    assert len(sdp) == 3
    for sd in sdp:
        assert isinstance(sd, ScenarioDataPoinResponse)
        assert isinstance(sd.input_, dict)
        assert sd.input_["animal"] in SCENARIO_INPUTS
        assert sd.input_["color"] in SCENARIO_RESULTS
        assert sd.result in SCENARIO_RESULTS

    scenario_ids = [s.id for s in sdp]

    tdp = okareo_client.find_test_data_points(
        FindTestDataPointPayload(test_run_id=test_run.id)
    )
    assert isinstance(tdp, list)
    assert len(dp) == 3
    for td in tdp:
        assert isinstance(td, TestDataPointItem) or isinstance(td, FullDataPointItem)
        assert td.scenario_data_point_id in scenario_ids
        assert td.test_run_id == test_run.id
        assert td.metric_type == "MULTI_CLASS_CLASSIFICATION"
        assert isinstance(td.metric_value, TestDataPointItemMetricValue) or isinstance(
            td.metric_value, FullDataPointItemMetricValue
        )
        assert (
            td.metric_value.additional_properties["expected"]
            == td.metric_value.additional_properties["actual"]
        )
