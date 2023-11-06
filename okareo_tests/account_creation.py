"""
Dual purpose test:
1. Test populating the account with typical scenario and test runs
2. A re-runnable script to populate a demo account

"""

from datetime import datetime
from typing import Any
from urllib.parse import urlparse

import pytest
from okareo_tests.common import API_KEY, OkareoAPIhost, integration
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo.common import BASE_URL
from okareo_api_client.models import ScenarioSetResponse, TestRunType


@pytest.fixture
def non_mocked_hosts() -> list:
    return [urlparse(BASE_URL).hostname]


@integration
def test_load_classification(httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost) -> None:
    if okareo_api.is_mock:
        return  # purely a live test

    today_with_time = datetime.now().strftime("%m-%d %H:%M:%S")

    okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)
    seed: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path="./okareo_tests/webbizz_class_seed.jsonl",
        scenario_name=f"Support - Seed Upload {today_with_time}",
    )

    assert seed.scenario_id
    assert seed.project_id
    assert seed.time_created

    rephrase: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path="./okareo_tests/webbizz_class_rephrase.jsonl",
        scenario_name=f"Support - Generated Rephrase {today_with_time}",
    )

    assert rephrase.scenario_id
    assert rephrase.project_id
    assert rephrase.time_created

    conditional: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path="./okareo_tests/webbizz_class_conditional.jsonl",
        scenario_name=f"Support - Generated Conditional {today_with_time}",
    )

    assert conditional.scenario_id
    assert conditional.project_id
    assert conditional.time_created

    # Callable to be applied to each scenario in the scenario set
    def call_model(query: str) -> tuple[Any, Any]:
        # call your model being tested here using <input> from the scenario set

        # mock code returnign a random label
        labels = ["returns", "complains", "pricing", "product", "shipping", "support"]
        import random

        actual = random.choice(labels)

        return actual, {
            "labels": actual,
            "confidence": round(random.uniform(0.30, 0.99), 2),
        }

    model_under_test = okareo.register_model(name="support_intent_classifier")

    test_run_name = f"Support - Rephrase Test Run {today_with_time}"

    rephrase_test_run = model_under_test.run_test(
        scenario_id=rephrase.scenario_id,
        model_invoker=call_model,
        test_run_name=test_run_name,
        test_run_type=TestRunType.MULTI_CLASS_CLASSIFICATION,
    )

    assert rephrase_test_run.id
    assert rephrase_test_run.model_metrics

    test_run_name = f"Support - Conditional Test Run {today_with_time}"

    conditional_test_run = model_under_test.run_test(
        scenario_id=conditional.scenario_id,
        model_invoker=call_model,
        test_run_name=test_run_name,
        test_run_type=TestRunType.MULTI_CLASS_CLASSIFICATION,
    )

    assert conditional_test_run.id
    assert conditional_test_run.model_metrics


@integration
def test_load_retrieval(httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost) -> None:
    if okareo_api.is_mock:
        return  # purely a live test

    today_with_time = datetime.now().strftime("%m-%d %H:%M:%S")

    okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)
    articles: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path="./examples/webbizz_10_articles.jsonl",
        scenario_name=f"Support - Articles Seed {today_with_time}",
    )

    assert articles.scenario_id
    assert articles.project_id
    assert articles.time_created

    questions: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path="./okareo_tests/webbizz_retrieval_questions.jsonl",
        scenario_name=f"Support - Generated Questions {today_with_time}",
    )

    assert questions.scenario_id
    assert questions.project_id
    assert questions.time_created

    # Callable to be applied to each scenario in the scenario set
    def call_model(query: str) -> tuple[Any, Any]:
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

    model_under_test = okareo.register_model(name="vectordb_retrieval")

    test_run_name = f"Support - Retrieval Test Run {today_with_time}"

    retrieval_test_run = model_under_test.run_test(
        scenario_id=questions.scenario_id,
        model_invoker=call_model,
        test_run_name=test_run_name,
        test_run_type=TestRunType.INFORMATION_RETRIEVAL,
    )

    assert retrieval_test_run.id
    assert retrieval_test_run.model_metrics
