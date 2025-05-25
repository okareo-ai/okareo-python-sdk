from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateTestDataPointPayload")


@_attrs_define
class UpdateTestDataPointPayload:
    """
    Attributes:
        ids (Union[Unset, list[UUID]]): IDs of the datapoints to update
        tags (Union[Unset, list[list[str]]]): Tags are strings that can be used to filter test data points in the Okareo
            app
    """

    ids: Union[Unset, list[UUID]] = UNSET
    tags: Union[Unset, list[list[str]]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.ids, Unset):
            ids = []
            for ids_item_data in self.ids:
                ids_item = str(ids_item_data)
                ids.append(ids_item)

        tags: Union[Unset, list[list[str]]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data

                tags.append(tags_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ids is not UNSET:
            field_dict["ids"] = ids
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ids = []
        _ids = d.pop("ids", UNSET)
        for ids_item_data in _ids or []:
            ids_item = UUID(ids_item_data)

            ids.append(ids_item)

        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in _tags or []:
            tags_item = cast(list[str], tags_item_data)

            tags.append(tags_item)

        update_test_data_point_payload = cls(
            ids=ids,
            tags=tags,
        )

        update_test_data_point_payload.additional_properties = d
        return update_test_data_point_payload

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
