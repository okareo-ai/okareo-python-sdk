from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeDimension")


@_attrs_define
class TimeDimension:
    """
    Attributes:
        dimension (str):
        date_range (list[str] | None | Unset):
        granularity (None | str | Unset):
    """

    dimension: str
    date_range: list[str] | None | Unset = UNSET
    granularity: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dimension = self.dimension

        date_range: list[str] | None | Unset
        if isinstance(self.date_range, Unset):
            date_range = UNSET
        elif isinstance(self.date_range, list):
            date_range = self.date_range

        else:
            date_range = self.date_range

        granularity: None | str | Unset
        if isinstance(self.granularity, Unset):
            granularity = UNSET
        else:
            granularity = self.granularity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dimension": dimension,
            }
        )
        if date_range is not UNSET:
            field_dict["date_range"] = date_range
        if granularity is not UNSET:
            field_dict["granularity"] = granularity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dimension = d.pop("dimension")

        def _parse_date_range(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                date_range_type_0 = cast(list[str], data)

                return date_range_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        date_range = _parse_date_range(d.pop("date_range", UNSET))

        def _parse_granularity(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        granularity = _parse_granularity(d.pop("granularity", UNSET))

        time_dimension = cls(
            dimension=dimension,
            date_range=date_range,
            granularity=granularity,
        )

        time_dimension.additional_properties = d
        return time_dimension

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
