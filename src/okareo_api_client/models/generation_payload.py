from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GenerationPayload")


@_attrs_define
class GenerationPayload:
    """
    Attributes:
        view (str):
        json_schema (Union[Unset, str]):
        return_results (Union[Unset, bool]):
    """

    view: str
    json_schema: Union[Unset, str] = UNSET
    return_results: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        view = self.view
        json_schema = self.json_schema
        return_results = self.return_results

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "view": view,
            }
        )
        if json_schema is not UNSET:
            field_dict["json_schema"] = json_schema
        if return_results is not UNSET:
            field_dict["return_results"] = return_results

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        view = d.pop("view")

        json_schema = d.pop("json_schema", UNSET)

        return_results = d.pop("return_results", UNSET)

        generation_payload = cls(
            view=view,
            json_schema=json_schema,
            return_results=return_results,
        )

        generation_payload.additional_properties = d
        return generation_payload

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
