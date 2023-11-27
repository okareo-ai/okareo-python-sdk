import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.seed_data import SeedData


T = TypeVar("T", bound="ScenarioSetResponse")


@_attrs_define
class ScenarioSetResponse:
    """
    Attributes:
        scenario_id (str):
        project_id (str):
        time_created (datetime.datetime):
        type (str):
        tags (Union[Unset, List[str]]):
        name (Union[Unset, str]):
        seed_data (Union[Unset, List['SeedData']]):
        scenario_count (Union[Unset, int]):
        scenario_input (Union[Unset, List[str]]):
    """

    scenario_id: str
    project_id: str
    time_created: datetime.datetime
    type: str
    tags: Union[Unset, List[str]] = UNSET
    name: Union[Unset, str] = UNSET
    seed_data: Union[Unset, List["SeedData"]] = UNSET
    scenario_count: Union[Unset, int] = 0
    scenario_input: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scenario_id = self.scenario_id
        project_id = self.project_id
        time_created = self.time_created.isoformat()

        type = self.type
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        name = self.name
        seed_data: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.seed_data, Unset):
            seed_data = []
            for seed_data_item_data in self.seed_data:
                seed_data_item = seed_data_item_data.to_dict()

                seed_data.append(seed_data_item)

        scenario_count = self.scenario_count
        scenario_input: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scenario_input, Unset):
            scenario_input = self.scenario_input

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scenario_id": scenario_id,
                "project_id": project_id,
                "time_created": time_created,
                "type": type,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags
        if name is not UNSET:
            field_dict["name"] = name
        if seed_data is not UNSET:
            field_dict["seed_data"] = seed_data
        if scenario_count is not UNSET:
            field_dict["scenario_count"] = scenario_count
        if scenario_input is not UNSET:
            field_dict["scenario_input"] = scenario_input

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.seed_data import SeedData

        d = src_dict.copy()
        scenario_id = d.pop("scenario_id")

        project_id = d.pop("project_id")

        time_created = isoparse(d.pop("time_created"))

        type = d.pop("type")

        tags = cast(List[str], d.pop("tags", UNSET))

        name = d.pop("name", UNSET)

        seed_data = []
        _seed_data = d.pop("seed_data", UNSET)
        for seed_data_item_data in _seed_data or []:
            seed_data_item = SeedData.from_dict(seed_data_item_data)

            seed_data.append(seed_data_item)

        scenario_count = d.pop("scenario_count", UNSET)

        scenario_input = cast(List[str], d.pop("scenario_input", UNSET))

        scenario_set_response = cls(
            scenario_id=scenario_id,
            project_id=project_id,
            time_created=time_created,
            type=type,
            tags=tags,
            name=name,
            seed_data=seed_data,
            scenario_count=scenario_count,
            scenario_input=scenario_input,
        )

        scenario_set_response.additional_properties = d
        return scenario_set_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
