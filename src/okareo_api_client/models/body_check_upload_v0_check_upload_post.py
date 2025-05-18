from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union, cast
from uuid import UUID

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
        output_data_type (Union[None, Unset, str]): Check output data type (i.e., bool, int, float)
        project_id (Union[None, UUID, Unset]): ID for the project
        file (Union[File, None, Unset]):
        update (Union[None, Unset, bool]): Update the check Default: False.
    """

    name: str
    requires_scenario_input: bool
    requires_scenario_result: bool
    description: Union[Unset, str] = "No description provided"
    output_data_type: Union[None, Unset, str] = UNSET
    project_id: Union[None, UUID, Unset] = UNSET
    file: Union[File, None, Unset] = UNSET
    update: Union[None, Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        requires_scenario_input = self.requires_scenario_input

        requires_scenario_result = self.requires_scenario_result

        description = self.description

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

        file: Union[FileJsonType, None, Unset]
        if isinstance(self.file, Unset):
            file = UNSET
        elif isinstance(self.file, File):
            file = self.file.to_tuple()

        else:
            file = self.file

        update: Union[None, Unset, bool]
        if isinstance(self.update, Unset):
            update = UNSET
        else:
            update = self.update

        field_dict: dict[str, Any] = {}
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

    def to_multipart(self) -> dict[str, Any]:
        name = (None, str(self.name).encode(), "text/plain")

        requires_scenario_input = (None, str(self.requires_scenario_input).encode(), "text/plain")

        requires_scenario_result = (None, str(self.requires_scenario_result).encode(), "text/plain")

        description = (
            self.description
            if isinstance(self.description, Unset)
            else (None, str(self.description).encode(), "text/plain")
        )

        output_data_type: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.output_data_type, Unset):
            output_data_type = UNSET
        elif isinstance(self.output_data_type, str):
            output_data_type = (None, str(self.output_data_type).encode(), "text/plain")
        else:
            output_data_type = (None, str(self.output_data_type).encode(), "text/plain")

        project_id: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = (None, str(self.project_id).encode(), "text/plain")

        file: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.file, Unset):
            file = UNSET
        elif isinstance(self.file, File):
            file = self.file.to_tuple()
        else:
            file = (None, str(self.file).encode(), "text/plain")

        update: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.update, Unset):
            update = UNSET
        elif isinstance(self.update, bool):
            update = (None, str(self.update).encode(), "text/plain")
        else:
            update = (None, str(self.update).encode(), "text/plain")

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        requires_scenario_input = d.pop("requires_scenario_input")

        requires_scenario_result = d.pop("requires_scenario_result")

        description = d.pop("description", UNSET)

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

        def _parse_file(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                file_type_0 = File(payload=BytesIO(data))

                return file_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        file = _parse_file(d.pop("file", UNSET))

        def _parse_update(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        update = _parse_update(d.pop("update", UNSET))

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
