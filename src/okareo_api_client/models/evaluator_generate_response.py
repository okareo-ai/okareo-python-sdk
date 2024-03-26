from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EvaluatorGenerateResponse")


@_attrs_define
class EvaluatorGenerateResponse:
    """
    Attributes:
        requirements (Union[Unset, str]): Requirements used to generate the evaluator
        requires_scenario_input (Union[Unset, bool]): Whether the evaluator requires scenario input
        requires_scenario_result (Union[Unset, bool]): Whether the evaluator requires scenario expected result
        generated_code (Union[Unset, str]): Generated code for the evaluator based on the requirements
    """

    requirements: Union[Unset, str] = UNSET
    requires_scenario_input: Union[Unset, bool] = False
    requires_scenario_result: Union[Unset, bool] = False
    generated_code: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        requirements = self.requirements
        requires_scenario_input = self.requires_scenario_input
        requires_scenario_result = self.requires_scenario_result
        generated_code = self.generated_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if requirements is not UNSET:
            field_dict["requirements"] = requirements
        if requires_scenario_input is not UNSET:
            field_dict["requires_scenario_input"] = requires_scenario_input
        if requires_scenario_result is not UNSET:
            field_dict["requires_scenario_result"] = requires_scenario_result
        if generated_code is not UNSET:
            field_dict["generated_code"] = generated_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        requirements = d.pop("requirements", UNSET)

        requires_scenario_input = d.pop("requires_scenario_input", UNSET)

        requires_scenario_result = d.pop("requires_scenario_result", UNSET)

        generated_code = d.pop("generated_code", UNSET)

        evaluator_generate_response = cls(
            requirements=requirements,
            requires_scenario_input=requires_scenario_input,
            requires_scenario_result=requires_scenario_result,
            generated_code=generated_code,
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
