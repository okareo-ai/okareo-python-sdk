"""Hermetic unit tests for the deprecated (inert) stop_check mechanism.

stop_check is retired backend-side: it is still accepted and serialized by the
SDK for backward compatibility, but no longer terminates a simulation early.
These tests assert the SDK still serializes it exactly as before (no network,
no server) and that a malformed dict remains a client-side TypeError.
"""

import pytest

from okareo.model_under_test import Simulation, StopConfig


class TestStopCheckDeprecation:
    def test_simulation_to_dict_serializes_stop_check_dict(self) -> None:
        sim = Simulation(stop_check={"check_name": "x", "stop_on": True})
        # A dict stop_check is coerced to StopConfig in __attrs_post_init__ and
        # serialized back via StopConfig.params() in to_dict().
        assert sim.to_dict()["stop_check"] == {"check_name": "x", "stop_on": True}

    def test_simulation_to_dict_serializes_stop_config_instance(self) -> None:
        sim = Simulation(stop_check=StopConfig(check_name="x", stop_on=True))
        assert sim.to_dict()["stop_check"] == {"check_name": "x", "stop_on": True}

    def test_simulation_to_dict_none_stop_check(self) -> None:
        sim = Simulation()
        assert sim.to_dict()["stop_check"] is None

    def test_stop_config_params_shape(self) -> None:
        sc = StopConfig(check_name="x", stop_on=False)
        assert sc.params() == {"check_name": "x", "stop_on": False}

    def test_stop_config_default_stop_on_is_true(self) -> None:
        sc = StopConfig(check_name="x")
        assert sc.params() == {"check_name": "x", "stop_on": True}

    def test_malformed_stop_check_dict_raises_type_error(self) -> None:
        # A malformed dict (missing check_name) is a caller bug and still raises
        # client-side, distinct from a valid-but-inert legacy stop_check.
        with pytest.raises(TypeError):
            Simulation(stop_check={"invalid_field": "model_refusal"})
