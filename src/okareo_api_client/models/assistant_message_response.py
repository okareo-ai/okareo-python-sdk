from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AssistantMessageResponse")


@_attrs_define
class AssistantMessageResponse:
    """
    Attributes:
        thread_id (str):
        assistant_response (str):
        message_id (str):
    """

    thread_id: str
    assistant_response: str
    message_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        thread_id = self.thread_id
        assistant_response = self.assistant_response
        message_id = self.message_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "thread_id": thread_id,
                "assistant_response": assistant_response,
                "message_id": message_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        thread_id = d.pop("thread_id")

        assistant_response = d.pop("assistant_response")

        message_id = d.pop("message_id")

        assistant_message_response = cls(
            thread_id=thread_id,
            assistant_response=assistant_response,
            message_id=message_id,
        )

        assistant_message_response.additional_properties = d
        return assistant_message_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
