import os
from typing import Any, Generator, Union

import pytest
from okareo_tests.common import API_KEY, random_string
from okareo_tests.utils import assert_metrics
from openai import OpenAI

from okareo import Okareo
from okareo.model_under_test import (
    CohereModel,
    CustomBatchModel,
    CustomModel,
    ModelInvocation,
    OpenAIAssistantModel,
    OpenAIModel,
    PineconeDb,
    QdrantDB,
)
from okareo_api_client.api.default import (
    find_test_data_points_v0_find_test_data_points_post,
    update_test_data_point_v0_update_test_data_point_post,
)
from okareo_api_client.models import ScenarioSetResponse
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_item import TestRunItem
from okareo_api_client.models.test_run_item_model_metrics import TestRunItemModelMetrics
from okareo_api_client.models.test_run_type import TestRunType


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


@pytest.fixture(scope="module")
def openai_client() -> OpenAI:
    return OpenAI()


TEST_SUMMARIZE_TEMPLATE = """
Provide a brief summary of the following paragraph of text:

{input}

Summary:

"""

TEST_ASSISTANT_TEMPLATE = """
How does the following text relate to WebBizz's corporate partnership opportunities?

{input}
"""


@pytest.fixture(scope="module")
def article_scenario_set(rnd: str, okareo: Okareo) -> ScenarioSetResponse:
    file_path = os.path.join(os.path.dirname(__file__), "webbizz_3_test_article.jsonl")
    articles: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path=file_path, scenario_name=f"openai-scenario-set-{rnd}"
    )

    return articles


@pytest.fixture(scope="module")
def article_clf_scenario_set(rnd: str, okareo: Okareo) -> ScenarioSetResponse:
    file_path = os.path.join(
        os.path.dirname(__file__), "webbizz_3_test_article_classification.jsonl"
    )
    articles: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path=file_path, scenario_name=f"webbizz-clf-scenario-set-{rnd}"
    )

    return articles


@pytest.fixture(scope="module")
def openai_assistant_id(openai_client: OpenAI) -> Generator[str, None, None]:
    assistant = openai_client.beta.assistants.create(
        name="WebBizz B2B Lead Generation",
        instructions=(
            "You are a B2B sales associate for WebBizz, an online retail platform. You are responsible for generating leads for new corporate partnerships. Keep the following instructions in mind when answering questions:\n\n"
            + "Instructions:\n\n"
            "- Be friendly and helpful.\n"
            "- Be brief. Keep all your responses to 100 words or less.\n"
            "- Do not talk about topics that are outside of your context. If the user asks you to discuss irrelevant topics, then nudge them towards discussing corporate partnerships with WebBizz.\n"
            "- Highlight the advantages for prospective partners of choosing WebBizz as their preferred sales or distribution platform.\n"
            "- Do not under any circumstances mention direct competitors, especially not Amazine, Demu, or Olli Bobo.\n"
        ),
        model="gpt-4o",
    )
    yield assistant.id
    openai_client.beta.assistants.delete(assistant.id)


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
    assert_metrics(run_resp, num_rows=3)


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
    assert_metrics(run_resp, num_rows=3)


def test_run_test_openai_assistant(
    rnd: str,
    okareo: Okareo,
    article_scenario_set: ScenarioSetResponse,
    openai_assistant_id: str,
) -> None:
    mut = okareo.register_model(
        name=f"openai-assistant-ci-run-{rnd}",
        model=OpenAIAssistantModel(
            model_id=openai_assistant_id,
            user_prompt_template=TEST_ASSISTANT_TEMPLATE,
        ),
    )

    run_resp = mut.run_test(
        name=f"openai-assistant-run-{rnd}",
        scenario=article_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
    )
    assert run_resp.name == f"openai-assistant-run-{rnd}"
    assert_metrics(run_resp, num_rows=3)


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


def test_run_batch_model_classification(
    rnd: str, okareo: Okareo, article_clf_scenario_set: ScenarioSetResponse
) -> None:
    def classification_rules(model_input: str) -> str:
        if "customer support" in model_input:
            return "Support"
        elif "Safety and security" in model_input:
            return "Safety"
        elif "customer's feedback" in model_input:
            return "Feedback"
        else:
            return "Miscellaneous"

    class ClassificationModel(CustomModel):
        def invoke(self, input_value: Any) -> ModelInvocation:
            return ModelInvocation(
                model_prediction=classification_rules(input_value),
                model_input=input_value,
                model_output_metadata={"model_data": input_value},
            )

    mut = okareo.register_model(
        name=f"ci-custom-clf-{rnd}",
        model=ClassificationModel(
            name="test_run_batch_model_classification - ClassificationModel"
        ),
        update=True,
    )
    run_resp = mut.run_test(
        name=f"ci-custom-clf-{rnd}",
        scenario=article_clf_scenario_set,
        test_run_type=TestRunType.MULTI_CLASS_CLASSIFICATION,
    )
    assert isinstance(run_resp, TestRunItem)
    assert isinstance(run_resp.model_metrics, TestRunItemModelMetrics)
    clf_avg_results = run_resp.model_metrics.additional_properties["weighted_average"]

    class BatchClassificationModel(CustomBatchModel):
        def invoke_batch(
            self, input_batch: list[dict[str, Any]]
        ) -> list[dict[str, Union[str, ModelInvocation]]]:
            invocations = []
            for i in range(min(len(input_batch), self.batch_size)):
                input_value = input_batch[i]["input_value"]
                batch_id = input_batch[i]["id"]
                invocation = ModelInvocation(
                    model_prediction=classification_rules(input_value),
                    model_input=input_value,
                    model_output_metadata={"model_data": input_value},
                )
                invocations.append({"id": batch_id, "model_invocation": invocation})
            return invocations

    batch_mut = okareo.register_model(
        name=f"ci-custom-clf-batch-{rnd}",
        model=BatchClassificationModel(
            name="test_run_batch_model_classification - BatchClassificationModel",
            batch_size=2,
        ),
        update=True,
    )
    batch_run_resp = batch_mut.run_test(
        name=f"ci-custom-clf-batch-{rnd}",
        scenario=article_clf_scenario_set,
        test_run_type=TestRunType.MULTI_CLASS_CLASSIFICATION,
    )
    assert isinstance(batch_run_resp, TestRunItem)
    assert isinstance(batch_run_resp.model_metrics, TestRunItemModelMetrics)
    clf_batch_avg_results = batch_run_resp.model_metrics.additional_properties[
        "weighted_average"
    ]

    for key in clf_avg_results.keys():
        assert clf_avg_results[key] == clf_batch_avg_results[key]


def test_run_batch_model_generation(
    rnd: str, okareo: Okareo, article_clf_scenario_set: ScenarioSetResponse
) -> None:
    def generation_rules(model_input: str) -> str:
        # simple generation rules to ensure consistent model outputs
        out = [s.split(" ")[0] for s in model_input.split(". ")]
        return " ".join(out)

    class GenerationModel(CustomModel):
        def invoke(self, input_value: Any) -> ModelInvocation:
            return ModelInvocation(
                model_prediction=generation_rules(input_value),
                model_input=input_value,
                model_output_metadata={"model_data": input_value},
            )

    mut = okareo.register_model(
        name=f"ci-custom-nlg-{rnd}",
        model=GenerationModel(name="test_run_batch_model_generation - GenerationModel"),
        update=True,
    )
    run_resp = mut.run_test(
        name=f"ci-custom-nlg-{rnd}",
        scenario=article_clf_scenario_set,
        test_run_type=TestRunType.NL_GENERATION,
        checks=["compression_ratio"],
    )
    assert isinstance(run_resp, TestRunItem)
    assert isinstance(run_resp.model_metrics, TestRunItemModelMetrics)
    nlg_metrics = run_resp.model_metrics

    class GenerationBatchModel(CustomBatchModel):
        def invoke_batch(
            self, input_batch: list[dict[str, Any]]
        ) -> list[dict[str, Union[str, ModelInvocation]]]:
            invocations = []
            for i in range(min(len(input_batch), self.batch_size)):
                input_value = input_batch[i]["input_value"]
                batch_id = input_batch[i]["id"]
                invocation = ModelInvocation(
                    model_prediction=generation_rules(input_value),
                    model_input=input_value,
                    model_output_metadata={"model_data": input_value},
                )
                invocations.append({"id": batch_id, "model_invocation": invocation})
            return invocations

    batch_mut = okareo.register_model(
        name=f"ci-custom-nlg-batch-{rnd}",
        model=GenerationBatchModel(
            name="test_run_batch_model_generation - BatchGenerationModel",
            batch_size=2,
        ),
        update=True,
    )
    batch_run_resp = batch_mut.run_test(
        name=f"ci-custom-nlg-batch-{rnd}",
        scenario=article_clf_scenario_set,
        test_run_type=TestRunType.NL_GENERATION,
        checks=["compression_ratio"],
    )
    assert isinstance(batch_run_resp, TestRunItem)
    assert isinstance(batch_run_resp.model_metrics, TestRunItemModelMetrics)
    batch_nlg_metrics = batch_run_resp.model_metrics

    # assert avg metrics are equal
    cr = nlg_metrics.additional_properties["mean_scores"]["compression_ratio"]
    batch_cr = batch_nlg_metrics.additional_properties["mean_scores"][
        "compression_ratio"
    ]
    assert cr == batch_cr

    # assert row metrics are equal
    rows = nlg_metrics.additional_properties["scores_by_row"]
    batch_rows = batch_nlg_metrics.additional_properties["scores_by_row"]
    for row, batch_row in zip(rows, batch_rows):
        assert row["compression_ratio"] == batch_row["compression_ratio"]


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
