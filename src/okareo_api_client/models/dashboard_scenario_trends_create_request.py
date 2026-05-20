from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.dashboard_scenario_trends_create_request_granularity import (
    DashboardScenarioTrendsCreateRequestGranularity,
)
from ..models.time_range import TimeRange
from ..types import UNSET, Unset

T = TypeVar("T", bound="DashboardScenarioTrendsCreateRequest")


@_attrs_define
class DashboardScenarioTrendsCreateRequest:
    """
    Attributes:
        name (str):
        scenario_id (UUID):
        check_ids (list[UUID]):
        description (None | str | Unset):
        time_range (TimeRange | Unset):
        granularity (DashboardScenarioTrendsCreateRequestGranularity | Unset):  Default:
            DashboardScenarioTrendsCreateRequestGranularity.DAY.
    """

    name: str
    scenario_id: UUID
    check_ids: list[UUID]
    description: None | str | Unset = UNSET
    time_range: TimeRange | Unset = UNSET
    granularity: DashboardScenarioTrendsCreateRequestGranularity | Unset = (
        DashboardScenarioTrendsCreateRequestGranularity.DAY
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        scenario_id = str(self.scenario_id)

        check_ids = []
        for check_ids_item_data in self.check_ids:
            check_ids_item = str(check_ids_item_data)
            check_ids.append(check_ids_item)

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        time_range: str | Unset = UNSET
        if not isinstance(self.time_range, Unset):
            time_range = self.time_range.value

        granularity: str | Unset = UNSET
        if not isinstance(self.granularity, Unset):
            granularity = self.granularity.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "scenario_id": scenario_id,
                "check_ids": check_ids,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if time_range is not UNSET:
            field_dict["time_range"] = time_range
        if granularity is not UNSET:
            field_dict["granularity"] = granularity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        scenario_id = UUID(d.pop("scenario_id"))

        check_ids = []
        _check_ids = d.pop("check_ids")
        for check_ids_item_data in _check_ids:
            check_ids_item = UUID(check_ids_item_data)

            check_ids.append(check_ids_item)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _time_range = d.pop("time_range", UNSET)
        time_range: TimeRange | Unset
        if isinstance(_time_range, Unset):
            time_range = UNSET
        else:
            time_range = TimeRange(_time_range)

        _granularity = d.pop("granularity", UNSET)
        granularity: DashboardScenarioTrendsCreateRequestGranularity | Unset
        if isinstance(_granularity, Unset):
            granularity = UNSET
        else:
            granularity = DashboardScenarioTrendsCreateRequestGranularity(_granularity)

        dashboard_scenario_trends_create_request = cls(
            name=name,
            scenario_id=scenario_id,
            check_ids=check_ids,
            description=description,
            time_range=time_range,
            granularity=granularity,
        )

        dashboard_scenario_trends_create_request.additional_properties = d
        return dashboard_scenario_trends_create_request

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
