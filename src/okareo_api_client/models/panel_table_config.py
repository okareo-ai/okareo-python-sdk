from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.panel_table_config_mode import PanelTableConfigMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="PanelTableConfig")


@_attrs_define
class PanelTableConfig:
    """
    Attributes:
        mode (PanelTableConfigMode | Unset):  Default: PanelTableConfigMode.FLAT.
        row_dimensions (list[str] | Unset):
        column_dimension (None | str | Unset):
        value_measure (None | str | Unset):
    """

    mode: PanelTableConfigMode | Unset = PanelTableConfigMode.FLAT
    row_dimensions: list[str] | Unset = UNSET
    column_dimension: None | str | Unset = UNSET
    value_measure: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        row_dimensions: list[str] | Unset = UNSET
        if not isinstance(self.row_dimensions, Unset):
            row_dimensions = self.row_dimensions

        column_dimension: None | str | Unset
        if isinstance(self.column_dimension, Unset):
            column_dimension = UNSET
        else:
            column_dimension = self.column_dimension

        value_measure: None | str | Unset
        if isinstance(self.value_measure, Unset):
            value_measure = UNSET
        else:
            value_measure = self.value_measure

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mode is not UNSET:
            field_dict["mode"] = mode
        if row_dimensions is not UNSET:
            field_dict["row_dimensions"] = row_dimensions
        if column_dimension is not UNSET:
            field_dict["column_dimension"] = column_dimension
        if value_measure is not UNSET:
            field_dict["value_measure"] = value_measure

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _mode = d.pop("mode", UNSET)
        mode: PanelTableConfigMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = PanelTableConfigMode(_mode)

        row_dimensions = cast(list[str], d.pop("row_dimensions", UNSET))

        def _parse_column_dimension(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        column_dimension = _parse_column_dimension(d.pop("column_dimension", UNSET))

        def _parse_value_measure(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        value_measure = _parse_value_measure(d.pop("value_measure", UNSET))

        panel_table_config = cls(
            mode=mode,
            row_dimensions=row_dimensions,
            column_dimension=column_dimension,
            value_measure=value_measure,
        )

        panel_table_config.additional_properties = d
        return panel_table_config

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
