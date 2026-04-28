from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.update_provider_integration_status_request_status import UpdateProviderIntegrationStatusRequestStatus

T = TypeVar("T", bound="UpdateProviderIntegrationStatusRequest")


@_attrs_define
class UpdateProviderIntegrationStatusRequest:
    """
    Attributes:
        status (UpdateProviderIntegrationStatusRequestStatus):
    """

    status: UpdateProviderIntegrationStatusRequestStatus

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = UpdateProviderIntegrationStatusRequestStatus(d.pop("status"))

        update_provider_integration_status_request = cls(
            status=status,
        )

        return update_provider_integration_status_request
