import os
import random
import string
import tempfile
from typing import List, Union

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import CohereModel, OpenAIModel, PineconeDb, QdrantDB
from okareo_api_client.models import ScenarioSetResponse
from okareo_api_client.models.evaluator_spec_request import EvaluatorSpecRequest
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_item import TestRunItem
from okareo_api_client.models.test_run_type import TestRunType
from okareo_api_client.types import Unset


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


TEST_SUMMARIZE_TEMPLATE = """
Provide a brief summary of the following paragraph of text:

{input}

Summary:

"""


@pytest.fixture(scope="module")
def article_scenario_set(rnd: str, okareo: Okareo) -> ScenarioSetResponse:
    file_path = os.path.join(os.path.dirname(__file__), "webbizz_3_test_article.jsonl")
    articles: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path=file_path, scenario_name=f"openai-scenario-set-{rnd}"
    )

    return articles


def test_run_test_openai(
    rnd: str, okareo: Okareo, article_scenario_set: ScenarioSetResponse
) -> None:
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
        scenario=article_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
    )
    assert run_resp.name == f"openai-chat-run-{rnd}"
    assert_metrics(run_resp)


def test_run_test_openai_2prompts(
    rnd: str, okareo: Okareo, article_scenario_set: ScenarioSetResponse
) -> None:
    mut2 = okareo.register_model(
        name=f"openai-ci-run-{rnd}",
        model=OpenAIModel(
            model_id="gpt-3.5-turbo",
            temperature=0,
            system_prompt_template=TEST_SUMMARIZE_TEMPLATE,
            user_prompt_template=TEST_SUMMARIZE_TEMPLATE,
        ),
    )

    run_resp = mut2.run_test(
        name=f"openai-chat-run-{rnd}",
        scenario=article_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
    )
    assert run_resp.name == f"openai-chat-run-{rnd}"
    assert_metrics(run_resp)


def assert_metrics(
    run_resp: TestRunItem, custom_dimensions: Union[List[str], None] = None
) -> None:
    assert run_resp.model_metrics is not None and not isinstance(
        run_resp.model_metrics, Unset
    )
    metrics_dict = run_resp.model_metrics.to_dict()

    assert metrics_dict["mean_scores"] is not None
    if custom_dimensions is not None:
        assert_scores(metrics_dict["mean_scores"], custom_dimensions)
    else:
        assert_scores_geval(metrics_dict["mean_scores"])
    assert metrics_dict["scores_by_row"] is not None
    assert len(metrics_dict["scores_by_row"]) == 3
    for row in metrics_dict["scores_by_row"]:
        if custom_dimensions is not None:
            assert_scores(row, custom_dimensions)
        else:
            assert_scores_geval(row)


def assert_scores_geval(scores: dict) -> None:
    dimension_keys = ["consistency", "coherence", "fluency", "relevance"]
    for dimension in dimension_keys:
        assert dimension in scores
        assert isinstance(scores[dimension], float)
        assert 1 <= scores[dimension] <= 5


def assert_scores(scores: dict, custom_dimensions: List[str]) -> None:
    dimension_keys = custom_dimensions
    for dimension in dimension_keys:
        assert dimension in scores


def test_run_test_cohere(rnd: str, okareo: Okareo) -> None:
    seed_data = [
        SeedData(input_="what are you able to set up in aws?", result="capabilities"),
        SeedData(
            input_="what's the procedure to request for more information?",
            result="general",
        ),
        SeedData(
            input_="what are the steps to deploy on heroku?", result="capabilities"
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"cohere-test-ci-{rnd}",
        seed_data=seed_data,
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    mut = okareo.register_model(
        name=f"classification-cohere-ci-{rnd}",
        model=CohereModel(
            model_id="2386d4d1-c617-4183-8c87-5550c7f222e6-ft",
            model_type="classify",
        ),
    )

    run_resp = mut.run_test(
        name=f"cohere-classification-run-{rnd}",
        scenario=scenario,
        api_key=os.environ["COHERE_API_KEY"],
        calculate_metrics=True,
    )
    assert run_resp.name == f"cohere-classification-run-{rnd}"


@pytest.fixture(scope="module")
def question_scenario_set(rnd: str, okareo: Okareo) -> ScenarioSetResponse:
    file_path = os.path.join(
        os.path.dirname(__file__), "webbizz_retrieval_questions.jsonl"
    )
    articles: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path=file_path, scenario_name=f"ci-pinecone-cohere-{rnd}"
    )

    return articles


def test_run_test_cohere_pinecone_ir(
    rnd: str, okareo: Okareo, question_scenario_set: ScenarioSetResponse
) -> None:
    mut = okareo.register_model(
        name=f"ci-pinecone-cohere-english-light-v3.0-{rnd}",
        model=[
            CohereModel(
                model_id="embed-english-light-v3.0",
                model_type="embed",
                input_type="search_query",
            ),
            PineconeDb(
                index_name="my-test-index",
                region="gcp-starter",
                project_id="kwnp6kx",
                top_k=3,
            ),
        ],
    )

    run_resp = mut.run_test(
        name=f"ci-pinecone-cohere-embed-{rnd}",
        scenario=question_scenario_set,
        calculate_metrics=True,
        test_run_type=TestRunType.INFORMATION_RETRIEVAL,
        api_keys={
            "cohere": os.environ["COHERE_API_KEY"],
            "pinecone": os.environ["PINECONE_API_KEY"],
        },
        metrics_kwargs={
            "mrr_at_k": [2, 4, 8],
            "map_at_k": [1, 2],
        },
    )
    assert run_resp.name == f"ci-pinecone-cohere-embed-{rnd}"


def test_run_test_cohere_qdrant_ir(
    rnd: str, okareo: Okareo, question_scenario_set: ScenarioSetResponse
) -> None:
    mut = okareo.register_model(
        name=f"ci-qdrant-cohere-english-light-v3.0-{rnd}",
        model=[
            CohereModel(
                model_id="embed-english-light-v3.0",
                model_type="embed",
                input_type="search_query",
            ),
            QdrantDB(
                collection_name="ci_test_collection",
                url="https://366662aa-e06e-4d40-a1d0-dc6aedbef44e.us-east4-0.gcp.cloud.qdrant.io:6333",
                top_k=10,
            ),
        ],
    )

    run_resp = mut.run_test(
        name=f"ci-qdrant-cohere-embed-{rnd}",
        scenario=question_scenario_set,
        calculate_metrics=True,
        test_run_type=TestRunType.INFORMATION_RETRIEVAL,
        api_keys={
            "cohere": os.environ["COHERE_API_KEY"],
            "qdrant": os.environ["QDRANT_API_KEY"],
        },
        metrics_kwargs={
            "mrr_at_k": [2, 4, 8, 16],
            "map_at_k": [1, 3, 5, 10, 20],
        },
    )
    assert run_resp.name == f"ci-qdrant-cohere-embed-{rnd}"


def test_run_test_checks(
    rnd: str, okareo: Okareo, article_scenario_set: ScenarioSetResponse
) -> None:
    generate_request = EvaluatorSpecRequest(
        description="""
        Return True if the model_output is at least 20 characters long, otherwise return False.""",
        requires_scenario_input=False,
        requires_scenario_result=False,
        output_data_type="bool",
    )
    check = okareo.generate_evaluator(generate_request)

    assert check.generated_code

    random_string = "".join(random.choices(string.ascii_letters, k=5))
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "sample_evaluator.py")
    with open(file_path, "w+") as file:
        file.write(check.generated_code)
    uploaded_evaluator = okareo.upload_evaluator(
        name=f"test_upload_check_{random_string}",
        file_path=file_path,
        requires_scenario_input=False,
        requires_scenario_result=False,
        output_data_type="bool",
    )
    os.remove(file_path)
    assert uploaded_evaluator.id
    assert uploaded_evaluator.name
    # TODO: Remove this once old evaluators are deprecated
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "sample_evaluator.py")
    with open(file_path, "w+") as file:
        file.write(
            """
# This is to bypass validation
class BaseCheck:
    def b():
        return True
class Check(BaseCheck):
    def a():
        return True
def evaluate(model_output: str) -> bool:
    return True if len(model_output) >= 20 else False
"""
        )
    manual_old_evaluator = okareo.upload_evaluator(
        name=f"test_upload_check_manual_{random_string}",
        file_path=file_path,
        requires_scenario_input=False,
        requires_scenario_result=False,
        output_data_type="bool",
    )
    os.remove(file_path)

    assert manual_old_evaluator.id
    assert manual_old_evaluator.name

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
        scenario=article_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
        checks=[uploaded_evaluator.id, manual_old_evaluator.id],
    )

    assert run_resp.name == f"openai-chat-run-{rnd}"
    assert run_resp.model_metrics is not None and not isinstance(
        run_resp.model_metrics, Unset
    )
    metrics_dict = run_resp.model_metrics.to_dict()

    assert metrics_dict["mean_scores"] is not None
    assert metrics_dict["scores_by_row"] is not None
    for row in metrics_dict["scores_by_row"]:
        dimension_keys = [
            f"test_upload_check_{random_string}",
            f"test_upload_check_manual_{random_string}",
        ]
        for dimension in dimension_keys:
            assert dimension in row
        assert row[dimension_keys[0]] == row[dimension_keys[1]]
    okareo.delete_evaluator(manual_old_evaluator.id, manual_old_evaluator.name)
    okareo.delete_evaluator(uploaded_evaluator.id, uploaded_evaluator.name)


def test_run_test_predefined_checks_levenshtein(
    rnd: str, okareo: Okareo, article_scenario_set: ScenarioSetResponse
) -> None:
    mut = okareo.register_model(
        name=f"openai-ci-run-levenshtein-{rnd}",
        model=OpenAIModel(
            model_id="gpt-3.5-turbo",
            temperature=0,
            system_prompt_template=TEST_SUMMARIZE_TEMPLATE,
            user_prompt_template=None,
        ),
    )

    checks = [
        "levenshtein_distance",
        "levenshtein_distance_input",
        "compression_ratio",
        "does_code_compile",
        "contains_all_imports",
    ]
    run_resp = mut.run_test(
        name=f"openai-chat-run-levenshtein-{rnd}",
        scenario=article_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        checks=checks,
        calculate_metrics=True,
    )
    assert run_resp.name == f"openai-chat-run-levenshtein-{rnd}"
    assert_metrics(run_resp, checks)
