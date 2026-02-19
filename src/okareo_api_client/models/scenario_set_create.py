from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scenario_type import ScenarioType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.seed_data import SeedData


T = TypeVar("T", bound="ScenarioSetCreate")


@_attrs_define
class ScenarioSetCreate:
    """
    Attributes:
        name (str): Name of the scenario set
        seed_data (list[SeedData]): Seed data is a list of dictionaries, each with an input and result
        project_id (None | Unset | UUID): ID for the project
        generation_type (ScenarioType | Unset): An enumeration. Default: ScenarioType.SEED.
    """

    name: str
    seed_data: list[SeedData]
    project_id: None | Unset | UUID = UNSET
    generation_type: ScenarioType | Unset = ScenarioType.SEED
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        seed_data = []
        for seed_data_item_data in self.seed_data:
            seed_data_item = seed_data_item_data.to_dict()
            seed_data.append(seed_data_item)

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        generation_type: str | Unset = UNSET
        if not isinstance(self.generation_type, Unset):
            generation_type = self.generation_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "seed_data": seed_data,
            }
        )
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if generation_type is not UNSET:
            field_dict["generation_type"] = generation_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.seed_data import SeedData

        d = dict(src_dict)
        name = d.pop("name")

        seed_data = []
        _seed_data = d.pop("seed_data")
        for seed_data_item_data in _seed_data:
            seed_data_item = SeedData.from_dict(seed_data_item_data)

            seed_data.append(seed_data_item)

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

        _generation_type = d.pop("generation_type", UNSET)
        generation_type: ScenarioType | Unset
        if isinstance(_generation_type, Unset):
            generation_type = UNSET
        else:
            generation_type = ScenarioType(_generation_type)

        scenario_set_create = cls(
            name=name,
            seed_data=seed_data,
            project_id=project_id,
            generation_type=generation_type,
        )

        scenario_set_create.additional_properties = d
        return scenario_set_create

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
