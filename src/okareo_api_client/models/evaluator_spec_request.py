from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EvaluatorSpecRequest")


@_attrs_define
class EvaluatorSpecRequest:
    """
    Attributes:
        name (Union[Unset, str]): Name of the evaluator
        description (Union[Unset, str]): Description for the evaluator.
                        When this request is sent to generate an evaluator, this field will be used to generate it.
        requires_scenario_input (Union[Unset, bool]): Whether the evaluator requires scenario input
        requires_scenario_result (Union[Unset, bool]): Whether the evaluator requires scenario expected result
        output_data_type (Union[Unset, str]): Evaluator output data type (i.e., bool, int, float)
        project_id (Union[Unset, str]): ID for the project
        check_type (Union[Unset, str]): model or code based check Default: 'code'.
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    requires_scenario_input: Union[Unset, bool] = False
    requires_scenario_result: Union[Unset, bool] = False
    output_data_type: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    check_type: Union[Unset, str] = "code"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        requires_scenario_input = self.requires_scenario_input
        requires_scenario_result = self.requires_scenario_result
        output_data_type = self.output_data_type
        project_id = self.project_id
        check_type = self.check_type

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
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if check_type is not UNSET:
            field_dict["check_type"] = check_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        requires_scenario_input = d.pop("requires_scenario_input", UNSET)

        requires_scenario_result = d.pop("requires_scenario_result", UNSET)

        output_data_type = d.pop("output_data_type", UNSET)

        project_id = d.pop("project_id", UNSET)

        check_type = d.pop("check_type", UNSET)

        evaluator_spec_request = cls(
            name=name,
            description=description,
            requires_scenario_input=requires_scenario_input,
            requires_scenario_result=requires_scenario_result,
            output_data_type=output_data_type,
            project_id=project_id,
            check_type=check_type,
        )

        evaluator_spec_request.additional_properties = d
        return evaluator_spec_request

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
