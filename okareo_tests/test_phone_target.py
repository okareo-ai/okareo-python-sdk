"""Unit tests for PhoneTarget — simplified voice target wrapper."""

import pytest

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


class TestPhoneTargetDtmfMechanism:
    """The DTMF control. Unset means in-band, which is what a phone target has
    always done, so targets saved before the field existed are unaffected."""

    def test_unset_emits_no_key_at_all(self) -> None:
        params = PhoneTarget(phone_number="+15551234567").params()
        assert "dtmf_mechanism" not in params

    def test_rfc2833_is_emitted(self) -> None:
        params = PhoneTarget(
            phone_number="+15551234567", dtmf_mechanism="rfc2833"
        ).params()
        assert params["dtmf_mechanism"] == "rfc2833"
        # The routing field only: the target is still saved as a phone target.
        assert params["edge_type"] == "twilio"

    def test_inband_is_emitted(self) -> None:
        params = PhoneTarget(
            phone_number="+15551234567", dtmf_mechanism="inband"
        ).params()
        assert params["dtmf_mechanism"] == "inband"

    def test_value_is_normalized(self) -> None:
        params = PhoneTarget(
            phone_number="+15551234567", dtmf_mechanism="  RFC2833 "
        ).params()
        assert params["dtmf_mechanism"] == "rfc2833"

    def test_blank_is_treated_as_unset(self) -> None:
        params = PhoneTarget(phone_number="+15551234567", dtmf_mechanism="   ").params()
        assert "dtmf_mechanism" not in params

    @pytest.mark.parametrize("value", ["both", "oob", "rfc4733", "off"])
    def test_invalid_value_fails_at_construction(self, value: str) -> None:
        """A typo should fail here, not as a 400 after the run is submitted.
        'both' is excluded on measured evidence, not an oversight."""
        with pytest.raises(ValueError, match="Invalid dtmf_mechanism"):
            PhoneTarget(phone_number="+15551234567", dtmf_mechanism=value)
