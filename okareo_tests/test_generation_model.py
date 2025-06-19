import os

import pytest
from okareo_tests.common import API_KEY, random_string
from okareo_tests.utils import assert_metrics

from okareo import Okareo
from okareo.model_under_test import GenerationModel
from okareo_api_client.models import (
    ScenarioSetCreate,
    ScenarioSetResponse,
    SeedData,
    TestRunType,
)


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


@pytest.fixture(scope="module")
def article_scenario_set(rnd: str, okareo: Okareo) -> ScenarioSetResponse:
    seed_data = [
        SeedData(
            input_="At WebBizz, we value our customer's feedback and are always striving to improve."
            + "Our product review section allows customers to share their experiences."
            + "This helps others make informed decisions when shopping on our platform.",
            result="35a4fd5b-453e-4ca6-9536-f20db7303344",
        )
    ]
    scenario_set_create = ScenarioSetCreate(
        name=f"ci-test-generate-scenario-set-{rnd}",
        seed_data=seed_data,
    )
    articles: ScenarioSetResponse = okareo.create_scenario_set(scenario_set_create)

    return articles


def run_generation_model_test(
    rnd: str,
    okareo: Okareo,
    article_scenario_set: ScenarioSetResponse,
    model_id: str,
    api_key: str,
    system_prompt: str,
    user_prompt: str,
) -> None:
    mut = okareo.register_model(
        name=f"ci-generation-model-{model_id}-test-{rnd}",
        model=GenerationModel(
            model_id=model_id,
            temperature=0,
            system_prompt_template=system_prompt,
            user_prompt_template=user_prompt,
        ),
    )

    run_resp = mut.run_test(
        name=f"ci-generation-model-{model_id}-run-{rnd}",
        scenario=article_scenario_set,
        api_key=api_key,
        test_run_type=TestRunType.NL_GENERATION,
        checks=["latency"],
    )

    assert run_resp.name == f"ci-generation-model-{model_id}-run-{rnd}"
    assert_metrics(run_resp, num_rows=1, custom_dimensions=["latency"])


def test_gpt35(
    rnd: str, okareo: Okareo, article_scenario_set: ScenarioSetResponse
) -> None:
    run_generation_model_test(
        rnd,
        okareo,
        article_scenario_set,
        model_id="gpt-4.1-mini",
        api_key=os.environ["OPENAI_API_KEY"],
        system_prompt="You are an AI assistant with a flair for dramatic storytelling and exaggeration.",
        user_prompt="Transform this mundane topic into a very brief dramatic story of heroic proportions: {scenario_input}",
    )


def test_claude3(
    rnd: str, okareo: Okareo, article_scenario_set: ScenarioSetResponse
) -> None:
    run_generation_model_test(
        rnd,
        okareo,
        article_scenario_set,
        model_id="claude-3-haiku-20240307",
        api_key=os.environ["ANTHROPIC_API_KEY"],
        system_prompt="You are an AI assistant with a flair for dramatic storytelling and exaggeration.",
        user_prompt="Transform this mundane topic into a very brief dramatic story of heroic proportions: {scenario_input}",
    )


def test_cohere(
    rnd: str, okareo: Okareo, article_scenario_set: ScenarioSetResponse
) -> None:
    run_generation_model_test(
        rnd,
        okareo,
        article_scenario_set,
        model_id="command-r",
        api_key=os.environ["COHERE_API_KEY"],
        system_prompt="You are an AI assistant with a flair for dramatic storytelling and exaggeration.",
        user_prompt="Transform this mundane topic into a very brief dramatic story of heroic proportions: {scenario_input}",
    )
