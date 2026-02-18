from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.check_create_update_schema_check_config import CheckCreateUpdateSchemaCheckConfig


T = TypeVar("T", bound="CheckCreateUpdateSchema")


@_attrs_define
class CheckCreateUpdateSchema:
    """
    Attributes:
        check_id (None | Unset | UUID): When provided, update existing check by ID (allows name change)
        name (str | Unset):
        description (str | Unset):
        check_config (CheckCreateUpdateSchemaCheckConfig | Unset):
        project_id (None | Unset | UUID): ID of the project
    """

    check_id: None | Unset | UUID = UNSET
    name: str | Unset = UNSET
    description: str | Unset = UNSET
    check_config: CheckCreateUpdateSchemaCheckConfig | Unset = UNSET
    project_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        check_id: None | str | Unset
        if isinstance(self.check_id, Unset):
            check_id = UNSET
        elif isinstance(self.check_id, UUID):
            check_id = str(self.check_id)
        else:
            check_id = self.check_id

        name = self.name

        description = self.description

        check_config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.check_config, Unset):
            check_config = self.check_config.to_dict()

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if check_id is not UNSET:
            field_dict["check_id"] = check_id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if check_config is not UNSET:
            field_dict["check_config"] = check_config
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.check_create_update_schema_check_config import CheckCreateUpdateSchemaCheckConfig

        d = dict(src_dict)

        def _parse_check_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                check_id_type_0 = UUID(data)

                return check_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        check_id = _parse_check_id(d.pop("check_id", UNSET))

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _check_config = d.pop("check_config", UNSET)
        check_config: CheckCreateUpdateSchemaCheckConfig | Unset
        if isinstance(_check_config, Unset):
            check_config = UNSET
        else:
            check_config = CheckCreateUpdateSchemaCheckConfig.from_dict(_check_config)

        def _parse_project_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        check_create_update_schema = cls(
            check_id=check_id,
            name=name,
            description=description,
            check_config=check_config,
            project_id=project_id,
        )

        check_create_update_schema.additional_properties = d
        return check_create_update_schema

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
