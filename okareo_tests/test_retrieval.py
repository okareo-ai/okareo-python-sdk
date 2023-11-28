import os
from datetime import datetime
from typing import Any

import pytest
from okareo_tests.common import API_KEY

from okareo import Okareo
from okareo_api_client.models import ScenarioSetResponse, ScenarioType, TestRunType

today_with_time = datetime.now().strftime("%m-%d %H:%M:%S")


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


@pytest.fixture(scope="module")
def uploaded_scenario_set(okareo_client: Okareo) -> ScenarioSetResponse:
    file_path = os.path.join(os.path.dirname(__file__), "webbizz_1_test_article.jsonl")
    articles: ScenarioSetResponse = okareo_client.upload_scenario_set(
        file_path=file_path, scenario_name=f"test_upload_scenario_set {today_with_time}"
    )

    return articles


@pytest.fixture(scope="module")
def generate_scenarios(
    okareo_client: Okareo, uploaded_scenario_set: ScenarioSetResponse
) -> ScenarioSetResponse:
    questions: ScenarioSetResponse = okareo_client.generate_scenarios(
        source_scenario_id=uploaded_scenario_set.scenario_id,
        name=f"test_generate_scenarios {today_with_time}",
        number_examples=2,
        generation_type=ScenarioType.TEXT_REVERSE_QUESTION,
    )
    return questions


def test_upload_scenario_set(uploaded_scenario_set: ScenarioSetResponse) -> None:
    assert uploaded_scenario_set is not None
    assert uploaded_scenario_set.scenario_id
    assert uploaded_scenario_set.project_id
    assert uploaded_scenario_set.time_created


def test_generate_scenarios(generate_scenarios: ScenarioSetResponse) -> None:
    assert generate_scenarios is not None
    assert generate_scenarios.scenario_id
    assert generate_scenarios.project_id
    assert generate_scenarios.time_created


def test_run_test_retrieval(
    okareo_client: Okareo, generate_scenarios: ScenarioSetResponse
) -> None:
    # Callable to be applied to each scenario in the scenario set
    def call_model(query: str) -> tuple[Any, Any]:
        # call your embedding model and vector db retrieval being tested here using <input> from the scenario set
        # we are using a random response here for demonstration purposes
        article_ids = [
            "75eaa363-dfcc-499f-b2af-1407b43cb133",
            "ac0d464c-f673-44b8-8195-60c965e47525",
        ]
        import random

        selected_ids = random.sample(article_ids, 1)
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

    model_under_test = okareo_client.register_model(name="vectordb_retrieval")

    test_run_name = f"test_run_test_retrieval {today_with_time}"

    retrieval_test_run = model_under_test.run_test(
        scenario_id=generate_scenarios.scenario_id,
        model_invoker=call_model,
        test_run_name=test_run_name,
        test_run_type=TestRunType.INFORMATION_RETRIEVAL,
    )

    assert retrieval_test_run.id
    assert retrieval_test_run.model_metrics
