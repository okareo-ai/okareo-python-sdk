"""Offline tests for LiveKitSessionVoiceTarget and JoinCallConfig: the "LiveKit
Session" voice Target, where the agent's own API sets up a LiveKit room per
conversation (e.g. Agentforce voice)."""

import json
import uuid
from typing import Any

import pytest
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo.model_under_test import (
    AuthConfig,
    CustomEndpointTarget,
    EndSessionConfig,
    JoinCallConfig,
    LiveKitSessionVoiceTarget,
    SessionConfig,
    Target,
    TracePullConfig,
    TurnConfig,
)
from okareo_api_client.models import TargetModelResponse

INTEGRATION_ID = "3f1c2b9e-8a4d-4c47-9d61-2a7e5b0c8f13"
PROJECT_ID = "9b0e4f6a-1c2d-4e3f-8a5b-6c7d8e9f0a1b"
BASE_URL = "http://mocked.com"

TOKEN_URL = "https://login.example.com/services/oauth2/token"
AGENT_API = "https://api.example.com/agent"
START_URL = AGENT_API + "/v1/agents/agent-123/sessions"
JOIN_URL = AGENT_API + "/v1.1/realtime/sessions/{session_id}/join"
END_URL = AGENT_API + "/v1/sessions/{session_id}"
FORM_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}
JSON_HEADERS = {
    "Authorization": "Bearer {access_token}",
    "Content-Type": "application/json",
}
END_HEADERS = {
    "Authorization": "Bearer {access_token}",
    "x-session-end-reason": "UserRequest",
}
AUTH_BODY = {
    "grant_type": "client_credentials",
    "client_id": "client-id-placeholder",
    "client_secret": "client-secret-placeholder",
}
START_BODY = {
    "externalSessionKey": "{scenario_row_run_guid}",
    "bypassUser": True,
}
SECRET_PATH = "auth_params.body.client_secret"


def _auth(body: Any = None) -> AuthConfig:
    return AuthConfig(
        url=TOKEN_URL,
        headers=FORM_HEADERS,
        body=AUTH_BODY if body is None else body,
        response_access_token_path="response.access_token",
    )


def _start() -> SessionConfig:
    return SessionConfig(
        url=START_URL,
        headers=JSON_HEADERS,
        body=START_BODY,
        response_session_id_path="response.sessionId",
    )


def _join(**kwargs: Any) -> JoinCallConfig:
    args: dict = {
        "url": JOIN_URL,
        "headers": JSON_HEADERS,
        "body": {"greeted": False},
        "response_livekit_url_path": "response.room.endpoint",
        "response_room_token_path": "response.room.token",
        "response_room_name_path": "response.room.name",
    }
    args.update(kwargs)
    return JoinCallConfig(**args)


def _end() -> EndSessionConfig:
    return EndSessionConfig(url=END_URL, method="DELETE", headers=END_HEADERS)


def _full_target(**kwargs: Any) -> LiveKitSessionVoiceTarget:
    args: dict = {
        "auth": _auth(),
        "start_session": _start(),
        "join_call": _join(),
        "end_session": _end(),
        "max_parallel_requests": 4,
    }
    args.update(kwargs)
    return LiveKitSessionVoiceTarget(**args)


# The payload the server reads (webrtc edge, platform=livekit, broker mode) and
# the Okareo app saves for a "LiveKit Session" Target.
EXPECTED_FULL = {
    "type": "voice",
    "edge_type": "webrtc",
    "platform": "livekit",
    "auth_params": {
        "url": TOKEN_URL,
        "method": "POST",
        "headers": FORM_HEADERS,
        "body": AUTH_BODY,
        "status_code": None,
        "response_access_token_path": "response.access_token",
    },
    "start_session_params": {
        "url": START_URL,
        "method": "POST",
        "headers": JSON_HEADERS,
        "body": START_BODY,
        "status_code": None,
        "response_session_id_path": "response.sessionId",
        "response_message_path": "",
    },
    "join_call_params": {
        "url": JOIN_URL,
        "method": "POST",
        "headers": JSON_HEADERS,
        "body": {"greeted": False},
        "status_code": None,
        "response_room_token_path": "response.room.token",
        "response_livekit_url_path": "response.room.endpoint",
        "response_room_name_path": "response.room.name",
    },
    "end_session_params": {
        "url": END_URL,
        "method": "DELETE",
        "headers": END_HEADERS,
        "body": "{}",
        "status_code": None,
    },
    "max_parallel_requests": 4,
}


# --- JoinCallConfig ---------------------------------------------------------


class TestJoinCallConfig:
    def test_defaults_and_required_path_only(self) -> None:
        cfg = JoinCallConfig(
            url=JOIN_URL, response_room_token_path="response.room.token"
        )
        assert cfg.to_dict() == {
            "url": JOIN_URL,
            "method": "POST",
            "headers": "{}",
            "body": "{}",
            "status_code": None,
            "response_room_token_path": "response.room.token",
        }

    def test_all_fields(self) -> None:
        cfg = _join(
            method="PUT",
            status_code=201,
            response_session_id_path="response.session.id",
        )
        assert cfg.to_dict() == {
            "url": JOIN_URL,
            "method": "PUT",
            "headers": JSON_HEADERS,
            "body": {"greeted": False},
            "status_code": 201,
            "response_room_token_path": "response.room.token",
            "response_livekit_url_path": "response.room.endpoint",
            "response_room_name_path": "response.room.name",
            "response_session_id_path": "response.session.id",
        }

    def test_requires_url(self) -> None:
        with pytest.raises(ValueError, match="requires url"):
            JoinCallConfig(url="", response_room_token_path="response.room.token")

    def test_requires_room_token_path(self) -> None:
        with pytest.raises(ValueError, match="requires response_room_token_path"):
            JoinCallConfig(url=JOIN_URL)


# --- LiveKitSessionVoiceTarget payload -------------------------------------


class TestLiveKitSessionVoiceTargetParams:
    def test_full_target_payload(self) -> None:
        assert _full_target().params() == EXPECTED_FULL

    def test_full_target_with_trace_pull(self) -> None:
        target = _full_target(
            trace_pull=TracePullConfig(
                INTEGRATION_ID, initial_delay_s=45, poll_interval_s=20, timeout_s=900
            )
        )
        assert target.params() == {
            **EXPECTED_FULL,
            "trace_params": {
                "integration_id": INTEGRATION_ID,
                "initial_delay_s": 45,
                "poll_interval_s": 20,
                "timeout_s": 900,
            },
        }

    def test_trace_pull_carries_no_credentials(self) -> None:
        tp = _full_target(trace_pull=TracePullConfig(INTEGRATION_ID)).params()[
            "trace_params"
        ]
        assert tp == {"integration_id": INTEGRATION_ID}

    def test_only_join_call(self) -> None:
        target = LiveKitSessionVoiceTarget(start_session=None, join_call=_join())
        assert target.params() == {
            "type": "voice",
            "edge_type": "webrtc",
            "platform": "livekit",
            "join_call_params": EXPECTED_FULL["join_call_params"],
            "max_parallel_requests": None,
        }

    def test_never_emits_direct_livekit_credentials(self) -> None:
        params = _full_target().params()
        for key in ("livekit_api_key", "livekit_api_secret", "room_name"):
            assert key not in params

    def test_livekit_url_fallback_is_sent_when_set(self) -> None:
        target = LiveKitSessionVoiceTarget(
            start_session=_start(),
            join_call=_join(response_livekit_url_path=""),
            livekit_url="wss://agent.livekit.example.com",
        )
        params = target.params()
        assert params["livekit_url"] == "wss://agent.livekit.example.com"
        assert "response_livekit_url_path" not in params["join_call_params"]

    def test_templated_values_are_sent_verbatim(self) -> None:
        params = _full_target().params()
        assert params["join_call_params"]["url"] == JOIN_URL
        assert "{session_id}" in params["join_call_params"]["url"]
        assert params["end_session_params"]["url"] == END_URL
        assert (
            params["join_call_params"]["headers"]["Authorization"]
            == "Bearer {access_token}"
        )
        assert (
            params["start_session_params"]["body"]["externalSessionKey"]
            == "{scenario_row_run_guid}"
        )

    def test_blocks_match_custom_endpoint_target(self) -> None:
        """auth/start/end serialize exactly as they do on a text CustomEndpointTarget."""
        text = CustomEndpointTarget(
            start_session=_start(),
            next_turn=TurnConfig(url=AGENT_API + "/messages"),
            end_session=_end(),
            auth=_auth(),
        ).params()
        voice = _full_target().params()
        for key in ("auth_params", "start_session_params", "end_session_params"):
            assert voice[key] == text[key]

    def test_params_keep_the_secret_for_the_server(self) -> None:
        """The SDK sends the real value; the server masks it on read."""
        body = _full_target().params()["auth_params"]["body"]
        assert body["client_secret"] == "client-secret-placeholder"


# --- Validation -------------------------------------------------------------


class TestLiveKitSessionVoiceTargetValidation:
    def test_requires_join_call(self) -> None:
        with pytest.raises(ValueError, match="requires join_call"):
            LiveKitSessionVoiceTarget(start_session=_start(), join_call=None)  # type: ignore[arg-type]

    def test_requires_a_livekit_server_url_source(self) -> None:
        with pytest.raises(ValueError, match="needs the LiveKit server URL"):
            LiveKitSessionVoiceTarget(
                start_session=_start(),
                join_call=_join(response_livekit_url_path=""),
            )

    def test_rejects_a_turn_config_as_join_call(self) -> None:
        with pytest.raises(TypeError, match="join_call must be a JoinCallConfig"):
            LiveKitSessionVoiceTarget(
                start_session=_start(),
                join_call=TurnConfig(url=JOIN_URL),  # type: ignore[arg-type]
            )

    @pytest.mark.parametrize(
        "field,value,expected",
        [
            ("auth", {"url": TOKEN_URL}, "AuthConfig"),
            ("start_session", {"url": START_URL}, "SessionConfig"),
            ("end_session", {"url": END_URL}, "EndSessionConfig"),
            ("trace_pull", {"integration_id": INTEGRATION_ID}, "TracePullConfig"),
        ],
    )
    def test_rejects_raw_dicts_for_config_blocks(
        self, field: str, value: dict, expected: str
    ) -> None:
        kwargs: dict = {"start_session": _start(), "join_call": _join(), field: value}
        with pytest.raises(TypeError, match=f"{field} must be a {expected}"):
            LiveKitSessionVoiceTarget(**kwargs)


# --- Sensitive fields -------------------------------------------------------


class TestLiveKitSessionSensitiveFields:
    def test_client_secret_in_auth_body(self) -> None:
        assert _full_target().get_sensitive_fields() == [SECRET_PATH]

    def test_client_secret_in_json_string_body(self) -> None:
        target = _full_target(auth=_auth(body=json.dumps(AUTH_BODY)))
        assert target.get_sensitive_fields() == [SECRET_PATH]

    @pytest.mark.parametrize(
        "body", [{"grant_type": "client_credentials"}, "{}", "not json", "[]"]
    )
    def test_no_client_secret_in_auth_body(self, body: Any) -> None:
        assert _full_target(auth=_auth(body=body)).get_sensitive_fields() == []

    def test_without_auth(self) -> None:
        assert _full_target(auth=None).get_sensitive_fields() == []

    def test_target_to_dict_promotes_sensitive_fields(self) -> None:
        out = Target(name="agentforce-voice", target=_full_target()).to_dict()
        assert out["sensitive_fields"] == [SECRET_PATH]
        assert out["target"] == EXPECTED_FULL


# --- Round trip through the Okareo client ---------------------------------


def _mock_projects(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        json=[
            {
                "id": PROJECT_ID,
                "name": "Global",
                "onboarding_status": "onboarding_status",
                "tags": [],
            }
        ],
        status_code=201,
    )


def _mut_json(models: dict) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "project_id": PROJECT_ID,
        "name": "agentforce-voice",
        "tags": [],
        "time_created": "2026-10-06T18:00:00",
        "version": 1,
        "models": models,
    }


def _register_bodies(httpx_mock: HTTPXMock) -> list:
    return [
        json.loads(r.content)
        for r in httpx_mock.get_requests()
        if r.url.path == "/v0/register_model"
    ]


class TestLiveKitSessionTargetRoundTrip:
    def test_create_or_update_target_sends_broker_payload_with_trace_params(
        self, httpx_mock: HTTPXMock
    ) -> None:
        voice = _full_target(trace_pull=TracePullConfig(INTEGRATION_ID, timeout_s=900))
        expected_trace = {"integration_id": INTEGRATION_ID, "timeout_s": 900}
        _mock_projects(httpx_mock)
        httpx_mock.add_response(
            url=f"{BASE_URL}/v0/register_model",
            json=_mut_json({"voice": voice.params()}),
            status_code=201,
        )

        okareo = Okareo("api-key", BASE_URL)
        saved = okareo.create_or_update_target(
            Target(name="agentforce-voice", target=voice),
            sensitive_fields=voice.get_sensitive_fields(),
        )

        (body,) = _register_bodies(httpx_mock)
        assert body["name"] == "agentforce-voice"
        assert body["models"] == {
            "voice": {**EXPECTED_FULL, "trace_params": expected_trace}
        }
        assert body["sensitive_fields"] == [SECRET_PATH]
        assert isinstance(saved.target, dict)
        assert saved.target["trace_params"] == expected_trace
        assert saved.target["join_call_params"] == EXPECTED_FULL["join_call_params"]

    def test_sensitive_fields_are_sent_only_when_passed(
        self, httpx_mock: HTTPXMock
    ) -> None:
        """Like CustomEndpointTarget: the caller passes sensitive_fields; the SDK
        does not add the Target's own get_sensitive_fields() to the request."""
        voice = _full_target()
        _mock_projects(httpx_mock)
        httpx_mock.add_response(
            url=f"{BASE_URL}/v0/register_model",
            json=_mut_json({"voice": voice.params()}),
            status_code=201,
        )

        okareo = Okareo("api-key", BASE_URL)
        okareo.create_or_update_target(Target(name="agentforce-voice", target=voice))

        (body,) = _register_bodies(httpx_mock)
        assert body.get("sensitive_fields") is None

    def test_target_from_response_keeps_the_broker_blocks(self) -> None:
        stored = _full_target(trace_pull=TracePullConfig(INTEGRATION_ID)).params()
        response = TargetModelResponse.from_dict(
            {"id": str(uuid.uuid4()), "name": "agentforce-voice", "target": stored}
        )
        target = Target.from_response(response)
        assert target.to_dict()["target"] == stored
