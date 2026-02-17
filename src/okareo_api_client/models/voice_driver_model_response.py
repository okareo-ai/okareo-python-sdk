from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VoiceDriverModelResponse")


@_attrs_define
class VoiceDriverModelResponse:
    """
    Attributes:
        id (UUID):
        name (str):
        temperature (float):
        prompt_template (str):
        time_created (str):
        model_id (None | str | Unset):
        project_id (None | Unset | UUID):
        voice_instructions (None | str | Unset):
        voice (None | str | Unset):
        language (None | str | Unset):
    """

    id: UUID
    name: str
    temperature: float
    prompt_template: str
    time_created: str
    model_id: None | str | Unset = UNSET
    project_id: None | Unset | UUID = UNSET
    voice_instructions: None | str | Unset = UNSET
    voice: None | str | Unset = UNSET
    language: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        temperature = self.temperature

        prompt_template = self.prompt_template

        time_created = self.time_created

        model_id: None | str | Unset
        if isinstance(self.model_id, Unset):
            model_id = UNSET
        else:
            model_id = self.model_id

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        voice_instructions: None | str | Unset
        if isinstance(self.voice_instructions, Unset):
            voice_instructions = UNSET
        else:
            voice_instructions = self.voice_instructions

        voice: None | str | Unset
        if isinstance(self.voice, Unset):
            voice = UNSET
        else:
            voice = self.voice

        language: None | str | Unset
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "temperature": temperature,
                "prompt_template": prompt_template,
                "time_created": time_created,
            }
        )
        if model_id is not UNSET:
            field_dict["model_id"] = model_id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if voice_instructions is not UNSET:
            field_dict["voice_instructions"] = voice_instructions
        if voice is not UNSET:
            field_dict["voice"] = voice
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        temperature = d.pop("temperature")

        prompt_template = d.pop("prompt_template")

        time_created = d.pop("time_created")

        def _parse_model_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_id = _parse_model_id(d.pop("model_id", UNSET))

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

        def _parse_voice_instructions(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        voice_instructions = _parse_voice_instructions(d.pop("voice_instructions", UNSET))

        def _parse_voice(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        voice = _parse_voice(d.pop("voice", UNSET))

        def _parse_language(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        language = _parse_language(d.pop("language", UNSET))

        voice_driver_model_response = cls(
            id=id,
            name=name,
            temperature=temperature,
            prompt_template=prompt_template,
            time_created=time_created,
            model_id=model_id,
            project_id=project_id,
            voice_instructions=voice_instructions,
            voice=voice,
            language=language,
        )

        voice_driver_model_response.additional_properties = d
        return voice_driver_model_response

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
