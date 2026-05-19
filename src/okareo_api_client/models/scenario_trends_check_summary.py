from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScenarioTrendsCheckSummary")


@_attrs_define
class ScenarioTrendsCheckSummary:
    """
    Attributes:
        check_id (UUID):
        check_name (str):
        run_count (int):
        datapoint_count (int):
        latest_seen_at (datetime.datetime | None | Unset):
    """

    check_id: UUID
    check_name: str
    run_count: int
    datapoint_count: int
    latest_seen_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        check_id = str(self.check_id)

        check_name = self.check_name

        run_count = self.run_count

        datapoint_count = self.datapoint_count

        latest_seen_at: None | str | Unset
        if isinstance(self.latest_seen_at, Unset):
            latest_seen_at = UNSET
        elif isinstance(self.latest_seen_at, datetime.datetime):
            latest_seen_at = self.latest_seen_at.isoformat()
        else:
            latest_seen_at = self.latest_seen_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "check_id": check_id,
                "check_name": check_name,
                "run_count": run_count,
                "datapoint_count": datapoint_count,
            }
        )
        if latest_seen_at is not UNSET:
            field_dict["latest_seen_at"] = latest_seen_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        check_id = UUID(d.pop("check_id"))

        check_name = d.pop("check_name")

        run_count = d.pop("run_count")

        datapoint_count = d.pop("datapoint_count")

        def _parse_latest_seen_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                latest_seen_at_type_0 = isoparse(data)

                return latest_seen_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        latest_seen_at = _parse_latest_seen_at(d.pop("latest_seen_at", UNSET))

        scenario_trends_check_summary = cls(
            check_id=check_id,
            check_name=check_name,
            run_count=run_count,
            datapoint_count=datapoint_count,
            latest_seen_at=latest_seen_at,
        )

        scenario_trends_check_summary.additional_properties = d
        return scenario_trends_check_summary

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
