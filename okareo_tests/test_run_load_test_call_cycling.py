"""Unit tests for run_load_test's optional call-cycling (per-call max-duration) knob.

These construct a bare Okareo via ``__new__`` (bypassing __init__/network). run_load_test
builds its OWN simulation_params (repeats + first_turn + the flat loadtest_* knobs)
and submits via the shared ``_submit_multiturn`` seam — run_simulation is never involved —
so the tests patch that seam and capture the simulation_params it is handed. Shape/pacing
caps are enforced server-side, so the SDK only forwards the flat knob (guarding a
non-positive value). The cap is per-call truncation only: the scenario is an existing set
forwarded verbatim (the server cycles its rows for the whole hold), so the cap never
sizes anything and ``create_scenario_set`` is never called.
"""

from typing import Any

import pytest

from okareo import Okareo

SCENARIO_ID = "scenario-id"


def _bare_client() -> Okareo:
    # Bypass __init__ (which would need an API key / network). run_load_test's cycling
    # path only touches its args, the Simulation it builds, and the submit seam.
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


def _loadtest_keys(simulation_params: dict) -> set:
    return {k for k in simulation_params if k.startswith("loadtest_")}


def test_cap_forwarded_in_simulation_params(monkeypatch: pytest.MonkeyPatch) -> None:
    """A per-call cap is shipped as the flat loadtest_per_call_max_duration_s knob inside
    simulation_params, alongside the two base load knobs."""
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario=SCENARIO_ID,
        target="t",
        load_concurrent=50,
        load_duration_s=120,
        per_call_max_duration_s=90,
    )
    sp = captured["simulation_params"]
    assert sp["loadtest_target_concurrent"] == 50
    assert sp["loadtest_load_duration_s"] == 120.0
    assert sp["loadtest_per_call_max_duration_s"] == 90.0
    # repeats / first_turn ride in the same dict (built via Simulation); no max_turns
    # is ever sent -- the per-call bound is a duration, not a turn count.
    assert sp["max_turns"] == 5  # run_simulation's default
    assert sp["repeats"] == 1
    assert sp["first_turn"] == "target"
    assert captured["scenario"] == SCENARIO_ID


def test_small_cap_is_forwarded_not_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    """The SDK no longer second-guesses the shape (floor / hard-cap / backfill feasibility
    are server-owned); even a small cap is forwarded verbatim."""
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario=SCENARIO_ID,
        target="t",
        load_concurrent=10,
        load_duration_s=60,
        per_call_max_duration_s=5,
    )
    assert captured["simulation_params"]["loadtest_per_call_max_duration_s"] == 5.0


def test_non_positive_cap_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    ok = _bare_client()
    _capture(ok, monkeypatch)
    with pytest.raises(ValueError, match="must be > 0"):
        ok.run_load_test(
            name="lt",
            scenario=SCENARIO_ID,
            target="t",
            load_concurrent=10,
            load_duration_s=60,
            per_call_max_duration_s=0,
        )


def test_omitting_cap_ships_only_the_two_base_load_knobs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No per_call_max_duration_s => the only loadtest_* keys are the two base load knobs
    (the classic held-call contract)."""
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)
    ok.run_load_test(
        name="lt",
        scenario=SCENARIO_ID,
        target="t",
        load_concurrent=50,
        load_duration_s=120,
    )
    sp = captured["simulation_params"]
    assert _loadtest_keys(sp) == {
        "loadtest_target_concurrent",
        "loadtest_load_duration_s",
    }


def test_cap_does_not_touch_the_scenario(monkeypatch: pytest.MonkeyPatch) -> None:
    """The per-call cap is truncation only. The scenario is forwarded verbatim whether or
    not a cap is set (the server cycles its rows for the whole hold), nothing is created,
    and the old CPS / drain-margin env mirrors have no effect."""
    monkeypatch.setenv("OKAREO_LOADTEST_CPS", "1")
    monkeypatch.setenv("MANAGER_LOADTEST_DRAIN_MARGIN_S", "9999")
    ok = _bare_client()
    captured = _capture(ok, monkeypatch)

    ok.run_load_test(
        name="lt",
        scenario=SCENARIO_ID,
        target="t",
        load_concurrent=50,
        load_duration_s=120,
        per_call_max_duration_s=90,
    )
    assert captured["scenario"] == SCENARIO_ID
    assert captured["simulation_params"]["loadtest_per_call_max_duration_s"] == 90.0

    captured.clear()
    ok.run_load_test(
        name="lt",
        scenario=SCENARIO_ID,
        target="t",
        load_concurrent=50,
        load_duration_s=120,
    )
    assert captured["scenario"] == SCENARIO_ID
    assert "loadtest_per_call_max_duration_s" not in captured["simulation_params"]
