"""Unit tests for run_load_test's optional call-cycling (per-call max-duration) knob.

These construct a bare Okareo via ``__new__`` (bypassing __init__/network). Shape and
pacing caps (floor, hard per-call kill, dial rate) are enforced SERVER-SIDE, so the SDK
only forwards the flat knob (guarding a non-positive value) and the happy path is covered
by capturing the run_simulation kwargs.
"""

from typing import Any

import pytest

from okareo import Okareo


def _bare_client() -> Okareo:
    # Bypass __init__ (which would need an API key / network). run_load_test's cycling
    # path only touches its args and the loadtest passthrough it builds.
    return Okareo.__new__(Okareo)


def test_cap_forwarded_in_loadtest_cfg(monkeypatch: pytest.MonkeyPatch) -> None:
    """A per-call cap is shipped as the flat loadtest_per_call_max_duration_s knob, and the
    two load knobs are left intact."""
    ok = _bare_client()
    captured: dict[str, Any] = {}
    monkeypatch.setattr(ok, "create_scenario_set", lambda _s: object())
    monkeypatch.setattr(
        ok, "run_simulation", lambda **k: captured.update(k) or object()
    )
    ok.run_load_test(
        name="lt",
        target="t",
        load_concurrent=50,
        load_duration_s=120,
        per_call_max_duration_s=90,
    )
    cfg = captured["loadtest"]
    assert cfg["loadtest_target_concurrent"] == 50
    assert cfg["loadtest_load_duration_s"] == 120.0
    assert cfg["loadtest_per_call_max_duration_s"] == 90.0


def test_small_cap_is_forwarded_not_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    """The SDK no longer second-guesses the shape (floor / hard-cap / backfill feasibility
    are server-owned); even a small cap is forwarded verbatim."""
    ok = _bare_client()
    captured: dict[str, Any] = {}
    monkeypatch.setattr(ok, "create_scenario_set", lambda _s: object())
    monkeypatch.setattr(
        ok, "run_simulation", lambda **k: captured.update(k) or object()
    )
    ok.run_load_test(
        name="lt",
        target="t",
        load_concurrent=10,
        load_duration_s=60,
        per_call_max_duration_s=5,
    )
    assert captured["loadtest"]["loadtest_per_call_max_duration_s"] == 5.0


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


def test_omitting_cap_leaves_loadtest_cfg_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No per_call_max_duration_s => the passthrough carries only the two load knobs
    (byte-for-byte the classic held-call contract)."""
    ok = _bare_client()
    captured: dict[str, Any] = {}
    monkeypatch.setattr(ok, "create_scenario_set", lambda _s: object())
    monkeypatch.setattr(
        ok, "run_simulation", lambda **k: captured.update(k) or object()
    )
    ok.run_load_test(
        name="lt",
        target="t",
        load_concurrent=50,
        load_duration_s=120,
    )
    cfg = captured["loadtest"]
    assert "loadtest_per_call_max_duration_s" not in cfg
    assert set(cfg) == {"loadtest_target_concurrent", "loadtest_load_duration_s"}
