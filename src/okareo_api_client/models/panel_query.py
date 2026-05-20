from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.analytics_filter import AnalyticsFilter
    from ..models.panel_query_order import PanelQueryOrder
    from ..models.time_dimension import TimeDimension


T = TypeVar("T", bound="PanelQuery")


@_attrs_define
class PanelQuery:
    """Query template stored per panel.

    Does NOT include project_id.  ``time_range`` is injected by the frontend
    from the dashboard context and global time picker. Panels may include
    optional ``time_dimensions`` and ``order`` for Cube-style query shape.

        Attributes:
            measures (list[str]):
            cube (str | Unset):  Default: 'check_trend'.
            dimensions (list[str] | Unset):
            filters (list[AnalyticsFilter] | Unset):
            time_dimensions (list[TimeDimension] | Unset):
            order (PanelQueryOrder | Unset):
    """

    measures: list[str]
    cube: str | Unset = "check_trend"
    dimensions: list[str] | Unset = UNSET
    filters: list[AnalyticsFilter] | Unset = UNSET
    time_dimensions: list[TimeDimension] | Unset = UNSET
    order: PanelQueryOrder | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        measures = self.measures

        cube = self.cube

        dimensions: list[str] | Unset = UNSET
        if not isinstance(self.dimensions, Unset):
            dimensions = self.dimensions

        filters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()
                filters.append(filters_item)

        time_dimensions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.time_dimensions, Unset):
            time_dimensions = []
            for time_dimensions_item_data in self.time_dimensions:
                time_dimensions_item = time_dimensions_item_data.to_dict()
                time_dimensions.append(time_dimensions_item)

        order: dict[str, Any] | Unset = UNSET
        if not isinstance(self.order, Unset):
            order = self.order.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "measures": measures,
            }
        )
        if cube is not UNSET:
            field_dict["cube"] = cube
        if dimensions is not UNSET:
            field_dict["dimensions"] = dimensions
        if filters is not UNSET:
            field_dict["filters"] = filters
        if time_dimensions is not UNSET:
            field_dict["time_dimensions"] = time_dimensions
        if order is not UNSET:
            field_dict["order"] = order

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.analytics_filter import AnalyticsFilter
        from ..models.panel_query_order import PanelQueryOrder
        from ..models.time_dimension import TimeDimension

        d = dict(src_dict)
        measures = cast(list[str], d.pop("measures"))

        cube = d.pop("cube", UNSET)

        dimensions = cast(list[str], d.pop("dimensions", UNSET))

        _filters = d.pop("filters", UNSET)
        filters: list[AnalyticsFilter] | Unset = UNSET
        if _filters is not UNSET:
            filters = []
            for filters_item_data in _filters:
                filters_item = AnalyticsFilter.from_dict(filters_item_data)

                filters.append(filters_item)

        _time_dimensions = d.pop("time_dimensions", UNSET)
        time_dimensions: list[TimeDimension] | Unset = UNSET
        if _time_dimensions is not UNSET:
            time_dimensions = []
            for time_dimensions_item_data in _time_dimensions:
                time_dimensions_item = TimeDimension.from_dict(time_dimensions_item_data)

                time_dimensions.append(time_dimensions_item)

        _order = d.pop("order", UNSET)
        order: PanelQueryOrder | Unset
        if isinstance(_order, Unset):
            order = UNSET
        else:
            order = PanelQueryOrder.from_dict(_order)

        panel_query = cls(
            measures=measures,
            cube=cube,
            dimensions=dimensions,
            filters=filters,
            time_dimensions=time_dimensions,
            order=order,
        )

        panel_query.additional_properties = d
        return panel_query

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
