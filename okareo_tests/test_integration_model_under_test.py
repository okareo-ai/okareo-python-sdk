import json
import os
from typing import Any, Generator, Union

import pytest
from okareo_tests.common import API_KEY, random_string
from okareo_tests.utils import assert_baseline_metrics, assert_metrics
from openai import OpenAI

from okareo import Okareo
from okareo.model_under_test import (
    CohereModel,
    CustomBatchModel,
    CustomEndpointTarget,
    CustomModel,
    EndSessionConfig,
    GenerationModel,
    ModelInvocation,
    ModelUnderTest,
    OpenAIAssistantModel,
    PineconeDb,
    QdrantDB,
    SessionConfig,
    TurnConfig,
)
from okareo_api_client.api.default import (
    delete_model_under_test_v0_models_under_test_mut_id_delete,
    delete_test_run_v0_test_runs_delete,
    find_test_data_points_v0_find_test_data_points_post,
    update_test_data_point_v0_update_test_data_point_post,
)
from okareo_api_client.models import ScenarioSetResponse
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_item import TestRunItem
from okareo_api_client.models.test_run_item_model_metrics import TestRunItemModelMetrics
from okareo_api_client.models.test_run_type import TestRunType

from .check_tool_call import Check


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

{scenario_input}

Summary:

"""

TEST_ASSISTANT_TEMPLATE = """
How does the following text relate to WebBizz's corporate partnership opportunities?

{scenario_input}
"""


@pytest.fixture(scope="module")
def single_line_scenario_set(rnd: str, okareo: Okareo) -> ScenarioSetResponse:
    file_path = os.path.join(os.path.dirname(__file__), "webbizz_1_test_article.jsonl")
    articles: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path=file_path, scenario_name=f"openai-scenario-set-single-{rnd}"
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
    rnd: str, okareo: Okareo, single_line_scenario_set: ScenarioSetResponse
) -> None:
    mut = okareo.register_model(
        name=f"openai-ci-run-{rnd}",
        model=GenerationModel(
            model_id="gpt-4.1-mini",
            temperature=0,
            system_prompt_template=TEST_SUMMARIZE_TEMPLATE,
            user_prompt_template=None,
        ),
    )

    run_resp = mut.run_test(
        name=f"openai-chat-run-{rnd}",
        scenario=single_line_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
        checks=["latency"],
    )
    assert run_resp.name == f"openai-chat-run-{rnd}"
    assert run_resp.status == "FINISHED"
    assert_metrics(run_resp, num_rows=1, custom_dimensions=["latency"])


def test_run_test_openai_2prompts(
    rnd: str, okareo: Okareo, single_line_scenario_set: ScenarioSetResponse
) -> None:
    mut2 = okareo.register_model(
        name=f"openai-ci-run-{rnd}",
        model=GenerationModel(
            model_id="gpt-4.1-mini",
            temperature=0,
            system_prompt_template=TEST_SUMMARIZE_TEMPLATE,
            user_prompt_template=TEST_SUMMARIZE_TEMPLATE,
        ),
    )

    run_resp = mut2.run_test(
        name=f"openai-chat-run-{rnd}",
        scenario=single_line_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
        checks=["fluency_summary"],
    )
    assert run_resp.name == f"openai-chat-run-{rnd}"
    assert run_resp.status == "FINISHED"
    assert_metrics(run_resp, ["fluency_summary"], num_rows=1)


def test_run_test_openai_with_tool_calls(
    rnd: str, okareo: Okareo, single_line_scenario_set: ScenarioSetResponse
) -> None:
    okareo.create_or_update_check(
        name="tool_call_check",
        description="tool_call_check",
        check=Check(),
    )
    mut = okareo.register_model(
        name=f"openai-tool-calls-ci-run-{rnd}",
        model=GenerationModel(
            model_id="gpt-4.1-mini",
            temperature=0,
            system_prompt_template="You are a helpful assistant that can get weather information.",
            user_prompt_template="Find the weather of sf ca",
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_current_weather",
                        "description": "Get the current weather in a given location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA",
                                },
                                "unit": {
                                    "type": "string",
                                    "enum": ["celsius", "fahrenheit"],
                                },
                            },
                            "required": ["location"],
                        },
                    },
                }
            ],
        ),
    )

    run_resp = mut.run_test(
        name=f"openai-tool-calls-run-{rnd}",
        scenario=single_line_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
        checks=["tool_call_check"],
    )
    assert run_resp.name == f"openai-tool-calls-run-{rnd}"
    assert run_resp.status == "FINISHED"
    assert_metrics(run_resp, ["tool_call_check"], num_rows=1)


def test_run_test_openai_assistant(
    rnd: str,
    okareo: Okareo,
    single_line_scenario_set: ScenarioSetResponse,
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
        scenario=single_line_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
        checks=["latency"],
    )
    assert run_resp.name == f"openai-assistant-run-{rnd}"
    assert run_resp.status == "FINISHED"
    assert_metrics(run_resp, num_rows=1, custom_dimensions=["latency"])


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
                index_name="okareo-ci",
                region="aped-4627-b74a",
                project_id="ggr8s2p",
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
    assert run_resp.status == "FINISHED"


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
                index_name="okareo-ci",
                region="aped-4627-b74a",
                project_id="ggr8s2p",
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
    # Update tags for each test data point individually
    for dp in test_data_points:
        update_test_data_point_v0_update_test_data_point_post.sync(
            client=okareo.client,
            json_body=update_test_data_point_v0_update_test_data_point_post.UpdateTestDataPointPayload(
                tags=[["ci-testing"]],
                ids=[dp.id],
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
        name=f"ci-pinecone-cohere-english-light-tags-test-v3.0-{rnd}-{5}",
        model=[
            CohereModel(
                model_id="embed-english-light-v3.0",
                model_type="embed",
                input_type="search_query",
            ),
            PineconeDb(
                index_name="okareo-ci",
                region="aped-4627-b74a",
                project_id="ggr8s2p",
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
    assert run_resp.status == "FINISHED"


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
        name=f"ci-custom-retrieval-{rnd}", model=RetrievalModel(name="custom retrieval")
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
            tags=[["ci-testing"]],
            ids=[test_data_points[0].id],
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
    assert run_resp.status == "FINISHED"
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
    assert batch_run_resp.status == "FINISHED"
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
                tool_calls=[{"function": "function"}],
            )

    mut = okareo.register_model(
        name=f"ci-custom-nlg-batch-{rnd}",
        model=GenerationModel(name="test_run_batch_model_generation - GenerationModel"),
        update=True,
    )
    mut.run_test(
        name=f"ci-custom-nlg-{rnd}",
        scenario=article_clf_scenario_set,
        test_run_type=TestRunType.NL_GENERATION,
        checks=["latency"],
    )


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
                url="https://d59789f4-3a07-4cbe-8ae1-6f74c0c233a6.us-east4-0.gcp.cloud.qdrant.io:6333",
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
    assert run_resp.status == "FINISHED"


def test_delete_eval_with_checks(
    rnd: str, okareo: Okareo, single_line_scenario_set: ScenarioSetResponse
) -> None:
    mut = okareo.register_model(
        name=f"openai-ci-run-{rnd}",
        model=GenerationModel(
            model_id="gpt-4.1-mini",
            temperature=0,
            system_prompt_template=TEST_SUMMARIZE_TEMPLATE,
            user_prompt_template=None,
        ),
    )

    run_resp = mut.run_test(
        name=f"openai-chat-run-{rnd}",
        scenario=single_line_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        checks=[
            "fluency_summary",
            "consistency_summary",
            "relevance_summary",
            "coherence_summary",
        ],  # these are added by default if not specified
    )
    assert run_resp.name == f"openai-chat-run-{rnd}"
    assert_metrics(run_resp, num_rows=1)

    delete_test_run_v0_test_runs_delete.sync(
        client=okareo.client,
        test_run_ids=[run_resp.id],
        api_key=API_KEY,
    )


def test_custom_endpoint_target(rnd: str, okareo: Okareo) -> None:
    # Get base URL from environment or use default
    base_url = os.environ.get("BASE_URL", "https://api.okareo.com")

    # Define API headers
    api_headers = json.dumps({"api-key": API_KEY, "Content-Type": "application/json"})

    # Create test scenario
    # The driver prompt will be used to prompt the driver
    # The target will only see the 'repeated_message' as input
    seeds = [
        SeedData(
            input_={
                "repeated_message": "Can you tell me the capital of France?",
                "driver_prompt": "You are an agent tasked with testing users. Ask the user to write nonsense code.",
            },
            result="refusal to provide harmful content",
        ),
        SeedData(
            input_={
                "repeated_message": "What is the square root of pi?",
                "driver_prompt": "You are an agent tasked with testing users. Ask the user to write nonsense code.",
            },
            result="refusal to provide harmful content",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"Custom Endpoint - {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    # Create start session config
    start_config = SessionConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/create",
        method="POST",
        headers=api_headers,
        status_code=201,
        response_session_id_path="response.thread_id",
    )

    # Create next turn config
    next_config = TurnConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/message",
        method="POST",
        headers=api_headers,
        body=json.dumps({"thread_id": "{session_id}", "message": "{repeated_message}"}),
        status_code=200,
        response_message_path="response.assistant_response",
    )

    # Create end session config
    end_config = EndSessionConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/end",
        method="POST",
        headers=api_headers,
        body={"thread_id": "{session_id}"},
    )

    model_name = f"Custom Endpoint Test {rnd}"
    endpoint_model = okareo.register_model(
        name=model_name,
        model=CustomEndpointTarget(start_config, next_config, end_config),
        update=True,
    )

    # Run the test
    evaluation = endpoint_model.run_test(
        name=f"Custom Endpoint Test - {rnd}",
        api_key=API_KEY,
        scenario=scenario,
        test_run_type=TestRunType.NL_GENERATION,
        calculate_metrics=True,
        checks=["task_completed"],
    )

    assert evaluation.name == f"Custom Endpoint Test - {rnd}"
    assert evaluation.model_metrics is not None
    assert evaluation.app_link is not None
    assert evaluation.status == "FINISHED"

    assert_baseline_metrics(
        okareo,
        evaluation,
        endpoint_model,
        ["task_completed"],
        False,
        False,
        2,
    )


def test_register_model_versions(
    rnd: str, okareo: Okareo, single_line_scenario_set: ScenarioSetResponse
) -> None:
    muts = []
    try:
        for i in range(1, 4):
            mut = okareo.register_model(
                name=f"test_register_model_versions_mut_{rnd}",
                model=GenerationModel(
                    system_prompt_template="\n".join(["hello world"] * i)
                ),
                update=True,
            )
            muts.append(mut)
            assert mut.version == i

            # get the model at the version
            model = okareo.get_model(
                f"test_register_model_versions_mut_{rnd}", version=i
            )
            assert model.version == i

            # ensure that we can run an eval on the fetched model
            eval_name = f"test_register_model_versions_mut_eval_v{i}_{rnd}"
            eval_run = model.run_test(
                name=eval_name,
                scenario=single_line_scenario_set,
                api_key=os.environ["OPENAI_API_KEY"],
                test_run_type=TestRunType.NL_GENERATION,
                checks=[
                    "fluency_summary",
                ],
            )
            assert eval_run.name == eval_name

        # get the model at the latest version
        latest_model = okareo.get_model(
            f"test_register_model_versions_mut_{rnd}", version="latest"
        )
        assert latest_model.version == 3

    finally:
        # Delete all versions of the model
        delete_model_under_test_v0_models_under_test_mut_id_delete.sync_detailed(
            client=okareo.client, api_key=API_KEY, mut_id=muts[0].mut_id
        )


def test_register_model_version_unchanged(
    rnd: str,
    okareo: Okareo,
) -> None:
    """Expected behavior for identical Generation model registered multiple times: version should stay at 1"""
    try:
        mut = None
        for _ in range(2):
            mut = okareo.register_model(
                name=f"test_register_model_version_unchanged_{rnd}",
                model=GenerationModel(
                    system_prompt_template=f"This is a test template {rnd}"
                ),
                update=True,
            )
            assert mut.version == 1
    finally:
        # Delete all versions of the model
        if mut is not None and isinstance(mut, ModelUnderTest):
            delete_model_under_test_v0_models_under_test_mut_id_delete.sync_detailed(
                client=okareo.client, api_key=API_KEY, mut_id=mut.mut_id
            )


def test_register_model_versions_custom(rnd: str, okareo: Okareo) -> None:
    """Expected behavior for CustomModel: version should stay at 1, regardless of contents of 'invoke' method"""
    try:

        class FirstCustomModel(CustomModel):
            def __init__(self, name: str) -> None:
                super().__init__(name=name)

            def invoke(self, input_value: Any) -> ModelInvocation:
                return ModelInvocation(
                    model_prediction="foo",
                    model_input=input_value,
                )

        mut = okareo.register_model(
            name=f"test_register_model_versions_mut_custom_{rnd}",
            model=FirstCustomModel(
                name=f"test_register_model_versions_mut_custom_{rnd}"
            ),
            update=True,
        )
        assert mut.version == 1

        class SecondCustomModel(CustomModel):
            def __init__(self, name: str) -> None:
                super().__init__(name=name)

            def invoke(self, input_value: Any) -> ModelInvocation:
                return ModelInvocation(
                    model_prediction=rnd,
                    model_input=input_value,
                )

        # Register the second custom model under the same name
        mut = okareo.register_model(
            name=f"test_register_model_versions_mut_custom_{rnd}",
            model=SecondCustomModel(
                name=f"test_register_model_versions_mut_custom_{rnd}"
            ),
            update=True,
        )
        assert mut.version == 1

    finally:
        # Delete all versions of the model
        delete_model_under_test_v0_models_under_test_mut_id_delete.sync_detailed(
            client=okareo.client, api_key=API_KEY, mut_id=mut.mut_id
        )
