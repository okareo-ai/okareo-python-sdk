from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FindTestDataPointPayload")


@_attrs_define
class FindTestDataPointPayload:
    """
    Attributes:
        id (None | Unset | UUID): ID of the datapoint
        test_run_id (None | Unset | UUID): ID of the test run
        scenario_data_point_id (None | Unset | UUID): ID of the scenario data point
        metric_type (None | str | Unset):
        full_data_point (bool | None | Unset):  Default: False.
    """

    id: None | Unset | UUID = UNSET
    test_run_id: None | Unset | UUID = UNSET
    scenario_data_point_id: None | Unset | UUID = UNSET
    metric_type: None | str | Unset = UNSET
    full_data_point: bool | None | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        elif isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        test_run_id: None | str | Unset
        if isinstance(self.test_run_id, Unset):
            test_run_id = UNSET
        elif isinstance(self.test_run_id, UUID):
            test_run_id = str(self.test_run_id)
        else:
            test_run_id = self.test_run_id

        scenario_data_point_id: None | str | Unset
        if isinstance(self.scenario_data_point_id, Unset):
            scenario_data_point_id = UNSET
        elif isinstance(self.scenario_data_point_id, UUID):
            scenario_data_point_id = str(self.scenario_data_point_id)
        else:
            scenario_data_point_id = self.scenario_data_point_id

        metric_type: None | str | Unset
        if isinstance(self.metric_type, Unset):
            metric_type = UNSET
        else:
            metric_type = self.metric_type

        full_data_point: bool | None | Unset
        if isinstance(self.full_data_point, Unset):
            full_data_point = UNSET
        else:
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

        def _parse_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                id_type_0 = UUID(data)

                return id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_test_run_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                test_run_id_type_0 = UUID(data)

                return test_run_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        test_run_id = _parse_test_run_id(d.pop("test_run_id", UNSET))

        def _parse_scenario_data_point_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scenario_data_point_id_type_0 = UUID(data)

                return scenario_data_point_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        scenario_data_point_id = _parse_scenario_data_point_id(d.pop("scenario_data_point_id", UNSET))

        def _parse_metric_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        metric_type = _parse_metric_type(d.pop("metric_type", UNSET))

        def _parse_full_data_point(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        full_data_point = _parse_full_data_point(d.pop("full_data_point", UNSET))

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
