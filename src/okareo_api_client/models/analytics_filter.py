from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.comparison_operator import ComparisonOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnalyticsFilter")


@_attrs_define
class AnalyticsFilter:
    """
    Attributes:
        member (str):
        operator (ComparisonOperator | Unset):
        values (list[str | UUID] | Unset):
    """

    member: str
    operator: ComparisonOperator | Unset = UNSET
    values: list[str | UUID] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        member = self.member

        operator: str | Unset = UNSET
        if not isinstance(self.operator, Unset):
            operator = self.operator.value

        values: list[str] | Unset = UNSET
        if not isinstance(self.values, Unset):
            values = []
            for values_item_data in self.values:
                values_item: str
                if isinstance(values_item_data, UUID):
                    values_item = str(values_item_data)
                else:
                    values_item = values_item_data
                values.append(values_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "member": member,
            }
        )
        if operator is not UNSET:
            field_dict["operator"] = operator
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        member = d.pop("member")

        _operator = d.pop("operator", UNSET)
        operator: ComparisonOperator | Unset
        if isinstance(_operator, Unset):
            operator = UNSET
        else:
            operator = ComparisonOperator(_operator)

        _values = d.pop("values", UNSET)
        values: list[str | UUID] | Unset = UNSET
        if _values is not UNSET:
            values = []
            for values_item_data in _values:

                def _parse_values_item(data: object) -> str | UUID:
                    try:
                        if not isinstance(data, str):
                            raise TypeError()
                        values_item_type_1 = UUID(data)

                        return values_item_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    return cast(str | UUID, data)

                values_item = _parse_values_item(values_item_data)

                values.append(values_item)

        analytics_filter = cls(
            member=member,
            operator=operator,
            values=values,
        )

        analytics_filter.additional_properties = d
        return analytics_filter

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
