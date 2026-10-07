from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define

from ..models.connection_test_request_provider import ConnectionTestRequestProvider
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.connection_test_request_metadata import ConnectionTestRequestMetadata
    from ..models.connection_test_request_secrets import ConnectionTestRequestSecrets


T = TypeVar("T", bound="ConnectionTestRequest")


@_attrs_define
class ConnectionTestRequest:
    """Unsaved settings to check before creating an integration. Nothing is stored.

    Attributes:
        provider (ConnectionTestRequestProvider):
        secrets (ConnectionTestRequestSecrets):
        project_id (None | Unset | UUID):
        metadata (ConnectionTestRequestMetadata | Unset):
    """

    provider: ConnectionTestRequestProvider
    secrets: ConnectionTestRequestSecrets
    project_id: None | Unset | UUID = UNSET
    metadata: ConnectionTestRequestMetadata | Unset = UNSET

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
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.connection_test_request_metadata import ConnectionTestRequestMetadata
        from ..models.connection_test_request_secrets import ConnectionTestRequestSecrets

        d = dict(src_dict)
        provider = ConnectionTestRequestProvider(d.pop("provider"))

        secrets = ConnectionTestRequestSecrets.from_dict(d.pop("secrets"))

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

        _metadata = d.pop("metadata", UNSET)
        metadata: ConnectionTestRequestMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ConnectionTestRequestMetadata.from_dict(_metadata)

        connection_test_request = cls(
            provider=provider,
            secrets=secrets,
            project_id=project_id,
            metadata=metadata,
        )

        return connection_test_request
