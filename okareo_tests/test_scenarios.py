import json
import os
import time
from typing import List

import pytest
import requests  # type: ignore
from okareo_tests.common import API_KEY, random_string

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
from okareo_api_client.models.scenario_type import ScenarioType


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
def custom_data() -> List[SeedData]:
    return [
        SeedData(input_="Lorem ipsum dolor sit amet", result="N/A"),
        SeedData(input_="consectetur adipiscing elit, sed do", result="N/A"),
        SeedData(input_="eiusmod tempor incididunt ut labore", result="N/A"),
    ]


create_scenario_name = f"my_test_scenario_set_{random_string(5)}"
examples_scenario_name = f"my_examples_scenario_set_{random_string(5)}"


@pytest.fixture(scope="module")
def create_scenario_set(
    okareo_client: Okareo, seed_data: List[SeedData]
) -> ScenarioSetResponse:
    scenario_set_create = ScenarioSetCreate(
        name=create_scenario_name,
        seed_data=seed_data,
    )
    articles: ScenarioSetResponse = okareo_client.create_scenario_set(
        scenario_set_create
    )

    return articles


@pytest.fixture(scope="module")
def create_examples_scenario_set(
    okareo_client: Okareo, custom_data: List[SeedData]
) -> ScenarioSetResponse:
    scenario_set_create = ScenarioSetCreate(
        name=examples_scenario_name,
        seed_data=custom_data,
    )
    examples: ScenarioSetResponse = okareo_client.create_scenario_set(
        scenario_set_create
    )

    return examples


@pytest.fixture(scope="module")
def generate_scenarios(
    okareo_client: Okareo, create_scenario_set: ScenarioSetResponse
) -> ScenarioSetResponse:
    scenario_set_generate = ScenarioSetGenerate(
        source_scenario_id=create_scenario_set.scenario_id,
        name=f"generated scenario set {random_string(5)}",
        number_examples=2,
    )
    response = okareo_client.generate_scenario_set(scenario_set_generate)
    return response


@pytest.fixture(scope="module")
def generate_scenarios_qa(
    okareo_client: Okareo, create_scenario_set: ScenarioSetResponse
) -> ScenarioSetResponse:
    scenario_set_generate = ScenarioSetGenerate(
        source_scenario_id=create_scenario_set.scenario_id,
        name=f"generated scenario set {random_string(5)}",
        number_examples=1,
        generation_type=ScenarioType.TEXT_REVERSE_QUESTION_ANSWER,
    )
    response = okareo_client.generate_scenario_set(scenario_set_generate)
    return response


@pytest.fixture(scope="module")
def generate_scenarios_custom(
    okareo_client: Okareo, create_examples_scenario_set: ScenarioSetResponse
) -> ScenarioSetResponse:
    scenario_set_generate = ScenarioSetGenerate(
        source_scenario_id=create_examples_scenario_set.scenario_id,
        name=f"generated custom scenario set {random_string(5)}",
        number_examples=1,
        generation_type=ScenarioType.CUSTOM_GENERATOR,
        generation_prompt="generate the next 5 words of 'lorem ipsum' based on the following text: {input}",
    )
    response = okareo_client.generate_scenario_set(scenario_set_generate)
    print(response)
    return response


@pytest.fixture(scope="module")
def get_scenario_data_points(
    okareo_client: Okareo, create_scenario_set: ScenarioSetResponse
) -> List[ScenarioDataPoinResponse]:
    return okareo_client.get_scenario_data_points(create_scenario_set.scenario_id)


def test_create_scenario_set(
    create_scenario_set: ScenarioSetResponse, seed_data: List[SeedData]
) -> None:
    assert create_scenario_set.type == "SEED"  # default test
    assert create_scenario_set.scenario_id
    assert create_scenario_set.project_id
    assert create_scenario_set.time_created
    if isinstance(create_scenario_set.seed_data, List):
        for i in range(1):
            assert seed_data[i].input_ == create_scenario_set.seed_data[i].input_
            assert seed_data[i].result == create_scenario_set.seed_data[i].result


def test_download_scenario_set(
    okareo_client: Okareo,
    create_scenario_set: ScenarioSetResponse,
    seed_data: List[SeedData],
) -> None:
    response_file = okareo_client.download_scenario_set(create_scenario_set)
    with open(response_file.name) as scenario_file:
        for line in scenario_file:
            assert json.loads(line)["input"] != ""
            assert json.loads(line)["result"] != ""

    os.remove(create_scenario_name + ".jsonl")


def test_duplicate_scenario_name(
    okareo_client: Okareo,
    seed_data: List[SeedData],
) -> None:
    name = f"my test scenario set {random_string(5)}"
    scenario = okareo_client.create_scenario_set(
        ScenarioSetCreate(
            name=name,
            seed_data=seed_data,
        )
    )
    assert scenario.warning is None
    scenario = okareo_client.create_scenario_set(
        ScenarioSetCreate(
            name=name,
            seed_data=seed_data,
        )
    )
    assert scenario.warning


def test_download_scenario_set_with_file(
    okareo_client: Okareo,
    create_scenario_set: ScenarioSetResponse,
    seed_data: List[SeedData],
) -> None:
    response_file = okareo_client.download_scenario_set(
        create_scenario_set, "./scenario.jsonl"
    )
    with open(response_file.name) as scenario_file:
        for line in scenario_file:
            assert json.loads(line)["input"] != ""
            assert json.loads(line)["result"] != ""

    os.remove("./scenario.jsonl")


def test_create_scenario_set_all_fields(
    okareo_client: Okareo, seed_data: List[SeedData]
) -> None:
    scenario_set_create = ScenarioSetCreate(
        name=f"my test scenario set {random_string(5)}",
        seed_data=seed_data,
    )
    create_scenario_set: ScenarioSetResponse = okareo_client.create_scenario_set(
        scenario_set_create
    )

    assert create_scenario_set.type == "SEED"
    assert create_scenario_set.scenario_id
    assert create_scenario_set.project_id
    assert create_scenario_set.time_created
    assert isinstance(create_scenario_set.scenario_input, List)
    assert isinstance(create_scenario_set.seed_data, List)
    for i in range(3):
        assert seed_data[i].input_ == create_scenario_set.seed_data[i].input_


def test_generate_scenarios(
    generate_scenarios: ScenarioSetResponse,
    seed_data: List[SeedData],
    okareo_client: Okareo,
) -> None:
    assert generate_scenarios.type == "REPHRASE_INVARIANT"
    assert generate_scenarios.seed_data == []
    assert generate_scenarios is not None
    assert generate_scenarios.scenario_id
    assert generate_scenarios.project_id
    assert generate_scenarios.time_created
    assert type(generate_scenarios.tags) is list

    # assert each seed_id in generated scenario meta_data is in the seed data
    gen_dp = okareo_client.get_scenario_data_points(generate_scenarios.scenario_id)
    seed_dp = okareo_client.get_scenario_data_points(
        generate_scenarios.tags[0].split(":")[1]
    )
    seed_ids = [dp.id for dp in seed_dp]
    for dp in gen_dp:
        assert dp.meta_data
        assert dp.meta_data["seed_id"] in seed_ids


def test_generate_scenarios_qa(
    generate_scenarios_qa: ScenarioSetResponse,
    seed_data: List[SeedData],
    okareo_client: Okareo,
) -> None:
    assert generate_scenarios_qa.type == "TEXT_REVERSE_QUESTION_ANSWER"
    assert generate_scenarios_qa.seed_data == []
    assert generate_scenarios_qa is not None
    assert generate_scenarios_qa.scenario_id
    assert generate_scenarios_qa.project_id
    assert generate_scenarios_qa.time_created
    assert type(generate_scenarios_qa.tags) is list

    # assert each seed_id in generated scenario meta_data is in the seed data
    gen_dp = okareo_client.get_scenario_data_points(generate_scenarios_qa.scenario_id)
    seed_dp = okareo_client.get_scenario_data_points(
        generate_scenarios_qa.tags[0].split(":")[1]
    )
    seed_ids = [dp.id for dp in seed_dp]
    for dp in gen_dp:
        assert dp.meta_data
        assert dp.meta_data["seed_id"] in seed_ids


def test_generate_scenarios_custom(
    generate_scenarios_custom: ScenarioSetResponse,
    seed_data: List[SeedData],
    okareo_client: Okareo,
) -> None:
    assert generate_scenarios_custom.type == "CUSTOM_GENERATOR"
    assert generate_scenarios_custom.seed_data == []
    assert generate_scenarios_custom is not None
    assert generate_scenarios_custom.scenario_id
    assert generate_scenarios_custom.project_id
    assert generate_scenarios_custom.time_created
    assert type(generate_scenarios_custom.tags) is list

    # assert each seed_id in generated scenario meta_data is in the seed data
    gen_dp = okareo_client.get_scenario_data_points(
        generate_scenarios_custom.scenario_id
    )
    seed_dp = okareo_client.get_scenario_data_points(
        generate_scenarios_custom.tags[0].split(":")[1]
    )
    seed_ids = [dp.id for dp in seed_dp]
    for dp in gen_dp:
        assert dp.meta_data
        assert dp.meta_data["seed_id"] in seed_ids


def test_get_scenario_data_points(
    get_scenario_data_points: List[ScenarioDataPoinResponse], seed_data: List[SeedData]
) -> None:
    assert get_scenario_data_points is not None
    assert len(get_scenario_data_points) == 3


def delete_scenario_data_points(
    api_key: str, scenario_id: str, scenario_name: str
) -> None:
    url = f"https://api.okareo.com/v0/scenario_sets/{scenario_id}?name={scenario_name}"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "api-key": api_key,
    }
    requests.delete(url, headers=headers)


def test_create_scenario_empty_seed_data(
    okareo_client: Okareo,
) -> None:
    scenario_set_create = ScenarioSetCreate(
        name=f"my test scenario set {random_string(5)}",
        seed_data=[],
    )
    with pytest.raises(
        ValueError, match="Non-empty seed data is required to create a scenario set"
    ):
        okareo_client.create_scenario_set(scenario_set_create)


def dtest_create_delete_scenario_set_contraction_tiny_load(
    okareo_client: Okareo, seed_data: List[SeedData]
) -> None:
    seed_data = []
    file_path = os.path.join(
        os.path.dirname(__file__), "datasets/random_sentence_tiny.txt"
    )
    with open(file_path) as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split("\t")
            assert len(parts) == 2
            seed_data.append(
                SeedData(input_=parts[0], result=parts[1]),
            )

    scenario_set_create = ScenarioSetCreate(
        name="my contraction test scenario set tiny load",
        seed_data=seed_data,
    )
    scenario: ScenarioSetResponse = okareo_client.create_scenario_set(
        scenario_set_create
    )

    time.sleep(10)

    if isinstance(scenario.tags, list) and isinstance(scenario.name, str):
        scenario_seed_id = scenario.tags[0].split(":")[1]
        delete_scenario_data_points(API_KEY, scenario_seed_id, scenario.name)
        delete_scenario_data_points(API_KEY, scenario.scenario_id, scenario.name)

    assert scenario.type == "COMMON_CONTRACTIONS"


def dtest_create_delete_scenario_set_misspelling_tiny_load(
    okareo_client: Okareo, seed_data: List[SeedData]
) -> None:
    seed_data = []
    file_path = os.path.join(
        os.path.dirname(__file__), "datasets/random_sentence_tiny.txt"
    )
    with open(file_path) as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split("\t")
            assert len(parts) == 2
            seed_data.append(
                SeedData(input_=parts[0], result=parts[1]),
            )

    scenario_set_create = ScenarioSetCreate(
        name=f"my misspelling test scenario set tiny load {random_string(5)}",
        seed_data=seed_data,
    )
    scenario: ScenarioSetResponse = okareo_client.create_scenario_set(
        scenario_set_create
    )

    time.sleep(10)

    if isinstance(scenario.tags, list) and isinstance(scenario.name, str):
        scenario_seed_id = scenario.tags[0].split(":")[1]
        delete_scenario_data_points(API_KEY, scenario_seed_id, scenario.name)
        delete_scenario_data_points(API_KEY, scenario.scenario_id, scenario.name)

    assert scenario.type == "COMMON_MISSPELLINGS"
