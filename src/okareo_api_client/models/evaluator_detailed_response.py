import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.evaluator_detailed_response_check_config_type_0 import EvaluatorDetailedResponseCheckConfigType0


T = TypeVar("T", bound="EvaluatorDetailedResponse")


@_attrs_define
class EvaluatorDetailedResponse:
    """
    Attributes:
        id (Union[None, UUID, Unset]):
        project_id (Union[None, UUID, Unset]):
        name (Union[None, Unset, str]):
        description (Union[None, Unset, str]):  Default: ''.
        requires_scenario_input (Union[None, Unset, bool]):
        requires_scenario_result (Union[None, Unset, bool]):
        output_data_type (Union[None, Unset, str]):  Default: ''.
        code_contents (Union[None, Unset, str]):  Default: ''.
        time_created (Union[None, Unset, datetime.datetime]):
        warning (Union[None, Unset, str]):
        check_config (Union['EvaluatorDetailedResponseCheckConfigType0', None, Unset]):
        is_predefined (Union[None, Unset, bool]):  Default: False.
    """

    id: Union[None, UUID, Unset] = UNSET
    project_id: Union[None, UUID, Unset] = UNSET
    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = ""
    requires_scenario_input: Union[None, Unset, bool] = UNSET
    requires_scenario_result: Union[None, Unset, bool] = UNSET
    output_data_type: Union[None, Unset, str] = ""
    code_contents: Union[None, Unset, str] = ""
    time_created: Union[None, Unset, datetime.datetime] = UNSET
    warning: Union[None, Unset, str] = UNSET
    check_config: Union["EvaluatorDetailedResponseCheckConfigType0", None, Unset] = UNSET
    is_predefined: Union[None, Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.evaluator_detailed_response_check_config_type_0 import EvaluatorDetailedResponseCheckConfigType0

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        elif isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

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

        requires_scenario_input: Union[None, Unset, bool]
        if isinstance(self.requires_scenario_input, Unset):
            requires_scenario_input = UNSET
        else:
            requires_scenario_input = self.requires_scenario_input

        requires_scenario_result: Union[None, Unset, bool]
        if isinstance(self.requires_scenario_result, Unset):
            requires_scenario_result = UNSET
        else:
            requires_scenario_result = self.requires_scenario_result

        output_data_type: Union[None, Unset, str]
        if isinstance(self.output_data_type, Unset):
            output_data_type = UNSET
        else:
            output_data_type = self.output_data_type

        code_contents: Union[None, Unset, str]
        if isinstance(self.code_contents, Unset):
            code_contents = UNSET
        else:
            code_contents = self.code_contents

        time_created: Union[None, Unset, str]
        if isinstance(self.time_created, Unset):
            time_created = UNSET
        elif isinstance(self.time_created, datetime.datetime):
            time_created = self.time_created.isoformat()
        else:
            time_created = self.time_created

        warning: Union[None, Unset, str]
        if isinstance(self.warning, Unset):
            warning = UNSET
        else:
            warning = self.warning

        check_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.check_config, Unset):
            check_config = UNSET
        elif isinstance(self.check_config, EvaluatorDetailedResponseCheckConfigType0):
            check_config = self.check_config.to_dict()
        else:
            check_config = self.check_config

        is_predefined: Union[None, Unset, bool]
        if isinstance(self.is_predefined, Unset):
            is_predefined = UNSET
        else:
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
        from ..models.evaluator_detailed_response_check_config_type_0 import EvaluatorDetailedResponseCheckConfigType0

        d = dict(src_dict)

        def _parse_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                id_type_0 = UUID(data)

                return id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        id = _parse_id(d.pop("id", UNSET))

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

        def _parse_requires_scenario_input(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        requires_scenario_input = _parse_requires_scenario_input(d.pop("requires_scenario_input", UNSET))

        def _parse_requires_scenario_result(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        requires_scenario_result = _parse_requires_scenario_result(d.pop("requires_scenario_result", UNSET))

        def _parse_output_data_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output_data_type = _parse_output_data_type(d.pop("output_data_type", UNSET))

        def _parse_code_contents(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        code_contents = _parse_code_contents(d.pop("code_contents", UNSET))

        def _parse_time_created(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                time_created_type_0 = isoparse(data)

                return time_created_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        time_created = _parse_time_created(d.pop("time_created", UNSET))

        def _parse_warning(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        warning = _parse_warning(d.pop("warning", UNSET))

        def _parse_check_config(data: object) -> Union["EvaluatorDetailedResponseCheckConfigType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                check_config_type_0 = EvaluatorDetailedResponseCheckConfigType0.from_dict(data)

                return check_config_type_0
            except:  # noqa: E722
                pass
            return cast(Union["EvaluatorDetailedResponseCheckConfigType0", None, Unset], data)

        check_config = _parse_check_config(d.pop("check_config", UNSET))

        def _parse_is_predefined(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_predefined = _parse_is_predefined(d.pop("is_predefined", UNSET))

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
