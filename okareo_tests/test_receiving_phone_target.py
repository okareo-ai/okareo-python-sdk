"""Unit tests for ReceivingPhoneTarget — the voice target an agent calls."""

from okareo.model_under_test import (
    RECEIVING_CALL_DIRECTION,
    ReceivingPhoneTarget,
    Target,
)


class TestReceivingPhoneTarget:
    def test_params_carry_the_direction_and_nothing_to_dial(self) -> None:
        params = ReceivingPhoneTarget().params()
        # Closed contract: a receiving target has nothing to dial, so it sends
        # no number and no edge. A stray edge_type or to_phone_number here
        # would describe a target Okareo dials.
        assert params == {"type": "voice", "call_direction": "agent_calls_okareo"}
        assert params["call_direction"] == RECEIVING_CALL_DIRECTION

    def test_optional_settings_are_sent_only_when_set(self) -> None:
        params = ReceivingPhoneTarget(
            expected_caller_ids=["+15551234567"], max_parallel_requests=3
        ).params()
        assert params == {
            "type": "voice",
            "call_direction": "agent_calls_okareo",
            "expected_caller_ids": ["+15551234567"],
            "max_parallel_requests": 3,
        }

    def test_an_empty_caller_list_is_not_sent(self) -> None:
        assert (
            "expected_caller_ids"
            not in ReceivingPhoneTarget(expected_caller_ids=[]).params()
        )

    def test_it_has_no_sensitive_fields(self) -> None:
        assert ReceivingPhoneTarget().get_sensitive_fields() == []

    def test_it_wraps_in_a_target(self) -> None:
        out = Target(name="collections line", target=ReceivingPhoneTarget()).to_dict()
        assert out["name"] == "collections line"
        assert out["target"]["call_direction"] == "agent_calls_okareo"
        assert "sensitive_fields" not in out
