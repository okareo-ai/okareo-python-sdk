"""Live tests of the SDK's custom Target code: a custom model and a custom batch model that run in the test
process, through the blocking and the submit paths.

Each test deletes the Scenario, Targets and Runs it creates. Marked `live`: they call a real Okareo backend
and skip when OKAREO_API_KEY is unset.
"""

import os
from typing import Any, Union

import pytest
from okareo_tests.common import API_KEY, random_string
from okareo_tests.live_artifacts import LiveArtifacts

from okareo import Okareo
from okareo.model_under_test import CustomBatchModel, CustomModel, ModelInvocation
from okareo_api_client.models import ScenarioSetResponse
from okareo_api_client.models.test_run_item import TestRunItem
from okareo_api_client.models.test_run_item_model_metrics_type_0 import (
    TestRunItemModelMetricsType0,
)
from okareo_api_client.models.test_run_type import TestRunType

pytestmark = pytest.mark.live


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


@pytest.fixture
def article_clf_scenario_set(
    rnd: str, okareo: Okareo, created: LiveArtifacts
) -> ScenarioSetResponse:
    file_path = os.path.join(
        os.path.dirname(__file__), "webbizz_3_test_article_classification.jsonl"
    )
    name = f"webbizz-clf-scenario-set-{rnd}-{random_string(5)}"
    articles: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path=file_path, scenario_name=name
    )
    created.scenario(articles.scenario_id, name)

    return articles


def test_run_batch_model_classification(
    rnd: str,
    okareo: Okareo,
    article_clf_scenario_set: ScenarioSetResponse,
    created: LiveArtifacts,
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
    created.target(mut.mut_id)
    run_resp = mut.run_test(
        name=f"ci-custom-clf-{rnd}",
        scenario=article_clf_scenario_set,
        test_run_type=TestRunType.MULTI_CLASS_CLASSIFICATION,
    )
    created.run(run_resp.id)
    assert isinstance(run_resp, TestRunItem)
    assert isinstance(run_resp.model_metrics, TestRunItemModelMetricsType0)
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
    created.target(batch_mut.mut_id)
    batch_run_resp = batch_mut.run_test(
        name=f"ci-custom-clf-batch-{rnd}",
        scenario=article_clf_scenario_set,
        test_run_type=TestRunType.MULTI_CLASS_CLASSIFICATION,
    )
    created.run(batch_run_resp.id)
    assert isinstance(batch_run_resp, TestRunItem)
    assert isinstance(batch_run_resp.model_metrics, TestRunItemModelMetricsType0)
    assert batch_run_resp.status == "FINISHED"
    clf_batch_avg_results = batch_run_resp.model_metrics.additional_properties[
        "weighted_average"
    ]

    for key in clf_avg_results.keys():
        assert clf_avg_results[key] == clf_batch_avg_results[key]


def generation_rules(model_input: str) -> str:
    # simple generation rules to ensure consistent model outputs
    out = [s.split(" ")[0] for s in model_input.split(". ")]
    return " ".join(out)


class TestGenerationModel(CustomModel):
    def invoke(self, input_value: Any) -> ModelInvocation:
        return ModelInvocation(
            model_prediction=generation_rules(input_value),
            model_input=input_value,
            model_output_metadata={"model_data": input_value},
            tool_calls=[{"function": "function"}],
        )


def test_submit_model_generation(
    rnd: str,
    okareo: Okareo,
    article_clf_scenario_set: ScenarioSetResponse,
    created: LiveArtifacts,
) -> None:
    mut = okareo.register_model(
        name=f"ci-custom-nlg-batch-submit-{rnd}",
        model=TestGenerationModel(
            name="test_submit_model_generation - GenerationModel"
        ),
        update=True,
    )
    created.target(mut.mut_id)
    submit_response = mut.submit_test(
        name=f"ci-custom-nlg-submit-{rnd}",
        scenario=article_clf_scenario_set,
        test_run_type=TestRunType.NL_GENERATION,
        checks=["latency"],
    )
    created.run(submit_response.id)

    num_tries = 5
    backoff = 3
    for i in range(1, num_tries + 1):
        test_run = mut.get_test_run(submit_response.id)
        if test_run.status == "FINISHED":
            break
        else:
            import time

            time.sleep(i * backoff)
    assert test_run.status == "FINISHED"
