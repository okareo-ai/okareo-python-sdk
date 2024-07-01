from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

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
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        check_config (Union[Unset, CheckCreateUpdateSchemaCheckConfig]):
        project_id (Union[Unset, str]): ID of the project
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    check_config: Union[Unset, "CheckCreateUpdateSchemaCheckConfig"] = UNSET
    project_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        check_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.check_config, Unset):
            check_config = self.check_config.to_dict()

        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
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
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.check_create_update_schema_check_config import CheckCreateUpdateSchemaCheckConfig

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _check_config = d.pop("check_config", UNSET)
        check_config: Union[Unset, CheckCreateUpdateSchemaCheckConfig]
        if isinstance(_check_config, Unset):
            check_config = UNSET
        else:
            check_config = CheckCreateUpdateSchemaCheckConfig.from_dict(_check_config)

        project_id = d.pop("project_id", UNSET)

        check_create_update_schema = cls(
            name=name,
            description=description,
            check_config=check_config,
            project_id=project_id,
        )

        check_create_update_schema.additional_properties = d
        return check_create_update_schema

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
