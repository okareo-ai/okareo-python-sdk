from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatapointTagsSchema")


@_attrs_define
class DatapointTagsSchema:
    """
    Attributes:
        tags (Union[Unset, List[str]]): Tags are strings that can be used to filter datapoints in the Okareo app
        resolved (Union[Unset, bool]): If the datapoint is resolved or not
    """

    tags: Union[Unset, List[str]] = UNSET
    resolved: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        resolved = self.resolved

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tags is not UNSET:
            field_dict["tags"] = tags
        if resolved is not UNSET:
            field_dict["resolved"] = resolved

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tags = cast(List[str], d.pop("tags", UNSET))

        resolved = d.pop("resolved", UNSET)

        datapoint_tags_schema = cls(
            tags=tags,
            resolved=resolved,
        )

        datapoint_tags_schema.additional_properties = d
        return datapoint_tags_schema

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
