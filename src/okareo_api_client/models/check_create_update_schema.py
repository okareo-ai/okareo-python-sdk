from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.check_create_update_schema_check_config_type_0 import CheckCreateUpdateSchemaCheckConfigType0


T = TypeVar("T", bound="CheckCreateUpdateSchema")


@_attrs_define
class CheckCreateUpdateSchema:
    """
    Attributes:
        name (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        check_config (Union['CheckCreateUpdateSchemaCheckConfigType0', None, Unset]):
        project_id (Union[None, UUID, Unset]): ID of the project
    """

    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    check_config: Union["CheckCreateUpdateSchemaCheckConfigType0", None, Unset] = UNSET
    project_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.check_create_update_schema_check_config_type_0 import CheckCreateUpdateSchemaCheckConfigType0

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

        check_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.check_config, Unset):
            check_config = UNSET
        elif isinstance(self.check_config, CheckCreateUpdateSchemaCheckConfigType0):
            check_config = self.check_config.to_dict()
        else:
            check_config = self.check_config

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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
        from ..models.check_create_update_schema_check_config_type_0 import CheckCreateUpdateSchemaCheckConfigType0

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

        def _parse_check_config(data: object) -> Union["CheckCreateUpdateSchemaCheckConfigType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                check_config_type_0 = CheckCreateUpdateSchemaCheckConfigType0.from_dict(data)

                return check_config_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CheckCreateUpdateSchemaCheckConfigType0", None, Unset], data)

        check_config = _parse_check_config(d.pop("check_config", UNSET))

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

        check_create_update_schema = cls(
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
