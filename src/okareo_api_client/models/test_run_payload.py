import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.test_run_type import TestRunType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestRunPayload")


@_attrs_define
class TestRunPayload:
    """
    Attributes:
        mut_id (Union[Unset, UUID]): ID of model
        scenario_set_id (Union[Unset, UUID]): ID of scenario set
        name (Union[Unset, str]): Name of test run
        tags (Union[Unset, list[str]]): Tags are strings that can be used to filter test runs in the Okareo app
        type_ (Union[Unset, TestRunType]): An enumeration.
        start_time (Union[Unset, datetime.datetime]):
        end_time (Union[Unset, datetime.datetime]):
        calculate_model_metrics (Union[Unset, bool]): Boolean value indicating if model metrics should be calculated
            Default: False.
    """

    mut_id: Union[Unset, UUID] = UNSET
    scenario_set_id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    type_: Union[Unset, TestRunType] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    end_time: Union[Unset, datetime.datetime] = UNSET
    calculate_model_metrics: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mut_id: Union[Unset, str] = UNSET
        if not isinstance(self.mut_id, Unset):
            mut_id = str(self.mut_id)

        scenario_set_id: Union[Unset, str] = UNSET
        if not isinstance(self.scenario_set_id, Unset):
            scenario_set_id = str(self.scenario_set_id)

        name = self.name

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        end_time: Union[Unset, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat()

        calculate_model_metrics = self.calculate_model_metrics

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mut_id is not UNSET:
            field_dict["mut_id"] = mut_id
        if scenario_set_id is not UNSET:
            field_dict["scenario_set_id"] = scenario_set_id
        if name is not UNSET:
            field_dict["name"] = name
        if tags is not UNSET:
            field_dict["tags"] = tags
        if type_ is not UNSET:
            field_dict["type"] = type_
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if calculate_model_metrics is not UNSET:
            field_dict["calculate_model_metrics"] = calculate_model_metrics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _mut_id = d.pop("mut_id", UNSET)
        mut_id: Union[Unset, UUID]
        if isinstance(_mut_id, Unset):
            mut_id = UNSET
        else:
            mut_id = UUID(_mut_id)

        _scenario_set_id = d.pop("scenario_set_id", UNSET)
        scenario_set_id: Union[Unset, UUID]
        if isinstance(_scenario_set_id, Unset):
            scenario_set_id = UNSET
        else:
            scenario_set_id = UUID(_scenario_set_id)

        name = d.pop("name", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, TestRunType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = TestRunType(_type_)

        _start_time = d.pop("start_time", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        _end_time = d.pop("end_time", UNSET)
        end_time: Union[Unset, datetime.datetime]
        if isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = isoparse(_end_time)

        calculate_model_metrics = d.pop("calculate_model_metrics", UNSET)

        test_run_payload = cls(
            mut_id=mut_id,
            scenario_set_id=scenario_set_id,
            name=name,
            tags=tags,
            type_=type_,
            start_time=start_time,
            end_time=end_time,
            calculate_model_metrics=calculate_model_metrics,
        )

        test_run_payload.additional_properties = d
        return test_run_payload

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
