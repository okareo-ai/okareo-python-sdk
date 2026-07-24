"""SDK unit tests for WebRTCVoiceTarget (native WebRTC voice edge)."""

import pytest

from okareo.model_under_test import Target, WebRTCVoiceTarget


def test_retell_params_shape() -> None:
    """Retell target serializes as edge_type=webrtc, platform=retell."""
    t = WebRTCVoiceTarget(platform="retell", agent_id="agent_x")
    params = t.params()
    assert params["type"] == "voice"
    assert params["edge_type"] == "webrtc"
    assert params["platform"] == "retell"
    assert params["agent_id"] == "agent_x"
    # No SIP/PSTN cruft.
    assert "sip_uri" not in params
    assert "to_phone_number" not in params


def test_livekit_direct_params_shape() -> None:
    t = WebRTCVoiceTarget(
        platform="livekit",
        livekit_url="wss://x.livekit.cloud",
        livekit_api_key="key",
        livekit_api_secret="secret",
        room_name="room-1",
    )
    params = t.params()
    assert params["platform"] == "livekit"
    assert params["livekit_url"] == "wss://x.livekit.cloud"
    assert params["room_name"] == "room-1"


def test_livekit_secrets_are_sensitive() -> None:
    """LiveKit creds live on the target and must be redacted; Retell rides api_keys."""
    lk = WebRTCVoiceTarget(
        platform="livekit",
        livekit_url="wss://x",
        livekit_api_key="key",
        livekit_api_secret="secret",
        room_name="r",
    )
    assert "livekit_api_secret" in lk.get_sensitive_fields()
    assert "livekit_api_key" in lk.get_sensitive_fields()
    assert (
        WebRTCVoiceTarget(platform="retell", agent_id="a").get_sensitive_fields() == []
    )


def test_target_union_accepts_webrtc_and_promotes_sensitive() -> None:
    t = WebRTCVoiceTarget(
        platform="livekit",
        livekit_url="wss://x",
        livekit_api_key="key",
        livekit_api_secret="secret",
        room_name="r",
    )
    out = Target(name="My LiveKit agent", target=t).to_dict()
    assert out["name"] == "My LiveKit agent"
    assert out["target"]["edge_type"] == "webrtc"
    assert "livekit_api_secret" in out["sensitive_fields"]


# --- fail-fast validation (the point of promoting past a raw dict) -----------


def test_unknown_platform_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown platform"):
        WebRTCVoiceTarget(platform="not-a-platform")


def test_unsupported_platform_rejected_with_fallback_hint() -> None:
    """daily/vapi/pipecat are known but not wired end-to-end yet."""
    for platform in ("daily", "vapi", "pipecat"):
        with pytest.raises(ValueError, match="not yet supported"):
            WebRTCVoiceTarget(platform=platform)


def test_missing_retell_agent_id_rejected() -> None:
    with pytest.raises(ValueError, match="agent_id"):
        WebRTCVoiceTarget(platform="retell")


def test_missing_livekit_credentials_rejected() -> None:
    with pytest.raises(ValueError, match="livekit_api_secret"):
        WebRTCVoiceTarget(platform="livekit", livekit_url="wss://x", room_name="r")


def test_valid_targets_do_not_raise() -> None:
    WebRTCVoiceTarget(platform="retell", agent_id="a")
    WebRTCVoiceTarget(
        platform="livekit",
        livekit_url="wss://x",
        livekit_api_key="k",
        livekit_api_secret="s",
        room_name="r",
    )
