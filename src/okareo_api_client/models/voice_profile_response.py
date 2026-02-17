from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

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
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        profile_name = self.profile_name

        voice_instructions = self.voice_instructions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profile_name": profile_name,
                "voice_instructions": voice_instructions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        profile_name = d.pop("profile_name")

        voice_instructions = d.pop("voice_instructions")

        voice_profile_response = cls(
            profile_name=profile_name,
            voice_instructions=voice_instructions,
        )

        voice_profile_response.additional_properties = d
        return voice_profile_response

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
