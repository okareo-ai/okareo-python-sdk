from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestDriverRequest")


@_attrs_define
class TestDriverRequest:
    """
    Attributes:
        test_input (str): Test prompt to which the driver model will respond.
        prompt_template (None | str | Unset): Prompt template for the driver model. If not provided, backend will
            generate one based on language parameter.
        temperature (float | None | Unset): Temperature of the driver model Default: 0.0.
        voice_instructions (None | str | Unset): Voice instructions for the driver model
        voice_profile (None | str | Unset): Voice profile for the driver model. Select from the following list of
            options: friendly, angry, confused, whispering, shouting, annoyed, urgent.
        voice (None | str | Unset): Voice setting for the driver model. Use GET /v0/voices to retrieve available voice
            options.
        language (None | str | Unset): Language code in BCP-47 format (e.g., 'en-US', 'es-MX', 'ja', 'fr-CA'). For voice
            targets, improves STT accuracy by constraining language model.
    """

    test_input: str
    prompt_template: None | str | Unset = UNSET
    temperature: float | None | Unset = 0.0
    voice_instructions: None | str | Unset = UNSET
    voice_profile: None | str | Unset = UNSET
    voice: None | str | Unset = UNSET
    language: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        test_input = self.test_input

        prompt_template: None | str | Unset
        if isinstance(self.prompt_template, Unset):
            prompt_template = UNSET
        else:
            prompt_template = self.prompt_template

        temperature: float | None | Unset
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_input": test_input,
            }
        )
        if prompt_template is not UNSET:
            field_dict["prompt_template"] = prompt_template
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if voice_instructions is not UNSET:
            field_dict["voice_instructions"] = voice_instructions
        if voice_profile is not UNSET:
            field_dict["voice_profile"] = voice_profile
        if voice is not UNSET:
            field_dict["voice"] = voice
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        test_input = d.pop("test_input")

        def _parse_prompt_template(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prompt_template = _parse_prompt_template(d.pop("prompt_template", UNSET))

        def _parse_temperature(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

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

        test_driver_request = cls(
            test_input=test_input,
            prompt_template=prompt_template,
            temperature=temperature,
            voice_instructions=voice_instructions,
            voice_profile=voice_profile,
            voice=voice,
            language=language,
        )

        test_driver_request.additional_properties = d
        return test_driver_request

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
