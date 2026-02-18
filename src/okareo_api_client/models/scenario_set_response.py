from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scenario_data_poin_response import ScenarioDataPoinResponse
    from ..models.seed_data import SeedData


T = TypeVar("T", bound="ScenarioSetResponse")


@_attrs_define
class ScenarioSetResponse:
    """
    Attributes:
        project_id (UUID):
        time_created (datetime.datetime):
        type_ (str):
        scenario_id (None | Unset | UUID):
        tags (list[str] | None | Unset):
        name (None | str | Unset):
        seed_data (list[SeedData] | None | Unset):
        scenario_data (list[ScenarioDataPoinResponse] | None | Unset):
        failed_data (list[ScenarioDataPoinResponse] | None | Unset):
        scenario_count (int | None | Unset):  Default: 0.
        scenario_input (list[str] | None | Unset):
        app_link (str | Unset): This URL links to the Okareo webpage for this scenario set Default: ''.
        warning (None | str | Unset):
    """

    project_id: UUID
    time_created: datetime.datetime
    type_: str
    scenario_id: None | Unset | UUID = UNSET
    tags: list[str] | None | Unset = UNSET
    name: None | str | Unset = UNSET
    seed_data: list[SeedData] | None | Unset = UNSET
    scenario_data: list[ScenarioDataPoinResponse] | None | Unset = UNSET
    failed_data: list[ScenarioDataPoinResponse] | None | Unset = UNSET
    scenario_count: int | None | Unset = 0
    scenario_input: list[str] | None | Unset = UNSET
    app_link: str | Unset = ""
    warning: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        time_created = self.time_created.isoformat()

        type_ = self.type_

        scenario_id: None | str | Unset
        if isinstance(self.scenario_id, Unset):
            scenario_id = UNSET
        elif isinstance(self.scenario_id, UUID):
            scenario_id = str(self.scenario_id)
        else:
            scenario_id = self.scenario_id

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        seed_data: list[dict[str, Any]] | None | Unset
        if isinstance(self.seed_data, Unset):
            seed_data = UNSET
        elif isinstance(self.seed_data, list):
            seed_data = []
            for seed_data_type_0_item_data in self.seed_data:
                seed_data_type_0_item = seed_data_type_0_item_data.to_dict()
                seed_data.append(seed_data_type_0_item)

        else:
            seed_data = self.seed_data

        scenario_data: list[dict[str, Any]] | None | Unset
        if isinstance(self.scenario_data, Unset):
            scenario_data = UNSET
        elif isinstance(self.scenario_data, list):
            scenario_data = []
            for scenario_data_type_0_item_data in self.scenario_data:
                scenario_data_type_0_item = scenario_data_type_0_item_data.to_dict()
                scenario_data.append(scenario_data_type_0_item)

        else:
            scenario_data = self.scenario_data

        failed_data: list[dict[str, Any]] | None | Unset
        if isinstance(self.failed_data, Unset):
            failed_data = UNSET
        elif isinstance(self.failed_data, list):
            failed_data = []
            for failed_data_type_0_item_data in self.failed_data:
                failed_data_type_0_item = failed_data_type_0_item_data.to_dict()
                failed_data.append(failed_data_type_0_item)

        else:
            failed_data = self.failed_data

        scenario_count: int | None | Unset
        if isinstance(self.scenario_count, Unset):
            scenario_count = UNSET
        else:
            scenario_count = self.scenario_count

        scenario_input: list[str] | None | Unset
        if isinstance(self.scenario_input, Unset):
            scenario_input = UNSET
        elif isinstance(self.scenario_input, list):
            scenario_input = self.scenario_input

        else:
            scenario_input = self.scenario_input

        app_link = self.app_link

        warning: None | str | Unset
        if isinstance(self.warning, Unset):
            warning = UNSET
        else:
            warning = self.warning

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "time_created": time_created,
                "type": type_,
            }
        )
        if scenario_id is not UNSET:
            field_dict["scenario_id"] = scenario_id
        if tags is not UNSET:
            field_dict["tags"] = tags
        if name is not UNSET:
            field_dict["name"] = name
        if seed_data is not UNSET:
            field_dict["seed_data"] = seed_data
        if scenario_data is not UNSET:
            field_dict["scenario_data"] = scenario_data
        if failed_data is not UNSET:
            field_dict["failed_data"] = failed_data
        if scenario_count is not UNSET:
            field_dict["scenario_count"] = scenario_count
        if scenario_input is not UNSET:
            field_dict["scenario_input"] = scenario_input
        if app_link is not UNSET:
            field_dict["app_link"] = app_link
        if warning is not UNSET:
            field_dict["warning"] = warning

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scenario_data_poin_response import ScenarioDataPoinResponse
        from ..models.seed_data import SeedData

        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))

        time_created = isoparse(d.pop("time_created"))

        type_ = d.pop("type")

        def _parse_scenario_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scenario_id_type_0 = UUID(data)

                return scenario_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        scenario_id = _parse_scenario_id(d.pop("scenario_id", UNSET))

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_seed_data(data: object) -> list[SeedData] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                seed_data_type_0 = []
                _seed_data_type_0 = data
                for seed_data_type_0_item_data in _seed_data_type_0:
                    seed_data_type_0_item = SeedData.from_dict(seed_data_type_0_item_data)

                    seed_data_type_0.append(seed_data_type_0_item)

                return seed_data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[SeedData] | None | Unset, data)

        seed_data = _parse_seed_data(d.pop("seed_data", UNSET))

        def _parse_scenario_data(data: object) -> list[ScenarioDataPoinResponse] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scenario_data_type_0 = []
                _scenario_data_type_0 = data
                for scenario_data_type_0_item_data in _scenario_data_type_0:
                    scenario_data_type_0_item = ScenarioDataPoinResponse.from_dict(scenario_data_type_0_item_data)

                    scenario_data_type_0.append(scenario_data_type_0_item)

                return scenario_data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ScenarioDataPoinResponse] | None | Unset, data)

        scenario_data = _parse_scenario_data(d.pop("scenario_data", UNSET))

        def _parse_failed_data(data: object) -> list[ScenarioDataPoinResponse] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                failed_data_type_0 = []
                _failed_data_type_0 = data
                for failed_data_type_0_item_data in _failed_data_type_0:
                    failed_data_type_0_item = ScenarioDataPoinResponse.from_dict(failed_data_type_0_item_data)

                    failed_data_type_0.append(failed_data_type_0_item)

                return failed_data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ScenarioDataPoinResponse] | None | Unset, data)

        failed_data = _parse_failed_data(d.pop("failed_data", UNSET))

        def _parse_scenario_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        scenario_count = _parse_scenario_count(d.pop("scenario_count", UNSET))

        def _parse_scenario_input(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scenario_input_type_0 = cast(list[str], data)

                return scenario_input_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        scenario_input = _parse_scenario_input(d.pop("scenario_input", UNSET))

        app_link = d.pop("app_link", UNSET)

        def _parse_warning(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        warning = _parse_warning(d.pop("warning", UNSET))

        scenario_set_response = cls(
            project_id=project_id,
            time_created=time_created,
            type_=type_,
            scenario_id=scenario_id,
            tags=tags,
            name=name,
            seed_data=seed_data,
            scenario_data=scenario_data,
            failed_data=failed_data,
            scenario_count=scenario_count,
            scenario_input=scenario_input,
            app_link=app_link,
            warning=warning,
        )

        scenario_set_response.additional_properties = d
        return scenario_set_response

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
