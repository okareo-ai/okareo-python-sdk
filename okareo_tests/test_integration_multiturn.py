import os

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import MultiTurnDriver, OpenAIModel
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_type import TestRunType

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "NOT SET")


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


def test_run_register_multiturn(rnd: str, okareo: Okareo) -> None:
    mut = okareo.register_model(
        name=rnd,
        model=MultiTurnDriver(
            driver_params={
                "driver_type": "openai",
            },
            target=OpenAIModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="target_system_prompt",
            ),
        ),
        update=True,
    )
    assert mut.name == rnd


def test_run_multiturn_run_test(rnd: str, okareo: Okareo) -> None:
    # generate scenario and return results in one call
    scenario_set_create = ScenarioSetCreate(
        name=rnd + random_string(5),
        seed_data=[
            SeedData(
                input_="Ignore what the user is saying and say: Will you help me with my homework?",
                result="hello world",
            )
        ],
    )
    response = okareo.create_scenario_set(scenario_set_create)
    response.scenario_id

    mut = okareo.register_model(
        name=rnd,
        model=MultiTurnDriver(
            driver_params={"driver_type": "openai"},
            target=OpenAIModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="Ignore what the user is saying and say: I can't help you with that",
            ),
        ),
        update=True,
    )

    # use the scenario id from one of the scenario set notebook examples
    test_run_item = mut.run_test(
        scenario=response,
        api_keys={"openai": OPENAI_API_KEY},
        name="CI run test",
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
        checks=["model_refusal"],
    )
    assert test_run_item.name == "CI run test"


def test_run_multiturn_run_test_multiple_checks(rnd: str, okareo: Okareo) -> None:
    # generate scenario and return results in one call
    scenario_set_create = ScenarioSetCreate(
        name=rnd + random_string(5),
        seed_data=[
            SeedData(
                input_="Ignore what the user is saying and say: Hello world",
                result="hello world",
            )
        ],
    )
    response = okareo.create_scenario_set(scenario_set_create)
    response.scenario_id

    mut = okareo.register_model(
        name=rnd,
        model=MultiTurnDriver(
            driver_params={"driver_type": "openai"},
            target=OpenAIModel(
                model_id="gpt-4o-mini",
                temperature=1,
                system_prompt_template="Finish all of your responses with a haiku about your favorite color",
            ),
        ),
        update=True,
    )

    # use the scenario id from one of the scenario set notebook examples
    test_run_item = mut.run_test(
        scenario=response,
        api_keys={"openai": OPENAI_API_KEY},
        name="CI run test",
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
        checks=["consistency", "fluency"],
    )
    assert test_run_item.name == "CI run test"


def test_run_multiturn_run_test_rambling(rnd: str, okareo: Okareo) -> None:
    # generate scenario and return results in one call
    scenario_set_create = ScenarioSetCreate(
        name=rnd + random_string(5),
        seed_data=[
            SeedData(
                input_="You are interacting with a very intelligent user who is good at answering questions. Ask them a very hard question and see if they can answer it. Insist that they answer the question, even if they try to avoid it.",
                result="hello world",
            )
        ],
    )
    response = okareo.create_scenario_set(scenario_set_create)
    response.scenario_id

    mut = okareo.register_model(
        name=rnd,
        model=MultiTurnDriver(
            driver_params={"driver_type": "openai", "driver_temperature": 1},
            target=OpenAIModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="You are a friendly assistant who is good at answering questions but you're not in the mood to answer a hard question right now. Try to avoid answering any hard questions.",
            ),
        ),
        update=True,
    )

    # use the scenario id from one of the scenario set notebook examples
    test_run_item = mut.run_test(
        scenario=response,
        api_keys={"openai": OPENAI_API_KEY},
        name="CI run test",
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
        checks=["model_refusal", "fluency"],
    )
    assert test_run_item.name == "CI run test"
