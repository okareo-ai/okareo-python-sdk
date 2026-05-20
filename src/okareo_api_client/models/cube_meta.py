from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.dimension_meta_response import DimensionMetaResponse
    from ..models.measure_meta_response import MeasureMetaResponse


T = TypeVar("T", bound="CubeMeta")


@_attrs_define
class CubeMeta:
    """
    Attributes:
        measures (list[MeasureMetaResponse]):
        dimensions (list[DimensionMetaResponse]):
        time_dimensions (list[str]):
        granularities (list[str]):
    """

    measures: list[MeasureMetaResponse]
    dimensions: list[DimensionMetaResponse]
    time_dimensions: list[str]
    granularities: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        measures = []
        for measures_item_data in self.measures:
            measures_item = measures_item_data.to_dict()
            measures.append(measures_item)

        dimensions = []
        for dimensions_item_data in self.dimensions:
            dimensions_item = dimensions_item_data.to_dict()
            dimensions.append(dimensions_item)

        time_dimensions = self.time_dimensions

        granularities = self.granularities

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "measures": measures,
                "dimensions": dimensions,
                "time_dimensions": time_dimensions,
                "granularities": granularities,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dimension_meta_response import DimensionMetaResponse
        from ..models.measure_meta_response import MeasureMetaResponse

        d = dict(src_dict)
        measures = []
        _measures = d.pop("measures")
        for measures_item_data in _measures:
            measures_item = MeasureMetaResponse.from_dict(measures_item_data)

            measures.append(measures_item)

        dimensions = []
        _dimensions = d.pop("dimensions")
        for dimensions_item_data in _dimensions:
            dimensions_item = DimensionMetaResponse.from_dict(dimensions_item_data)

            dimensions.append(dimensions_item)

        time_dimensions = cast(list[str], d.pop("time_dimensions"))

        granularities = cast(list[str], d.pop("granularities"))

        cube_meta = cls(
            measures=measures,
            dimensions=dimensions,
            time_dimensions=time_dimensions,
            granularities=granularities,
        )

        cube_meta.additional_properties = d
        return cube_meta

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
