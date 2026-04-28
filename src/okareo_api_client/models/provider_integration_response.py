from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.provider_integration_response_provider import ProviderIntegrationResponseProvider
from ..models.provider_integration_response_webhook_auth_type import ProviderIntegrationResponseWebhookAuthType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.provider_integration_response_metadata import ProviderIntegrationResponseMetadata
    from ..models.secret_summary_response import SecretSummaryResponse


T = TypeVar("T", bound="ProviderIntegrationResponse")


@_attrs_define
class ProviderIntegrationResponse:
    """
    Attributes:
        id (UUID):
        project_id (UUID):
        provider (ProviderIntegrationResponseProvider):
        public_id (str):
        status (str):
        webhook_auth_type (ProviderIntegrationResponseWebhookAuthType):
        metadata (ProviderIntegrationResponseMetadata):
        secret_summary (SecretSummaryResponse):
        last_validated_at (datetime.datetime | None | Unset):
        last_used_at (datetime.datetime | None | Unset):
    """

    id: UUID
    project_id: UUID
    provider: ProviderIntegrationResponseProvider
    public_id: str
    status: str
    webhook_auth_type: ProviderIntegrationResponseWebhookAuthType
    metadata: ProviderIntegrationResponseMetadata
    secret_summary: SecretSummaryResponse
    last_validated_at: datetime.datetime | None | Unset = UNSET
    last_used_at: datetime.datetime | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        provider = self.provider.value

        public_id = self.public_id

        status = self.status

        webhook_auth_type = self.webhook_auth_type.value

        metadata = self.metadata.to_dict()

        secret_summary = self.secret_summary.to_dict()

        last_validated_at: None | str | Unset
        if isinstance(self.last_validated_at, Unset):
            last_validated_at = UNSET
        elif isinstance(self.last_validated_at, datetime.datetime):
            last_validated_at = self.last_validated_at.isoformat()
        else:
            last_validated_at = self.last_validated_at

        last_used_at: None | str | Unset
        if isinstance(self.last_used_at, Unset):
            last_used_at = UNSET
        elif isinstance(self.last_used_at, datetime.datetime):
            last_used_at = self.last_used_at.isoformat()
        else:
            last_used_at = self.last_used_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "provider": provider,
                "public_id": public_id,
                "status": status,
                "webhook_auth_type": webhook_auth_type,
                "metadata": metadata,
                "secret_summary": secret_summary,
            }
        )
        if last_validated_at is not UNSET:
            field_dict["last_validated_at"] = last_validated_at
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provider_integration_response_metadata import ProviderIntegrationResponseMetadata
        from ..models.secret_summary_response import SecretSummaryResponse

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        project_id = UUID(d.pop("project_id"))

        provider = ProviderIntegrationResponseProvider(d.pop("provider"))

        public_id = d.pop("public_id")

        status = d.pop("status")

        webhook_auth_type = ProviderIntegrationResponseWebhookAuthType(d.pop("webhook_auth_type"))

        metadata = ProviderIntegrationResponseMetadata.from_dict(d.pop("metadata"))

        secret_summary = SecretSummaryResponse.from_dict(d.pop("secret_summary"))

        def _parse_last_validated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_validated_at_type_0 = isoparse(data)

                return last_validated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_validated_at = _parse_last_validated_at(d.pop("last_validated_at", UNSET))

        def _parse_last_used_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_used_at_type_0 = isoparse(data)

                return last_used_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_used_at = _parse_last_used_at(d.pop("last_used_at", UNSET))

        provider_integration_response = cls(
            id=id,
            project_id=project_id,
            provider=provider,
            public_id=public_id,
            status=status,
            webhook_auth_type=webhook_auth_type,
            metadata=metadata,
            secret_summary=secret_summary,
            last_validated_at=last_validated_at,
            last_used_at=last_used_at,
        )

        return provider_integration_response
