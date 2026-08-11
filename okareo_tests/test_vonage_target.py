"""Unit tests for VonagePhoneTarget — Vonage-backed voice target wrapper."""

import pytest

from okareo.model_under_test import Target, VonagePhoneTarget


class TestVonagePhoneTarget:
    def test_params_emits_vonage_format(self) -> None:
        vt = VonagePhoneTarget(
            phone_number="+15551234567",
            from_phone_number="+15557654321",
            application_id="app-123",
            private_key="-----BEGIN PRIVATE KEY-----\nabc\n-----END PRIVATE KEY-----",
        )
        params = vt.params()
        assert params["type"] == "voice"
        assert params["edge_type"] == "vonage"
        assert params["to_phone_number"] == "+15551234567"
        assert params["from_phone_number"] == "+15557654321"
        assert params["application_id"] == "app-123"
        assert (
            params["private_key"]
            == "-----BEGIN PRIVATE KEY-----\nabc\n-----END PRIVATE KEY-----"
        )
        assert params["max_parallel_requests"] is None
        # DTMF mechanism, recording, and sample rate are fixed server-side
        # defaults, not target params — they must not appear in the payload.
        for dropped in ("private_key_path", "sip_uri", "dtmf_mechanism", "record", "sr"):
            assert dropped not in params

    def test_phone_number_alias_maps_to_to_phone_number(self) -> None:
        vt = VonagePhoneTarget(phone_number="+15551234567")
        params = vt.params()
        assert params["to_phone_number"] == "+15551234567"

    def test_to_phone_number_takes_precedence_over_phone_number(self) -> None:
        vt = VonagePhoneTarget(
            phone_number="+15551234567", to_phone_number="+19998887777"
        )
        params = vt.params()
        assert params["to_phone_number"] == "+19998887777"

    def test_params_with_max_parallel(self) -> None:
        vt = VonagePhoneTarget(phone_number="+15551234567", max_parallel_requests=5)
        params = vt.params()
        assert params["max_parallel_requests"] == 5

    def test_get_sensitive_fields_marks_private_key(self) -> None:
        vt = VonagePhoneTarget(
            phone_number="+15551234567",
            application_id="app-123",
            private_key="pem-contents",
        )
        sensitive = vt.get_sensitive_fields()
        assert "private_key" in sensitive
        # application_id is not treated as sensitive, mirroring
        # TwilioVoiceTarget (account_sid is not sensitive, only auth_token).
        assert "application_id" not in sensitive

    def test_get_sensitive_fields_empty_when_no_creds(self) -> None:
        vt = VonagePhoneTarget(phone_number="+15551234567")
        assert vt.get_sensitive_fields() == []

    def test_requires_a_destination(self) -> None:
        # SDK-3: no destination fails fast at construction (like the siblings)
        # rather than surfacing late as an opaque Vonage dial error mid-run.
        with pytest.raises(ValueError):
            VonagePhoneTarget(application_id="app-123", private_key="pem")

    def test_template_destination_is_accepted(self) -> None:
        vt = VonagePhoneTarget(phone_number="{scenario_input.phone}")
        assert vt.params()["to_phone_number"] == "{scenario_input.phone}"

    def test_target_to_dict(self) -> None:
        t = Target(
            name="Test Agent",
            target=VonagePhoneTarget(
                phone_number="+15551234567",
                application_id="app-123",
                private_key="pem-contents",
            ),
        )
        d = t.to_dict()
        assert d["name"] == "Test Agent"
        assert d["target"]["to_phone_number"] == "+15551234567"
        assert d["target"]["type"] == "voice"
        assert d["target"]["edge_type"] == "vonage"
        assert d["target"]["application_id"] == "app-123"
        assert d["sensitive_fields"] == ["private_key"]
