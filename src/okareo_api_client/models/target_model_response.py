from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.target_model_response_target import TargetModelResponseTarget


T = TypeVar("T", bound="TargetModelResponse")


@_attrs_define
class TargetModelResponse:
    """
    Attributes:
        id (str):
        name (str):
        target (TargetModelResponseTarget):
    """

    id: str
    name: str
    target: "TargetModelResponseTarget"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        target = self.target.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "target": target,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.target_model_response_target import TargetModelResponseTarget

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        target = TargetModelResponseTarget.from_dict(d.pop("target"))

        target_model_response = cls(
            id=id,
            name=name,
            target=target,
        )

        target_model_response.additional_properties = d
        return target_model_response

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
