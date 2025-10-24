from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VoiceProfileResponse")


@_attrs_define
class VoiceProfileResponse:
    """
    Attributes:
        profile_name (str):
        voice_instructions (str):
    """

    profile_name: str
    voice_instructions: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        profile_name = self.profile_name
        voice_instructions = self.voice_instructions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profile_name": profile_name,
                "voice_instructions": voice_instructions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        profile_name = d.pop("profile_name")

        voice_instructions = d.pop("voice_instructions")

        voice_profile_response = cls(
            profile_name=profile_name,
            voice_instructions=voice_instructions,
        )

        voice_profile_response.additional_properties = d
        return voice_profile_response

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
