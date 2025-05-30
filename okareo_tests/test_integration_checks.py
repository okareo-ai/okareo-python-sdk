import os
from typing import Any, Union

import pytest
from okareo_tests.common import API_KEY, random_string
from okareo_tests.sample_check import Check
from okareo_tests.utils import assert_metrics

from okareo import Okareo
from okareo.checks import CheckOutputType, ModelBasedCheck
from okareo.model_under_test import CustomModel, GenerationModel, ModelInvocation
from okareo_api_client.models import ScenarioSetResponse
from okareo_api_client.models.evaluator_spec_request import EvaluatorSpecRequest
from okareo_api_client.models.test_run_type import TestRunType


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
    check_sample_code = okareo.create_or_update_check(
        name=f"check_sample_code {rnd}",
        description="check_sample_code",
        check=Check(),  # type: ignore
    )
    assert check_sample_code.id
    assert check_sample_code.name
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
        checks=[check_sample_code.name],
        calculate_metrics=True,
    )
    assert run_resp.name == f"openai-chat-run-predefined-{rnd}"
    assert_metrics(run_resp, [check_sample_code.name], num_rows=3)

    okareo.delete_check(check_sample_code.id, check_sample_code.name)


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
