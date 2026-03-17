from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scenario_comparison_item import ScenarioComparisonItem
    from ..models.statistical_tests import StatisticalTests


T = TypeVar("T", bound="CompareTestRunsResponse")


@_attrs_define
class CompareTestRunsResponse:
    """
    Attributes:
        test_run_type (str):
        control_test_run_id (None | Unset | UUID):
        variant_test_run_id (None | Unset | UUID):
        scenarios (list[ScenarioComparisonItem] | Unset):
        statistical_tests (None | StatisticalTests | Unset):
    """

    test_run_type: str
    control_test_run_id: None | Unset | UUID = UNSET
    variant_test_run_id: None | Unset | UUID = UNSET
    scenarios: list[ScenarioComparisonItem] | Unset = UNSET
    statistical_tests: None | StatisticalTests | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.statistical_tests import StatisticalTests

        test_run_type = self.test_run_type

        control_test_run_id: None | str | Unset
        if isinstance(self.control_test_run_id, Unset):
            control_test_run_id = UNSET
        elif isinstance(self.control_test_run_id, UUID):
            control_test_run_id = str(self.control_test_run_id)
        else:
            control_test_run_id = self.control_test_run_id

        variant_test_run_id: None | str | Unset
        if isinstance(self.variant_test_run_id, Unset):
            variant_test_run_id = UNSET
        elif isinstance(self.variant_test_run_id, UUID):
            variant_test_run_id = str(self.variant_test_run_id)
        else:
            variant_test_run_id = self.variant_test_run_id

        scenarios: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.scenarios, Unset):
            scenarios = []
            for scenarios_item_data in self.scenarios:
                scenarios_item = scenarios_item_data.to_dict()
                scenarios.append(scenarios_item)

        statistical_tests: dict[str, Any] | None | Unset
        if isinstance(self.statistical_tests, Unset):
            statistical_tests = UNSET
        elif isinstance(self.statistical_tests, StatisticalTests):
            statistical_tests = self.statistical_tests.to_dict()
        else:
            statistical_tests = self.statistical_tests

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_run_type": test_run_type,
            }
        )
        if control_test_run_id is not UNSET:
            field_dict["control_test_run_id"] = control_test_run_id
        if variant_test_run_id is not UNSET:
            field_dict["variant_test_run_id"] = variant_test_run_id
        if scenarios is not UNSET:
            field_dict["scenarios"] = scenarios
        if statistical_tests is not UNSET:
            field_dict["statistical_tests"] = statistical_tests

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scenario_comparison_item import ScenarioComparisonItem
        from ..models.statistical_tests import StatisticalTests

        d = dict(src_dict)
        test_run_type = d.pop("test_run_type")

        def _parse_control_test_run_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                control_test_run_id_type_0 = UUID(data)

                return control_test_run_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        control_test_run_id = _parse_control_test_run_id(d.pop("control_test_run_id", UNSET))

        def _parse_variant_test_run_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                variant_test_run_id_type_0 = UUID(data)

                return variant_test_run_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        variant_test_run_id = _parse_variant_test_run_id(d.pop("variant_test_run_id", UNSET))

        _scenarios = d.pop("scenarios", UNSET)
        scenarios: list[ScenarioComparisonItem] | Unset = UNSET
        if _scenarios is not UNSET:
            scenarios = []
            for scenarios_item_data in _scenarios:
                scenarios_item = ScenarioComparisonItem.from_dict(scenarios_item_data)

                scenarios.append(scenarios_item)

        def _parse_statistical_tests(data: object) -> None | StatisticalTests | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                statistical_tests_type_0 = StatisticalTests.from_dict(data)

                return statistical_tests_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | StatisticalTests | Unset, data)

        statistical_tests = _parse_statistical_tests(d.pop("statistical_tests", UNSET))

        compare_test_runs_response = cls(
            test_run_type=test_run_type,
            control_test_run_id=control_test_run_id,
            variant_test_run_id=variant_test_run_id,
            scenarios=scenarios,
            statistical_tests=statistical_tests,
        )

        compare_test_runs_response.additional_properties = d
        return compare_test_runs_response

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
