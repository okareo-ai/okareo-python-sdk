"""Hermetic unit tests for the outbound simulation methods on `Okareo`.

Every network call is mocked. `Okareo.__init__` issues `GET /v0/projects`, so each
test queues that response first. Driver and Target resolution is stubbed: these
tests are about the requests the outbound methods send and how they read the
replies, and assertions are made on the request actually sent.
"""

import json
from typing import Any, Dict, List

import pytest
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo.model_under_test import Driver, ReceivingPhoneTarget, Target

GLOBAL_ID = "0156f5d7-4ac4-4568-9d44-24750aa08d1a"
RUN_ID = "3f2b9a1c-5d6e-4f80-9a1b-2c3d4e5f6a7b"
TARGET_ID = "11111111-1111-4111-8111-111111111111"
DRIVER_ID = "22222222-2222-4222-8222-222222222222"
SCENARIO_ID = "33333333-3333-4333-8333-333333333333"
BASE = "http://mocked.com"

PROJECTS_JSON: List[Dict[str, Any]] = [
    {
        "id": GLOBAL_ID,
        "name": "Global",
        "onboarding_status": "onboarding_status",
        "tags": [],
    }
]


def _line(**overrides: Any) -> Dict[str, Any]:
    line: Dict[str, Any] = {
        "test_run_id": RUN_ID,
        "status": "on",
        "number": "+15550100000",
        "armed_at": 1794521876.4,
        "max_until": 1794529076.4,
        "idle_timeout_s": 1800,
        "calls_received": 0,
    }
    line.update(overrides)
    return line


@pytest.fixture
def okareo(httpx_mock: HTTPXMock, monkeypatch: pytest.MonkeyPatch) -> Okareo:
    httpx_mock.add_response(json=PROJECTS_JSON, status_code=201)
    client = Okareo("api-key", BASE)
    monkeypatch.setattr(
        client,
        "_resolve_driver_and_target",
        lambda **_: (
            Driver(name="debtor", id=DRIVER_ID),
            Target(
                name="collections line",
                target=ReceivingPhoneTarget().params(),
                id=TARGET_ID,
            ),
        ),
    )
    return client


def _last_request(httpx_mock: HTTPXMock) -> Any:
    return httpx_mock.get_requests()[-1]


class TestStart:
    def test_it_posts_the_resolved_ids_and_returns_the_number(
        self, okareo: Okareo, httpx_mock: HTTPXMock
    ) -> None:
        httpx_mock.add_response(
            method="POST",
            url=f"{BASE}/v0/outbound/lines",
            json=_line(),
            status_code=201,
        )
        line = okareo.start_outbound_simulation(
            name="collections dry run",
            scenario=SCENARIO_ID,
            target="collections line",
            driver="debtor",
            checks=["result_completed"],
        )
        assert str(line.test_run_id) == RUN_ID
        assert line.status == "on"
        assert line.number == "+15550100000"

        request = _last_request(httpx_mock)
        assert request.headers["api-key"] == "api-key"
        assert json.loads(request.content) == {
            "mut_id": TARGET_ID,
            "scenario_id": SCENARIO_ID,
            "driver_id": DRIVER_ID,
            "name": "collections dry run",
            "checks": ["result_completed"],
        }

    def test_limits_and_turn_settings_travel_under_the_servers_names(
        self, okareo: Okareo, httpx_mock: HTTPXMock
    ) -> None:
        httpx_mock.add_response(
            method="POST",
            url=f"{BASE}/v0/outbound/lines",
            json=_line(),
            status_code=201,
        )
        okareo.start_outbound_simulation(
            name="n",
            scenario=SCENARIO_ID,
            target="collections line",
            max_turns=6,
            first_turn="target",
            max_duration_s=600,
            idle_timeout_s=120,
            expected_caller_ids=["+15551234567"],
        )
        body = json.loads(_last_request(httpx_mock).content)
        assert body["simulation_params"] == {"max_turns": 6, "first_turn": "target"}
        assert body["armed_max_duration_s"] == 600
        assert body["idle_timeout_s"] == 120
        assert body["expected_caller_ids"] == ["+15551234567"]
        assert "max_duration_s" not in body

    @pytest.mark.parametrize(
        "kwargs, needle",
        [
            ({"max_duration_s": 30}, "between 60 and 28800"),
            ({"max_duration_s": 28801}, "between 60 and 28800"),
            ({"idle_timeout_s": 59}, "at least 60"),
        ],
    )
    def test_a_limit_out_of_range_is_refused_before_any_request(
        self,
        okareo: Okareo,
        httpx_mock: HTTPXMock,
        kwargs: Dict[str, Any],
        needle: str,
    ) -> None:
        with pytest.raises(ValueError, match=needle):
            okareo.start_outbound_simulation(
                name="n", scenario=SCENARIO_ID, target="collections line", **kwargs
            )
        assert len(httpx_mock.get_requests()) == 1  # only the projects call

    def test_a_target_okareo_dials_is_refused_before_any_request(
        self, okareo: Okareo, httpx_mock: HTTPXMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            okareo,
            "_resolve_driver_and_target",
            lambda **_: (
                Driver(name="debtor", id=DRIVER_ID),
                Target(
                    name="support line",
                    target={"type": "voice", "edge_type": "twilio"},
                    id=TARGET_ID,
                ),
            ),
        )
        with pytest.raises(ValueError, match="dialed by Okareo"):
            okareo.start_outbound_simulation(
                name="n", scenario=SCENARIO_ID, target="support line"
            )
        assert len(httpx_mock.get_requests()) == 1

    @pytest.mark.parametrize(
        "status, detail",
        [
            (403, "Outbound simulations (your agent calls Okareo) need a paid plan."),
            (429, "This workspace has 10 of 10 outbound Simulations on."),
            (503, "No Okareo number is available for this workspace."),
        ],
    )
    def test_a_refusal_carries_the_servers_reason(
        self, okareo: Okareo, httpx_mock: HTTPXMock, status: int, detail: str
    ) -> None:
        httpx_mock.add_response(
            method="POST",
            url=f"{BASE}/v0/outbound/lines",
            json={"detail": detail},
            status_code=status,
        )
        with pytest.raises(ValueError) as excinfo:
            okareo.start_outbound_simulation(
                name="n", scenario=SCENARIO_ID, target="collections line"
            )
        message = str(excinfo.value)
        assert message.startswith(f"start_outbound_simulation failed: {status} ")
        assert detail in message


class TestStopGetFind:
    def test_stop_posts_to_the_off_route(
        self, okareo: Okareo, httpx_mock: HTTPXMock
    ) -> None:
        httpx_mock.add_response(
            method="POST",
            url=f"{BASE}/v0/outbound/lines/{RUN_ID}/off",
            json=_line(status="draining", close_reason="turned_off", calls_received=2),
            status_code=200,
        )
        line = okareo.stop_outbound_simulation(RUN_ID)
        assert line.status == "draining"
        assert line.close_reason == "turned_off"
        assert line.calls_received == 2

    def test_get_reads_one(self, okareo: Okareo, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="GET",
            url=f"{BASE}/v0/outbound/lines/{RUN_ID}",
            json=_line(calls_received=1),
            status_code=200,
        )
        assert okareo.get_outbound_simulation(RUN_ID).calls_received == 1

    def test_an_unknown_id_is_a_value_error_with_the_reason(
        self, okareo: Okareo, httpx_mock: HTTPXMock
    ) -> None:
        httpx_mock.add_response(
            method="GET",
            url=f"{BASE}/v0/outbound/lines/{RUN_ID}",
            json={"detail": "Line not found."},
            status_code=404,
        )
        with pytest.raises(ValueError, match="404 Line not found."):
            okareo.get_outbound_simulation(RUN_ID)

    def test_find_lists_those_that_are_on(
        self, okareo: Okareo, httpx_mock: HTTPXMock
    ) -> None:
        httpx_mock.add_response(
            method="GET",
            url=f"{BASE}/v0/outbound/lines",
            json=[_line(), _line(calls_received=3)],
            status_code=200,
        )
        lines = okareo.find_outbound_simulations()
        assert [line.calls_received for line in lines] == [0, 3]

    def test_find_with_none_on_is_an_empty_list(
        self, okareo: Okareo, httpx_mock: HTTPXMock
    ) -> None:
        httpx_mock.add_response(
            method="GET", url=f"{BASE}/v0/outbound/lines", json=[], status_code=200
        )
        assert okareo.find_outbound_simulations() == []
