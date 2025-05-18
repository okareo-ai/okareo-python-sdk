from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
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
        project_id (Union[None, UUID, Unset]):
        mut_id (Union[None, UUID, Unset]):
    """

    id: UUID
    project_id: Union[None, UUID, Unset] = UNSET
    mut_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        mut_id: Union[None, Unset, str]
        if isinstance(self.mut_id, Unset):
            mut_id = UNSET
        elif isinstance(self.mut_id, UUID):
            mut_id = str(self.mut_id)
        else:
            mut_id = self.mut_id

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

        def _parse_mut_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mut_id_type_0 = UUID(data)

                return mut_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        mut_id = _parse_mut_id(d.pop("mut_id", UNSET))

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
