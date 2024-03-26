from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EvaluatorGenerateRequest")


@_attrs_define
class EvaluatorGenerateRequest:
    """
    Attributes:
        requirements (Union[Unset, str]): Requirements used to generate the evaluator
        requires_scenario_input (Union[Unset, bool]): Whether the evaluator requires scenario input
        requires_scenario_result (Union[Unset, bool]): Whether the evaluator requires scenario expected result
        output_data_type (Union[Unset, str]): Evaluator output data type (i.e., boolean, integer, float)
    """

    requirements: Union[Unset, str] = UNSET
    requires_scenario_input: Union[Unset, bool] = False
    requires_scenario_result: Union[Unset, bool] = False
    output_data_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        requirements = self.requirements
        requires_scenario_input = self.requires_scenario_input
        requires_scenario_result = self.requires_scenario_result
        output_data_type = self.output_data_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if requirements is not UNSET:
            field_dict["requirements"] = requirements
        if requires_scenario_input is not UNSET:
            field_dict["requires_scenario_input"] = requires_scenario_input
        if requires_scenario_result is not UNSET:
            field_dict["requires_scenario_result"] = requires_scenario_result
        if output_data_type is not UNSET:
            field_dict["output_data_type"] = output_data_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        requirements = d.pop("requirements", UNSET)

        requires_scenario_input = d.pop("requires_scenario_input", UNSET)

        requires_scenario_result = d.pop("requires_scenario_result", UNSET)

        output_data_type = d.pop("output_data_type", UNSET)

        evaluator_generate_request = cls(
            requirements=requirements,
            requires_scenario_input=requires_scenario_input,
            requires_scenario_result=requires_scenario_result,
            output_data_type=output_data_type,
        )

        evaluator_generate_request.additional_properties = d
        return evaluator_generate_request

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
