import os
import random
import string
import tempfile
from typing import Any, List, Union

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import (
    CohereModel,
    CustomModel,
    ModelInvocation,
    OpenAIModel,
    PineconeDb,
    QdrantDB,
)
from okareo_api_client.api.default import (
    find_test_data_points_v0_find_test_data_points_post,
    update_test_data_point_v0_update_test_data_point_post,
)
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


def test_okareo_client_integration() -> None:
    with pytest.raises(Exception, match="Okareo"):
        Okareo(api_key="")


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
    skip_keys = ["scenario_index", "test_id"]
    assert len(dimension_keys) == len([k for k in scores.keys() if k not in skip_keys])
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


def test_run_test_cohere_pinecone_ir_tags(
    rnd: str, okareo: Okareo, question_scenario_set: ScenarioSetResponse
) -> None:
    mut = okareo.register_model(
        name=f"ci-pinecone-cohere-english-light-tags-test-v3.0-{rnd}-{1}",
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
    test_data_points = find_test_data_points_v0_find_test_data_points_post.sync(
        client=okareo.client,
        json_body=find_test_data_points_v0_find_test_data_points_post.FindTestDataPointPayload(
            test_run_id=run_resp.id
        ),
        api_key=API_KEY,
    )
    assert isinstance(test_data_points, list)
    update_test_data_point_v0_update_test_data_point_post.sync(
        client=okareo.client,
        json_body=update_test_data_point_v0_update_test_data_point_post.UpdateTestDataPointPayload(
            tags=["ci-testing"],
            id=test_data_points[0].id,
        ),
        api_key=API_KEY,
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
    new_test_data_points = find_test_data_points_v0_find_test_data_points_post.sync(
        client=okareo.client,
        json_body=find_test_data_points_v0_find_test_data_points_post.FindTestDataPointPayload(
            test_run_id=run_resp.id
        ),
        api_key=API_KEY,
    )
    assert isinstance(new_test_data_points, list)
    assert test_data_points[0].id != new_test_data_points[0].id
    assert new_test_data_points[0].tags == ["ci-testing"]
    assert run_resp.name == f"ci-pinecone-cohere-embed-{rnd}"
    mut = okareo.register_model(
        name=f"ci-pinecone-cohere-english-light-tags-test-v3.0-{rnd}-{1}",
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
                top_k=1,
            ),
        ],
        update=True,
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
    new_test_data_points_no_tag = find_test_data_points_v0_find_test_data_points_post.sync(
        client=okareo.client,
        json_body=find_test_data_points_v0_find_test_data_points_post.FindTestDataPointPayload(
            test_run_id=run_resp.id
        ),
        api_key=API_KEY,
    )
    assert isinstance(new_test_data_points_no_tag, list)
    assert new_test_data_points_no_tag[0].tags != ["ci-testing"]


def test_run_test_custom_ir_tags(
    rnd: str, okareo: Okareo, question_scenario_set: ScenarioSetResponse
) -> None:
    def query_results_to_score(results: Any) -> Any:
        parsed_ids_with_scores = []
        for i in range(0, len(results["distances"][0])):
            # this turns cosine distance into a cosine similarity score
            score = (2 - results["distances"][0][i]) / 2
            parsed_ids_with_scores.append(
                {
                    "id": results["ids"][0][i],
                    "score": score,
                    "metadata": results["metadatas"][0][i],
                    "label": f"{results['metadatas'][0][i]['article_type']} WebBizz Article w/ ID: {results['ids'][0][i]}",
                }
            )
        return parsed_ids_with_scores

    class RetrievalModel(CustomModel):
        def invoke(self, model_input: Any) -> ModelInvocation:
            results = {
                "ids": [
                    [
                        "ac0d464c-f673-44b8-8195-60c965e47525",
                        "75eaa363-dfcc-499f-b2af-1407b43cb133",
                        "35a4fd5b-453e-4ca6-9536-f20db7303344",
                        "aacf7a34-9d3a-4e2a-9a5c-91f2a0e8a12d",
                        "f1a37b5e-58c4-4f5a-bc42-1b70253b8bf3",
                    ]
                ],
                "distances": [
                    [
                        0.33011454343795776,
                        0.3649076819419861,
                        0.43849390745162964,
                        0.45827627182006836,
                        0.466469943523407,
                    ]
                ],
                "metadatas": [
                    [
                        {"article_type": "Miscellaneous"},
                        {"article_type": "Support"},
                        {"article_type": "Support"},
                        {"article_type": "Miscellaneous"},
                        {"article_type": "Miscellaneous"},
                    ]
                ],
                "embeddings": None,
                "uris": None,
                "data": None,
            }
            query_results = query_results_to_score(results)
            query_results.sort(key=lambda x: x["id"], reverse=True)
            return ModelInvocation(
                model_prediction=query_results,
                model_output_metadata={"model_data": model_input},
            )

    mut = okareo.register_model(
        name=f"ci-custom-{rnd}", model=RetrievalModel(name="custom retrieval")
    )

    run_resp = mut.run_test(
        name=f"ci-custom-{rnd}",
        scenario=question_scenario_set,
        calculate_metrics=True,
        test_run_type=TestRunType.INFORMATION_RETRIEVAL,
        metrics_kwargs={
            "mrr_at_k": [2, 4, 8],
            "map_at_k": [1, 2],
        },
    )
    test_data_points = find_test_data_points_v0_find_test_data_points_post.sync(
        client=okareo.client,
        json_body=find_test_data_points_v0_find_test_data_points_post.FindTestDataPointPayload(
            test_run_id=run_resp.id
        ),
        api_key=API_KEY,
    )
    assert isinstance(test_data_points, list)
    update_test_data_point_v0_update_test_data_point_post.sync(
        client=okareo.client,
        json_body=update_test_data_point_v0_update_test_data_point_post.UpdateTestDataPointPayload(
            tags=["ci-testing"],
            id=test_data_points[0].id,
        ),
        api_key=API_KEY,
    )
    run_resp = mut.run_test(
        name=f"ci-custom-{rnd}",
        scenario=question_scenario_set,
        calculate_metrics=True,
        test_run_type=TestRunType.INFORMATION_RETRIEVAL,
        metrics_kwargs={
            "mrr_at_k": [2, 4, 8],
            "map_at_k": [1, 2],
        },
    )
    new_test_data_points = find_test_data_points_v0_find_test_data_points_post.sync(
        client=okareo.client,
        json_body=find_test_data_points_v0_find_test_data_points_post.FindTestDataPointPayload(
            test_run_id=run_resp.id
        ),
        api_key=API_KEY,
    )
    assert isinstance(new_test_data_points, list)
    assert test_data_points[0].id != new_test_data_points[0].id
    assert new_test_data_points[0].tags == ["ci-testing"]

    class RetrievalModelNew(CustomModel):
        def invoke(self, model_input: Any) -> ModelInvocation:
            results = {
                "ids": [
                    [
                        "ac0d464c-f673-44b8-8195-60c965e47525",
                        "75eaa363-dfcc-499f-b2af-1407b43cb133",
                        "35a4fd5b-453e-4ca6-9536-f20db7303344",
                        "aacf7a34-9d3a-4e2a-9a5c-91f2a0e8a12d",
                        "f1a37b5e-58c4-4f5a-bc42-1b70253b8bf3",
                    ]
                ],
                "distances": [
                    [
                        0.33011454343795776,
                        0.3649076819419861,
                        0.43849390745162964,
                        0.45827627182006836,
                        0.466469943523407,
                    ]
                ],
                "metadatas": [
                    [
                        {"article_type": "Miscellaneous"},
                        {"article_type": "Support"},
                        {"article_type": "Support"},
                        {"article_type": "Miscellaneous"},
                        {"article_type": "Miscellaneous"},
                    ]
                ],
                "embeddings": None,
                "uris": None,
                "data": None,
            }
            query_results = query_results_to_score(results)
            query_results.sort(key=lambda x: x["id"], reverse=False)
            return ModelInvocation(
                model_prediction=query_results,
                model_output_metadata={"model_data": model_input},
            )

    mut = okareo.register_model(
        name=f"ci-custom-{rnd}",
        model=RetrievalModelNew(name="custom retrieval"),
        update=True,
    )
    run_resp = mut.run_test(
        name=f"ci-custom-{rnd}",
        scenario=question_scenario_set,
        calculate_metrics=True,
        test_run_type=TestRunType.INFORMATION_RETRIEVAL,
        metrics_kwargs={
            "mrr_at_k": [2, 4, 8],
            "map_at_k": [1, 2],
        },
    )
    new_test_data_points_no_tag = find_test_data_points_v0_find_test_data_points_post.sync(
        client=okareo.client,
        json_body=find_test_data_points_v0_find_test_data_points_post.FindTestDataPointPayload(
            test_run_id=run_resp.id
        ),
        api_key=API_KEY,
    )
    assert isinstance(new_test_data_points_no_tag, list)
    assert new_test_data_points_no_tag[0].tags != ["ci-testing"]


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
    checks_to_generate = [
        {
            "description": "Return True if the model_output is at least 20 characters long, otherwise return False.",
            "requires_scenario_input": False,
            "requires_scenario_result": False,
            "name": "model_only",
        },
        {
            "description": "Return True if the scenario_result is at least 20 characters long, otherwise return False.",
            "requires_scenario_input": False,
            "requires_scenario_result": True,
            "name": "model_with_result",
        },
        {
            "description": "Return True if the scenario_input is at least 20 characters long, otherwise return False.",
            "requires_scenario_input": True,
            "requires_scenario_result": False,
            "name": "model_with_input",
        },
        {
            "description": "Return True if the combined length of the scenario_input and scenario_result is at least 20 characters long, otherwise return False.",
            "requires_scenario_input": True,
            "requires_scenario_result": True,
            "name": "model_with_input_and_result",
        },
    ]
    uploaded_checks = []
    random_string = "".join(random.choices(string.ascii_letters, k=5))
    for check_dict in checks_to_generate:
        generate_request = EvaluatorSpecRequest(
            description=str(check_dict["description"]),
            requires_scenario_input=bool(check_dict["requires_scenario_input"]),
            requires_scenario_result=bool(check_dict["requires_scenario_result"]),
            output_data_type="bool",
        )
        check = okareo.generate_check(generate_request)

        assert check.generated_code

        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, "sample_evaluator.py")
        with open(file_path, "w+") as file:
            file.write(check.generated_code)
        uploaded_check = okareo.upload_check(
            name=f"test_upload_check_{check_dict['name']}_{random_string}",
            file_path=file_path,
            requires_scenario_input=bool(check_dict["requires_scenario_input"]),
            requires_scenario_result=bool(check_dict["requires_scenario_result"]),
            output_data_type="bool",
        )
        os.remove(file_path)
        assert uploaded_check.id
        assert uploaded_check.name
        uploaded_checks.append(uploaded_check)
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
    manual_old_check = okareo.upload_check(
        name=f"test_upload_check_manual_{random_string}",
        file_path=file_path,
        requires_scenario_input=False,
        requires_scenario_result=False,
        output_data_type="bool",
    )
    os.remove(file_path)

    assert manual_old_check.id
    assert manual_old_check.name
    uploaded_checks.append(manual_old_check)

    mut = okareo.register_model(
        name=f"openai-ci-run-{rnd}",
        model=OpenAIModel(
            model_id="gpt-3.5-turbo",
            temperature=0,
            system_prompt_template=TEST_SUMMARIZE_TEMPLATE,
            user_prompt_template=None,
        ),
    )

    check_ids = [str(check.id) for check in uploaded_checks]
    check_names = [str(check.name) for check in uploaded_checks]
    run_resp = mut.run_test(
        name=f"openai-chat-run-{rnd}",
        scenario=article_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
        checks=check_ids,
    )

    assert run_resp.name == f"openai-chat-run-{rnd}"
    assert run_resp.model_metrics is not None and not isinstance(
        run_resp.model_metrics, Unset
    )
    metrics_dict = run_resp.model_metrics.to_dict()

    assert metrics_dict["mean_scores"] is not None
    assert metrics_dict["scores_by_row"] is not None
    for row in metrics_dict["scores_by_row"]:
        dimension_keys = [c.name for c in uploaded_checks]
        for dimension in dimension_keys:
            assert dimension in row
        assert row[dimension_keys[0]] == row[dimension_keys[1]]

    for c_name, c_id in zip(check_names, check_ids):
        okareo.delete_check(c_id, str(c_name))


def test_run_test_predefined_checks(
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
        "corpus_BLEU",
    ]
    run_resp = mut.run_test(
        name=f"openai-chat-run-predefined-{rnd}",
        scenario=article_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        checks=checks,
        calculate_metrics=True,
    )
    assert run_resp.name == f"openai-chat-run-predefined-{rnd}"
    assert_metrics(run_resp, checks)
