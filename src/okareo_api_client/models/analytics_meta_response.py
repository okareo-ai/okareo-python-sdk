from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.analytics_meta_response_cubes import AnalyticsMetaResponseCubes


T = TypeVar("T", bound="AnalyticsMetaResponse")


@_attrs_define
class AnalyticsMetaResponse:
    """
    Attributes:
        cubes (AnalyticsMetaResponseCubes):
    """

    cubes: AnalyticsMetaResponseCubes
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cubes = self.cubes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cubes": cubes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.analytics_meta_response_cubes import AnalyticsMetaResponseCubes

        d = dict(src_dict)
        cubes = AnalyticsMetaResponseCubes.from_dict(d.pop("cubes"))

        analytics_meta_response = cls(
            cubes=cubes,
        )

        analytics_meta_response.additional_properties = d
        return analytics_meta_response

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
