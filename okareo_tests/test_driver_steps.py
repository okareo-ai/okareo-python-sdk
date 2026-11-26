"""Hermetic unit tests for a Driver's steps on the way to Okareo and back.

A Driver's steps travel through the generated client twice: `create_or_update_driver`
turns the Driver into the request schema (`DriverModelSchema.from_dict(driver.to_dict())`),
and the response is turned back into a Driver (`Driver.from_response`). Every step kind
must survive both, including a list that ends with a Prompt step (`{"prompt": True}`):
its exact steps play first, then the Driver's `prompt_template` runs the rest. These tests
mock the HTTP layer (no server, no network).
"""

import json
from datetime import datetime
from typing import Any, List

import pytest
from pytest_httpx import HTTPXMock

from okareo.model_under_test import Driver
from okareo.okareo import Okareo
from okareo_api_client.models.driver_model_response import DriverModelResponse
from okareo_api_client.models.voice_driver_model_response import (
    VoiceDriverModelResponse,
)

MOCK_UUID = "0156f5d7-4ac4-4568-9d44-24750aa08d1a"

STEPS_THEN_PROMPT: List[dict] = [
    {"message": "Hi, I'm calling about my order."},
    {"dtmf": "1"},
    {"prompt": True},
]
STEPS_ONLY: List[dict] = [
    {"message": "Hi, I'm calling about my order."},
    {"end_conversation": "Thanks, goodbye.", "reason": "script done"},
]


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


def _driver_response(steps: Any) -> dict:
    return {
        "id": MOCK_UUID,
        "name": "driver",
        "temperature": 0.8,
        "prompt_template": "Ask where the order is.",
        "time_created": datetime.now().isoformat(),
        "steps": steps,
    }


def _driver_request_body(httpx_mock: HTTPXMock) -> Any:
    """Body of the POST /v0/driver the SDK sent."""
    requests = [
        r
        for r in httpx_mock.get_requests()
        if r.method == "POST" and r.url.path == "/v0/driver"
    ]
    assert len(requests) == 1
    return json.loads(requests[0].content.decode("utf-8"))


@pytest.mark.parametrize(
    "steps",
    [STEPS_THEN_PROMPT, STEPS_ONLY],
    ids=["ends-with-prompt-step", "ends-with-end-conversation"],
)
def test_create_or_update_driver_sends_and_reads_back_every_step(
    okareo_client: Okareo, httpx_mock: HTTPXMock, steps: List[dict]
) -> None:
    httpx_mock.add_response(json=_driver_response(steps), status_code=201)

    driver = okareo_client.create_or_update_driver(
        Driver(name="driver", prompt_template="Ask where the order is.", steps=steps)
    )

    assert _driver_request_body(httpx_mock)["steps"] == steps
    assert driver.steps == steps


@pytest.mark.parametrize(
    "response_class", [DriverModelResponse, VoiceDriverModelResponse]
)
def test_driver_read_back_keeps_the_prompt_step(response_class: Any) -> None:
    response = response_class.from_dict(_driver_response(STEPS_THEN_PROMPT))

    driver = Driver.from_response(response)

    assert driver.steps == STEPS_THEN_PROMPT
    assert driver.prompt_template == "Ask where the order is."
