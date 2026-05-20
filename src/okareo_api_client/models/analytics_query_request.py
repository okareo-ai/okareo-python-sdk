from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.analytics_filter import AnalyticsFilter
    from ..models.analytics_query_request_order import AnalyticsQueryRequestOrder
    from ..models.time_dimension import TimeDimension


T = TypeVar("T", bound="AnalyticsQueryRequest")


@_attrs_define
class AnalyticsQueryRequest:
    """
    Attributes:
        project_id (UUID):
        measures (list[str]):
        cube (str | Unset):  Default: 'check_trend'.
        dimensions (list[str] | Unset):
        filters (list[AnalyticsFilter] | Unset):
        time_dimensions (list[TimeDimension] | Unset):
        time_range (None | str | Unset):
        order (AnalyticsQueryRequestOrder | Unset):
    """

    project_id: UUID
    measures: list[str]
    cube: str | Unset = "check_trend"
    dimensions: list[str] | Unset = UNSET
    filters: list[AnalyticsFilter] | Unset = UNSET
    time_dimensions: list[TimeDimension] | Unset = UNSET
    time_range: None | str | Unset = UNSET
    order: AnalyticsQueryRequestOrder | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

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

        time_range: None | str | Unset
        if isinstance(self.time_range, Unset):
            time_range = UNSET
        else:
            time_range = self.time_range

        order: dict[str, Any] | Unset = UNSET
        if not isinstance(self.order, Unset):
            order = self.order.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
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
        if time_range is not UNSET:
            field_dict["time_range"] = time_range
        if order is not UNSET:
            field_dict["order"] = order

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.analytics_filter import AnalyticsFilter
        from ..models.analytics_query_request_order import AnalyticsQueryRequestOrder
        from ..models.time_dimension import TimeDimension

        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))

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

        def _parse_time_range(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        time_range = _parse_time_range(d.pop("time_range", UNSET))

        _order = d.pop("order", UNSET)
        order: AnalyticsQueryRequestOrder | Unset
        if isinstance(_order, Unset):
            order = UNSET
        else:
            order = AnalyticsQueryRequestOrder.from_dict(_order)

        analytics_query_request = cls(
            project_id=project_id,
            measures=measures,
            cube=cube,
            dimensions=dimensions,
            filters=filters,
            time_dimensions=time_dimensions,
            time_range=time_range,
            order=order,
        )

        analytics_query_request.additional_properties = d
        return analytics_query_request

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
