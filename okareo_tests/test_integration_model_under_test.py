import os

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import CohereModel, OpenAIModel, PineconeDb
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.scenario_type import ScenarioType
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_item import TestRunItem
from okareo_api_client.models.test_run_type import TestRunType
from okareo_api_client.types import Unset


@pytest.fixture
def rnd() -> str:
    return random_string(5)


@pytest.fixture
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


TEST_SUMMARIZE_TEMPLATE = """
Provide a brief summary of the following paragraph of text:

{input}

Summary:

"""


def test_run_test_v2_openai(rnd: str, okareo: Okareo) -> None:
    file_path = os.path.join(os.path.dirname(__file__), "webbizz_3_test_article.jsonl")
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

    run_resp = mut.run_test_v2(
        name=f"openai-chat-run-{rnd}",
        scenario=scenario,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
    )
    assert run_resp.name == f"openai-chat-run-{rnd}"
    assert_metrics(run_resp)


def test_run_test_v2_openai_2prompts(rnd: str, okareo: Okareo) -> None:
    file_path = os.path.join(os.path.dirname(__file__), "webbizz_3_test_article.jsonl")
    scenario = okareo.upload_scenario_set(
        file_path=file_path, scenario_name=f"openai-scenario-set-{rnd}"
    )

    mut2 = okareo.register_model(
        name=f"openai-ci-run-{rnd}",
        model=OpenAIModel(
            model_id="gpt-3.5-turbo",
            temperature=0,
            system_prompt_template=TEST_SUMMARIZE_TEMPLATE,
            user_prompt_template=TEST_SUMMARIZE_TEMPLATE,
        ),
    )

    run_resp = mut2.run_test_v2(
        name=f"openai-chat-run-{rnd}",
        scenario=scenario,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
    )
    assert run_resp.name == f"openai-chat-run-{rnd}"
    assert_metrics(run_resp)


def assert_metrics(run_resp: TestRunItem) -> None:
    assert run_resp.model_metrics is not None and not isinstance(
        run_resp.model_metrics, Unset
    )
    metrics_dict = run_resp.model_metrics.to_dict()

    assert metrics_dict["mean_scores"] is not None
    assert_scores(metrics_dict["mean_scores"])
    assert metrics_dict["scores_by_row"] is not None
    assert len(metrics_dict["scores_by_row"]) == 3
    for row in metrics_dict["scores_by_row"]:
        assert_scores(row)


def assert_scores(scores: dict) -> None:
    dimension_keys = ["consistency", "coherence", "fluency", "relevance", "overall"]
    for dimension in dimension_keys:
        assert dimension in scores
        assert isinstance(scores[dimension], float)
        assert 1 <= scores[dimension] <= 5


def test_run_test_v2_cohere(rnd: str, okareo: Okareo) -> None:
    seed_data = [
        SeedData(input_="are you able to set up in aws?", result="capabilities"),
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
        number_examples=1,
        seed_data=seed_data,
        generation_type=ScenarioType.REPHRASE_INVARIANT,
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    mut = okareo.register_model(
        name=f"classification-cohere-ci-{rnd}",
        model=CohereModel(
            model_id="2386d4d1-c617-4183-8c87-5550c7f222e6-ft",
            model_type="classify",
        ),
    )

    run_resp = mut.run_test_v2(
        name=f"cohere-classification-run-{rnd}",
        scenario=scenario,
        api_key=os.environ["COHERE_API_KEY"],
        calculate_metrics=True,
    )
    assert run_resp.name == f"cohere-classification-run-{rnd}"


def test_run_test_v2_cohere_info_retrieval(rnd: str, okareo: Okareo) -> None:
    seed_data = [
        SeedData(
            input_="which IAM groups have access to s3?",
            result="3cee94071d1bbbac096c0996987d8bb2",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"ci-pinecone-cohere-{rnd}",
        number_examples=1,
        seed_data=seed_data,
        generation_type=ScenarioType.TEXT_REVERSE_QUESTION,
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    mut = okareo.register_model(
        name=f"embed-english-light-v3.0-{rnd}",
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

    run_resp = mut.run_test_v2(
        name=f"ci-pinecone-cohere-embed-{rnd}",
        scenario=scenario,
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
