from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union
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
        project_id (Union[Unset, UUID]): Project ID or None for default project
        file (Union[Unset, File]):
    """

    name: str
    project_id: Union[Unset, UUID] = UNSET
    file: Union[Unset, File] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        project_id: Union[Unset, str] = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_tuple()

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

        project_id: Union[Unset, bytes] = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_tuple()

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

        _project_id = d.pop("project_id", UNSET)
        project_id: Union[Unset, UUID]
        if isinstance(_project_id, Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)

        _file = d.pop("file", UNSET)
        file: Union[Unset, File]
        if isinstance(_file, Unset):
            file = UNSET
        else:
            file = File(payload=BytesIO(_file))

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
