from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.driver_step_schema import DriverStepSchema


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
        voice_profile (None | str | Unset): Alias of voice_tone, kept for older clients.
        voice (None | str | Unset): Voice setting for the driver model. Use GET /v0/voices to retrieve available voice
            options.
        language (None | str | Unset): Language code in BCP-47 format (e.g., 'en-US', 'es-MX', 'ja', 'fr-CA'). For voice
            targets, improves STT accuracy by constraining language model. If not specified, defaults to 'multi' for
            automatic language detection.
        project_id (None | Unset | UUID): ID for project
        steps (list[DriverStepSchema] | None | str | Unset): Scripted Driver: an ordered list of steps ({message},
            {dtmf}, {end_conversation}), or one {scenario_input.<column>} reference that resolves to that list per scenario
            row. end_conversation must be last. When set, prompt_template is not used and no Driver LLM runs.
        voice_tone (None | str | Unset): The emotion the driver's voice performs: a supported tone token such as 'angry'
            or 'calm' (GET /v0/driver_profiles lists the presets), or a template such as {scenario_input.voice_tone}.
        voice_speed (float | None | Unset): Speech rate for the driver's voice, 0.6 to 1.5 times the voice's own pace.
            Omit for the voice's default.
        voice_volume (float | None | Unset): Loudness for the driver's voice, 0.5 to 2.0 times the voice's own level.
            Omit for the voice's default.
    """

    name: str
    temperature: float
    prompt_template: str
    id: None | Unset | UUID = UNSET
    model_id: None | str | Unset = UNSET
    voice_profile: None | str | Unset = UNSET
    voice: None | str | Unset = UNSET
    language: None | str | Unset = UNSET
    project_id: None | Unset | UUID = UNSET
    steps: list[DriverStepSchema] | None | str | Unset = UNSET
    voice_tone: None | str | Unset = UNSET
    voice_speed: float | None | Unset = UNSET
    voice_volume: float | None | Unset = UNSET
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

        steps: list[dict[str, Any]] | None | str | Unset
        if isinstance(self.steps, Unset):
            steps = UNSET
        elif isinstance(self.steps, list):
            steps = []
            for steps_type_0_item_data in self.steps:
                steps_type_0_item = steps_type_0_item_data.to_dict()
                steps.append(steps_type_0_item)

        else:
            steps = self.steps

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
                "name": name,
                "temperature": temperature,
                "prompt_template": prompt_template,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if model_id is not UNSET:
            field_dict["model_id"] = model_id
        if voice_profile is not UNSET:
            field_dict["voice_profile"] = voice_profile
        if voice is not UNSET:
            field_dict["voice"] = voice
        if language is not UNSET:
            field_dict["language"] = language
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if steps is not UNSET:
            field_dict["steps"] = steps
        if voice_tone is not UNSET:
            field_dict["voice_tone"] = voice_tone
        if voice_speed is not UNSET:
            field_dict["voice_speed"] = voice_speed
        if voice_volume is not UNSET:
            field_dict["voice_volume"] = voice_volume

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.driver_step_schema import DriverStepSchema

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

        def _parse_steps(data: object) -> list[DriverStepSchema] | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                steps_type_0 = []
                _steps_type_0 = data
                for steps_type_0_item_data in _steps_type_0:
                    steps_type_0_item = DriverStepSchema.from_dict(steps_type_0_item_data)

                    steps_type_0.append(steps_type_0_item)

                return steps_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[DriverStepSchema] | None | str | Unset, data)

        steps = _parse_steps(d.pop("steps", UNSET))

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

        driver_model_schema = cls(
            name=name,
            temperature=temperature,
            prompt_template=prompt_template,
            id=id,
            model_id=model_id,
            voice_profile=voice_profile,
            voice=voice,
            language=language,
            project_id=project_id,
            steps=steps,
            voice_tone=voice_tone,
            voice_speed=voice_speed,
            voice_volume=voice_volume,
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
