"""Live integration tests for `Okareo.calibrate_check`.

Runs against a real tenant and spends real judge calls — **owner-run only**.

Skipped unless `OKAREO_RUN_CALIBRATION_TESTS=1`. There is no hermetic allowlist to
sit outside of: CI runs a bare `poetry run pytest -n auto`, which collects this
directory whole against `BASE_URL` (https://api.okareo.com by default), and the
same suite is what `sdk-test-latest` runs against a fresh backend deploy. Without
the gate, every PR and every deploy would call `/v0/test_runs/{id}/calibrate_check`
on production, where the route does not exist yet.

Run them deliberately:

    OKAREO_RUN_CALIBRATION_TESTS=1 OKAREO_BASE_URL=http://localhost:8000 \\
        poetry run pytest okareo_tests/test_calibrate_check_integration.py

Covers, against a run this module creates:
FR-4/FR-6 (one self-identifying entry per test datapoint), FR-5 (verdicts), FR-7 (the
argument surface, model vs code), FR-9 (nothing persisted), FR-12 (inspect-only makes no
judge calls), FR-13 (the config comes back verbatim), and FR-2 (a bad placeholder is
refused before anything runs).
"""

import os
from typing import Any, Union
from uuid import UUID

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.checks import CheckOutputType, ModelBasedCheck
from okareo.model_under_test import CustomModel, ModelInvocation
from okareo_api_client.models.find_test_data_point_payload import (
    FindTestDataPointPayload,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_type import TestRunType

pytestmark = pytest.mark.skipif(
    os.environ.get("OKAREO_RUN_CALIBRATION_TESTS") != "1",
    reason=(
        "Live calibration tests are owner-run: they create a Test Run and spend "
        "real judge calls against BASE_URL. Set OKAREO_RUN_CALIBRATION_TESTS=1 to "
        "run them, and point OKAREO_BASE_URL at a backend that serves "
        "/v0/test_runs/{id}/calibrate_check."
    ),
)

CODE_CHECK_CONTENTS = """
from okareo.checks import CodeBasedCheck


class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str, metadata: dict) -> bool:
        return len(model_output) > 0
"""


class _SimpleModel(CustomModel):
    def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
        return ModelInvocation(
            model_prediction=f"prediction::{str(input_value)}",
            model_input=input_value,
        )


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(8)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


@pytest.fixture(scope="module")
def finished_run(okareo: Okareo, rnd: str) -> Any:
    """A small finished NL_GENERATION run to calibrate against."""
    scenario = okareo.create_scenario_set(
        ScenarioSetCreate(
            name=f"calibrate-scenario-{rnd}",
            seed_data=[
                SeedData(input_=f"input-{i}", result=f"result-{i}") for i in range(3)
            ],
        )
    )
    mut = okareo.register_model(
        name=f"calibrate-model-{rnd}",
        model=_SimpleModel(name=f"calibrate-model-{rnd}"),
    )
    run = mut.run_test(
        name=f"calibrate-run-{rnd}",
        scenario=scenario,
        test_run_type=TestRunType.NL_GENERATION,
    )
    assert run.id is not None
    return run


def _test_data_point_ids(okareo: Okareo, run_id: Union[str, UUID]) -> set:
    tdps = okareo.find_test_data_points(
        FindTestDataPointPayload(test_run_id=UUID(str(run_id)), full_data_point=True)
    )
    assert isinstance(tdps, list)
    return {str(tdp.id) for tdp in tdps}


def _model_draft() -> ModelBasedCheck:
    return ModelBasedCheck(
        prompt_template="Return True if {model_output} mentions the word prediction.",
        check_type=CheckOutputType.PASS_FAIL,
    )


def test_model_draft_returns_one_self_identifying_entry_per_row(
    okareo: Okareo, finished_run: Any
) -> None:
    expected_ids = _test_data_point_ids(okareo, finished_run.id)

    response = okareo.calibrate_check(
        test_run_id=str(finished_run.id),
        check=_model_draft(),
        name="calibrate-model-draft",
    )

    assert response["check_flow"] == "model"
    assert response["truncated"] is False
    assert {row["test_data_point_id"] for row in response["rows"]} == expected_ids
    for row in response["rows"]:
        # FR-7: the full current variable set, not only what the prompt referenced.
        assert "model_output" in row["arguments"]
        assert "message_history" in row["arguments"]
        assert "generation" not in row["arguments"]
        assert row["result"] is not None
        assert row["result"]["score"] is not None or row["result"]["error"] is not None


def test_code_draft_reports_only_its_declared_arguments(
    okareo: Okareo, finished_run: Any
) -> None:
    response = okareo.calibrate_check(
        test_run_id=str(finished_run.id),
        check={"code_contents": CODE_CHECK_CONTENTS},
        name="calibrate-code-draft",
    )

    assert response["check_flow"] == "code"
    assert response["rows"]
    for row in response["rows"]:
        assert set(row["arguments"]) == {"model_output", "metadata"}


def test_inspect_only_returns_arguments_and_no_verdicts(
    okareo: Okareo, finished_run: Any
) -> None:
    response = okareo.calibrate_check(
        test_run_id=str(finished_run.id),
        check=_model_draft(),
        inspect_only=True,
    )

    assert response["inspect_only"] is True
    assert response["rows"]
    for row in response["rows"]:
        assert row["result"] is None
        assert row["arguments"]


def test_check_config_comes_back_verbatim(okareo: Okareo, finished_run: Any) -> None:
    config = {
        "prompt_template": "Return True if {model_output} is non-empty.",
        "type": "pass_fail",
        "a_key_the_server_ignores": "still here",
    }

    response = okareo.calibrate_check(
        test_run_id=str(finished_run.id), check=config, inspect_only=True
    )

    assert response["check_config"] == config


def test_invalid_placeholder_is_refused(okareo: Okareo, finished_run: Any) -> None:
    draft = ModelBasedCheck(
        prompt_template="Return True if {tool_call} happened.",
        check_type=CheckOutputType.PASS_FAIL,
    )

    with pytest.raises(ValueError) as excinfo:
        okareo.calibrate_check(test_run_id=str(finished_run.id), check=draft)

    message = str(excinfo.value)
    assert "422" in message
    assert "tool_call" in message


def test_calibration_persists_nothing(okareo: Okareo, finished_run: Any) -> None:
    checks_before = len(okareo.get_all_checks())
    tdps_before = _test_data_point_ids(okareo, finished_run.id)

    okareo.calibrate_check(
        test_run_id=str(finished_run.id),
        check=_model_draft(),
        name="calibrate-persists-nothing",
    )

    assert len(okareo.get_all_checks()) == checks_before
    assert _test_data_point_ids(okareo, finished_run.id) == tdps_before
    assert "calibrate-persists-nothing" not in [
        check.name for check in okareo.get_all_checks()
    ]
