from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Metrics")


@_attrs_define
class Metrics:
    """Individual usage metrics.

    Attributes:
        voice_minutes (float): Total voice/audio minutes captured (completed sessions only)
        simulations (int): Count of completed test runs (all types: voice and non-voice)
        datapoints (int): Count of non-error datapoints (completed only)
        checks (int): Total check executions (from completed test runs and monitors)
    """

    voice_minutes: float
    simulations: int
    datapoints: int
    checks: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        voice_minutes = self.voice_minutes

        simulations = self.simulations

        datapoints = self.datapoints

        checks = self.checks

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
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
        voice_minutes = d.pop("voice_minutes")

        simulations = d.pop("simulations")

        datapoints = d.pop("datapoints")

        checks = d.pop("checks")

        metrics = cls(
            voice_minutes=voice_minutes,
            simulations=simulations,
            datapoints=datapoints,
            checks=checks,
        )

        metrics.additional_properties = d
        return metrics

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
