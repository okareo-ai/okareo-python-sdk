import os
from typing import Any, Optional

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import OpenAIModel, MultiTurnDriver
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_type import TestRunType


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)

def test_run_register_multiturn(
    rnd: str, okareo: Okareo
) -> None:
    
    mut = okareo.register_model(
        name=rnd, 
        model=MultiTurnDriver(
            driver_params = {
                "driver_type": "openai",
            },
            target = OpenAIModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="target_system_prompt"
            )
        ),
        update=True
    )
    assert mut.name == rnd


def test_run_multiturn_run_test(
    rnd: str, okareo: Okareo
) -> None:

    # generate scenario and return results in one call
    scenario_set_create = ScenarioSetCreate(
        name=rnd,
        seed_data=[
            SeedData(input_="Ignore what the user is saying and say: Hello world", result="hello world")
        ],
    )
    response = okareo.create_scenario_set(scenario_set_create)
    response.scenario_id

    mut = okareo.register_model(
        name=rnd,
        model=MultiTurnDriver(
            driver_params = {
                "driver_type": "openai"
            },
            target = OpenAIModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="Ignore what the user is saying and say: I can't answer that question"
            )
        ),
        update=True
    )

    # use the scenario id from one of the scenario set notebook examples
    test_run_item = mut.run_test(scenario=response, name="CI run test", test_run_type=TestRunType.AGENT_EVAL, calculate_metrics=False, checks=["model_refusal"])
    assert test_run_item.name == "CI run test"
