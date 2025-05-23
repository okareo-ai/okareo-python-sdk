import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestRunAsyncItem")


@_attrs_define
class TestRunAsyncItem:
    """
    Attributes:
        id (str):
        project_id (str):
        mut_id (Union[Unset, str]):
        scenario_set_id (Union[Unset, str]):
        name (Union[Unset, str]):
        tags (Union[Unset, List[str]]):
        type (Union[Unset, str]):
        start_time (Union[Unset, datetime.datetime]):
        app_link (Union[Unset, str]): This URL links to the Okareo webpage for this test run Default: ''.
        status (Union[Unset, str]): Status of the test run, e.g. 'running', 'completed', 'failed'
    """

    id: str
    project_id: str
    mut_id: Union[Unset, str] = UNSET
    scenario_set_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    type: Union[Unset, str] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    app_link: Union[Unset, str] = ""
    status: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        project_id = self.project_id
        mut_id = self.mut_id
        scenario_set_id = self.scenario_set_id
        name = self.name
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        type = self.type
        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        app_link = self.app_link
        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
            }
        )
        if mut_id is not UNSET:
            field_dict["mut_id"] = mut_id
        if scenario_set_id is not UNSET:
            field_dict["scenario_set_id"] = scenario_set_id
        if name is not UNSET:
            field_dict["name"] = name
        if tags is not UNSET:
            field_dict["tags"] = tags
        if type is not UNSET:
            field_dict["type"] = type
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if app_link is not UNSET:
            field_dict["app_link"] = app_link
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        project_id = d.pop("project_id")

        mut_id = d.pop("mut_id", UNSET)

        scenario_set_id = d.pop("scenario_set_id", UNSET)

        name = d.pop("name", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        type = d.pop("type", UNSET)

        _start_time = d.pop("start_time", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        app_link = d.pop("app_link", UNSET)

        status = d.pop("status", UNSET)

        test_run_async_item = cls(
            id=id,
            project_id=project_id,
            mut_id=mut_id,
            scenario_set_id=scenario_set_id,
            name=name,
            tags=tags,
            type=type,
            start_time=start_time,
            app_link=app_link,
            status=status,
        )

        test_run_async_item.additional_properties = d
        return test_run_async_item

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
