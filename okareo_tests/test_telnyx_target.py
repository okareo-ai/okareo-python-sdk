"""Unit tests for TelnyxPhoneTarget — Telnyx-backed voice target wrapper."""

import pytest

from okareo.model_under_test import Target, TelnyxPhoneTarget


class TestTelnyxPhoneTarget:
    def test_params_emits_telnyx_format(self) -> None:
        vt = TelnyxPhoneTarget(
            phone_number="+15551234567",
            from_phone_number="+15557654321",
            api_key="KEY0123abc",
            connection_id="conn-123",
        )
        params = vt.params()
        assert params["type"] == "voice"
        assert params["edge_type"] == "telnyx"
        assert params["to_phone_number"] == "+15551234567"
        assert params["from_phone_number"] == "+15557654321"
        assert params["api_key"] == "KEY0123abc"
        assert params["connection_id"] == "conn-123"
        assert params["max_parallel_requests"] is None
        # Closed contract: params() emits exactly these keys. Pins the cross-repo
        # payload (server factory + FE schema read it) and catches a stray/re-added
        # key without naming any specific field.
        assert set(params) == {
            "type",
            "edge_type",
            "to_phone_number",
            "from_phone_number",
            "api_key",
            "connection_id",
            "max_parallel_requests",
        }

    def test_phone_number_alias_maps_to_to_phone_number(self) -> None:
        vt = TelnyxPhoneTarget(phone_number="+15551234567")
        assert vt.params()["to_phone_number"] == "+15551234567"

    def test_to_phone_number_takes_precedence_over_phone_number(self) -> None:
        vt = TelnyxPhoneTarget(
            phone_number="+15551234567", to_phone_number="+19998887777"
        )
        assert vt.params()["to_phone_number"] == "+19998887777"

    def test_params_with_max_parallel(self) -> None:
        vt = TelnyxPhoneTarget(phone_number="+15551234567", max_parallel_requests=5)
        assert vt.params()["max_parallel_requests"] == 5

    def test_get_sensitive_fields_marks_api_key(self) -> None:
        vt = TelnyxPhoneTarget(
            phone_number="+15551234567",
            api_key="KEY0123abc",
            connection_id="conn-123",
        )
        sensitive = vt.get_sensitive_fields()
        assert "api_key" in sensitive
        # connection_id is not sensitive, mirroring how account_sid/application_id
        # are not sensitive on the Twilio/Vonage siblings.
        assert "connection_id" not in sensitive

    def test_get_sensitive_fields_empty_when_no_creds(self) -> None:
        vt = TelnyxPhoneTarget(phone_number="+15551234567")
        assert vt.get_sensitive_fields() == []

    def test_requires_a_destination(self) -> None:
        # No destination fails fast at construction (like the siblings) rather
        # than surfacing late as an opaque Telnyx dial error mid-run.
        with pytest.raises(ValueError):
            TelnyxPhoneTarget(api_key="KEY0123abc", connection_id="conn-123")

    def test_template_destination_is_accepted(self) -> None:
        vt = TelnyxPhoneTarget(phone_number="{scenario_input.phone}")
        assert vt.params()["to_phone_number"] == "{scenario_input.phone}"

    def test_target_to_dict(self) -> None:
        t = Target(
            name="Test Agent",
            target=TelnyxPhoneTarget(
                phone_number="+15551234567",
                api_key="KEY0123abc",
                connection_id="conn-123",
            ),
        )
        d = t.to_dict()
        assert d["name"] == "Test Agent"
        assert d["target"]["to_phone_number"] == "+15551234567"
        assert d["target"]["type"] == "voice"
        assert d["target"]["edge_type"] == "telnyx"
        assert d["target"]["connection_id"] == "conn-123"
        assert d["sensitive_fields"] == ["api_key"]
