from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.analytics_query_request_order_additional_property import AnalyticsQueryRequestOrderAdditionalProperty

T = TypeVar("T", bound="AnalyticsQueryRequestOrder")


@_attrs_define
class AnalyticsQueryRequestOrder:
    """ """

    additional_properties: dict[str, AnalyticsQueryRequestOrderAdditionalProperty] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        analytics_query_request_order = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = AnalyticsQueryRequestOrderAdditionalProperty(prop_dict)

            additional_properties[prop_name] = additional_property

        analytics_query_request_order.additional_properties = additional_properties
        return analytics_query_request_order

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> AnalyticsQueryRequestOrderAdditionalProperty:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: AnalyticsQueryRequestOrderAdditionalProperty) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
