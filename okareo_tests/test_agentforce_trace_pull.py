"""Offline tests for Agentforce trace pull: TracePullConfig on CustomEndpointTarget,
and the generated voice-integration client models and routes."""

import json
import uuid
from typing import Any, Optional

import pytest
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo.model_under_test import (
    AuthConfig,
    CustomEndpointTarget,
    SessionConfig,
    Target,
    TracePullConfig,
    TurnConfig,
)
from okareo_api_client.api.default import (
    check_integration_connection_v0_voice_integration_integration_id_test_post,
    check_unsaved_integration_connection_v0_voice_integration_test_post,
    list_provider_integrations_v0_voice_integrations_get,
)
from okareo_api_client.client import Client
from okareo_api_client.models import (
    ConnectionCheck,
    ConnectionTestRequest,
    ConnectionTestRequestMetadata,
    ConnectionTestRequestProvider,
    ConnectionTestRequestSecrets,
    ConnectionTestResponse,
    CreateProviderIntegrationRequest,
    CreateProviderIntegrationRequestMetadata,
    CreateProviderIntegrationRequestProvider,
    CreateProviderIntegrationRequestSecrets,
    CreateProviderIntegrationRequestWebhookAuthTypeType0,
    ProviderIntegrationResponse,
    ProviderIntegrationResponseDelivery,
    ProviderIntegrationResponseProvider,
    ProviderIntegrationResponseWebhookAuthType,
    TargetModelResponse,
)
from okareo_api_client.types import UNSET, Unset

INTEGRATION_ID = "3f1c2b9e-8a4d-4c47-9d61-2a7e5b0c8f13"
PROJECT_ID = "9b0e4f6a-1c2d-4e3f-8a5b-6c7d8e9f0a1b"
BASE_URL = "http://mocked.com"


def _endpoint_target(**kwargs: Any) -> CustomEndpointTarget:
    return CustomEndpointTarget(
        start_session=SessionConfig(url="https://agent.example.com/start"),
        next_turn=TurnConfig(
            url="https://agent.example.com/turn",
            response_message_path="response.message",
        ),
        **kwargs,
    )


def _integration_json(provider: str, auth_type: str, delivery: Optional[str]) -> dict:
    """An integration as the server returns it. delivery=None is the shape servers
    before the Agentforce release send: no `delivery` key at all."""
    out = {
        "id": INTEGRATION_ID,
        "project_id": PROJECT_ID,
        "provider": provider,
        "public_id": "pi_abc123",
        "status": "active",
        "webhook_auth_type": auth_type,
        "metadata": {"my_domain": "https://acme.my.salesforce.com"},
        "last_validated_at": "2026-10-06T18:00:00Z",
        "last_used_at": None,
        "secret_summary": {
            "secret_names": ["client_id", "client_secret"],
            "statuses": {"client_id": "active", "client_secret": "active"},
        },
    }
    if delivery is not None:
        out["delivery"] = delivery
    return out


# --- TracePullConfig ------------------------------------------------------


class TestTracePullConfig:
    def test_integration_id_only_omits_timings(self) -> None:
        assert TracePullConfig(INTEGRATION_ID).to_dict() == {
            "integration_id": INTEGRATION_ID
        }

    def test_all_timings(self) -> None:
        cfg = TracePullConfig(
            integration_id=INTEGRATION_ID,
            initial_delay_s=90,
            poll_interval_s=15,
            timeout_s=600,
        )
        assert cfg.to_dict() == {
            "integration_id": INTEGRATION_ID,
            "initial_delay_s": 90,
            "poll_interval_s": 15,
            "timeout_s": 600,
        }

    def test_partial_timings_only_emit_what_was_set(self) -> None:
        cfg = TracePullConfig(INTEGRATION_ID, timeout_s=300)
        assert cfg.to_dict() == {"integration_id": INTEGRATION_ID, "timeout_s": 300}

    def test_never_emits_credentials_or_provider(self) -> None:
        d = TracePullConfig(INTEGRATION_ID, 1, 2, 3).to_dict()
        assert "auth" not in d
        assert "provider" not in d

    def test_accepts_uuid_object_and_serializes_str(self) -> None:
        cfg = TracePullConfig(uuid.UUID(INTEGRATION_ID))
        assert cfg.to_dict()["integration_id"] == INTEGRATION_ID
        assert isinstance(cfg.to_dict()["integration_id"], str)

    def test_uppercase_uuid_is_normalized(self) -> None:
        cfg = TracePullConfig(INTEGRATION_ID.upper())
        assert cfg.integration_id == INTEGRATION_ID

    @pytest.mark.parametrize("bad_id", ["", "not-a-uuid", "1234"])
    def test_rejects_non_uuid_integration_id(self, bad_id: str) -> None:
        with pytest.raises(ValueError, match="integration_id must be a UUID"):
            TracePullConfig(bad_id)

    @pytest.mark.parametrize(
        "field", ["initial_delay_s", "poll_interval_s", "timeout_s"]
    )
    @pytest.mark.parametrize("bad", [0, -1, 1.5, 60.0, "60", True, False])
    def test_rejects_non_positive_or_non_int_timings(
        self, field: str, bad: Any
    ) -> None:
        with pytest.raises(ValueError, match=f"{field} must be a positive integer"):
            TracePullConfig(INTEGRATION_ID, **{field: bad})


# --- CustomEndpointTarget ---------------------------------------------------


class TestCustomEndpointTargetTracePull:
    def test_without_trace_pull_payload_is_unchanged(self) -> None:
        params = _endpoint_target().params()
        assert "trace_params" not in params
        assert set(params) == {
            "type",
            "start_session_params",
            "next_message_params",
            "end_session_params",
            "max_parallel_requests",
        }

    def test_with_trace_pull_emits_trace_params(self) -> None:
        cfg = TracePullConfig(INTEGRATION_ID, initial_delay_s=120)
        params = _endpoint_target(trace_pull=cfg).params()
        assert params["type"] == "custom_endpoint"
        assert params["trace_params"] == {
            "integration_id": INTEGRATION_ID,
            "initial_delay_s": 120,
        }

    def test_trace_pull_alongside_auth(self) -> None:
        params = _endpoint_target(
            auth=AuthConfig(url="https://agent.example.com/token"),
            trace_pull=TracePullConfig(INTEGRATION_ID),
        ).params()
        assert params["auth_params"]["url"] == "https://agent.example.com/token"
        assert params["trace_params"] == {"integration_id": INTEGRATION_ID}
        assert "auth" not in params["trace_params"]

    def test_target_to_dict_carries_trace_params(self) -> None:
        target = Target(
            name="agentforce-text",
            target=_endpoint_target(trace_pull=TracePullConfig(INTEGRATION_ID)),
        )
        out = target.to_dict()
        assert out["target"]["trace_params"] == {"integration_id": INTEGRATION_ID}
        assert "sensitive_fields" not in out


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
        "name": "agentforce-text",
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


class TestTargetRoundTrip:
    def test_create_or_update_target_sends_and_returns_trace_params(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        endpoint = _endpoint_target(
            trace_pull=TracePullConfig(INTEGRATION_ID, timeout_s=900)
        )
        expected = {"integration_id": INTEGRATION_ID, "timeout_s": 900}
        httpx_mock.add_response(
            url=f"{BASE_URL}/v0/register_model",
            json=_mut_json({"custom_endpoint": endpoint.params()}),
            status_code=201,
        )

        okareo = Okareo("api-key", BASE_URL)
        saved = okareo.create_or_update_target(
            Target(name="agentforce-text", target=endpoint)
        )

        (body,) = _register_bodies(httpx_mock)
        assert body["models"]["custom_endpoint"]["trace_params"] == expected
        assert isinstance(saved.target, dict)
        assert saved.target["trace_params"] == expected

    def test_get_then_resave_keeps_trace_params(self, httpx_mock: HTTPXMock) -> None:
        stored = _endpoint_target(
            trace_pull=TracePullConfig(INTEGRATION_ID, poll_interval_s=45)
        ).params()
        _mock_projects(httpx_mock)
        httpx_mock.add_response(
            url=f"{BASE_URL}/v0/target/agentforce-text",
            json={
                "id": str(uuid.uuid4()),
                "name": "agentforce-text",
                "target": stored,
            },
        )
        httpx_mock.add_response(
            url=f"{BASE_URL}/v0/register_model",
            json=_mut_json({"custom_endpoint": stored}),
            status_code=201,
        )

        okareo = Okareo("api-key", BASE_URL)
        loaded = okareo.get_target_by_name("agentforce-text")
        assert isinstance(loaded.target, dict)
        assert loaded.target["trace_params"] == stored["trace_params"]

        okareo.create_or_update_target(loaded)
        (body,) = _register_bodies(httpx_mock)
        assert body["models"]["custom_endpoint"]["trace_params"] == {
            "integration_id": INTEGRATION_ID,
            "poll_interval_s": 45,
        }

    def test_target_from_response_keeps_trace_params(self) -> None:
        stored = _endpoint_target(trace_pull=TracePullConfig(INTEGRATION_ID)).params()
        response = TargetModelResponse.from_dict(
            {"id": str(uuid.uuid4()), "name": "agentforce-text", "target": stored}
        )
        target = Target.from_response(response)
        assert target.to_dict()["target"]["trace_params"] == {
            "integration_id": INTEGRATION_ID
        }


# --- Generated client: provider integrations ------------------------------


class TestProviderIntegrationModels:
    def test_parses_agentforce_pull_integration(self) -> None:
        parsed = ProviderIntegrationResponse.from_dict(
            _integration_json("agentforce", "oauth_client_credentials", "pull")
        )
        assert parsed.provider is ProviderIntegrationResponseProvider.AGENTFORCE
        assert (
            parsed.webhook_auth_type
            is ProviderIntegrationResponseWebhookAuthType.OAUTH_CLIENT_CREDENTIALS
        )
        assert parsed.delivery is ProviderIntegrationResponseDelivery.PULL
        assert parsed.metadata["my_domain"] == "https://acme.my.salesforce.com"
        assert parsed.secret_summary.secret_names == ["client_id", "client_secret"]
        assert parsed.to_dict()["delivery"] == "pull"

    @pytest.mark.parametrize(
        "provider,auth_type",
        [
            ("livekit", "livekit_jwt"),
            ("twilio", "twilio_signature"),
            ("retell", "retell_signature"),
        ],
    )
    def test_parses_webhook_integrations(self, provider: str, auth_type: str) -> None:
        parsed = ProviderIntegrationResponse.from_dict(
            _integration_json(provider, auth_type, "webhook")
        )
        assert parsed.provider.value == provider
        assert parsed.delivery is ProviderIntegrationResponseDelivery.WEBHOOK

    @pytest.mark.parametrize(
        "provider,auth_type",
        [("twilio", "twilio_signature"), ("retell", "retell_signature")],
    )
    def test_parses_integration_without_delivery(
        self, provider: str, auth_type: str
    ) -> None:
        """Servers before the Agentforce release send no `delivery`."""
        raw = _integration_json(provider, auth_type, None)
        assert "delivery" not in raw
        parsed = ProviderIntegrationResponse.from_dict(raw)
        assert parsed.provider.value == provider
        assert parsed.delivery is UNSET
        assert isinstance(parsed.delivery, Unset)
        assert "delivery" not in parsed.to_dict()

    def test_list_route_parses_response_without_delivery(
        self, httpx_mock: HTTPXMock
    ) -> None:
        httpx_mock.add_response(
            json=[
                _integration_json("twilio", "twilio_signature", None),
                _integration_json("retell", "retell_signature", None),
            ]
        )
        result = list_provider_integrations_v0_voice_integrations_get.sync(
            client=Client(base_url=BASE_URL), api_key="api-key"
        )
        assert isinstance(result, list)
        assert [r.provider.value for r in result] == ["twilio", "retell"]
        assert all(r.delivery is UNSET for r in result)

    def test_list_route_parses_mixed_providers(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            json=[
                _integration_json("agentforce", "oauth_client_credentials", "pull"),
                _integration_json("livekit", "livekit_jwt", "webhook"),
                _integration_json("twilio", "twilio_signature", "webhook"),
            ]
        )
        result = list_provider_integrations_v0_voice_integrations_get.sync(
            client=Client(base_url=BASE_URL), api_key="api-key"
        )
        assert isinstance(result, list)
        assert [r.provider.value for r in result] == ["agentforce", "livekit", "twilio"]
        assert [r.delivery for r in result] == [
            ProviderIntegrationResponseDelivery.PULL,
            ProviderIntegrationResponseDelivery.WEBHOOK,
            ProviderIntegrationResponseDelivery.WEBHOOK,
        ]

    def test_create_agentforce_request_omits_unset_auth_type_and_project(
        self,
    ) -> None:
        body = CreateProviderIntegrationRequest(
            provider=CreateProviderIntegrationRequestProvider.AGENTFORCE,
            secrets=CreateProviderIntegrationRequestSecrets.from_dict(
                {"client_id": "cid", "client_secret": "csecret"}
            ),
            metadata=CreateProviderIntegrationRequestMetadata.from_dict(
                {"my_domain": "acme.my.salesforce.com"}
            ),
        ).to_dict()
        assert body == {
            "provider": "agentforce",
            "secrets": {"client_id": "cid", "client_secret": "csecret"},
            "metadata": {"my_domain": "acme.my.salesforce.com"},
        }

    def test_create_request_with_explicit_auth_type_and_project(self) -> None:
        body = CreateProviderIntegrationRequest(
            provider=CreateProviderIntegrationRequestProvider.AGENTFORCE,
            secrets=CreateProviderIntegrationRequestSecrets.from_dict({}),
            project_id=uuid.UUID(PROJECT_ID),
            webhook_auth_type=(
                CreateProviderIntegrationRequestWebhookAuthTypeType0.OAUTH_CLIENT_CREDENTIALS
            ),
        ).to_dict()
        assert body["project_id"] == PROJECT_ID
        assert body["webhook_auth_type"] == "oauth_client_credentials"


# --- Generated client: connection test ------------------------------------

CONNECTION_TEST_JSON = {
    "ok": False,
    "checks": [
        {"name": "settings", "ok": True, "detail": "https://acme.my.salesforce.com"},
        {
            "name": "token",
            "ok": False,
            "detail": "Salesforce refused the credentials (invalid_client).",
        },
    ],
}


class TestConnectionTest:
    def test_response_model_parses(self) -> None:
        parsed = ConnectionTestResponse.from_dict(CONNECTION_TEST_JSON)
        assert parsed.ok is False
        assert all(isinstance(c, ConnectionCheck) for c in parsed.checks)
        assert [(c.name, c.ok) for c in parsed.checks] == [
            ("settings", True),
            ("token", False),
        ]
        assert parsed.to_dict() == CONNECTION_TEST_JSON

    def test_saved_integration_route(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="POST",
            url=(
                f"{BASE_URL}/v0/voice/integration/{INTEGRATION_ID}/test"
                f"?project_id={PROJECT_ID}"
            ),
            json=CONNECTION_TEST_JSON,
        )
        result = check_integration_connection_v0_voice_integration_integration_id_test_post.sync(
            uuid.UUID(INTEGRATION_ID),
            client=Client(base_url=BASE_URL),
            project_id=uuid.UUID(PROJECT_ID),
            api_key="api-key",
        )
        assert isinstance(result, ConnectionTestResponse)
        assert result.ok is False
        assert httpx_mock.get_requests()[0].headers["api-key"] == "api-key"

    def test_unsaved_settings_route_sends_body(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="POST",
            url=f"{BASE_URL}/v0/voice/integration/test",
            json={
                "ok": True,
                "checks": [{"name": "token", "ok": True, "detail": "ok"}],
            },
        )
        request = ConnectionTestRequest(
            provider=ConnectionTestRequestProvider.AGENTFORCE,
            secrets=ConnectionTestRequestSecrets.from_dict(
                {"client_id": "cid", "client_secret": "csecret"}
            ),
            metadata=ConnectionTestRequestMetadata.from_dict(
                {"my_domain": "acme.my.salesforce.com"}
            ),
        )
        result = (
            check_unsaved_integration_connection_v0_voice_integration_test_post.sync(
                client=Client(base_url=BASE_URL), body=request, api_key="api-key"
            )
        )
        assert isinstance(result, ConnectionTestResponse) and result.ok is True
        sent = json.loads(httpx_mock.get_requests()[0].content)
        assert sent == {
            "provider": "agentforce",
            "secrets": {"client_id": "cid", "client_secret": "csecret"},
            "metadata": {"my_domain": "acme.my.salesforce.com"},
        }
