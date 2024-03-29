from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BodyEvaluatorDeleteV0EvaluatorEvaluatorIdDelete")


@_attrs_define
class BodyEvaluatorDeleteV0EvaluatorEvaluatorIdDelete:
    """
    Attributes:
        name (str): Name of the Evaluator to delete
    """

    name: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        body_evaluator_delete_v0_evaluator_evaluator_id_delete = cls(
            name=name,
        )

        body_evaluator_delete_v0_evaluator_evaluator_id_delete.additional_properties = d
        return body_evaluator_delete_v0_evaluator_evaluator_id_delete

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
