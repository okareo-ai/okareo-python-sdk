from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EvaluatorSpecRequest")


@_attrs_define
class EvaluatorSpecRequest:
    """
    Attributes:
        name (Union[None, Unset, str]): Name of the evaluator
        description (Union[None, Unset, str]): Description for the evaluator.
                        When this request is sent to generate an evaluator, this field will be used to generate it.
        requires_scenario_input (Union[Unset, bool]): Whether the evaluator requires scenario input Default: False.
        requires_scenario_result (Union[Unset, bool]): Whether the evaluator requires scenario expected result Default:
            False.
        output_data_type (Union[None, Unset, str]): Evaluator output data type (i.e., bool, int, float)
        project_id (Union[None, UUID, Unset]): ID for the project
        check_type (Union[None, Unset, str]): model or code based check Default: 'code'.
    """

    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    requires_scenario_input: Union[Unset, bool] = False
    requires_scenario_result: Union[Unset, bool] = False
    output_data_type: Union[None, Unset, str] = UNSET
    project_id: Union[None, UUID, Unset] = UNSET
    check_type: Union[None, Unset, str] = "code"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        requires_scenario_input = self.requires_scenario_input

        requires_scenario_result = self.requires_scenario_result

        output_data_type: Union[None, Unset, str]
        if isinstance(self.output_data_type, Unset):
            output_data_type = UNSET
        else:
            output_data_type = self.output_data_type

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        check_type: Union[None, Unset, str]
        if isinstance(self.check_type, Unset):
            check_type = UNSET
        else:
            check_type = self.check_type

        field_dict: dict[str, Any] = {}
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        requires_scenario_input = d.pop("requires_scenario_input", UNSET)

        requires_scenario_result = d.pop("requires_scenario_result", UNSET)

        def _parse_output_data_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output_data_type = _parse_output_data_type(d.pop("output_data_type", UNSET))

        def _parse_project_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_check_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        check_type = _parse_check_type(d.pop("check_type", UNSET))

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
