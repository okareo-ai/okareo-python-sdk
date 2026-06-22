"""SDK unit tests for SipTarget. Authored TDD — failing before implementation."""
import pytest


def test_a1_sip_target_params_shape():
    """A1: SipTarget(sip_uri=...) round-trips with edge_type=twilio + sip_uri exposed."""
    from okareo.model_under_test import SipTarget

    t = SipTarget(sip_uri="sip:agent@room.sip.daily.co")
    params = t.params()
    assert params["type"] == "voice"
    assert params["edge_type"] == "twilio"  # MVP rides Twilio egress
    assert params["sip_uri"] == "sip:agent@room.sip.daily.co"
    # SIP URI surfaced via the existing dial slot so the Twilio edge picks it up
    assert params["to_phone_number"] == "sip:agent@room.sip.daily.co"
    assert params["sip_username"] is None
    assert params["sip_password"] is None


def test_a2_sip_target_credentials_in_params():
    """A2: optional SIP digest creds appear in params verbatim."""
    from okareo.model_under_test import SipTarget

    t = SipTarget(
        sip_uri="trunk.sip.twilio.com",
        sip_username="okareo",
        sip_password="secret",
    )
    params = t.params()
    assert params["sip_username"] == "okareo"
    assert params["sip_password"] == "secret"


def test_a3_sip_password_is_sensitive():
    """A3: sip_password is reported as sensitive when set, not when absent."""
    from okareo.model_under_test import SipTarget

    with_pw = SipTarget(sip_uri="trunk.sip.twilio.com", sip_password="secret")
    no_pw = SipTarget(sip_uri="sip:agent@host")
    assert with_pw.get_sensitive_fields() == ["sip_password"]
    assert no_pw.get_sensitive_fields() == []


def test_a4_target_union_accepts_sip_and_promotes_sensitive():
    """A4: Target(name, target=SipTarget) renders correctly and lifts sensitive fields."""
    from okareo.model_under_test import SipTarget, Target

    t = SipTarget(sip_uri="trunk.sip.twilio.com", sip_password="secret")
    target = Target(name="Pipecat (Twilio SIP)", target=t)
    out = target.to_dict()
    assert out["name"] == "Pipecat (Twilio SIP)"
    assert out["target"]["sip_uri"] == "trunk.sip.twilio.com"
    assert out["sensitive_fields"] == ["sip_password"]
