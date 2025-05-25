from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestDataPointPayload")


@_attrs_define
class TestDataPointPayload:
    """
    Attributes:
        test_run_id (Union[Unset, UUID]): ID for the testrun
        scenario_data_point_id (Union[Unset, UUID]): ID of the scenario data point
        metric_type (Union[Unset, str]):
        metric_value (Union[Unset, str]):
    """

    test_run_id: Union[Unset, UUID] = UNSET
    scenario_data_point_id: Union[Unset, UUID] = UNSET
    metric_type: Union[Unset, str] = UNSET
    metric_value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        test_run_id: Union[Unset, str] = UNSET
        if not isinstance(self.test_run_id, Unset):
            test_run_id = str(self.test_run_id)

        scenario_data_point_id: Union[Unset, str] = UNSET
        if not isinstance(self.scenario_data_point_id, Unset):
            scenario_data_point_id = str(self.scenario_data_point_id)

        metric_type = self.metric_type

        metric_value = self.metric_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if test_run_id is not UNSET:
            field_dict["test_run_id"] = test_run_id
        if scenario_data_point_id is not UNSET:
            field_dict["scenario_data_point_id"] = scenario_data_point_id
        if metric_type is not UNSET:
            field_dict["metric_type"] = metric_type
        if metric_value is not UNSET:
            field_dict["metric_value"] = metric_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _test_run_id = d.pop("test_run_id", UNSET)
        test_run_id: Union[Unset, UUID]
        if isinstance(_test_run_id, Unset):
            test_run_id = UNSET
        else:
            test_run_id = UUID(_test_run_id)

        _scenario_data_point_id = d.pop("scenario_data_point_id", UNSET)
        scenario_data_point_id: Union[Unset, UUID]
        if isinstance(_scenario_data_point_id, Unset):
            scenario_data_point_id = UNSET
        else:
            scenario_data_point_id = UUID(_scenario_data_point_id)

        metric_type = d.pop("metric_type", UNSET)

        metric_value = d.pop("metric_value", UNSET)

        test_data_point_payload = cls(
            test_run_id=test_run_id,
            scenario_data_point_id=scenario_data_point_id,
            metric_type=metric_type,
            metric_value=metric_value,
        )

        test_data_point_payload.additional_properties = d
        return test_data_point_payload

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
