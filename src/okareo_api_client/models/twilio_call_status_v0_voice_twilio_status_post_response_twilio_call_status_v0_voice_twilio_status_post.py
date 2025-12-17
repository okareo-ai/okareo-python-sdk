from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TwilioCallStatusV0VoiceTwilioStatusPostResponseTwilioCallStatusV0VoiceTwilioStatusPost")


@_attrs_define
class TwilioCallStatusV0VoiceTwilioStatusPostResponseTwilioCallStatusV0VoiceTwilioStatusPost:
    """ """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        twilio_call_status_v0_voice_twilio_status_post_response_twilio_call_status_v0_voice_twilio_status_post = cls()

        twilio_call_status_v0_voice_twilio_status_post_response_twilio_call_status_v0_voice_twilio_status_post.additional_properties = d
        return twilio_call_status_v0_voice_twilio_status_post_response_twilio_call_status_v0_voice_twilio_status_post

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
