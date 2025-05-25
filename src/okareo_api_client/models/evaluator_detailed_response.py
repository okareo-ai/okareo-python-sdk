import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.evaluator_detailed_response_check_config import EvaluatorDetailedResponseCheckConfig


T = TypeVar("T", bound="EvaluatorDetailedResponse")


@_attrs_define
class EvaluatorDetailedResponse:
    """
    Attributes:
        id (Union[Unset, UUID]):
        project_id (Union[Unset, UUID]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):  Default: ''.
        requires_scenario_input (Union[Unset, bool]):
        requires_scenario_result (Union[Unset, bool]):
        output_data_type (Union[Unset, str]):  Default: ''.
        code_contents (Union[Unset, str]):  Default: ''.
        time_created (Union[Unset, datetime.datetime]):
        warning (Union[Unset, str]):
        check_config (Union[Unset, EvaluatorDetailedResponseCheckConfig]):
        is_predefined (Union[Unset, bool]):  Default: False.
    """

    id: Union[Unset, UUID] = UNSET
    project_id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = ""
    requires_scenario_input: Union[Unset, bool] = UNSET
    requires_scenario_result: Union[Unset, bool] = UNSET
    output_data_type: Union[Unset, str] = ""
    code_contents: Union[Unset, str] = ""
    time_created: Union[Unset, datetime.datetime] = UNSET
    warning: Union[Unset, str] = UNSET
    check_config: Union[Unset, "EvaluatorDetailedResponseCheckConfig"] = UNSET
    is_predefined: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        project_id: Union[Unset, str] = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        name = self.name

        description = self.description

        requires_scenario_input = self.requires_scenario_input

        requires_scenario_result = self.requires_scenario_result

        output_data_type = self.output_data_type

        code_contents = self.code_contents

        time_created: Union[Unset, str] = UNSET
        if not isinstance(self.time_created, Unset):
            time_created = self.time_created.isoformat()

        warning = self.warning

        check_config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.check_config, Unset):
            check_config = self.check_config.to_dict()

        is_predefined = self.is_predefined

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
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
        if code_contents is not UNSET:
            field_dict["code_contents"] = code_contents
        if time_created is not UNSET:
            field_dict["time_created"] = time_created
        if warning is not UNSET:
            field_dict["warning"] = warning
        if check_config is not UNSET:
            field_dict["check_config"] = check_config
        if is_predefined is not UNSET:
            field_dict["is_predefined"] = is_predefined

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluator_detailed_response_check_config import EvaluatorDetailedResponseCheckConfig

        d = dict(src_dict)
        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        _project_id = d.pop("project_id", UNSET)
        project_id: Union[Unset, UUID]
        if isinstance(_project_id, Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        requires_scenario_input = d.pop("requires_scenario_input", UNSET)

        requires_scenario_result = d.pop("requires_scenario_result", UNSET)

        output_data_type = d.pop("output_data_type", UNSET)

        code_contents = d.pop("code_contents", UNSET)

        _time_created = d.pop("time_created", UNSET)
        time_created: Union[Unset, datetime.datetime]
        if isinstance(_time_created, Unset):
            time_created = UNSET
        else:
            time_created = isoparse(_time_created)

        warning = d.pop("warning", UNSET)

        _check_config = d.pop("check_config", UNSET)
        check_config: Union[Unset, EvaluatorDetailedResponseCheckConfig]
        if isinstance(_check_config, Unset):
            check_config = UNSET
        else:
            check_config = EvaluatorDetailedResponseCheckConfig.from_dict(_check_config)

        is_predefined = d.pop("is_predefined", UNSET)

        evaluator_detailed_response = cls(
            id=id,
            project_id=project_id,
            name=name,
            description=description,
            requires_scenario_input=requires_scenario_input,
            requires_scenario_result=requires_scenario_result,
            output_data_type=output_data_type,
            code_contents=code_contents,
            time_created=time_created,
            warning=warning,
            check_config=check_config,
            is_predefined=is_predefined,
        )

        evaluator_detailed_response.additional_properties = d
        return evaluator_detailed_response

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
