from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sample_count import SampleCount


T = TypeVar("T", bound="PassFailCheckResult")


@_attrs_define
class PassFailCheckResult:
    """
    Attributes:
        name (str):
        control_pass_rate (float):
        variant_pass_rate (float):
        improvements (int):
        regressions (int):
        concordant_pass (int):
        concordant_fail (int):
        p_value (float):
        p_value_adjusted (float):
        significant (bool):
        check_id (None | Unset | UUID):
        check_type (str | Unset):  Default: 'pass_fail'.
        chance_to_beat (float | None | Unset):
        ci_lower (float | None | Unset):
        ci_upper (float | None | Unset):
        risk_to_ship (float | None | Unset):
        risk_to_keep (float | None | Unset):
        sample_count (None | SampleCount | Unset):
    """

    name: str
    control_pass_rate: float
    variant_pass_rate: float
    improvements: int
    regressions: int
    concordant_pass: int
    concordant_fail: int
    p_value: float
    p_value_adjusted: float
    significant: bool
    check_id: None | Unset | UUID = UNSET
    check_type: str | Unset = "pass_fail"
    chance_to_beat: float | None | Unset = UNSET
    ci_lower: float | None | Unset = UNSET
    ci_upper: float | None | Unset = UNSET
    risk_to_ship: float | None | Unset = UNSET
    risk_to_keep: float | None | Unset = UNSET
    sample_count: None | SampleCount | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.sample_count import SampleCount

        name = self.name

        control_pass_rate = self.control_pass_rate

        variant_pass_rate = self.variant_pass_rate

        improvements = self.improvements

        regressions = self.regressions

        concordant_pass = self.concordant_pass

        concordant_fail = self.concordant_fail

        p_value = self.p_value

        p_value_adjusted = self.p_value_adjusted

        significant = self.significant

        check_id: None | str | Unset
        if isinstance(self.check_id, Unset):
            check_id = UNSET
        elif isinstance(self.check_id, UUID):
            check_id = str(self.check_id)
        else:
            check_id = self.check_id

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

        sample_count: dict[str, Any] | None | Unset
        if isinstance(self.sample_count, Unset):
            sample_count = UNSET
        elif isinstance(self.sample_count, SampleCount):
            sample_count = self.sample_count.to_dict()
        else:
            sample_count = self.sample_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "control_pass_rate": control_pass_rate,
                "variant_pass_rate": variant_pass_rate,
                "improvements": improvements,
                "regressions": regressions,
                "concordant_pass": concordant_pass,
                "concordant_fail": concordant_fail,
                "p_value": p_value,
                "p_value_adjusted": p_value_adjusted,
                "significant": significant,
            }
        )
        if check_id is not UNSET:
            field_dict["check_id"] = check_id
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
        if sample_count is not UNSET:
            field_dict["sample_count"] = sample_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sample_count import SampleCount

        d = dict(src_dict)
        name = d.pop("name")

        control_pass_rate = d.pop("control_pass_rate")

        variant_pass_rate = d.pop("variant_pass_rate")

        improvements = d.pop("improvements")

        regressions = d.pop("regressions")

        concordant_pass = d.pop("concordant_pass")

        concordant_fail = d.pop("concordant_fail")

        p_value = d.pop("p_value")

        p_value_adjusted = d.pop("p_value_adjusted")

        significant = d.pop("significant")

        def _parse_check_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                check_id_type_0 = UUID(data)

                return check_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        check_id = _parse_check_id(d.pop("check_id", UNSET))

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

        def _parse_sample_count(data: object) -> None | SampleCount | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sample_count_type_0 = SampleCount.from_dict(data)

                return sample_count_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SampleCount | Unset, data)

        sample_count = _parse_sample_count(d.pop("sample_count", UNSET))

        pass_fail_check_result = cls(
            name=name,
            control_pass_rate=control_pass_rate,
            variant_pass_rate=variant_pass_rate,
            improvements=improvements,
            regressions=regressions,
            concordant_pass=concordant_pass,
            concordant_fail=concordant_fail,
            p_value=p_value,
            p_value_adjusted=p_value_adjusted,
            significant=significant,
            check_id=check_id,
            check_type=check_type,
            chance_to_beat=chance_to_beat,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            risk_to_ship=risk_to_ship,
            risk_to_keep=risk_to_keep,
            sample_count=sample_count,
        )

        pass_fail_check_result.additional_properties = d
        return pass_fail_check_result

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
