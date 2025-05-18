from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="BodyScenarioSetsUploadV0ScenarioSetsUploadPost")


@_attrs_define
class BodyScenarioSetsUploadV0ScenarioSetsUploadPost:
    """
    Attributes:
        name (str): Name of the Scenario Set
        project_id (Union[None, UUID, Unset]): Project ID or None for default project
        file (Union[File, None, Unset]):
    """

    name: str
    project_id: Union[None, UUID, Unset] = UNSET
    file: Union[File, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if file is not UNSET:
            field_dict["file"] = file

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        name = (None, str(self.name).encode(), "text/plain")

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

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "name": name,
            }
        )
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if file is not UNSET:
            field_dict["file"] = file

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

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

        body_scenario_sets_upload_v0_scenario_sets_upload_post = cls(
            name=name,
            project_id=project_id,
            file=file,
        )

        body_scenario_sets_upload_v0_scenario_sets_upload_post.additional_properties = d
        return body_scenario_sets_upload_v0_scenario_sets_upload_post

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
