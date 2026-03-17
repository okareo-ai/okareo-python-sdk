from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pass_fail_check_result import PassFailCheckResult
    from ..models.score_check_result import ScoreCheckResult


T = TypeVar("T", bound="StatisticalTests")


@_attrs_define
class StatisticalTests:
    """
    Attributes:
        alpha (float):
        pass_fail_checks (list[PassFailCheckResult] | Unset):
        score_checks (list[ScoreCheckResult] | Unset):
        matched_scenario_count (int | Unset):  Default: 0.
        excluded_tie_count (int | Unset):  Default: 0.
        correction_method (str | Unset):  Default: 'benjamini-hochberg'.
    """

    alpha: float
    pass_fail_checks: list[PassFailCheckResult] | Unset = UNSET
    score_checks: list[ScoreCheckResult] | Unset = UNSET
    matched_scenario_count: int | Unset = 0
    excluded_tie_count: int | Unset = 0
    correction_method: str | Unset = "benjamini-hochberg"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alpha = self.alpha

        pass_fail_checks: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.pass_fail_checks, Unset):
            pass_fail_checks = []
            for pass_fail_checks_item_data in self.pass_fail_checks:
                pass_fail_checks_item = pass_fail_checks_item_data.to_dict()
                pass_fail_checks.append(pass_fail_checks_item)

        score_checks: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.score_checks, Unset):
            score_checks = []
            for score_checks_item_data in self.score_checks:
                score_checks_item = score_checks_item_data.to_dict()
                score_checks.append(score_checks_item)

        matched_scenario_count = self.matched_scenario_count

        excluded_tie_count = self.excluded_tie_count

        correction_method = self.correction_method

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "alpha": alpha,
            }
        )
        if pass_fail_checks is not UNSET:
            field_dict["pass_fail_checks"] = pass_fail_checks
        if score_checks is not UNSET:
            field_dict["score_checks"] = score_checks
        if matched_scenario_count is not UNSET:
            field_dict["matched_scenario_count"] = matched_scenario_count
        if excluded_tie_count is not UNSET:
            field_dict["excluded_tie_count"] = excluded_tie_count
        if correction_method is not UNSET:
            field_dict["correction_method"] = correction_method

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pass_fail_check_result import PassFailCheckResult
        from ..models.score_check_result import ScoreCheckResult

        d = dict(src_dict)
        alpha = d.pop("alpha")

        _pass_fail_checks = d.pop("pass_fail_checks", UNSET)
        pass_fail_checks: list[PassFailCheckResult] | Unset = UNSET
        if _pass_fail_checks is not UNSET:
            pass_fail_checks = []
            for pass_fail_checks_item_data in _pass_fail_checks:
                pass_fail_checks_item = PassFailCheckResult.from_dict(pass_fail_checks_item_data)

                pass_fail_checks.append(pass_fail_checks_item)

        _score_checks = d.pop("score_checks", UNSET)
        score_checks: list[ScoreCheckResult] | Unset = UNSET
        if _score_checks is not UNSET:
            score_checks = []
            for score_checks_item_data in _score_checks:
                score_checks_item = ScoreCheckResult.from_dict(score_checks_item_data)

                score_checks.append(score_checks_item)

        matched_scenario_count = d.pop("matched_scenario_count", UNSET)

        excluded_tie_count = d.pop("excluded_tie_count", UNSET)

        correction_method = d.pop("correction_method", UNSET)

        statistical_tests = cls(
            alpha=alpha,
            pass_fail_checks=pass_fail_checks,
            score_checks=score_checks,
            matched_scenario_count=matched_scenario_count,
            excluded_tie_count=excluded_tie_count,
            correction_method=correction_method,
        )

        statistical_tests.additional_properties = d
        return statistical_tests

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
