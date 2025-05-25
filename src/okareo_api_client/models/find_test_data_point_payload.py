from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FindTestDataPointPayload")


@_attrs_define
class FindTestDataPointPayload:
    """
    Attributes:
        id (Union[Unset, UUID]): ID of the datapoint
        test_run_id (Union[Unset, UUID]): ID of the test run
        scenario_data_point_id (Union[Unset, UUID]): ID of the scenario data point
        metric_type (Union[Unset, str]):
        full_data_point (Union[Unset, bool]):  Default: False.
    """

    id: Union[Unset, UUID] = UNSET
    test_run_id: Union[Unset, UUID] = UNSET
    scenario_data_point_id: Union[Unset, UUID] = UNSET
    metric_type: Union[Unset, str] = UNSET
    full_data_point: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        test_run_id: Union[Unset, str] = UNSET
        if not isinstance(self.test_run_id, Unset):
            test_run_id = str(self.test_run_id)

        scenario_data_point_id: Union[Unset, str] = UNSET
        if not isinstance(self.scenario_data_point_id, Unset):
            scenario_data_point_id = str(self.scenario_data_point_id)

        metric_type = self.metric_type

        full_data_point = self.full_data_point

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if test_run_id is not UNSET:
            field_dict["test_run_id"] = test_run_id
        if scenario_data_point_id is not UNSET:
            field_dict["scenario_data_point_id"] = scenario_data_point_id
        if metric_type is not UNSET:
            field_dict["metric_type"] = metric_type
        if full_data_point is not UNSET:
            field_dict["full_data_point"] = full_data_point

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

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

        full_data_point = d.pop("full_data_point", UNSET)

        find_test_data_point_payload = cls(
            id=id,
            test_run_id=test_run_id,
            scenario_data_point_id=scenario_data_point_id,
            metric_type=metric_type,
            full_data_point=full_data_point,
        )

        find_test_data_point_payload.additional_properties = d
        return find_test_data_point_payload

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
