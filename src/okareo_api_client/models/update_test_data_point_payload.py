from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateTestDataPointPayload")


@_attrs_define
class UpdateTestDataPointPayload:
    """
    Attributes:
        ids (Union[Unset, List[str]]): IDs of the datapoints to update
        tags (Union[Unset, List[List[str]]]): Tags are strings that can be used to filter test data points in the Okareo
            app
    """

    ids: Union[Unset, List[str]] = UNSET
    tags: Union[Unset, List[List[str]]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.ids, Unset):
            ids = self.ids

        tags: Union[Unset, List[List[str]]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data

                tags.append(tags_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ids is not UNSET:
            field_dict["ids"] = ids
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ids = cast(List[str], d.pop("ids", UNSET))

        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in _tags or []:
            tags_item = cast(List[str], tags_item_data)

            tags.append(tags_item)

        update_test_data_point_payload = cls(
            ids=ids,
            tags=tags,
        )

        update_test_data_point_payload.additional_properties = d
        return update_test_data_point_payload

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
