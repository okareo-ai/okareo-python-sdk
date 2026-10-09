"""Hermetic unit tests for the temperature the SDK sends when it registers a Driver.

A Driver built without a temperature must get Okareo's default (0.8, what the Okareo
app gives a new Driver), not a default the SDK picked. POST /v0/driver requires a
number, so "no temperature" can never reach the server as null. An explicit
temperature, including 0, is sent as given. These tests mock the HTTP layer (no
server, no network) and read the body of the POST that registers the Driver.
"""

import json
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

import pytest
from pytest_httpx import HTTPXMock

from okareo.model_under_test import Driver
from okareo.okareo import Okareo
from okareo_api_client.models.scenario_set_response import ScenarioSetResponse
from okareo_api_client.models.scenario_type import ScenarioType

MOCK_UUID = "0156f5d7-4ac4-4568-9d44-24750aa08d1a"
OKAREO_DEFAULT_DRIVER_TEMPERATURE = 0.8


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
            "temperature": OKAREO_DEFAULT_DRIVER_TEMPERATURE,
            "prompt_template": "{scenario_input}",
            "time_created": datetime.now().isoformat(),
        },
        status_code=201,
    )


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
    "driver",
    [Driver(name="driver"), Driver(name="driver", temperature=None)],
    ids=["temperature-omitted", "temperature-none"],
)
def test_driver_without_temperature_sends_okareo_default(
    okareo_client: Okareo, httpx_mock: HTTPXMock, driver: Driver
) -> None:
    _add_driver_response(httpx_mock)

    okareo_client.create_or_update_driver(driver)

    body = _driver_request_body(httpx_mock)
    assert body["temperature"] == OKAREO_DEFAULT_DRIVER_TEMPERATURE


@pytest.mark.parametrize("temperature", [0, 0.3, 1.2])
def test_driver_with_temperature_sends_it_as_given(
    okareo_client: Okareo, httpx_mock: HTTPXMock, temperature: float
) -> None:
    _add_driver_response(httpx_mock)

    okareo_client.create_or_update_driver(
        Driver(name="driver", temperature=temperature)
    )

    body = _driver_request_body(httpx_mock)
    assert body["temperature"] == temperature


def _add_target_lookup_response(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        json={
            "id": MOCK_UUID,
            "name": "target",
            "target": {
                "type": "openai",
                "model_id": "gpt-4o-mini",
                "temperature": 0,
                "system_prompt_template": "Be helpful",
            },
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
            "name": "sim",
            "type": "MULTI_TURN",
        },
        status_code=201,
    )


@pytest.mark.parametrize(
    "driver",
    [None, Driver(name="driver")],
    ids=["no-driver", "inline-driver-without-temperature"],
)
def test_run_simulation_registers_driver_with_okareo_default(
    okareo_client: Okareo, httpx_mock: HTTPXMock, driver: Optional[Driver]
) -> None:
    _add_driver_response(httpx_mock)
    _add_target_lookup_response(httpx_mock)
    _add_test_run_response(httpx_mock)

    okareo_client.run_simulation(
        name="sim",
        scenario=ScenarioSetResponse(
            scenario_id=UUID(MOCK_UUID),
            project_id=UUID(MOCK_UUID),
            name="scenario",
            time_created=datetime.now(),
            type_=ScenarioType.SEED,
        ),
        target="target",
        driver=driver,
    )

    body = _driver_request_body(httpx_mock)
    assert body["temperature"] == OKAREO_DEFAULT_DRIVER_TEMPERATURE
