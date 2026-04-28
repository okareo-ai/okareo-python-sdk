from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SampleCount")


@_attrs_define
class SampleCount:
    """
    Attributes:
        control (int | Unset):  Default: 0.
        variant (int | Unset):  Default: 0.
        total (int | Unset):  Default: 0.
    """

    control: int | Unset = 0
    variant: int | Unset = 0
    total: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        control = self.control

        variant = self.variant

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if control is not UNSET:
            field_dict["control"] = control
        if variant is not UNSET:
            field_dict["variant"] = variant
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        control = d.pop("control", UNSET)

        variant = d.pop("variant", UNSET)

        total = d.pop("total", UNSET)

        sample_count = cls(
            control=control,
            variant=variant,
            total=total,
        )

        sample_count.additional_properties = d
        return sample_count

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
