from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="MetricDetail")


@_attrs_define
class MetricDetail:
    """Metrics for a specific time period.

    Attributes:
        period_start (datetime.datetime): Start of this time period
        period_end (datetime.datetime): End of this time period
        voice_minutes (float): Voice minutes for this period
        simulations (int): Simulations for this period
        datapoints (int): Datapoints for this period
        checks (int): Checks for this period
    """

    period_start: datetime.datetime
    period_end: datetime.datetime
    voice_minutes: float
    simulations: int
    datapoints: int
    checks: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period_start = self.period_start.isoformat()

        period_end = self.period_end.isoformat()

        voice_minutes = self.voice_minutes

        simulations = self.simulations

        datapoints = self.datapoints

        checks = self.checks

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period_start": period_start,
                "period_end": period_end,
                "voice_minutes": voice_minutes,
                "simulations": simulations,
                "datapoints": datapoints,
                "checks": checks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period_start = isoparse(d.pop("period_start"))

        period_end = isoparse(d.pop("period_end"))

        voice_minutes = d.pop("voice_minutes")

        simulations = d.pop("simulations")

        datapoints = d.pop("datapoints")

        checks = d.pop("checks")

        metric_detail = cls(
            period_start=period_start,
            period_end=period_end,
            voice_minutes=voice_minutes,
            simulations=simulations,
            datapoints=datapoints,
            checks=checks,
        )

        metric_detail.additional_properties = d
        return metric_detail

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
