from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.update_provider_integration_request_metadata import UpdateProviderIntegrationRequestMetadata


T = TypeVar("T", bound="UpdateProviderIntegrationRequest")


@_attrs_define
class UpdateProviderIntegrationRequest:
    """
    Attributes:
        metadata (UpdateProviderIntegrationRequestMetadata):
    """

    metadata: UpdateProviderIntegrationRequestMetadata

    def to_dict(self) -> dict[str, Any]:
        metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_provider_integration_request_metadata import UpdateProviderIntegrationRequestMetadata

        d = dict(src_dict)
        metadata = UpdateProviderIntegrationRequestMetadata.from_dict(d.pop("metadata"))

        update_provider_integration_request = cls(
            metadata=metadata,
        )

        return update_provider_integration_request
