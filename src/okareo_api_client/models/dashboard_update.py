from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.time_range import TimeRange
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.panel_config import PanelConfig


T = TypeVar("T", bound="DashboardUpdate")


@_attrs_define
class DashboardUpdate:
    """
    Attributes:
        name (None | str | Unset):
        description (None | str | Unset):
        time_range (None | TimeRange | Unset):
        panels (list[PanelConfig] | None | Unset):
    """

    name: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    time_range: None | TimeRange | Unset = UNSET
    panels: list[PanelConfig] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        time_range: None | str | Unset
        if isinstance(self.time_range, Unset):
            time_range = UNSET
        elif isinstance(self.time_range, TimeRange):
            time_range = self.time_range.value
        else:
            time_range = self.time_range

        panels: list[dict[str, Any]] | None | Unset
        if isinstance(self.panels, Unset):
            panels = UNSET
        elif isinstance(self.panels, list):
            panels = []
            for panels_type_0_item_data in self.panels:
                panels_type_0_item = panels_type_0_item_data.to_dict()
                panels.append(panels_type_0_item)

        else:
            panels = self.panels

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if time_range is not UNSET:
            field_dict["time_range"] = time_range
        if panels is not UNSET:
            field_dict["panels"] = panels

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.panel_config import PanelConfig

        d = dict(src_dict)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_time_range(data: object) -> None | TimeRange | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                time_range_type_0 = TimeRange(data)

                return time_range_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TimeRange | Unset, data)

        time_range = _parse_time_range(d.pop("time_range", UNSET))

        def _parse_panels(data: object) -> list[PanelConfig] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                panels_type_0 = []
                _panels_type_0 = data
                for panels_type_0_item_data in _panels_type_0:
                    panels_type_0_item = PanelConfig.from_dict(panels_type_0_item_data)

                    panels_type_0.append(panels_type_0_item)

                return panels_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PanelConfig] | None | Unset, data)

        panels = _parse_panels(d.pop("panels", UNSET))

        dashboard_update = cls(
            name=name,
            description=description,
            time_range=time_range,
            panels=panels,
        )

        dashboard_update.additional_properties = d
        return dashboard_update

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
