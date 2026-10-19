"""``Simulation.to_dict``: the voice timeouts ride along only when set."""

from okareo.model_under_test import Simulation


def test_timeouts_are_absent_unless_set() -> None:
    d = Simulation().to_dict()

    assert "silence_timeout_ms" not in d
    assert "hold_timeout_ms" not in d


def test_timeouts_are_sent_when_set() -> None:
    d = Simulation(silence_timeout_ms=15000, hold_timeout_ms=60000).to_dict()

    assert d["silence_timeout_ms"] == 15000
    assert d["hold_timeout_ms"] == 60000


def test_the_rest_of_the_payload_is_unchanged() -> None:
    before = dict(Simulation().to_dict())
    after = Simulation(hold_timeout_ms=60000).to_dict()
    after.pop("hold_timeout_ms")

    assert after == before
