from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define

from ..models.create_provider_integration_request_provider import CreateProviderIntegrationRequestProvider
from ..models.create_provider_integration_request_webhook_auth_type_type_0 import (
    CreateProviderIntegrationRequestWebhookAuthTypeType0,
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
        provider (CreateProviderIntegrationRequestProvider):
        secrets (CreateProviderIntegrationRequestSecrets):
        project_id (None | Unset | UUID):
        webhook_auth_type (CreateProviderIntegrationRequestWebhookAuthTypeType0 | None | Unset): Defaults to the
            provider's auth type.
        metadata (CreateProviderIntegrationRequestMetadata | Unset):
    """

    provider: CreateProviderIntegrationRequestProvider
    secrets: CreateProviderIntegrationRequestSecrets
    project_id: None | Unset | UUID = UNSET
    webhook_auth_type: CreateProviderIntegrationRequestWebhookAuthTypeType0 | None | Unset = UNSET
    metadata: CreateProviderIntegrationRequestMetadata | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        provider = self.provider.value

        secrets = self.secrets.to_dict()

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        webhook_auth_type: None | str | Unset
        if isinstance(self.webhook_auth_type, Unset):
            webhook_auth_type = UNSET
        elif isinstance(self.webhook_auth_type, CreateProviderIntegrationRequestWebhookAuthTypeType0):
            webhook_auth_type = self.webhook_auth_type.value
        else:
            webhook_auth_type = self.webhook_auth_type

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "provider": provider,
                "secrets": secrets,
            }
        )
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if webhook_auth_type is not UNSET:
            field_dict["webhook_auth_type"] = webhook_auth_type
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_provider_integration_request_metadata import CreateProviderIntegrationRequestMetadata
        from ..models.create_provider_integration_request_secrets import CreateProviderIntegrationRequestSecrets

        d = dict(src_dict)
        provider = CreateProviderIntegrationRequestProvider(d.pop("provider"))

        secrets = CreateProviderIntegrationRequestSecrets.from_dict(d.pop("secrets"))

        def _parse_project_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_webhook_auth_type(
            data: object,
        ) -> CreateProviderIntegrationRequestWebhookAuthTypeType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                webhook_auth_type_type_0 = CreateProviderIntegrationRequestWebhookAuthTypeType0(data)

                return webhook_auth_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CreateProviderIntegrationRequestWebhookAuthTypeType0 | None | Unset, data)

        webhook_auth_type = _parse_webhook_auth_type(d.pop("webhook_auth_type", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: CreateProviderIntegrationRequestMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreateProviderIntegrationRequestMetadata.from_dict(_metadata)

        create_provider_integration_request = cls(
            provider=provider,
            secrets=secrets,
            project_id=project_id,
            webhook_auth_type=webhook_auth_type,
            metadata=metadata,
        )

        return create_provider_integration_request
