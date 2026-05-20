from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define

from ..models.create_provider_integration_request_provider import CreateProviderIntegrationRequestProvider
from ..models.create_provider_integration_request_webhook_auth_type import (
    CreateProviderIntegrationRequestWebhookAuthType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_provider_integration_request_metadata import CreateProviderIntegrationRequestMetadata
    from ..models.create_provider_integration_request_secrets import CreateProviderIntegrationRequestSecrets


T = TypeVar("T", bound="CreateProviderIntegrationRequest")


@_attrs_define
class CreateProviderIntegrationRequest:
    """
    Attributes:
        project_id (UUID):
        provider (CreateProviderIntegrationRequestProvider):
        webhook_auth_type (CreateProviderIntegrationRequestWebhookAuthType):
        secrets (CreateProviderIntegrationRequestSecrets):
        metadata (CreateProviderIntegrationRequestMetadata | Unset):
    """

    project_id: UUID
    provider: CreateProviderIntegrationRequestProvider
    webhook_auth_type: CreateProviderIntegrationRequestWebhookAuthType
    secrets: CreateProviderIntegrationRequestSecrets
    metadata: CreateProviderIntegrationRequestMetadata | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        provider = self.provider.value

        webhook_auth_type = self.webhook_auth_type.value

        secrets = self.secrets.to_dict()

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "project_id": project_id,
                "provider": provider,
                "webhook_auth_type": webhook_auth_type,
                "secrets": secrets,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_provider_integration_request_metadata import CreateProviderIntegrationRequestMetadata
        from ..models.create_provider_integration_request_secrets import CreateProviderIntegrationRequestSecrets

        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))

        provider = CreateProviderIntegrationRequestProvider(d.pop("provider"))

        webhook_auth_type = CreateProviderIntegrationRequestWebhookAuthType(d.pop("webhook_auth_type"))

        secrets = CreateProviderIntegrationRequestSecrets.from_dict(d.pop("secrets"))

        _metadata = d.pop("metadata", UNSET)
        metadata: CreateProviderIntegrationRequestMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreateProviderIntegrationRequestMetadata.from_dict(_metadata)

        create_provider_integration_request = cls(
            project_id=project_id,
            provider=provider,
            webhook_auth_type=webhook_auth_type,
            secrets=secrets,
            metadata=metadata,
        )

        return create_provider_integration_request
