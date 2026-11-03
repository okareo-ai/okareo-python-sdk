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
        voice_profile (None | str | Unset): Alias of voice_tone, kept for older clients.
        voice (None | str | Unset): Voice setting for the driver model. Use GET /v0/voices to retrieve available voice
            options.
        language (None | str | Unset): Language code in BCP-47 format (e.g., 'en-US', 'es-MX', 'ja', 'fr-CA'). For voice
            targets, improves STT accuracy by constraining language model.
        voice_tone (None | str | Unset): The emotion the driver's voice performs: a supported tone token such as 'angry'
            or 'calm', or a template such as {scenario_input.voice_tone}.
        voice_speed (float | None | Unset): Speech rate for the driver's voice, 0.6 to 1.5 times the voice's own pace.
            Omit for the voice's default.
        voice_volume (float | None | Unset): Loudness for the driver's voice, 0.5 to 2.0 times the voice's own level.
            Omit for the voice's default.
    """

    test_input: str
    prompt_template: None | str | Unset = UNSET
    temperature: float | None | Unset = 0.0
    voice_profile: None | str | Unset = UNSET
    voice: None | str | Unset = UNSET
    language: None | str | Unset = UNSET
    voice_tone: None | str | Unset = UNSET
    voice_speed: float | None | Unset = UNSET
    voice_volume: float | None | Unset = UNSET
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

        voice_tone: None | str | Unset
        if isinstance(self.voice_tone, Unset):
            voice_tone = UNSET
        else:
            voice_tone = self.voice_tone

        voice_speed: float | None | Unset
        if isinstance(self.voice_speed, Unset):
            voice_speed = UNSET
        else:
            voice_speed = self.voice_speed

        voice_volume: float | None | Unset
        if isinstance(self.voice_volume, Unset):
            voice_volume = UNSET
        else:
            voice_volume = self.voice_volume

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
        if voice_profile is not UNSET:
            field_dict["voice_profile"] = voice_profile
        if voice is not UNSET:
            field_dict["voice"] = voice
        if language is not UNSET:
            field_dict["language"] = language
        if voice_tone is not UNSET:
            field_dict["voice_tone"] = voice_tone
        if voice_speed is not UNSET:
            field_dict["voice_speed"] = voice_speed
        if voice_volume is not UNSET:
            field_dict["voice_volume"] = voice_volume

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

        def _parse_voice_tone(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        voice_tone = _parse_voice_tone(d.pop("voice_tone", UNSET))

        def _parse_voice_speed(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        voice_speed = _parse_voice_speed(d.pop("voice_speed", UNSET))

        def _parse_voice_volume(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        voice_volume = _parse_voice_volume(d.pop("voice_volume", UNSET))

        test_driver_request = cls(
            test_input=test_input,
            prompt_template=prompt_template,
            temperature=temperature,
            voice_profile=voice_profile,
            voice=voice,
            language=language,
            voice_tone=voice_tone,
            voice_speed=voice_speed,
            voice_volume=voice_volume,
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
