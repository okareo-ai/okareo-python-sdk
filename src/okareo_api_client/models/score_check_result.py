from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScoreCheckResult")


@_attrs_define
class ScoreCheckResult:
    """
    Attributes:
        name (str):
        control_summary (float):
        variant_summary (float):
        mean_diff (float):
        p_value (float):
        p_value_adjusted (float):
        significant (bool):
        check_type (str | Unset):  Default: 'score'.
        chance_to_beat (float | None | Unset):
        ci_lower (float | None | Unset):
        ci_upper (float | None | Unset):
        risk_to_ship (float | None | Unset):
        risk_to_keep (float | None | Unset):
    """

    name: str
    control_summary: float
    variant_summary: float
    mean_diff: float
    p_value: float
    p_value_adjusted: float
    significant: bool
    check_type: str | Unset = "score"
    chance_to_beat: float | None | Unset = UNSET
    ci_lower: float | None | Unset = UNSET
    ci_upper: float | None | Unset = UNSET
    risk_to_ship: float | None | Unset = UNSET
    risk_to_keep: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        control_summary = self.control_summary

        variant_summary = self.variant_summary

        mean_diff = self.mean_diff

        p_value = self.p_value

        p_value_adjusted = self.p_value_adjusted

        significant = self.significant

        check_type = self.check_type

        chance_to_beat: float | None | Unset
        if isinstance(self.chance_to_beat, Unset):
            chance_to_beat = UNSET
        else:
            chance_to_beat = self.chance_to_beat

        ci_lower: float | None | Unset
        if isinstance(self.ci_lower, Unset):
            ci_lower = UNSET
        else:
            ci_lower = self.ci_lower

        ci_upper: float | None | Unset
        if isinstance(self.ci_upper, Unset):
            ci_upper = UNSET
        else:
            ci_upper = self.ci_upper

        risk_to_ship: float | None | Unset
        if isinstance(self.risk_to_ship, Unset):
            risk_to_ship = UNSET
        else:
            risk_to_ship = self.risk_to_ship

        risk_to_keep: float | None | Unset
        if isinstance(self.risk_to_keep, Unset):
            risk_to_keep = UNSET
        else:
            risk_to_keep = self.risk_to_keep

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "control_summary": control_summary,
                "variant_summary": variant_summary,
                "mean_diff": mean_diff,
                "p_value": p_value,
                "p_value_adjusted": p_value_adjusted,
                "significant": significant,
            }
        )
        if check_type is not UNSET:
            field_dict["check_type"] = check_type
        if chance_to_beat is not UNSET:
            field_dict["chance_to_beat"] = chance_to_beat
        if ci_lower is not UNSET:
            field_dict["ci_lower"] = ci_lower
        if ci_upper is not UNSET:
            field_dict["ci_upper"] = ci_upper
        if risk_to_ship is not UNSET:
            field_dict["risk_to_ship"] = risk_to_ship
        if risk_to_keep is not UNSET:
            field_dict["risk_to_keep"] = risk_to_keep

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        control_summary = d.pop("control_summary")

        variant_summary = d.pop("variant_summary")

        mean_diff = d.pop("mean_diff")

        p_value = d.pop("p_value")

        p_value_adjusted = d.pop("p_value_adjusted")

        significant = d.pop("significant")

        check_type = d.pop("check_type", UNSET)

        def _parse_chance_to_beat(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        chance_to_beat = _parse_chance_to_beat(d.pop("chance_to_beat", UNSET))

        def _parse_ci_lower(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        ci_lower = _parse_ci_lower(d.pop("ci_lower", UNSET))

        def _parse_ci_upper(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        ci_upper = _parse_ci_upper(d.pop("ci_upper", UNSET))

        def _parse_risk_to_ship(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        risk_to_ship = _parse_risk_to_ship(d.pop("risk_to_ship", UNSET))

        def _parse_risk_to_keep(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        risk_to_keep = _parse_risk_to_keep(d.pop("risk_to_keep", UNSET))

        score_check_result = cls(
            name=name,
            control_summary=control_summary,
            variant_summary=variant_summary,
            mean_diff=mean_diff,
            p_value=p_value,
            p_value_adjusted=p_value_adjusted,
            significant=significant,
            check_type=check_type,
            chance_to_beat=chance_to_beat,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            risk_to_ship=risk_to_ship,
            risk_to_keep=risk_to_keep,
        )

        score_check_result.additional_properties = d
        return score_check_result

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
