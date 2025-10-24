from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestDriverRequest")


@_attrs_define
class TestDriverRequest:
    """
    Attributes:
        prompt_template (str): Prompt template for the driver model
        test_input (str): Test prompt to which the driver model will respond.
        temperature (Union[Unset, float]): Temperature of the driver model
        voice_instructions (Union[Unset, str]): Voice instructions for the driver model
        voice_profile (Union[Unset, str]): Voice profile for the driver model. Select from the following list of
            options: friendly, angry, confused, whispering, shouting, annoyed, urgent.
        voice (Union[Unset, str]): Voice setting for the driver model. Select from following available voices: oliver,
            olivia, oscar, ophelia, owen, opal.
    """

    prompt_template: str
    test_input: str
    temperature: Union[Unset, float] = 0.0
    voice_instructions: Union[Unset, str] = UNSET
    voice_profile: Union[Unset, str] = UNSET
    voice: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prompt_template = self.prompt_template
        test_input = self.test_input
        temperature = self.temperature
        voice_instructions = self.voice_instructions
        voice_profile = self.voice_profile
        voice = self.voice

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt_template": prompt_template,
                "test_input": test_input,
            }
        )
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if voice_instructions is not UNSET:
            field_dict["voice_instructions"] = voice_instructions
        if voice_profile is not UNSET:
            field_dict["voice_profile"] = voice_profile
        if voice is not UNSET:
            field_dict["voice"] = voice

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        prompt_template = d.pop("prompt_template")

        test_input = d.pop("test_input")

        temperature = d.pop("temperature", UNSET)

        voice_instructions = d.pop("voice_instructions", UNSET)

        voice_profile = d.pop("voice_profile", UNSET)

        voice = d.pop("voice", UNSET)

        test_driver_request = cls(
            prompt_template=prompt_template,
            test_input=test_input,
            temperature=temperature,
            voice_instructions=voice_instructions,
            voice_profile=voice_profile,
            voice=voice,
        )

        test_driver_request.additional_properties = d
        return test_driver_request

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
