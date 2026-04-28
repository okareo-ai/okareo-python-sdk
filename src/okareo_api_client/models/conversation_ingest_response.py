from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_ingest_response_conversations_item import ConversationIngestResponseConversationsItem


T = TypeVar("T", bound="ConversationIngestResponse")


@_attrs_define
class ConversationIngestResponse:
    """Response after enqueuing conversations for processing.

    Attributes:
        conversations (list[ConversationIngestResponseConversationsItem]): List of call_id and context_token pairs
        status (str | Unset): Processing status Default: 'accepted'.
    """

    conversations: list[ConversationIngestResponseConversationsItem]
    status: str | Unset = "accepted"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        conversations = []
        for conversations_item_data in self.conversations:
            conversations_item = conversations_item_data.to_dict()
            conversations.append(conversations_item)

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "conversations": conversations,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.conversation_ingest_response_conversations_item import ConversationIngestResponseConversationsItem

        d = dict(src_dict)
        conversations = []
        _conversations = d.pop("conversations")
        for conversations_item_data in _conversations:
            conversations_item = ConversationIngestResponseConversationsItem.from_dict(conversations_item_data)

            conversations.append(conversations_item)

        status = d.pop("status", UNSET)

        conversation_ingest_response = cls(
            conversations=conversations,
            status=status,
        )

        conversation_ingest_response.additional_properties = d
        return conversation_ingest_response

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
