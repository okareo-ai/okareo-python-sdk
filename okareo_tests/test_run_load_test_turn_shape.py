"""Unit tests for run_load_test's ``first_turn`` knob.

Same harness as test_run_load_test_call_cycling.py: a bare Okareo via ``__new__`` (no
__init__/network), ``create_scenario_set`` patched to FAIL if ever called (run_load_test
forwards an existing scenario and creates nothing), and the shared ``_submit_multiturn``
seam patched to capture the simulation_params run_load_test hands it. ``first_turn`` shapes
each held call, not the load: the default must match run_simulation (target-first), an
explicit value must be forwarded verbatim into the Simulation, and a bad value must fail
fast before any network call.
"""

from typing import Any

import pytest

from okareo import Okareo

SCENARIO_ID = "scenario-id"


def _bare_client() -> Okareo:
    return Okareo.__new__(Okareo)


def _capture(ok: Okareo, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    captured: dict[str, Any] = {}

    def _boom(*_a: Any, **_k: Any) -> Any:
        raise AssertionError("run_load_test must not call create_scenario_set")

    monkeypatch.setattr(ok, "create_scenario_set", _boom)
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


def test_default_is_target_first(monkeypatch: pytest.MonkeyPatch) -> None:
    """Omitting first_turn gives run_simulation's default: the agent speaks first. The
    25-turn backstop and repeats=1 are untouched."""
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario=SCENARIO_ID,
        target="t",
        load_concurrent=10,
        load_duration_s=60,
    )
    sp = captured["simulation_params"]
    assert sp["first_turn"] == "target"
    assert sp["max_turns"] == 25
    assert sp["repeats"] == 1


def test_driver_first_is_forwarded(monkeypatch: pytest.MonkeyPatch) -> None:
    """A target that waits for the caller: first_turn="driver" rides verbatim in the
    Simulation, and the load knobs are untouched by it."""
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario=SCENARIO_ID,
        target="t",
        load_concurrent=10,
        load_duration_s=60,
        first_turn="driver",
    )
    sp = captured["simulation_params"]
    assert sp["first_turn"] == "driver"
    assert sp["max_turns"] == 25
    assert sp["repeats"] == 1
    assert sp["loadtest_target_concurrent"] == 10
    assert sp["loadtest_load_duration_s"] == 60.0
    assert {k for k in sp if k.startswith("loadtest_")} == {
        "loadtest_target_concurrent",
        "loadtest_load_duration_s",
    }


def test_explicit_target_first_is_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario=SCENARIO_ID,
        target="t",
        load_concurrent=10,
        load_duration_s=60,
        first_turn="target",
    )
    assert captured["simulation_params"]["first_turn"] == "target"


@pytest.mark.parametrize("bad", ["caller", "Target", "", None])
def test_invalid_first_turn_raises_before_network(
    monkeypatch: pytest.MonkeyPatch, bad: Any
) -> None:
    ok = _bare_client()
    _no_network(ok, monkeypatch)
    with pytest.raises(ValueError, match="first_turn"):
        ok.run_load_test(
            name="lt",
            scenario=SCENARIO_ID,
            target="t",
            load_concurrent=10,
            load_duration_s=60,
            first_turn=bad,
        )


def test_first_turn_does_not_change_the_scenario(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """first_turn shapes the conversation, not the load: the scenario is forwarded
    verbatim (the server cycles its rows) and nothing is created, regardless of who
    speaks first."""
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario=SCENARIO_ID,
        target="t",
        load_concurrent=50,
        load_duration_s=120,
        first_turn="driver",
    )
    assert captured["scenario"] == SCENARIO_ID
    assert captured["simulation_params"]["first_turn"] == "driver"
