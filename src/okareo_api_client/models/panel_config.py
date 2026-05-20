from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.panel_config_chart_type import PanelConfigChartType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.panel_layout import PanelLayout
    from ..models.panel_query import PanelQuery
    from ..models.panel_table_config import PanelTableConfig


T = TypeVar("T", bound="PanelConfig")


@_attrs_define
class PanelConfig:
    """
    Attributes:
        title (str):
        chart_type (PanelConfigChartType):
        query (PanelQuery): Query template stored per panel.

            Does NOT include project_id.  ``time_range`` is injected by the frontend
            from the dashboard context and global time picker. Panels may include
            optional ``time_dimensions`` and ``order`` for Cube-style query shape.
        layout (PanelLayout):
        id (None | Unset | UUID):
        table_config (None | PanelTableConfig | Unset):
    """

    title: str
    chart_type: PanelConfigChartType
    query: PanelQuery
    layout: PanelLayout
    id: None | Unset | UUID = UNSET
    table_config: None | PanelTableConfig | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.panel_table_config import PanelTableConfig

        title = self.title

        chart_type = self.chart_type.value

        query = self.query.to_dict()

        layout = self.layout.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        elif isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        table_config: dict[str, Any] | None | Unset
        if isinstance(self.table_config, Unset):
            table_config = UNSET
        elif isinstance(self.table_config, PanelTableConfig):
            table_config = self.table_config.to_dict()
        else:
            table_config = self.table_config

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "chart_type": chart_type,
                "query": query,
                "layout": layout,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if table_config is not UNSET:
            field_dict["table_config"] = table_config

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.panel_layout import PanelLayout
        from ..models.panel_query import PanelQuery
        from ..models.panel_table_config import PanelTableConfig

        d = dict(src_dict)
        title = d.pop("title")

        chart_type = PanelConfigChartType(d.pop("chart_type"))

        query = PanelQuery.from_dict(d.pop("query"))

        layout = PanelLayout.from_dict(d.pop("layout"))

        def _parse_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                id_type_0 = UUID(data)

                return id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_table_config(data: object) -> None | PanelTableConfig | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                table_config_type_0 = PanelTableConfig.from_dict(data)

                return table_config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PanelTableConfig | Unset, data)

        table_config = _parse_table_config(d.pop("table_config", UNSET))

        panel_config = cls(
            title=title,
            chart_type=chart_type,
            query=query,
            layout=layout,
            id=id,
            table_config=table_config,
        )

        panel_config.additional_properties = d
        return panel_config

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
