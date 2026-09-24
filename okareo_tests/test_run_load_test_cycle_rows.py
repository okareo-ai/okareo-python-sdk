"""Unit tests for run_load_test's scenario contract and the loadtest_* wire contract.

``run_load_test`` takes an existing scenario set exactly as ``run_simulation`` does (a
``ScenarioSetResponse`` or a scenario-set id, required, second positional) and forwards
it verbatim; the server cycles its rows for the whole hold. The SDK creates NOTHING: no
scenario set, no tiling, no over-provisioned pool. ``seed_data`` is gone (a contract
change from 0.0.157). ``max_total_calls`` is an optional conversation budget shipped as
``loadtest_max_total_calls`` and validated client-side before any network call.

Same harness as test_run_load_test_call_cycling.py: a bare Okareo via ``__new__`` (no
__init__/network), ``create_scenario_set`` patched to FAIL if ever called, and the shared
``_submit_multiturn`` seam patched to capture what run_load_test hands it.
"""

import datetime
from typing import Any
from uuid import UUID

import pytest

from okareo import Okareo
from okareo_api_client.models.scenario_set_response import ScenarioSetResponse


def _bare_client() -> Okareo:
    return Okareo.__new__(Okareo)


def _forbid_scenario_creation(ok: Okareo, monkeypatch: pytest.MonkeyPatch) -> None:
    """run_load_test must never create a scenario set; make any attempt fail loudly."""

    def _boom(*_a: Any, **_k: Any) -> Any:
        raise AssertionError("run_load_test must not call create_scenario_set")

    monkeypatch.setattr(ok, "create_scenario_set", _boom)


def _capture(ok: Okareo, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Capture the _submit_multiturn kwargs; scenario creation is forbidden."""
    captured: dict[str, Any] = {}
    _forbid_scenario_creation(ok, monkeypatch)
    monkeypatch.setattr(
        ok, "_submit_multiturn", lambda **k: captured.update(k) or object()
    )
    return captured


def _no_network(ok: Okareo, monkeypatch: pytest.MonkeyPatch) -> None:
    """Fail loudly if validation lets a bad call reach the scenario/submit seams."""

    def _boom(*_a: Any, **_k: Any) -> Any:
        raise AssertionError("network seam reached before validation rejected input")

    monkeypatch.setattr(ok, "create_scenario_set", _boom)
    monkeypatch.setattr(ok, "_submit_multiturn", _boom)


def _loadtest_keys(simulation_params: dict) -> set:
    return {k for k in simulation_params if k.startswith("loadtest_")}


def _scenario_response() -> ScenarioSetResponse:
    return ScenarioSetResponse(
        project_id=UUID(int=1),
        time_created=datetime.datetime.now(),
        type_="SEED",
        scenario_id=UUID(int=2),
        name="existing",
    )


# --- scenario: forwarded verbatim, nothing created ------------------------------------


def test_scenario_id_forwarded_verbatim(monkeypatch: pytest.MonkeyPatch) -> None:
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario="9b1d3c2e-existing-scenario-id",
        target="t",
        load_concurrent=10,
        load_duration_s=60,
    )
    assert captured["scenario"] == "9b1d3c2e-existing-scenario-id"
    assert captured["name"] == "lt"
    assert captured["target"] == "t"
    assert captured["submit"] is True
    assert captured["simulation_params"]["loadtest_target_concurrent"] == 10


def test_scenario_response_object_forwarded_verbatim(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A ScenarioSetResponse is handed to the submit seam as the SAME object, exactly as
    run_simulation does; the SDK does not unwrap it to an id or re-create it."""
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    scenario = _scenario_response()
    ok.run_load_test(
        name="lt",
        scenario=scenario,
        target="t",
        load_concurrent=10,
        load_duration_s=60,
    )
    assert captured["scenario"] is scenario


def test_create_scenario_set_is_never_called(monkeypatch: pytest.MonkeyPatch) -> None:
    """Even with every optional knob set, no scenario set is created; the patched
    create_scenario_set raises AssertionError if reached."""
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario="existing-id",
        target="t",
        load_concurrent=50,
        load_duration_s=1800,
        per_call_max_duration_s=90,
        first_turn="driver",
        max_total_calls=200,
    )
    assert captured["scenario"] == "existing-id"


def test_positional_order_mirrors_run_simulation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """(name, scenario, target, load_concurrent, load_duration_s) positionally, the same
    leading order as run_simulation(name, scenario, target, ...)."""
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test("lt", "scenario-id", "t", 25, 300)
    assert captured["name"] == "lt"
    assert captured["scenario"] == "scenario-id"
    assert captured["target"] == "t"
    sp = captured["simulation_params"]
    assert sp["loadtest_target_concurrent"] == 25
    assert sp["loadtest_load_duration_s"] == 300.0


def test_seed_data_keyword_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    """Contract change from 0.0.157: seed_data no longer exists on run_load_test."""
    ok = _bare_client()
    _no_network(ok, monkeypatch)
    with pytest.raises(TypeError, match="seed_data"):
        ok.run_load_test(  # type: ignore[call-arg]
            name="lt",
            scenario="scenario-id",
            target="t",
            load_concurrent=10,
            load_duration_s=60,
            seed_data=[{"q": "a"}],
        )


def test_scenario_is_required(monkeypatch: pytest.MonkeyPatch) -> None:
    ok = _bare_client()
    _no_network(ok, monkeypatch)
    with pytest.raises(TypeError, match="scenario"):
        ok.run_load_test(  # type: ignore[call-arg]
            name="lt", target="t", load_concurrent=10, load_duration_s=60
        )


# --- max_total_calls ---------------------------------------------------------------------


def test_max_total_calls_forwarded(monkeypatch: pytest.MonkeyPatch) -> None:
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario="scenario-id",
        target="t",
        load_concurrent=25,
        load_duration_s=1800,
        max_total_calls=100,
    )
    sp = captured["simulation_params"]
    assert sp["loadtest_max_total_calls"] == 100
    assert isinstance(sp["loadtest_max_total_calls"], int)


def test_max_total_calls_equal_to_concurrency_is_accepted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario="scenario-id",
        target="t",
        load_concurrent=25,
        load_duration_s=60,
        max_total_calls=25,
    )
    assert captured["simulation_params"]["loadtest_max_total_calls"] == 25


def test_max_total_calls_none_omits_the_key(monkeypatch: pytest.MonkeyPatch) -> None:
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario="scenario-id",
        target="t",
        load_concurrent=25,
        load_duration_s=60,
        max_total_calls=None,
    )
    assert "loadtest_max_total_calls" not in captured["simulation_params"]


@pytest.mark.parametrize("bad", [0, -1, -100])
def test_max_total_calls_below_one_raises_before_network(
    monkeypatch: pytest.MonkeyPatch, bad: int
) -> None:
    ok = _bare_client()
    _no_network(ok, monkeypatch)
    with pytest.raises(ValueError, match="max_total_calls must be >= 1"):
        ok.run_load_test(
            name="lt",
            scenario="scenario-id",
            target="t",
            load_concurrent=1,
            load_duration_s=60,
            max_total_calls=bad,
        )


def test_max_total_calls_below_concurrency_raises_before_network(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ok = _bare_client()
    _no_network(ok, monkeypatch)
    with pytest.raises(ValueError, match="must be >= load_concurrent"):
        ok.run_load_test(
            name="lt",
            scenario="scenario-id",
            target="t",
            load_concurrent=25,
            load_duration_s=60,
            max_total_calls=24,
        )


# --- per-call cap and the wire contract -------------------------------------------------


def test_per_call_cap_still_forwarded(monkeypatch: pytest.MonkeyPatch) -> None:
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario="scenario-id",
        target="t",
        load_concurrent=10,
        load_duration_s=60,
        per_call_max_duration_s=45,
    )
    sp = captured["simulation_params"]
    assert sp["loadtest_per_call_max_duration_s"] == 45.0


def test_wire_contract_default_key_set(monkeypatch: pytest.MonkeyPatch) -> None:
    """Defaults ship exactly the two base load knobs and nothing else."""
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario="scenario-id",
        target="t",
        load_concurrent=10,
        load_duration_s=60,
    )
    sp = captured["simulation_params"]
    assert _loadtest_keys(sp) == {
        "loadtest_target_concurrent",
        "loadtest_load_duration_s",
    }
    assert sp["loadtest_target_concurrent"] == 10
    assert sp["loadtest_load_duration_s"] == 60.0
    # Conventional turn controls are untouched by the cycling change.
    assert sp["max_turns"] == 25
    assert sp["repeats"] == 1
    assert sp["first_turn"] == "target"


def test_wire_contract_full_key_set(monkeypatch: pytest.MonkeyPatch) -> None:
    """With every optional knob set, the loadtest_* keys are exactly the wire contract:
    target_concurrent, load_duration_s, per_call_max_duration_s, max_total_calls."""
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario="existing-id",
        target="t",
        load_concurrent=25,
        load_duration_s=1800,
        per_call_max_duration_s=90,
        max_total_calls=100,
    )
    sp = captured["simulation_params"]
    assert _loadtest_keys(sp) == {
        "loadtest_target_concurrent",
        "loadtest_load_duration_s",
        "loadtest_per_call_max_duration_s",
        "loadtest_max_total_calls",
    }
    assert sp["loadtest_target_concurrent"] == 25
    assert sp["loadtest_load_duration_s"] == 1800.0
    assert sp["loadtest_per_call_max_duration_s"] == 90.0
    assert sp["loadtest_max_total_calls"] == 100
    assert captured["scenario"] == "existing-id"
