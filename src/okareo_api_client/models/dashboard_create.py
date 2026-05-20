from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.time_range import TimeRange
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.panel_config import PanelConfig


T = TypeVar("T", bound="DashboardCreate")


@_attrs_define
class DashboardCreate:
    """
    Attributes:
        name (str):
        description (None | str | Unset):
        time_range (TimeRange | Unset):
        panels (list[PanelConfig] | Unset):
    """

    name: str
    description: None | str | Unset = UNSET
    time_range: TimeRange | Unset = UNSET
    panels: list[PanelConfig] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        time_range: str | Unset = UNSET
        if not isinstance(self.time_range, Unset):
            time_range = self.time_range.value

        panels: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.panels, Unset):
            panels = []
            for panels_item_data in self.panels:
                panels_item = panels_item_data.to_dict()
                panels.append(panels_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
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
        name = d.pop("name")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _time_range = d.pop("time_range", UNSET)
        time_range: TimeRange | Unset
        if isinstance(_time_range, Unset):
            time_range = UNSET
        else:
            time_range = TimeRange(_time_range)

        _panels = d.pop("panels", UNSET)
        panels: list[PanelConfig] | Unset = UNSET
        if _panels is not UNSET:
            panels = []
            for panels_item_data in _panels:
                panels_item = PanelConfig.from_dict(panels_item_data)

                panels.append(panels_item)

        dashboard_create = cls(
            name=name,
            description=description,
            time_range=time_range,
            panels=panels,
        )

        dashboard_create.additional_properties = d
        return dashboard_create

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
