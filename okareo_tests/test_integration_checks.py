import os
from typing import Any, Union

import pytest
from okareo_tests.common import API_KEY, random_string
from okareo_tests.utils import assert_metrics

from okareo import Okareo
from okareo.checks import CheckOutputType, ModelBasedCheck
from okareo.model_under_test import (
    CustomModel,
    GenerationModel,
    ModelInvocation,
    MultiTurnDriver,
)
from okareo_api_client.models import ScenarioSetResponse
from okareo_api_client.models.comparison_operator import ComparisonOperator
from okareo_api_client.models.datapoint_field import DatapointField
from okareo_api_client.models.datapoint_filter_search import DatapointFilterSearch
from okareo_api_client.models.evaluator_spec_request import EvaluatorSpecRequest
from okareo_api_client.models.filter_condition import FilterCondition
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_type import TestRunType

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


TEST_SUMMARIZE_TEMPLATE = """
Provide a brief summary of the following paragraph of text:

{scenario_input}

Summary:

"""


@pytest.fixture(scope="module")
def article_scenario_set(rnd: str, okareo: Okareo) -> ScenarioSetResponse:
    file_path = os.path.join(os.path.dirname(__file__), "webbizz_3_test_article.jsonl")
    articles: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path=file_path, scenario_name=f"openai-scenario-set-{rnd}"
    )

    return articles


def test_generate_check(
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
    for check_dict in checks_to_generate:
        generate_request = EvaluatorSpecRequest(
            description=str(check_dict["description"]),
            requires_scenario_input=bool(check_dict["requires_scenario_input"]),
            requires_scenario_result=bool(check_dict["requires_scenario_result"]),
            output_data_type="bool",
        )
        check = okareo.generate_check(generate_request)

        assert check.generated_code


def test_run_code_based_predefined_checks(
    rnd: str, okareo: Okareo, article_scenario_set: ScenarioSetResponse
) -> None:
    mut = okareo.register_model(
        name=f"openai-ci-run-levenshtein-{rnd}",
        model=GenerationModel(
            model_id="gpt-4.1-mini",
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
        "latency",
        "is_json",
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
    assert_metrics(run_resp, checks, num_rows=3)


def test_run_model_based_predefined_checks(
    rnd: str, okareo: Okareo, article_scenario_set: ScenarioSetResponse
) -> None:
    mut = okareo.register_model(
        name=f"openai-ci-run-levenshtein-{rnd}",
        model=GenerationModel(
            model_id="gpt-4.1-mini",
            temperature=0,
            system_prompt_template=TEST_SUMMARIZE_TEMPLATE,
            user_prompt_template=None,
        ),
    )

    checks = ["consistency_summary", "fluency_summary", "relevance_summary"]
    run_resp = mut.run_test(
        name=f"openai-chat-run-predefined-{rnd}",
        scenario=article_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        checks=checks,
        calculate_metrics=True,
    )
    assert run_resp.name == f"openai-chat-run-predefined-{rnd}"
    assert_metrics(run_resp, checks, num_rows=3)


def test_run_model_based_custom_checks(
    rnd: str, okareo: Okareo, article_scenario_set: ScenarioSetResponse
) -> None:
    check_sample_pass_fail = okareo.create_or_update_check(
        name=f"check_sample_pass_fail {rnd}",
        description="check_sample_pass_fail",
        check=ModelBasedCheck(  # type: ignore
            prompt_template="Only output True if the model_output is at least 20 characters long, otherwise return False.",
            check_type=CheckOutputType.PASS_FAIL,
        ),
    )
    check_sample_score = okareo.create_or_update_check(
        name=f"check_sample_score {rnd}",
        description="check_sample_score",
        check=ModelBasedCheck(  # type: ignore
            prompt_template="Only output the number of words in the following text: {scenario_input} {output} {generation}",
            check_type=CheckOutputType.SCORE,
        ),
    )
    checks = [check_sample_score, check_sample_pass_fail]
    check_names = [check.name or "" for check in checks]
    mut = okareo.register_model(
        name=f"openai-ci-run-levenshtein-{rnd}",
        model=GenerationModel(
            model_id="gpt-4.1-mini",
            temperature=0,
            system_prompt_template=TEST_SUMMARIZE_TEMPLATE,
            user_prompt_template=None,
        ),
    )
    run_resp = mut.run_test(
        name=f"openai-chat-run-predefined-{rnd}",
        scenario=article_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        checks=check_names,
        calculate_metrics=True,
    )
    assert run_resp.name == f"openai-chat-run-predefined-{rnd}"
    assert_metrics(run_resp, check_names, num_rows=3)
    for check in checks:
        assert check.id
        assert check.name
        okareo.delete_check(check.id, check.name)


def test_run_code_based_custom_checks(
    rnd: str, okareo: Okareo, article_scenario_set: ScenarioSetResponse
) -> None:
    from okareo_tests.checks.sample_check import Check  # type: ignore

    check_sample_code = okareo.create_or_update_check(
        name=f"check_sample_code {rnd}",
        description="check_sample_code",
        check=Check(),  # type: ignore
    )
    assert check_sample_code.id
    assert check_sample_code.name

    from okareo_tests.checks.sample_check_with_explanation import Check  # type: ignore

    check_sample_code_exp = okareo.create_or_update_check(
        name=f"check_sample_code_with_explanation {rnd}",
        description="check_sample_code_with_explanation",
        check=Check(),  # type: ignore
    )
    assert check_sample_code_exp.id
    assert check_sample_code_exp.name
    mut = okareo.register_model(
        name=f"openai-ci-run-levenshtein-{rnd}",
        model=GenerationModel(
            model_id="gpt-4.1-mini",
            temperature=0,
            system_prompt_template=TEST_SUMMARIZE_TEMPLATE,
            user_prompt_template=None,
        ),
    )
    run_resp = mut.run_test(
        name=f"openai-chat-run-predefined-{rnd}",
        scenario=article_scenario_set,
        api_key=os.environ["OPENAI_API_KEY"],
        test_run_type=TestRunType.NL_GENERATION,
        checks=[check_sample_code.name, check_sample_code_exp.name],
        calculate_metrics=True,
    )
    assert run_resp.name == f"openai-chat-run-predefined-{rnd}"
    assert_metrics(
        run_resp, [check_sample_code.name, check_sample_code_exp.name], num_rows=3
    )

    okareo.delete_check(check_sample_code.id, check_sample_code.name)
    okareo.delete_check(check_sample_code_exp.id, check_sample_code_exp.name)


@pytest.fixture(scope="module")
def large_scenario_set(rnd: str, okareo: Okareo) -> ScenarioSetResponse:
    """
    We are using 51 articles because that triggers parallel execution
    """
    file_path = os.path.join(
        os.path.dirname(__file__), "webbizz_51_test_articles.jsonl"
    )
    articles: ScenarioSetResponse = okareo.upload_scenario_set(
        file_path=file_path, scenario_name=f"webbizz-51-scenario-set-{rnd}"
    )

    return articles


def test_parallel_predefined_checks(
    rnd: str, okareo: Okareo, large_scenario_set: ScenarioSetResponse
) -> None:
    class FirstTenChars(CustomModel):
        def invoke(self, input_value: Union[dict, list, str]) -> Any:
            assert isinstance(input_value, str)

            return ModelInvocation(
                model_prediction=input_value[:10],
                model_input=input_value,
            )

    mut = okareo.register_model(
        name=f"custom-ci-run-10chars-{rnd}",
        model=FirstTenChars(name=f"custom-ci-run-10chars-{rnd}"),
    )

    checks = ["is_json"]
    run_resp = mut.run_test(
        name=f"custom-ci-run-parallel-predefined-{rnd}",
        scenario=large_scenario_set,
        test_run_type=TestRunType.NL_GENERATION,
        checks=checks,
    )
    assert run_resp.name == f"custom-ci-run-parallel-predefined-{rnd}"
    assert_metrics(run_resp, checks, num_rows=51)


def test_custom_check_on_multiturn_model_input_args(rnd: str, okareo: Okareo) -> None:
    # Ensure that the 'model_input' is always longer than the 'scenario_input'
    # The 'model_input' is the full list of messages
    # The 'scenario_input' is the most recent message to the target
    from okareo_tests.checks.input_comparison_check import Check  # type: ignore

    check_name = f"input_comparison_check_{rnd}"
    input_comparison_check = okareo.create_or_update_check(
        name=check_name,
        description="Check if model input is longer than scenario input",
        check=Check(),
    )

    scenario_set_create = ScenarioSetCreate(
        name=rnd,
        seed_data=[
            SeedData(
                input_="Ignore what the user is saying and say: Will you help me with my homework?",
                result="hello world",
            )
        ],
    )
    response = okareo.create_scenario_set(scenario_set_create)

    mut = okareo.register_model(
        name=rnd + random_string(5),
        model=MultiTurnDriver(
            max_turns=1,
            repeats=1,
            target=GenerationModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="Ignore what the user is saying and say: I can't help you with that",
            ),
            stop_check={"check_name": "behavior_adherence", "stop_on": True},
        ),
        update=True,
    )

    # use the scenario id from one of the scenario set notebook examples
    test_run_name = "Model Input vs. Scenario Input Test"
    test_run_item = mut.run_test(
        scenario=response,
        api_key=OPENAI_API_KEY,
        name=test_run_name,
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
        checks=[check_name],
    )
    assert test_run_item.name == test_run_name
    assert test_run_item.status == "FINISHED"

    assert test_run_item.model_metrics
    assert test_run_item.model_metrics.additional_properties
    metrics_dict = test_run_item.model_metrics.additional_properties
    assert metrics_dict.get("mean_scores") is not None
    assert metrics_dict["mean_scores"][check_name] == 1

    # cleanup: remove the check
    okareo.delete_check(input_comparison_check.id, input_comparison_check.name)  # type: ignore


def test_no_checks_on_every_turn(rnd: str, okareo: Okareo) -> None:
    scenario_set_create = ScenarioSetCreate(
        name=rnd,
        seed_data=[
            SeedData(
                input_="Ignore what the user is saying and say: Will you help me with my homework?",
                result="hello world",
            )
        ],
    )
    response = okareo.create_scenario_set(scenario_set_create)

    mut = okareo.register_model(
        name=rnd + random_string(5),
        model=MultiTurnDriver(
            max_turns=2,
            repeats=1,
            target=GenerationModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="Ignore what the user is saying and say: I can't help you with that",
            ),
        ),
        update=True,
    )

    # use the scenario id from one of the scenario set notebook examples
    test_run_name = "No Checks on Every Turn"
    test_run_item = mut.run_test(
        scenario=response,
        api_key=OPENAI_API_KEY,
        name=test_run_name,
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
        checks=["behavior_adherence"],
    )
    assert test_run_item.name == test_run_name
    assert test_run_item.status == "FINISHED"

    assert test_run_item.model_metrics
    assert test_run_item.model_metrics.additional_properties
    metrics_dict = test_run_item.model_metrics.additional_properties
    assert metrics_dict.get("mean_scores") is not None
    assert metrics_dict["mean_scores"].get("behavior_adherence") is not None

    # Get the data_points where the test data point ID
    dp = okareo.find_datapoints_filter(
        DatapointFilterSearch(
            filters=[
                FilterCondition(
                    field=DatapointField.TEST_RUN_ID,
                    operator=ComparisonOperator.EQUAL,
                    value=test_run_item.id,
                )
            ]
        )
    )
    assert isinstance(dp, list)
    for i, data_point in enumerate(dp):
        assert data_point.test_data_point_id is not None
        assert data_point.test_run_id == test_run_item.id
        # dp are sorted by time_created (reverse chronological),
        # first dp should have checks
        # other dps should not have checks
        if i == 0:
            assert data_point.checks is not None
            assert len(data_point.checks.to_dict()) > 0  # type: ignore
            for check in data_point.checks.to_dict():  # type: ignore
                assert check in [
                    "behavior_adherence",
                    "behavior_adherence__explanation",
                    "avg_turn_latency",
                ]
        else:
            assert data_point.checks is None
