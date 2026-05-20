from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define

from ..models.provider_integration_status_response_status import ProviderIntegrationStatusResponseStatus

T = TypeVar("T", bound="ProviderIntegrationStatusResponse")


@_attrs_define
class ProviderIntegrationStatusResponse:
    """
    Attributes:
        id (UUID):
        status (ProviderIntegrationStatusResponseStatus):
    """

    id: UUID
    status: ProviderIntegrationStatusResponseStatus

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        status = self.status.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        status = ProviderIntegrationStatusResponseStatus(d.pop("status"))

        provider_integration_status_response = cls(
            id=id,
            status=status,
        )

        return provider_integration_status_response
