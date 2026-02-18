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
    from ..models.seed_data import SeedData


T = TypeVar("T", bound="ScenarioSetUpdate")


@_attrs_define
class ScenarioSetUpdate:
    """
    Attributes:
        project_id (None | Unset | UUID): ID for the project
        time_created (datetime.datetime | None | Unset):
        type_ (None | str | Unset): Generation type of scenario
        tags (list[str] | None | Unset): Tags are strings that can be used to filter scenario sets in the Okareo app
        name (None | str | Unset): Name of the scenario set
        seed_data (list[SeedData] | None | Unset): Seed data is a list of dictionaries, each with an input and result
        scenario_input (list[str] | None | Unset):
    """

    project_id: None | Unset | UUID = UNSET
    time_created: datetime.datetime | None | Unset = UNSET
    type_: None | str | Unset = UNSET
    tags: list[str] | None | Unset = UNSET
    name: None | str | Unset = UNSET
    seed_data: list[SeedData] | None | Unset = UNSET
    scenario_input: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        time_created: None | str | Unset
        if isinstance(self.time_created, Unset):
            time_created = UNSET
        elif isinstance(self.time_created, datetime.datetime):
            time_created = self.time_created.isoformat()
        else:
            time_created = self.time_created

        type_: None | str | Unset
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

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

        scenario_input: list[str] | None | Unset
        if isinstance(self.scenario_input, Unset):
            scenario_input = UNSET
        elif isinstance(self.scenario_input, list):
            scenario_input = self.scenario_input

        else:
            scenario_input = self.scenario_input

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if time_created is not UNSET:
            field_dict["time_created"] = time_created
        if type_ is not UNSET:
            field_dict["type"] = type_
        if tags is not UNSET:
            field_dict["tags"] = tags
        if name is not UNSET:
            field_dict["name"] = name
        if seed_data is not UNSET:
            field_dict["seed_data"] = seed_data
        if scenario_input is not UNSET:
            field_dict["scenario_input"] = scenario_input

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.seed_data import SeedData

        d = dict(src_dict)

        def _parse_project_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_time_created(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                time_created_type_0 = isoparse(data)

                return time_created_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        time_created = _parse_time_created(d.pop("time_created", UNSET))

        def _parse_type_(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        type_ = _parse_type_(d.pop("type", UNSET))

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

        scenario_set_update = cls(
            project_id=project_id,
            time_created=time_created,
            type_=type_,
            tags=tags,
            name=name,
            seed_data=seed_data,
            scenario_input=scenario_input,
        )

        scenario_set_update.additional_properties = d
        return scenario_set_update

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
