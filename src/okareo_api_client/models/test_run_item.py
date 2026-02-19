from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_run_item_model_metrics import TestRunItemModelMetrics
    from ..models.test_run_item_simulation_params import TestRunItemSimulationParams


T = TypeVar("T", bound="TestRunItem")


@_attrs_define
class TestRunItem:
    """
    Attributes:
        id (UUID):
        project_id (UUID):
        mut_id (None | Unset | UUID):
        scenario_set_id (None | Unset | UUID):
        filter_group_id (None | Unset | UUID):
        name (None | str | Unset):
        tags (list[str] | Unset):
        type_ (None | str | Unset):
        start_time (datetime.datetime | None | Unset):
        end_time (datetime.datetime | None | Unset):
        test_data_point_count (int | None | Unset):
        model_metrics (None | TestRunItemModelMetrics | Unset):
        error_matrix (list[Any] | None | Unset):
        status (None | str | Unset):
        failure_message (None | str | Unset):
        progress (int | Unset): Number in percent of progress of test run Default: 0.
        app_link (str | Unset): This URL links to the Okareo webpage for this test run Default: ''.
        simulation_params (None | TestRunItemSimulationParams | Unset):
        driver_id (None | Unset | UUID): ID of the driver used for the run, if applicable.
    """

    id: UUID
    project_id: UUID
    mut_id: None | Unset | UUID = UNSET
    scenario_set_id: None | Unset | UUID = UNSET
    filter_group_id: None | Unset | UUID = UNSET
    name: None | str | Unset = UNSET
    tags: list[str] | Unset = UNSET
    type_: None | str | Unset = UNSET
    start_time: datetime.datetime | None | Unset = UNSET
    end_time: datetime.datetime | None | Unset = UNSET
    test_data_point_count: int | None | Unset = UNSET
    model_metrics: None | TestRunItemModelMetrics | Unset = UNSET
    error_matrix: list[Any] | None | Unset = UNSET
    status: None | str | Unset = UNSET
    failure_message: None | str | Unset = UNSET
    progress: int | Unset = 0
    app_link: str | Unset = ""
    simulation_params: None | TestRunItemSimulationParams | Unset = UNSET
    driver_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.test_run_item_model_metrics import TestRunItemModelMetrics
        from ..models.test_run_item_simulation_params import TestRunItemSimulationParams

        id = str(self.id)

        project_id = str(self.project_id)

        mut_id: None | str | Unset
        if isinstance(self.mut_id, Unset):
            mut_id = UNSET
        elif isinstance(self.mut_id, UUID):
            mut_id = str(self.mut_id)
        else:
            mut_id = self.mut_id

        scenario_set_id: None | str | Unset
        if isinstance(self.scenario_set_id, Unset):
            scenario_set_id = UNSET
        elif isinstance(self.scenario_set_id, UUID):
            scenario_set_id = str(self.scenario_set_id)
        else:
            scenario_set_id = self.scenario_set_id

        filter_group_id: None | str | Unset
        if isinstance(self.filter_group_id, Unset):
            filter_group_id = UNSET
        elif isinstance(self.filter_group_id, UUID):
            filter_group_id = str(self.filter_group_id)
        else:
            filter_group_id = self.filter_group_id

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        type_: None | str | Unset
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

        start_time: None | str | Unset
        if isinstance(self.start_time, Unset):
            start_time = UNSET
        elif isinstance(self.start_time, datetime.datetime):
            start_time = self.start_time.isoformat()
        else:
            start_time = self.start_time

        end_time: None | str | Unset
        if isinstance(self.end_time, Unset):
            end_time = UNSET
        elif isinstance(self.end_time, datetime.datetime):
            end_time = self.end_time.isoformat()
        else:
            end_time = self.end_time

        test_data_point_count: int | None | Unset
        if isinstance(self.test_data_point_count, Unset):
            test_data_point_count = UNSET
        else:
            test_data_point_count = self.test_data_point_count

        model_metrics: dict[str, Any] | None | Unset
        if isinstance(self.model_metrics, Unset):
            model_metrics = UNSET
        elif isinstance(self.model_metrics, TestRunItemModelMetrics):
            model_metrics = self.model_metrics.to_dict()
        else:
            model_metrics = self.model_metrics

        error_matrix: list[Any] | None | Unset
        if isinstance(self.error_matrix, Unset):
            error_matrix = UNSET
        elif isinstance(self.error_matrix, list):
            error_matrix = self.error_matrix

        else:
            error_matrix = self.error_matrix

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        failure_message: None | str | Unset
        if isinstance(self.failure_message, Unset):
            failure_message = UNSET
        else:
            failure_message = self.failure_message

        progress = self.progress

        app_link = self.app_link

        simulation_params: dict[str, Any] | None | Unset
        if isinstance(self.simulation_params, Unset):
            simulation_params = UNSET
        elif isinstance(self.simulation_params, TestRunItemSimulationParams):
            simulation_params = self.simulation_params.to_dict()
        else:
            simulation_params = self.simulation_params

        driver_id: None | str | Unset
        if isinstance(self.driver_id, Unset):
            driver_id = UNSET
        elif isinstance(self.driver_id, UUID):
            driver_id = str(self.driver_id)
        else:
            driver_id = self.driver_id

        field_dict: dict[str, Any] = {}
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
        if filter_group_id is not UNSET:
            field_dict["filter_group_id"] = filter_group_id
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
        if test_data_point_count is not UNSET:
            field_dict["test_data_point_count"] = test_data_point_count
        if model_metrics is not UNSET:
            field_dict["model_metrics"] = model_metrics
        if error_matrix is not UNSET:
            field_dict["error_matrix"] = error_matrix
        if status is not UNSET:
            field_dict["status"] = status
        if failure_message is not UNSET:
            field_dict["failure_message"] = failure_message
        if progress is not UNSET:
            field_dict["progress"] = progress
        if app_link is not UNSET:
            field_dict["app_link"] = app_link
        if simulation_params is not UNSET:
            field_dict["simulation_params"] = simulation_params
        if driver_id is not UNSET:
            field_dict["driver_id"] = driver_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.test_run_item_model_metrics import TestRunItemModelMetrics
        from ..models.test_run_item_simulation_params import TestRunItemSimulationParams

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        project_id = UUID(d.pop("project_id"))

        def _parse_mut_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mut_id_type_0 = UUID(data)

                return mut_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        mut_id = _parse_mut_id(d.pop("mut_id", UNSET))

        def _parse_scenario_set_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scenario_set_id_type_0 = UUID(data)

                return scenario_set_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        scenario_set_id = _parse_scenario_set_id(d.pop("scenario_set_id", UNSET))

        def _parse_filter_group_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                filter_group_id_type_0 = UUID(data)

                return filter_group_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        filter_group_id = _parse_filter_group_id(d.pop("filter_group_id", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_type_(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        type_ = _parse_type_(d.pop("type", UNSET))

        def _parse_start_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0 = isoparse(data)

                return start_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        start_time = _parse_start_time(d.pop("start_time", UNSET))

        def _parse_end_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_time_type_0 = isoparse(data)

                return end_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        end_time = _parse_end_time(d.pop("end_time", UNSET))

        def _parse_test_data_point_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        test_data_point_count = _parse_test_data_point_count(d.pop("test_data_point_count", UNSET))

        def _parse_model_metrics(data: object) -> None | TestRunItemModelMetrics | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_metrics_type_0 = TestRunItemModelMetrics.from_dict(data)

                return model_metrics_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TestRunItemModelMetrics | Unset, data)

        model_metrics = _parse_model_metrics(d.pop("model_metrics", UNSET))

        def _parse_error_matrix(data: object) -> list[Any] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                error_matrix_type_0 = cast(list[Any], data)

                return error_matrix_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Any] | None | Unset, data)

        error_matrix = _parse_error_matrix(d.pop("error_matrix", UNSET))

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_failure_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        failure_message = _parse_failure_message(d.pop("failure_message", UNSET))

        progress = d.pop("progress", UNSET)

        app_link = d.pop("app_link", UNSET)

        def _parse_simulation_params(data: object) -> None | TestRunItemSimulationParams | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                simulation_params_type_0 = TestRunItemSimulationParams.from_dict(data)

                return simulation_params_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TestRunItemSimulationParams | Unset, data)

        simulation_params = _parse_simulation_params(d.pop("simulation_params", UNSET))

        def _parse_driver_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                driver_id_type_0 = UUID(data)

                return driver_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        driver_id = _parse_driver_id(d.pop("driver_id", UNSET))

        test_run_item = cls(
            id=id,
            project_id=project_id,
            mut_id=mut_id,
            scenario_set_id=scenario_set_id,
            filter_group_id=filter_group_id,
            name=name,
            tags=tags,
            type_=type_,
            start_time=start_time,
            end_time=end_time,
            test_data_point_count=test_data_point_count,
            model_metrics=model_metrics,
            error_matrix=error_matrix,
            status=status,
            failure_message=failure_message,
            progress=progress,
            app_link=app_link,
            simulation_params=simulation_params,
            driver_id=driver_id,
        )

        test_run_item.additional_properties = d
        return test_run_item

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
