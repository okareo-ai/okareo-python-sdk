"""Hermetic unit tests for tag propagation from run_simulation to the test run.

`Okareo.run_simulation(..., tags=[...])` must put those tags on the *test run*
it creates, so the run is findable via `find_test_runs(tags=[...])` and filterable
in the Okareo app. These tests mock the HTTP layer (no server, no network) and
assert the tags land in the body of the POST that creates the test run.
"""

import json
from datetime import datetime
from typing import Any
from uuid import UUID

import pytest
from pytest_httpx import HTTPXMock

from okareo.model_under_test import OpenAIModel, Target
from okareo.okareo import Okareo
from okareo_api_client.models.scenario_set_response import ScenarioSetResponse
from okareo_api_client.models.scenario_type import ScenarioType

MOCK_UUID = "0156f5d7-4ac4-4568-9d44-24750aa08d1a"

SIMULATION_TAGS = ["driver-hangup-validation", "bare", "voice"]

OPENAI_TARGET_MODEL = {
    "type": "openai",
    "model_id": "gpt-4o-mini",
    "temperature": 0,
    "system_prompt_template": "Be helpful",
}


@pytest.fixture
def okareo_client(httpx_mock: HTTPXMock) -> Okareo:
    httpx_mock.add_response(
        json=[
            {
                "id": MOCK_UUID,
                "name": "Global",
                "onboarding_status": "onboarding_status",
                "tags": [],
                "additional_properties": {},
            }
        ],
        status_code=201,
    )
    return Okareo("foo", "http://mocked.com")


def _add_driver_response(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        json={
            "id": MOCK_UUID,
            "name": "driver",
            "temperature": 0.6,
            "model_id": "gpt-4o-mini",
            "prompt_template": "{scenario_input}",
            "time_created": datetime.now().isoformat(),
        },
        status_code=201,
    )


def _add_target_registration_response(httpx_mock: HTTPXMock) -> None:
    """Response for POST /v0/register_model (target passed as a Target object)."""
    httpx_mock.add_response(
        json={
            "id": MOCK_UUID,
            "project_id": MOCK_UUID,
            "name": "target",
            "tags": SIMULATION_TAGS,
            "time_created": datetime.now().isoformat(),
            "version": 1,
            "models": {"openai": OPENAI_TARGET_MODEL},
        },
        status_code=201,
    )


def _add_target_lookup_response(httpx_mock: HTTPXMock) -> None:
    """Response for GET /v0/target/{name} (target passed as a string name)."""
    httpx_mock.add_response(
        json={
            "id": MOCK_UUID,
            "name": "target",
            "target": OPENAI_TARGET_MODEL,
        },
        status_code=200,
    )


def _add_test_run_response(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        json={
            "id": MOCK_UUID,
            "project_id": MOCK_UUID,
            "mut_id": MOCK_UUID,
            "scenario_set_id": MOCK_UUID,
            "name": "tagged sim",
            "type": "MULTI_TURN",
            "tags": SIMULATION_TAGS,
        },
        status_code=201,
    )


def _scenario() -> ScenarioSetResponse:
    return ScenarioSetResponse(
        scenario_id=UUID(MOCK_UUID),
        project_id=UUID(MOCK_UUID),
        name="scenario",
        time_created=datetime.now(),
        type_=ScenarioType.SEED,
    )


def _test_run_request_body(httpx_mock: HTTPXMock) -> Any:
    """Body of the POST that creates the test run (the last request made)."""
    request = httpx_mock.get_requests()[-1]
    assert request.url.path in ("/v0/test_run", "/v0/test_run/submit")
    return json.loads(request.content.decode("utf-8"))


def test_run_simulation_sends_tags_on_test_run_payload_for_target_object(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    _add_driver_response(httpx_mock)
    _add_target_registration_response(httpx_mock)
    _add_test_run_response(httpx_mock)

    okareo_client.run_simulation(
        name="tagged sim",
        scenario=_scenario(),
        target=Target(
            name="target",
            target=OpenAIModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="Be helpful",
            ),
        ),
        tags=SIMULATION_TAGS,
    )

    body = _test_run_request_body(httpx_mock)
    assert body["tags"] == SIMULATION_TAGS


def test_run_simulation_sends_tags_on_test_run_payload_for_target_by_name(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    """Tags must reach the test run even when the target is referenced by name."""
    _add_driver_response(httpx_mock)
    _add_target_lookup_response(httpx_mock)
    _add_test_run_response(httpx_mock)

    okareo_client.run_simulation(
        name="tagged sim",
        scenario=_scenario(),
        target="target",
        tags=SIMULATION_TAGS,
    )

    body = _test_run_request_body(httpx_mock)
    assert body["tags"] == SIMULATION_TAGS


def test_run_simulation_sends_tags_on_submit(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    _add_driver_response(httpx_mock)
    _add_target_lookup_response(httpx_mock)
    _add_test_run_response(httpx_mock)

    okareo_client.run_simulation(
        name="tagged sim",
        scenario=_scenario(),
        target="target",
        tags=SIMULATION_TAGS,
        submit=True,
    )

    body = _test_run_request_body(httpx_mock)
    assert body["tags"] == SIMULATION_TAGS


def test_run_simulation_without_tags_omits_tags_from_payload(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    _add_driver_response(httpx_mock)
    _add_target_lookup_response(httpx_mock)
    _add_test_run_response(httpx_mock)

    okareo_client.run_simulation(
        name="tagged sim",
        scenario=_scenario(),
        target="target",
    )

    body = _test_run_request_body(httpx_mock)
    assert body.get("tags", []) == []
