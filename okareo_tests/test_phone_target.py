"""Unit tests for PhoneTarget — simplified voice target wrapper."""

from okareo.model_under_test import PhoneTarget, Target


class TestPhoneTarget:
    def test_params_emits_twilio_format(self) -> None:
        pt = PhoneTarget(phone_number="+15551234567")
        params = pt.params()
        assert params["type"] == "voice"
        assert params["edge_type"] == "twilio"
        assert params["to_phone_number"] == "+15551234567"
        assert params["account_sid"] == ""
        assert params["auth_token"] == ""
        assert params["from_phone_number"] is None

    def test_params_with_max_parallel(self) -> None:
        pt = PhoneTarget(phone_number="+15551234567", max_parallel_requests=5)
        params = pt.params()
        assert params["max_parallel_requests"] == 5

    def test_target_to_dict(self) -> None:
        t = Target(name="Test Agent", target=PhoneTarget(phone_number="+15551234567"))
        d = t.to_dict()
        assert d["name"] == "Test Agent"
        assert d["target"]["to_phone_number"] == "+15551234567"
        assert d["target"]["type"] == "voice"
        assert d["target"]["edge_type"] == "twilio"
