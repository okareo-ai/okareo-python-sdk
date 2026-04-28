from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.conversation_audio_type import ConversationAudioType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConversationAudio")


@_attrs_define
class ConversationAudio:
    """Audio attachment for a conversation ingest request.

    Attributes:
        type_ (ConversationAudioType): Audio reference type
        url (None | str | Unset): Externally hosted audio URL when type='url'
        voice_file_id (None | str | Unset): Existing Okareo voice file identifier when type='voice_file_id'
        inline_b64 (None | str | Unset): Base64-encoded audio bytes when type='inline_b64'
    """

    type_: ConversationAudioType
    url: None | str | Unset = UNSET
    voice_file_id: None | str | Unset = UNSET
    inline_b64: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        url: None | str | Unset
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        voice_file_id: None | str | Unset
        if isinstance(self.voice_file_id, Unset):
            voice_file_id = UNSET
        else:
            voice_file_id = self.voice_file_id

        inline_b64: None | str | Unset
        if isinstance(self.inline_b64, Unset):
            inline_b64 = UNSET
        else:
            inline_b64 = self.inline_b64

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if url is not UNSET:
            field_dict["url"] = url
        if voice_file_id is not UNSET:
            field_dict["voice_file_id"] = voice_file_id
        if inline_b64 is not UNSET:
            field_dict["inline_b64"] = inline_b64

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = ConversationAudioType(d.pop("type"))

        def _parse_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        url = _parse_url(d.pop("url", UNSET))

        def _parse_voice_file_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        voice_file_id = _parse_voice_file_id(d.pop("voice_file_id", UNSET))

        def _parse_inline_b64(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        inline_b64 = _parse_inline_b64(d.pop("inline_b64", UNSET))

        conversation_audio = cls(
            type_=type_,
            url=url,
            voice_file_id=voice_file_id,
            inline_b64=inline_b64,
        )

        conversation_audio.additional_properties = d
        return conversation_audio

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
