from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CompareTestRunsPayload")


@_attrs_define
class CompareTestRunsPayload:
    """
    Attributes:
        control_test_run_id (None | Unset | UUID): ID of the control (baseline) test run
        variant_test_run_id (None | Unset | UUID): ID of the variant (candidate) test run
        alpha (float | None | Unset): Significance threshold for statistical tests
        include_scenarios (bool | None | Unset): When False, skip building paired scenario data to reduce response size
            Default: True.
    """

    control_test_run_id: None | Unset | UUID = UNSET
    variant_test_run_id: None | Unset | UUID = UNSET
    alpha: float | None | Unset = UNSET
    include_scenarios: bool | None | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        alpha: float | None | Unset
        if isinstance(self.alpha, Unset):
            alpha = UNSET
        else:
            alpha = self.alpha

        include_scenarios: bool | None | Unset
        if isinstance(self.include_scenarios, Unset):
            include_scenarios = UNSET
        else:
            include_scenarios = self.include_scenarios

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if control_test_run_id is not UNSET:
            field_dict["control_test_run_id"] = control_test_run_id
        if variant_test_run_id is not UNSET:
            field_dict["variant_test_run_id"] = variant_test_run_id
        if alpha is not UNSET:
            field_dict["alpha"] = alpha
        if include_scenarios is not UNSET:
            field_dict["include_scenarios"] = include_scenarios

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

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

        def _parse_alpha(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        alpha = _parse_alpha(d.pop("alpha", UNSET))

        def _parse_include_scenarios(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        include_scenarios = _parse_include_scenarios(d.pop("include_scenarios", UNSET))

        compare_test_runs_payload = cls(
            control_test_run_id=control_test_run_id,
            variant_test_run_id=variant_test_run_id,
            alpha=alpha,
            include_scenarios=include_scenarios,
        )

        compare_test_runs_payload.additional_properties = d
        return compare_test_runs_payload

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
