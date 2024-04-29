from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="BodyCheckUploadV0CheckUploadPost")


@_attrs_define
class BodyCheckUploadV0CheckUploadPost:
    """
    Attributes:
        name (str): Name of the Check
        requires_scenario_input (bool): Whether the check requires scenario input
        requires_scenario_result (bool): Whether the check requires scenario expected result
        description (Union[Unset, str]): Description of the Check Default: 'No description provided'.
        output_data_type (Union[Unset, str]): Check output data type (i.e., bool, int, float)
        project_id (Union[Unset, str]): ID for the project
        file (Union[Unset, File]):
        update (Union[Unset, bool]): Update the check
    """

    name: str
    requires_scenario_input: bool
    requires_scenario_result: bool
    description: Union[Unset, str] = "No description provided"
    output_data_type: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    file: Union[Unset, File] = UNSET
    update: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        requires_scenario_input = self.requires_scenario_input
        requires_scenario_result = self.requires_scenario_result
        description = self.description
        output_data_type = self.output_data_type
        project_id = self.project_id
        file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_tuple()

        update = self.update

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "requires_scenario_input": requires_scenario_input,
                "requires_scenario_result": requires_scenario_result,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if output_data_type is not UNSET:
            field_dict["output_data_type"] = output_data_type
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if file is not UNSET:
            field_dict["file"] = file
        if update is not UNSET:
            field_dict["update"] = update

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        name = self.name if isinstance(self.name, Unset) else (None, str(self.name).encode(), "text/plain")
        requires_scenario_input = (
            self.requires_scenario_input
            if isinstance(self.requires_scenario_input, Unset)
            else (None, str(self.requires_scenario_input).encode(), "text/plain")
        )
        requires_scenario_result = (
            self.requires_scenario_result
            if isinstance(self.requires_scenario_result, Unset)
            else (None, str(self.requires_scenario_result).encode(), "text/plain")
        )
        description = (
            self.description
            if isinstance(self.description, Unset)
            else (None, str(self.description).encode(), "text/plain")
        )
        output_data_type = (
            self.output_data_type
            if isinstance(self.output_data_type, Unset)
            else (None, str(self.output_data_type).encode(), "text/plain")
        )
        project_id = (
            self.project_id
            if isinstance(self.project_id, Unset)
            else (None, str(self.project_id).encode(), "text/plain")
        )
        file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_tuple()

        update = self.update if isinstance(self.update, Unset) else (None, str(self.update).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update(
            {
                "name": name,
                "requires_scenario_input": requires_scenario_input,
                "requires_scenario_result": requires_scenario_result,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if output_data_type is not UNSET:
            field_dict["output_data_type"] = output_data_type
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if file is not UNSET:
            field_dict["file"] = file
        if update is not UNSET:
            field_dict["update"] = update

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        requires_scenario_input = d.pop("requires_scenario_input")

        requires_scenario_result = d.pop("requires_scenario_result")

        description = d.pop("description", UNSET)

        output_data_type = d.pop("output_data_type", UNSET)

        project_id = d.pop("project_id", UNSET)

        _file = d.pop("file", UNSET)
        file: Union[Unset, File]
        if isinstance(_file, Unset):
            file = UNSET
        else:
            file = File(payload=BytesIO(_file))

        update = d.pop("update", UNSET)

        body_check_upload_v0_check_upload_post = cls(
            name=name,
            requires_scenario_input=requires_scenario_input,
            requires_scenario_result=requires_scenario_result,
            description=description,
            output_data_type=output_data_type,
            project_id=project_id,
            file=file,
            update=update,
        )

        body_check_upload_v0_check_upload_post.additional_properties = d
        return body_check_upload_v0_check_upload_post

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
