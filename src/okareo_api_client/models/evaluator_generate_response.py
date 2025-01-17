from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EvaluatorGenerateResponse")


@_attrs_define
class EvaluatorGenerateResponse:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        requires_scenario_input (Union[Unset, bool]):
        requires_scenario_result (Union[Unset, bool]):
        output_data_type (Union[Unset, str]):
        generated_code (Union[Unset, str]):
        generated_prompt (Union[Unset, str]):
        warning (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    requires_scenario_input: Union[Unset, bool] = UNSET
    requires_scenario_result: Union[Unset, bool] = UNSET
    output_data_type: Union[Unset, str] = UNSET
    generated_code: Union[Unset, str] = UNSET
    generated_prompt: Union[Unset, str] = UNSET
    warning: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        requires_scenario_input = self.requires_scenario_input
        requires_scenario_result = self.requires_scenario_result
        output_data_type = self.output_data_type
        generated_code = self.generated_code
        generated_prompt = self.generated_prompt
        warning = self.warning

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if requires_scenario_input is not UNSET:
            field_dict["requires_scenario_input"] = requires_scenario_input
        if requires_scenario_result is not UNSET:
            field_dict["requires_scenario_result"] = requires_scenario_result
        if output_data_type is not UNSET:
            field_dict["output_data_type"] = output_data_type
        if generated_code is not UNSET:
            field_dict["generated_code"] = generated_code
        if generated_prompt is not UNSET:
            field_dict["generated_prompt"] = generated_prompt
        if warning is not UNSET:
            field_dict["warning"] = warning

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        requires_scenario_input = d.pop("requires_scenario_input", UNSET)

        requires_scenario_result = d.pop("requires_scenario_result", UNSET)

        output_data_type = d.pop("output_data_type", UNSET)

        generated_code = d.pop("generated_code", UNSET)

        generated_prompt = d.pop("generated_prompt", UNSET)

        warning = d.pop("warning", UNSET)

        evaluator_generate_response = cls(
            name=name,
            description=description,
            requires_scenario_input=requires_scenario_input,
            requires_scenario_result=requires_scenario_result,
            output_data_type=output_data_type,
            generated_code=generated_code,
            generated_prompt=generated_prompt,
            warning=warning,
        )

        evaluator_generate_response.additional_properties = d
        return evaluator_generate_response

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
