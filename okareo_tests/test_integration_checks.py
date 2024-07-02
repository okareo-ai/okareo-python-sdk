import os
import random
import string
import tempfile

import pytest
from okareo_tests.common import API_KEY, random_string
from okareo_tests.sample_check import Check
from okareo_tests.utils import assert_metrics

from okareo import Okareo
from okareo.checks import CheckType, ModelBasedCheck
from okareo.model_under_test import OpenAIModel
from okareo_api_client.models import ScenarioSetResponse
from okareo_api_client.models.evaluator_spec_request import EvaluatorSpecRequest
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


def test_run_code_based_predefined_checks(
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


def test_run_model_based_predefined_checks(
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

    checks = ["consistency", "fluency", "conciseness"]
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


def test_run_model_based_custom_checks(
    rnd: str, okareo: Okareo, article_scenario_set: ScenarioSetResponse
) -> None:
    check_sample_pass_fail = okareo.create_or_update_check(
        name=f"check_sample_pass_fail {rnd}",
        description="check_sample_pass_fail",
        check=ModelBasedCheck(  # type: ignore
            prompt_template="Only output True if the model_output is at least 20 characters long, otherwise return False.",
            check_type=CheckType.PASS_FAIL,
        ),
    )
    check_sample_score = okareo.create_or_update_check(
        name=f"check_sample_score {rnd}",
        description="check_sample_score",
        check=ModelBasedCheck(  # type: ignore
            prompt_template="Only output the number of words in the following text: {input} {output} {generation}",
            check_type=CheckType.SCORE,
        ),
    )
    checks = [
        check_sample_pass_fail.name or f"check_sample_pass_fail {rnd}",
        check_sample_score.name or f"check_sample_score {rnd}",
    ]
    mut = okareo.register_model(
        name=f"openai-ci-run-levenshtein-{rnd}",
        model=OpenAIModel(
            model_id="gpt-3.5-turbo",
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
        checks=checks,
        calculate_metrics=True,
    )
    assert run_resp.name == f"openai-chat-run-predefined-{rnd}"
    assert_metrics(run_resp, checks)
    for check in checks:
        okareo.delete_check(check, check)


def test_run_code_based_custom_checks(
    rnd: str, okareo: Okareo, article_scenario_set: ScenarioSetResponse
) -> None:
    check_sample_code = okareo.create_or_update_check(
        name=f"check_sample_code {rnd}",
        description="check_sample_code",
        check=Check(),  # type: ignore
    )
    checks = [
        check_sample_code.name or f"check_sample_code {rnd}",
    ]
    mut = okareo.register_model(
        name=f"openai-ci-run-levenshtein-{rnd}",
        model=OpenAIModel(
            model_id="gpt-3.5-turbo",
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
        checks=checks,
        calculate_metrics=True,
    )
    assert run_resp.name == f"openai-chat-run-predefined-{rnd}"
    assert_metrics(run_resp, checks)
    for check in checks:
        okareo.delete_check(check, check)
