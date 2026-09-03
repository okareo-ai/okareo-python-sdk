"""Hermetic unit tests for `Okareo.calibrate_check`.

Every network call is mocked — `Okareo.__init__` issues `GET /v0/projects`, so each
test queues that response first and then the calibration response.

Assertions are made on the request the method actually sends, never on a private
helper: a body key that stops being sent has to fail here.
"""

import json
from typing import Any, Dict, List
from uuid import uuid4

import pytest
from okareo_tests.checks import code_check_pass_fail
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo.checks import CheckOutputType, ModelBasedCheck
from okareo.common import CALIBRATE_TIME_OUT

GLOBAL_ID = "0156f5d7-4ac4-4568-9d44-24750aa08d1a"
TEST_RUN_ID = "3f2b9a1c-5d6e-4f80-9a1b-2c3d4e5f6a7b"

PROJECTS_JSON: List[Dict[str, Any]] = [
    {
        "id": GLOBAL_ID,
        "name": "Global",
        "onboarding_status": "onboarding_status",
        "tags": [],
    }
]

CALIBRATION_JSON: Dict[str, Any] = {
    "test_run_id": TEST_RUN_ID,
    "name": "draft_check",
    "check_config": {
        "prompt_template": "Is {model_output} polite?",
        "type": "pass_fail",
    },
    "check_flow": "model",
    "inspect_only": False,
    "row_count": 1,
    "total_row_count": 1,
    "truncated": False,
    "rows": [
        {
            "test_data_point_id": str(uuid4()),
            "arguments": {"model_output": "sure thing"},
            "result": {
                "score": True,
                "explanation": "polite",
                "check_metadata": None,
                "error": None,
            },
            "error": None,
        }
    ],
}


@pytest.fixture
def okareo(httpx_mock: HTTPXMock) -> Okareo:
    httpx_mock.add_response(json=PROJECTS_JSON, status_code=201)
    return Okareo("foo", "http://mocked.com")


def _model_check() -> ModelBasedCheck:
    return ModelBasedCheck(
        prompt_template="Is {model_output} polite?",
        check_type=CheckOutputType.PASS_FAIL,
    )


def _sent(httpx_mock: HTTPXMock) -> Any:
    """The JSON body of the last outgoing request."""
    return json.loads(httpx_mock.get_requests()[-1].content)


def test_posts_the_four_body_keys_for_a_base_check(
    okareo: Okareo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(json=CALIBRATION_JSON, status_code=200)

    result = okareo.calibrate_check(
        test_run_id=TEST_RUN_ID, check=_model_check(), name="draft_check"
    )

    request = httpx_mock.get_requests()[-1]
    assert request.method == "POST"
    assert str(request.url) == (
        f"http://mocked.com/v0/test_runs/{TEST_RUN_ID}/calibrate_check"
    )
    assert request.headers["api-key"] == "foo"
    assert set(_sent(httpx_mock)) == {
        "name",
        "check_config",
        "check_type",
        "inspect_only",
    }
    assert result == CALIBRATION_JSON


def test_check_config_is_sent_verbatim_including_a_key_the_server_ignores(
    okareo: Okareo, httpx_mock: HTTPXMock
) -> None:
    """FR-13: the config the caller hands in is the config that goes on the wire."""
    httpx_mock.add_response(json=CALIBRATION_JSON, status_code=200)
    config = {
        "prompt_template": "Is {model_output} polite?",
        "type": "pass_fail",
        "an_ignored_key": "kept anyway",
    }

    okareo.calibrate_check(test_run_id=TEST_RUN_ID, check=config, name="draft_check")

    assert _sent(httpx_mock)["check_config"] == config


def test_check_type_is_derived_from_a_model_check_instance(
    okareo: Okareo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(json=CALIBRATION_JSON, status_code=200)

    okareo.calibrate_check(test_run_id=TEST_RUN_ID, check=_model_check())

    body = _sent(httpx_mock)
    assert body["check_type"] == "model"
    assert body["check_config"]["prompt_template"] == "Is {model_output} polite?"


def test_check_type_is_derived_from_a_code_check_instance(
    okareo: Okareo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(json=CALIBRATION_JSON, status_code=200)

    okareo.calibrate_check(test_run_id=TEST_RUN_ID, check=code_check_pass_fail.Check())

    body = _sent(httpx_mock)
    assert body["check_type"] == "code"
    assert "code_contents" in body["check_config"]
    assert "type" not in body["check_config"]


def test_raw_dict_omits_check_type_entirely(
    okareo: Okareo, httpx_mock: HTTPXMock
) -> None:
    """A dict carries no class to derive from, and guessing "model" for a config
    holding `code_contents` is exactly the disagreement the server rejects."""
    httpx_mock.add_response(json=CALIBRATION_JSON, status_code=200)

    okareo.calibrate_check(
        test_run_id=TEST_RUN_ID, check={"code_contents": "def evaluate(): return True"}
    )

    assert "check_type" not in _sent(httpx_mock)


def test_inspect_only_is_forwarded(okareo: Okareo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json=CALIBRATION_JSON, status_code=200)

    okareo.calibrate_check(
        test_run_id=TEST_RUN_ID, check=_model_check(), inspect_only=True
    )

    assert _sent(httpx_mock)["inspect_only"] is True


def test_inspect_only_defaults_to_false(okareo: Okareo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json=CALIBRATION_JSON, status_code=200)

    okareo.calibrate_check(test_run_id=TEST_RUN_ID, check=_model_check())

    assert _sent(httpx_mock)["inspect_only"] is False


def test_name_defaults_to_draft_check(okareo: Okareo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json=CALIBRATION_JSON, status_code=200)

    okareo.calibrate_check(test_run_id=TEST_RUN_ID, check=_model_check())

    assert _sent(httpx_mock)["name"] == "draft_check"


def test_validation_error_detail_reaches_the_caller(
    okareo: Okareo, httpx_mock: HTTPXMock
) -> None:
    """FR-2: the 422 message names the offending placeholder — it is the whole
    feedback loop, so it has to survive into the raised error."""
    detail = "Invalid template variables: {tool_call}. Valid variables are: ..."
    httpx_mock.add_response(json={"detail": detail}, status_code=422)

    with pytest.raises(ValueError) as excinfo:
        okareo.calibrate_check(test_run_id=TEST_RUN_ID, check=_model_check())

    message = str(excinfo.value)
    assert "422" in message
    assert "{tool_call}" in message


def test_timeout_error_is_distinguishable(
    okareo: Okareo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(json={"detail": "Calibration timed out"}, status_code=504)

    with pytest.raises(ValueError) as excinfo:
        okareo.calibrate_check(test_run_id=TEST_RUN_ID, check=_model_check())

    assert "504" in str(excinfo.value)


def test_default_timeout_is_the_calibrate_constant(
    okareo: Okareo, httpx_mock: HTTPXMock
) -> None:
    """`Okareo.__init__` never forwards its own timeout to the httpx client, so the
    request has to carry one itself or it inherits httpx's "no timeout"."""
    httpx_mock.add_response(json=CALIBRATION_JSON, status_code=200)

    okareo.calibrate_check(test_run_id=TEST_RUN_ID, check=_model_check())

    timeout = httpx_mock.get_requests()[-1].extensions["timeout"]
    assert timeout["read"] == CALIBRATE_TIME_OUT
    # The client must outlast the server's worst case so the server's 504 wins the
    # race. The server checks its 600s budget only between rows, so the last row can
    # start at ~600s and then run a judge call plus its one retry, each capped at
    # LLM_TIMEOUT (default 30s).
    server_budget_seconds = 600
    llm_timeout_seconds = 30
    judge_call_plus_retry = 2 * llm_timeout_seconds
    assert CALIBRATE_TIME_OUT > server_budget_seconds + judge_call_plus_retry


def test_explicit_timeout_is_passed(okareo: Okareo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json=CALIBRATION_JSON, status_code=200)

    okareo.calibrate_check(test_run_id=TEST_RUN_ID, check=_model_check(), timeout=12.5)

    assert httpx_mock.get_requests()[-1].extensions["timeout"]["read"] == 12.5


def test_analysis_output_type_is_constructible() -> None:
    """The backend has three model-check types; without ANALYSIS an analysis draft
    cannot be built at all."""
    check = ModelBasedCheck(
        prompt_template="Summarize {model_output}.",
        check_type=CheckOutputType.ANALYSIS,
    )

    assert check.check_config()["type"] == "analysis"
