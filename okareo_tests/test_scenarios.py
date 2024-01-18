from datetime import datetime
from typing import List

import pytest
from okareo_tests.common import API_KEY

from okareo import Okareo
from okareo_api_client.models import (
    ScenarioSetCreate,
    ScenarioSetGenerate,
    ScenarioSetResponse,
    SeedData,
)
from okareo_api_client.models.scenario_data_poin_response import (
    ScenarioDataPoinResponse,
)

today_with_time = datetime.now().strftime("%m-%d %H:%M:%S")


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


@pytest.fixture(scope="module")
def seed_data() -> List[SeedData]:
    return [
        SeedData(input_="example question or statement", result="example result"),
        SeedData(
            input_="tell me about your capability", result="unique example result"
        ),
        SeedData(input_="what are your limitations", result="different example result"),
    ]


@pytest.fixture(scope="module")
def create_scenario_set(
    okareo_client: Okareo, seed_data: List[SeedData]
) -> ScenarioSetResponse:
    scenario_set_create = ScenarioSetCreate(
        name="my test scenario set",
        number_examples=1,
        seed_data=seed_data,
    )
    articles: ScenarioSetResponse = okareo_client.create_scenario_set(
        scenario_set_create
    )

    return articles


@pytest.fixture(scope="module")
def generate_scenarios(
    okareo_client: Okareo, create_scenario_set: ScenarioSetResponse
) -> ScenarioSetResponse:
    scenario_set_generate = ScenarioSetGenerate(
        source_scenario_id=create_scenario_set.scenario_id,
        name="generated scenario set",
        number_examples=2,
    )
    response = okareo_client.generate_scenario_set(scenario_set_generate)
    return response


@pytest.fixture(scope="module")
def get_scenario_data_points(
    okareo_client: Okareo, create_scenario_set: ScenarioSetResponse
) -> List[ScenarioDataPoinResponse]:
    return okareo_client.get_scenario_data_points(create_scenario_set.scenario_id)


def test_create_scenario_set(
    create_scenario_set: ScenarioSetResponse, seed_data: List[SeedData]
) -> None:
    assert create_scenario_set.type == "REPHRASE_INVARIANT"
    assert create_scenario_set.scenario_id
    assert create_scenario_set.project_id
    assert create_scenario_set.time_created
    if isinstance(create_scenario_set.seed_data, List):
        for i in range(3):
            assert seed_data[i].input_ == create_scenario_set.seed_data[i].input_
            assert seed_data[i].result == create_scenario_set.seed_data[i].result


def test_generate_scenarios(
    generate_scenarios: ScenarioSetResponse, seed_data: List[SeedData]
) -> None:
    assert generate_scenarios.type == "REPHRASE_INVARIANT"
    assert generate_scenarios.seed_data == []
    assert generate_scenarios is not None
    assert generate_scenarios.scenario_id
    assert generate_scenarios.project_id
    assert generate_scenarios.time_created


def test_get_scenario_data_points(
    get_scenario_data_points: List[ScenarioDataPoinResponse], seed_data: List[SeedData]
) -> None:
    assert get_scenario_data_points is not None
    assert len(get_scenario_data_points) == 3
