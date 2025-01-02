import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

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
        project_id (str):
        time_created (datetime.datetime):
        type (str):
        scenario_id (Union[Unset, str]):
        tags (Union[Unset, List[str]]):
        name (Union[Unset, str]):
        seed_data (Union[Unset, List['SeedData']]):
        scenario_data (Union[Unset, List['ScenarioDataPoinResponse']]):
        failed_data (Union[Unset, List['ScenarioDataPoinResponse']]):
        scenario_count (Union[Unset, int]):
        scenario_input (Union[Unset, List[str]]):
        app_link (Union[Unset, str]): This URL links to the Okareo webpage for this scenario set Default: ''.
        warning (Union[Unset, str]):
    """

    project_id: str
    time_created: datetime.datetime
    type: str
    scenario_id: Union[Unset, str] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    name: Union[Unset, str] = UNSET
    seed_data: Union[Unset, List["SeedData"]] = UNSET
    scenario_data: Union[Unset, List["ScenarioDataPoinResponse"]] = UNSET
    failed_data: Union[Unset, List["ScenarioDataPoinResponse"]] = UNSET
    scenario_count: Union[Unset, int] = 0
    scenario_input: Union[Unset, List[str]] = UNSET
    app_link: Union[Unset, str] = ""
    warning: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        project_id = self.project_id
        time_created = self.time_created.isoformat()

        type = self.type
        scenario_id = self.scenario_id
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

        scenario_data: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.scenario_data, Unset):
            scenario_data = []
            for scenario_data_item_data in self.scenario_data:
                scenario_data_item = scenario_data_item_data.to_dict()

                scenario_data.append(scenario_data_item)

        failed_data: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.failed_data, Unset):
            failed_data = []
            for failed_data_item_data in self.failed_data:
                failed_data_item = failed_data_item_data.to_dict()

                failed_data.append(failed_data_item)

        scenario_count = self.scenario_count
        scenario_input: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scenario_input, Unset):
            scenario_input = self.scenario_input

        app_link = self.app_link
        warning = self.warning

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "time_created": time_created,
                "type": type,
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
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.scenario_data_poin_response import ScenarioDataPoinResponse
        from ..models.seed_data import SeedData

        d = src_dict.copy()
        project_id = d.pop("project_id")

        time_created = isoparse(d.pop("time_created"))

        type = d.pop("type")

        scenario_id = d.pop("scenario_id", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        name = d.pop("name", UNSET)

        seed_data = []
        _seed_data = d.pop("seed_data", UNSET)
        for seed_data_item_data in _seed_data or []:
            seed_data_item = SeedData.from_dict(seed_data_item_data)

            seed_data.append(seed_data_item)

        scenario_data = []
        _scenario_data = d.pop("scenario_data", UNSET)
        for scenario_data_item_data in _scenario_data or []:
            scenario_data_item = ScenarioDataPoinResponse.from_dict(scenario_data_item_data)

            scenario_data.append(scenario_data_item)

        failed_data = []
        _failed_data = d.pop("failed_data", UNSET)
        for failed_data_item_data in _failed_data or []:
            failed_data_item = ScenarioDataPoinResponse.from_dict(failed_data_item_data)

            failed_data.append(failed_data_item)

        scenario_count = d.pop("scenario_count", UNSET)

        scenario_input = cast(List[str], d.pop("scenario_input", UNSET))

        app_link = d.pop("app_link", UNSET)

        warning = d.pop("warning", UNSET)

        scenario_set_response = cls(
            project_id=project_id,
            time_created=time_created,
            type=type,
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
