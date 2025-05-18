from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestDataPointPayload")


@_attrs_define
class TestDataPointPayload:
    """
    Attributes:
        metric_value (str):
        test_run_id (Union[None, UUID, Unset]): ID for the testrun
        scenario_data_point_id (Union[None, UUID, Unset]): ID of the scenario data point
        metric_type (Union[None, Unset, str]):
    """

    metric_value: str
    test_run_id: Union[None, UUID, Unset] = UNSET
    scenario_data_point_id: Union[None, UUID, Unset] = UNSET
    metric_type: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric_value = self.metric_value

        test_run_id: Union[None, Unset, str]
        if isinstance(self.test_run_id, Unset):
            test_run_id = UNSET
        elif isinstance(self.test_run_id, UUID):
            test_run_id = str(self.test_run_id)
        else:
            test_run_id = self.test_run_id

        scenario_data_point_id: Union[None, Unset, str]
        if isinstance(self.scenario_data_point_id, Unset):
            scenario_data_point_id = UNSET
        elif isinstance(self.scenario_data_point_id, UUID):
            scenario_data_point_id = str(self.scenario_data_point_id)
        else:
            scenario_data_point_id = self.scenario_data_point_id

        metric_type: Union[None, Unset, str]
        if isinstance(self.metric_type, Unset):
            metric_type = UNSET
        else:
            metric_type = self.metric_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric_value": metric_value,
            }
        )
        if test_run_id is not UNSET:
            field_dict["test_run_id"] = test_run_id
        if scenario_data_point_id is not UNSET:
            field_dict["scenario_data_point_id"] = scenario_data_point_id
        if metric_type is not UNSET:
            field_dict["metric_type"] = metric_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        metric_value = d.pop("metric_value")

        def _parse_test_run_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                test_run_id_type_0 = UUID(data)

                return test_run_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        test_run_id = _parse_test_run_id(d.pop("test_run_id", UNSET))

        def _parse_scenario_data_point_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scenario_data_point_id_type_0 = UUID(data)

                return scenario_data_point_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        scenario_data_point_id = _parse_scenario_data_point_id(d.pop("scenario_data_point_id", UNSET))

        def _parse_metric_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metric_type = _parse_metric_type(d.pop("metric_type", UNSET))

        test_data_point_payload = cls(
            metric_value=metric_value,
            test_run_id=test_run_id,
            scenario_data_point_id=scenario_data_point_id,
            metric_type=metric_type,
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
