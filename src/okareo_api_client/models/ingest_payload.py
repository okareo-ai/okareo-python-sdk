from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_ingest_request import ConversationIngestRequest


T = TypeVar("T", bound="IngestPayload")


@_attrs_define
class IngestPayload:
    """Top-level ingest request with project context.

    This is the monitoring path - conversations are ingested and monitored
    based on filter groups, not associated with a specific MUT like test runs.

        Attributes:
            project_id (UUID): Okareo project ID
            conversations (list[ConversationIngestRequest]): List of conversations to ingest (1+)
            mut_id (None | Unset | UUID): Optional model under test ID. If not provided, datapoints are created without a
                MUT association (monitoring path).
    """

    project_id: UUID
    conversations: list[ConversationIngestRequest]
    mut_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        conversations = []
        for conversations_item_data in self.conversations:
            conversations_item = conversations_item_data.to_dict()
            conversations.append(conversations_item)

        mut_id: None | str | Unset
        if isinstance(self.mut_id, Unset):
            mut_id = UNSET
        elif isinstance(self.mut_id, UUID):
            mut_id = str(self.mut_id)
        else:
            mut_id = self.mut_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "conversations": conversations,
            }
        )
        if mut_id is not UNSET:
            field_dict["mut_id"] = mut_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.conversation_ingest_request import ConversationIngestRequest

        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))

        conversations = []
        _conversations = d.pop("conversations")
        for conversations_item_data in _conversations:
            conversations_item = ConversationIngestRequest.from_dict(conversations_item_data)

            conversations.append(conversations_item)

        def _parse_mut_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mut_id_type_0 = UUID(data)

                return mut_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        mut_id = _parse_mut_id(d.pop("mut_id", UNSET))

        ingest_payload = cls(
            project_id=project_id,
            conversations=conversations,
            mut_id=mut_id,
        )

        ingest_payload.additional_properties = d
        return ingest_payload

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
