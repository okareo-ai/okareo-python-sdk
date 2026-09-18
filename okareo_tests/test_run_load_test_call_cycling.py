"""Unit tests for run_load_test's optional call-cycling (per-call max-duration) knob.

These construct a bare Okareo via ``__new__`` (bypassing __init__/network). run_load_test
builds its OWN simulation_params (conventional turn controls + the flat loadtest_* knobs)
and submits via the shared ``_submit_multiturn`` seam — run_simulation is never involved —
so the tests patch that seam and capture the simulation_params it is handed. Shape/pacing
caps are enforced server-side, so the SDK only forwards the flat knob (guarding a
non-positive value).
"""

from typing import Any

import pytest

from okareo import Okareo


def _bare_client() -> Okareo:
    # Bypass __init__ (which would need an API key / network). run_load_test's cycling
    # path only touches its args, the Simulation it builds, and the submit seam.
    return Okareo.__new__(Okareo)


def _loadtest_keys(simulation_params: dict) -> set:
    return {k for k in simulation_params if k.startswith("loadtest_")}


def test_cap_forwarded_in_simulation_params(monkeypatch: pytest.MonkeyPatch) -> None:
    """A per-call cap is shipped as the flat loadtest_per_call_max_duration_s knob inside
    simulation_params, alongside the two base load knobs."""
    ok = _bare_client()
    captured: dict[str, Any] = {}
    monkeypatch.setattr(ok, "create_scenario_set", lambda _s: object())
    monkeypatch.setattr(
        ok, "_submit_multiturn", lambda **k: captured.update(k) or object()
    )
    ok.run_load_test(
        name="lt",
        target="t",
        load_concurrent=50,
        load_duration_s=120,
        per_call_max_duration_s=90,
    )
    sp = captured["simulation_params"]
    assert sp["loadtest_target_concurrent"] == 50
    assert sp["loadtest_load_duration_s"] == 120.0
    assert sp["loadtest_per_call_max_duration_s"] == 90.0
    # Conventional turn controls ride in the same dict (built via Simulation).
    assert sp["max_turns"] == 25
    assert sp["repeats"] == 1
    assert sp["first_turn"] == "driver"


def test_small_cap_is_forwarded_not_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    """The SDK no longer second-guesses the shape (floor / hard-cap / backfill feasibility
    are server-owned); even a small cap is forwarded verbatim."""
    ok = _bare_client()
    captured: dict[str, Any] = {}
    monkeypatch.setattr(ok, "create_scenario_set", lambda _s: object())
    monkeypatch.setattr(
        ok, "_submit_multiturn", lambda **k: captured.update(k) or object()
    )
    ok.run_load_test(
        name="lt",
        target="t",
        load_concurrent=10,
        load_duration_s=60,
        per_call_max_duration_s=5,
    )
    assert captured["simulation_params"]["loadtest_per_call_max_duration_s"] == 5.0


def test_non_positive_cap_raises() -> None:
    ok = _bare_client()
    with pytest.raises(ValueError, match="must be > 0"):
        ok.run_load_test(
            name="lt",
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
    captured: dict[str, Any] = {}
    monkeypatch.setattr(ok, "create_scenario_set", lambda _s: object())
    monkeypatch.setattr(
        ok, "_submit_multiturn", lambda **k: captured.update(k) or object()
    )
    ok.run_load_test(
        name="lt",
        target="t",
        load_concurrent=50,
        load_duration_s=120,
    )
    sp = captured["simulation_params"]
    assert _loadtest_keys(sp) == {
        "loadtest_target_concurrent",
        "loadtest_load_duration_s",
    }


def test_cycling_presizes_row_pool_for_the_window(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """With cycling the finite pool must cover the whole ramp+hold+drain window, so n_rows is
    scaled by the number of cycles — much larger than the drop-margin-only pool a held-call
    run uses. Uses the server's pacing defaults (overridable via env)."""
    monkeypatch.setenv("OKAREO_LOADTEST_CPS", "5")
    monkeypatch.setenv("MANAGER_LOADTEST_DRAIN_MARGIN_S", "120")
    ok = _bare_client()
    sizes: dict[str, int] = {}

    def _capture_scenario(spec: Any) -> Any:
        sizes["n_rows"] = len(spec.seed_data)
        return object()

    monkeypatch.setattr(ok, "create_scenario_set", _capture_scenario)
    monkeypatch.setattr(ok, "_submit_multiturn", lambda **k: object())

    # ramp=50/5=10; window=10+120+120=250; cycles=ceil(250/90)=3; n_rows=ceil(50*1.2*3)=180.
    ok.run_load_test(
        name="lt",
        target="t",
        load_concurrent=50,
        load_duration_s=120,
        per_call_max_duration_s=90,
    )
    assert sizes["n_rows"] == 180

    # Held-call (no cap) pool is just the drop margin: ceil(50*1.2)=60.
    sizes.clear()
    ok.run_load_test(
        name="lt",
        target="t",
        load_concurrent=50,
        load_duration_s=120,
    )
    assert sizes["n_rows"] == 60
