import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_run_type import TestRunType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestRunPayload")


@_attrs_define
class TestRunPayload:
    """
    Attributes:
        mut_id (str):
        scenario_id (str):
        api_key (Union[Unset, str]):
        name (Union[Unset, str]):
        tags (Union[Unset, List[str]]):
        type (Union[Unset, TestRunType]): An enumeration.
        start_time (Union[Unset, datetime.datetime]):
        end_time (Union[Unset, datetime.datetime]):
        calculate_model_metrics (Union[Unset, bool]):
    """

    mut_id: str
    scenario_id: str
    api_key: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    type: Union[Unset, TestRunType] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    end_time: Union[Unset, datetime.datetime] = UNSET
    calculate_model_metrics: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mut_id = self.mut_id
        scenario_id = self.scenario_id
        api_key = self.api_key
        name = self.name
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mut_id": mut_id,
                "scenario_id": scenario_id,
            }
        )
        if api_key is not UNSET:
            field_dict["api_key"] = api_key
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type
        if tags is not UNSET:
            field_dict["tags"] = tags
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        mut_id = d.pop("mut_id")

        scenario_id = d.pop("scenario_id")

        api_key = d.pop("api_key", UNSET)

        name = d.pop("name", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, TestRunType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = TestRunType(_type)

        tags = cast(List[str], d.pop("tags", UNSET))

        project_id = d.pop("project_id", UNSET)

        test_run_payload = cls(
            mut_id=mut_id,
            scenario_id=scenario_id,
            api_key=api_key,
            name=name,
            type=type,
            tags=tags,
            project_id=project_id,
        )

        test_run_payload.additional_properties = d
        return test_run_payload

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
