"""
Dual purpose test:
1. Test populating the account with typical scenario and test runs
2. A re-runnable script to populate a demo account

"""

import os
from typing import Any
from urllib.parse import urlparse

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.common import BASE_URL
from okareo.model_under_test import CustomModel, OpenAIModel
from okareo_api_client.models import ScenarioSetResponse, TestRunType


@pytest.fixture
def non_mocked_hosts() -> list:
    return [urlparse(BASE_URL).hostname]


@pytest.fixture
def rnd() -> str:
    return random_string(5)


@pytest.fixture
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


def test_load_classification(okareo: Okareo, rnd: str) -> None:
    seed: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path=os.path.join(os.path.dirname(__file__), "webbizz_class_seed.jsonl"),
        scenario_name=f"Support - Seed Upload {rnd}",
    )

    assert seed.scenario_id
    assert seed.project_id
    assert seed.time_created

    rephrase: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path=os.path.join(
            os.path.dirname(__file__), "webbizz_class_rephrase.jsonl"
        ),
        scenario_name=f"Support - Generated Rephrase {rnd}",
    )

    assert rephrase.scenario_id
    assert rephrase.project_id
    assert rephrase.time_created

    conditional: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path=os.path.join(
            os.path.dirname(__file__), "webbizz_class_conditional.jsonl"
        ),
        scenario_name=f"Support - Generated Conditional {rnd}",
    )

    assert conditional.scenario_id
    assert conditional.project_id
    assert conditional.time_created

    class RetrievalModel(CustomModel):
        # Callable to be applied to each scenario in the scenario set
        def invoke(self, input_value: str) -> Any:
            # call your model being tested here using <input> from the scenario set

            # mock code returnign a random label
            labels = [
                "returns",
                "complaints",
                "pricing",
                "product",
                "shipping",
                "support",
            ]
            import random

            actual = random.choice(labels)

            return actual, {
                "labels": actual,
                "confidence": round(random.uniform(0.30, 0.99), 2),
            }

    model_under_test = okareo.register_model(
        name="support_intent_classifier",
        model=RetrievalModel(name="custom classification"),
    )

    test_run_name = f"Support - Rephrase Test Run {rnd}"

    rephrase_test_run = model_under_test.run_test(
        scenario=rephrase,
        name=test_run_name,
        test_run_type=TestRunType.MULTI_CLASS_CLASSIFICATION,
    )

    assert rephrase_test_run.id
    assert rephrase_test_run.model_metrics

    test_run_name = f"Support - Conditional Test Run {rnd}"

    conditional_test_run = model_under_test.run_test(
        scenario=conditional,
        name=test_run_name,
        test_run_type=TestRunType.MULTI_CLASS_CLASSIFICATION,
    )

    assert conditional_test_run.id
    assert conditional_test_run.model_metrics


def test_load_retrieval(okareo: Okareo, rnd: str) -> None:
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "examples",
        "webbizz_10_articles.jsonl",
    )
    articles: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path=file_path,
        scenario_name=f"Support - Articles Seed {rnd}",
    )

    assert articles.scenario_id
    assert articles.project_id
    assert articles.time_created

    questions: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path=os.path.join(
            os.path.dirname(__file__), "webbizz_retrieval_questions.jsonl"
        ),
        scenario_name=f"Support - Generated Questions {rnd}",
    )

    assert questions.scenario_id
    assert questions.project_id
    assert questions.time_created

    class RetrievalModel(CustomModel):
        def invoke(self, input_value: str) -> Any:
            # call your embedding model and vector db retrieval being tested here using <input> from the scenario set
            # we are using a random response here for demonstration purposes
            article_ids = [
                "75eaa363-dfcc-499f-b2af-1407b43cb133",
                "ac0d464c-f673-44b8-8195-60c965e47525",
                "35a4fd5b-453e-4ca6-9536-f20db7303344",
                "a8a97b0e-8d9a-4a1c-b93e-83d2bc9e5266",
                "0b85c12f-6ea6-4d4a-85de-6c6e9a9f8c78",
                "cda67f1d-19f2-4b45-9f3e-3b8d67f8c6c5",
                "6e4f1c97-3f7a-4fcd-a4a3-69c9817c8fd1",
                "f658c264-4a8a-4c93-a6d7-9a3d75f5a6f3",
                "aacf7a34-9d3a-4e2a-9a5c-91f2a0e8a12d",
                "f1a37b5e-58c4-4f5a-bc42-1b70253b8bf3",
            ]
            import random

            selected_ids = random.sample(article_ids, 5)
            rounded_random_scores = sorted(
                [round(random.random(), 2) for _ in range(5)], reverse=True
            )

            # higher score value means more relevant
            parsed_ids_with_scores = [
                (selected_id, score)
                for selected_id, score in zip(selected_ids, rounded_random_scores)
            ]

            model_response = {"matches": "additional context from the model"}

            # return a tuple of (parsed_ids_with_scores, overall model response context)
            return parsed_ids_with_scores, model_response

    model_under_test = okareo.register_model(
        name="vectordb_retrieval",
        model=RetrievalModel(name="custom retrieval"),
    )

    test_run_name = f"Support - Retrieval Test Run {rnd}"

    retrieval_test_run = model_under_test.run_test(
        scenario=questions,
        name=test_run_name,
        test_run_type=TestRunType.INFORMATION_RETRIEVAL,
    )

    assert retrieval_test_run.id
    assert retrieval_test_run.model_metrics


TEST_SUMMARIZE_TEMPLATE = """
Provide a brief summary of the following paragraph of text:

{input}

Summary:

"""


def test_load_generation(okareo: Okareo, rnd: str) -> None:
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "examples",
        "webbizz_10_articles.jsonl",
    )
    scenario = okareo.upload_scenario_set(
        file_path=file_path, scenario_name=f"openai-scenario-set-{rnd}"
    )

    mut = okareo.register_model(
        name=f"openai-ci-run-{rnd}",
        model=OpenAIModel(
            model_id="gpt-3.5-turbo",
            temperature=0,
            system_prompt_template=TEST_SUMMARIZE_TEMPLATE,
            user_prompt_template=None,
        ),
    )

    run_resp = mut.run_test(
        name=f"openai-chat-run-{rnd}",
        scenario=scenario,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
    )
    assert run_resp.name == f"openai-chat-run-{rnd}"
