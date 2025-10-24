from typing import Any, Dict, List, Type, TypeVar, Union

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
        id (Union[Unset, str]): ID of the driver model
        model_id (Union[Unset, str]): Model ID of the driver model
        voice_instructions (Union[Unset, str]): Voice instructions for the driver model
        voice_profile (Union[Unset, str]): Voice profile for the driver model. Select from the following list of
            options: friendly, angry, confused, whispering, shouting, annoyed, urgent.
        voice (Union[Unset, str]): Voice setting for the driver model. Select from following available voices: oliver,
            olivia, oscar, ophelia, owen, opal.
        project_id (Union[Unset, str]): ID for project
    """

    name: str
    temperature: float
    prompt_template: str
    id: Union[Unset, str] = UNSET
    model_id: Union[Unset, str] = UNSET
    voice_instructions: Union[Unset, str] = UNSET
    voice_profile: Union[Unset, str] = UNSET
    voice: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        temperature = self.temperature
        prompt_template = self.prompt_template
        id = self.id
        model_id = self.model_id
        voice_instructions = self.voice_instructions
        voice_profile = self.voice_profile
        voice = self.voice
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
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
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        temperature = d.pop("temperature")

        prompt_template = d.pop("prompt_template")

        id = d.pop("id", UNSET)

        model_id = d.pop("model_id", UNSET)

        voice_instructions = d.pop("voice_instructions", UNSET)

        voice_profile = d.pop("voice_profile", UNSET)

        voice = d.pop("voice", UNSET)

        project_id = d.pop("project_id", UNSET)

        driver_model_schema = cls(
            name=name,
            temperature=temperature,
            prompt_template=prompt_template,
            id=id,
            model_id=model_id,
            voice_instructions=voice_instructions,
            voice_profile=voice_profile,
            voice=voice,
            project_id=project_id,
        )

        driver_model_schema.additional_properties = d
        return driver_model_schema

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
