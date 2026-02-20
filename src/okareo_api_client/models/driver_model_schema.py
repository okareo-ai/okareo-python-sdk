from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DriverModelSchema")


@_attrs_define
class DriverModelSchema:
    """
    Attributes:
        name (str): Name of the driver model
        temperature (float): Temperature of the driver model
        prompt_template (str): Prompt template for the driver model
        id (None | Unset | UUID): ID of the driver model
        model_id (None | str | Unset): Model ID of the driver model
        voice_instructions (None | str | Unset): Voice instructions for the driver model
        voice_profile (None | str | Unset): Voice profile for the driver model. Select from the following list of
            options: friendly, angry, confused, whispering, shouting, annoyed, urgent.
        voice (None | str | Unset): Voice setting for the driver model. Use GET /v0/voices to retrieve available voice
            options.
        language (None | str | Unset): Language code in BCP-47 format (e.g., 'en-US', 'es-MX', 'ja', 'fr-CA'). For voice
            targets, improves STT accuracy by constraining language model. If not specified, defaults to 'multi' for
            automatic language detection.
        project_id (None | Unset | UUID): ID for project
    """

    name: str
    temperature: float
    prompt_template: str
    id: None | Unset | UUID = UNSET
    model_id: None | str | Unset = UNSET
    voice_instructions: None | str | Unset = UNSET
    voice_profile: None | str | Unset = UNSET
    voice: None | str | Unset = UNSET
    language: None | str | Unset = UNSET
    project_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        temperature = self.temperature

        prompt_template = self.prompt_template

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        elif isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        model_id: None | str | Unset
        if isinstance(self.model_id, Unset):
            model_id = UNSET
        else:
            model_id = self.model_id

        voice_instructions: None | str | Unset
        if isinstance(self.voice_instructions, Unset):
            voice_instructions = UNSET
        else:
            voice_instructions = self.voice_instructions

        voice_profile: None | str | Unset
        if isinstance(self.voice_profile, Unset):
            voice_profile = UNSET
        else:
            voice_profile = self.voice_profile

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

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "temperature": temperature,
                "prompt_template": prompt_template,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if model_id is not UNSET:
            field_dict["model_id"] = model_id
        if voice_instructions is not UNSET:
            field_dict["voice_instructions"] = voice_instructions
        if voice_profile is not UNSET:
            field_dict["voice_profile"] = voice_profile
        if voice is not UNSET:
            field_dict["voice"] = voice
        if language is not UNSET:
            field_dict["language"] = language
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        temperature = d.pop("temperature")

        prompt_template = d.pop("prompt_template")

        def _parse_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                id_type_0 = UUID(data)

                return id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_model_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_id = _parse_model_id(d.pop("model_id", UNSET))

        def _parse_voice_instructions(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        voice_instructions = _parse_voice_instructions(d.pop("voice_instructions", UNSET))

        def _parse_voice_profile(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        voice_profile = _parse_voice_profile(d.pop("voice_profile", UNSET))

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

        driver_model_schema = cls(
            name=name,
            temperature=temperature,
            prompt_template=prompt_template,
            id=id,
            model_id=model_id,
            voice_instructions=voice_instructions,
            voice_profile=voice_profile,
            voice=voice,
            language=language,
            project_id=project_id,
        )

        driver_model_schema.additional_properties = d
        return driver_model_schema

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
