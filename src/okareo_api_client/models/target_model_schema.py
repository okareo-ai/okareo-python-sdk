from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.target_model_schema_target import TargetModelSchemaTarget


T = TypeVar("T", bound="TargetModelSchema")


@_attrs_define
class TargetModelSchema:
    """
    Attributes:
        name (str): Name of the target model
        target (TargetModelSchemaTarget): Parameters for the target model
        id (Union[Unset, str]): ID of the target model
    """

    name: str
    target: "TargetModelSchemaTarget"
    id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        target = self.target.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "target": target,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.target_model_schema_target import TargetModelSchemaTarget

        d = src_dict.copy()
        name = d.pop("name")

        target = TargetModelSchemaTarget.from_dict(d.pop("target"))

        id = d.pop("id", UNSET)

        target_model_schema = cls(
            name=name,
            target=target,
            id=id,
        )

        target_model_schema.additional_properties = d
        return target_model_schema

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
