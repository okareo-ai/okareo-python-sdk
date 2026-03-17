from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.full_data_point_item import FullDataPointItem


T = TypeVar("T", bound="ScenarioComparisonItem")


@_attrs_define
class ScenarioComparisonItem:
    """
    Attributes:
        scenario_data_point_id (UUID):
        scenario_input (Any | None | Unset):
        scenario_result (Any | None | Unset):
        control (list[FullDataPointItem] | Unset):
        variant (list[FullDataPointItem] | Unset):
    """

    scenario_data_point_id: UUID
    scenario_input: Any | None | Unset = UNSET
    scenario_result: Any | None | Unset = UNSET
    control: list[FullDataPointItem] | Unset = UNSET
    variant: list[FullDataPointItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scenario_data_point_id = str(self.scenario_data_point_id)

        scenario_input: Any | None | Unset
        if isinstance(self.scenario_input, Unset):
            scenario_input = UNSET
        else:
            scenario_input = self.scenario_input

        scenario_result: Any | None | Unset
        if isinstance(self.scenario_result, Unset):
            scenario_result = UNSET
        else:
            scenario_result = self.scenario_result

        control: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.control, Unset):
            control = []
            for control_item_data in self.control:
                control_item = control_item_data.to_dict()
                control.append(control_item)

        variant: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.variant, Unset):
            variant = []
            for variant_item_data in self.variant:
                variant_item = variant_item_data.to_dict()
                variant.append(variant_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scenario_data_point_id": scenario_data_point_id,
            }
        )
        if scenario_input is not UNSET:
            field_dict["scenario_input"] = scenario_input
        if scenario_result is not UNSET:
            field_dict["scenario_result"] = scenario_result
        if control is not UNSET:
            field_dict["control"] = control
        if variant is not UNSET:
            field_dict["variant"] = variant

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.full_data_point_item import FullDataPointItem

        d = dict(src_dict)
        scenario_data_point_id = UUID(d.pop("scenario_data_point_id"))

        def _parse_scenario_input(data: object) -> Any | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | None | Unset, data)

        scenario_input = _parse_scenario_input(d.pop("scenario_input", UNSET))

        def _parse_scenario_result(data: object) -> Any | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | None | Unset, data)

        scenario_result = _parse_scenario_result(d.pop("scenario_result", UNSET))

        _control = d.pop("control", UNSET)
        control: list[FullDataPointItem] | Unset = UNSET
        if _control is not UNSET:
            control = []
            for control_item_data in _control:
                control_item = FullDataPointItem.from_dict(control_item_data)

                control.append(control_item)

        _variant = d.pop("variant", UNSET)
        variant: list[FullDataPointItem] | Unset = UNSET
        if _variant is not UNSET:
            variant = []
            for variant_item_data in _variant:
                variant_item = FullDataPointItem.from_dict(variant_item_data)

                variant.append(variant_item)

        scenario_comparison_item = cls(
            scenario_data_point_id=scenario_data_point_id,
            scenario_input=scenario_input,
            scenario_result=scenario_result,
            control=control,
            variant=variant,
        )

        scenario_comparison_item.additional_properties = d
        return scenario_comparison_item

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
