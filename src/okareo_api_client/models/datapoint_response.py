from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatapointResponse")


@_attrs_define
class DatapointResponse:
    """
    Attributes:
        id (UUID):
        project_id (Union[Unset, UUID]):
        mut_id (Union[Unset, UUID]):
    """

    id: UUID
    project_id: Union[Unset, UUID] = UNSET
    mut_id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id: Union[Unset, str] = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        mut_id: Union[Unset, str] = UNSET
        if not isinstance(self.mut_id, Unset):
            mut_id = str(self.mut_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if mut_id is not UNSET:
            field_dict["mut_id"] = mut_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        _project_id = d.pop("project_id", UNSET)
        project_id: Union[Unset, UUID]
        if isinstance(_project_id, Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)

        _mut_id = d.pop("mut_id", UNSET)
        mut_id: Union[Unset, UUID]
        if isinstance(_mut_id, Unset):
            mut_id = UNSET
        else:
            mut_id = UUID(_mut_id)

        datapoint_response = cls(
            id=id,
            project_id=project_id,
            mut_id=mut_id,
        )

        datapoint_response.additional_properties = d
        return datapoint_response

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
