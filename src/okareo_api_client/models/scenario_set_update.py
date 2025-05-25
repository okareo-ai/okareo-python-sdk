import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
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
        project_id (Union[Unset, UUID]): ID for the project
        time_created (Union[Unset, datetime.datetime]):
        type_ (Union[Unset, str]): Generation type of scenario
        tags (Union[Unset, list[str]]): Tags are strings that can be used to filter scenario sets in the Okareo app
        name (Union[Unset, str]): Name of the scenario set
        seed_data (Union[Unset, list['SeedData']]): Seed data is a list of dictionaries, each with an input and result
        scenario_input (Union[Unset, list[str]]):
    """

    project_id: Union[Unset, UUID] = UNSET
    time_created: Union[Unset, datetime.datetime] = UNSET
    type_: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    name: Union[Unset, str] = UNSET
    seed_data: Union[Unset, list["SeedData"]] = UNSET
    scenario_input: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id: Union[Unset, str] = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        time_created: Union[Unset, str] = UNSET
        if not isinstance(self.time_created, Unset):
            time_created = self.time_created.isoformat()

        type_ = self.type_

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        name = self.name

        seed_data: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.seed_data, Unset):
            seed_data = []
            for seed_data_item_data in self.seed_data:
                seed_data_item = seed_data_item_data.to_dict()
                seed_data.append(seed_data_item)

        scenario_input: Union[Unset, list[str]] = UNSET
        if not isinstance(self.scenario_input, Unset):
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
        _project_id = d.pop("project_id", UNSET)
        project_id: Union[Unset, UUID]
        if isinstance(_project_id, Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)

        _time_created = d.pop("time_created", UNSET)
        time_created: Union[Unset, datetime.datetime]
        if isinstance(_time_created, Unset):
            time_created = UNSET
        else:
            time_created = isoparse(_time_created)

        type_ = d.pop("type", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        name = d.pop("name", UNSET)

        seed_data = []
        _seed_data = d.pop("seed_data", UNSET)
        for seed_data_item_data in _seed_data or []:
            seed_data_item = SeedData.from_dict(seed_data_item_data)

            seed_data.append(seed_data_item)

        scenario_input = cast(list[str], d.pop("scenario_input", UNSET))

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
