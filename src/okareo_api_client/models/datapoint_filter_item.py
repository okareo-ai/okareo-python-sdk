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
    from ..models.datapoint_filter_item_average_metrics_type_0 import DatapointFilterItemAverageMetricsType0
    from ..models.datapoint_filter_item_latest_test_run_type_0 import DatapointFilterItemLatestTestRunType0
    from ..models.filter_condition import FilterCondition


T = TypeVar("T", bound="DatapointFilterItem")


@_attrs_define
class DatapointFilterItem:
    """
    Attributes:
        filters (list[FilterCondition]): List of filter conditions to apply
        name (None | str | Unset): Optional name describing this filter
        description (None | str | Unset): Optional description for this filter
        checks (list[str] | None | Unset): Checks to apply to datapoints in the filter.
        project_id (None | Unset | UUID): Project ID these filters belong to
        filter_group_id (None | Unset | UUID): Group ID for filter
        latest_test_run (Any | DatapointFilterItemLatestTestRunType0 | None | Unset): Group ID for filter
        datapoint_count (Any | int | None | Unset): Group ID for filter
        issue_count (Any | int | None | Unset): Count of issues for this filter
        error_count (Any | int | None | Unset): Count of errors for this filter
        average_metrics (Any | DatapointFilterItemAverageMetricsType0 | None | Unset): Metrics for checks in this filter
        failed_checks (Any | Unset): Array of failed cheßck names Default: [].
        avg_latency (Any | float | None | Unset): Average latency for completions
        total_cost (Any | float | None | Unset): Total dollar cost of all completions
        avg_num_turns (Any | float | None | Unset): Average number of turns for completions
        slack_enabled (bool | None | Unset): Whether Slack notifications are enabled for this filter group
        email_enabled (bool | None | Unset): Whether Email notifications are enabled for this filter group
        time_created (datetime.datetime | None | Unset): Created datetime for this filter group
        time_updated (datetime.datetime | None | Unset): Last updated datetime for this filter group
    """

    filters: list[FilterCondition]
    name: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    checks: list[str] | None | Unset = UNSET
    project_id: None | Unset | UUID = UNSET
    filter_group_id: None | Unset | UUID = UNSET
    latest_test_run: Any | DatapointFilterItemLatestTestRunType0 | None | Unset = UNSET
    datapoint_count: Any | int | None | Unset = UNSET
    issue_count: Any | int | None | Unset = UNSET
    error_count: Any | int | None | Unset = UNSET
    average_metrics: Any | DatapointFilterItemAverageMetricsType0 | None | Unset = UNSET
    failed_checks: Any | Unset = []
    avg_latency: Any | float | None | Unset = UNSET
    total_cost: Any | float | None | Unset = UNSET
    avg_num_turns: Any | float | None | Unset = UNSET
    slack_enabled: bool | None | Unset = UNSET
    email_enabled: bool | None | Unset = UNSET
    time_created: datetime.datetime | None | Unset = UNSET
    time_updated: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.datapoint_filter_item_average_metrics_type_0 import DatapointFilterItemAverageMetricsType0
        from ..models.datapoint_filter_item_latest_test_run_type_0 import DatapointFilterItemLatestTestRunType0

        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()
            filters.append(filters_item)

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        checks: list[str] | None | Unset
        if isinstance(self.checks, Unset):
            checks = UNSET
        elif isinstance(self.checks, list):
            checks = self.checks

        else:
            checks = self.checks

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        filter_group_id: None | str | Unset
        if isinstance(self.filter_group_id, Unset):
            filter_group_id = UNSET
        elif isinstance(self.filter_group_id, UUID):
            filter_group_id = str(self.filter_group_id)
        else:
            filter_group_id = self.filter_group_id

        latest_test_run: Any | dict[str, Any] | None | Unset
        if isinstance(self.latest_test_run, Unset):
            latest_test_run = UNSET
        elif isinstance(self.latest_test_run, DatapointFilterItemLatestTestRunType0):
            latest_test_run = self.latest_test_run.to_dict()
        else:
            latest_test_run = self.latest_test_run

        datapoint_count: Any | int | None | Unset
        if isinstance(self.datapoint_count, Unset):
            datapoint_count = UNSET
        else:
            datapoint_count = self.datapoint_count

        issue_count: Any | int | None | Unset
        if isinstance(self.issue_count, Unset):
            issue_count = UNSET
        else:
            issue_count = self.issue_count

        error_count: Any | int | None | Unset
        if isinstance(self.error_count, Unset):
            error_count = UNSET
        else:
            error_count = self.error_count

        average_metrics: Any | dict[str, Any] | None | Unset
        if isinstance(self.average_metrics, Unset):
            average_metrics = UNSET
        elif isinstance(self.average_metrics, DatapointFilterItemAverageMetricsType0):
            average_metrics = self.average_metrics.to_dict()
        else:
            average_metrics = self.average_metrics

        failed_checks = self.failed_checks

        avg_latency: Any | float | None | Unset
        if isinstance(self.avg_latency, Unset):
            avg_latency = UNSET
        else:
            avg_latency = self.avg_latency

        total_cost: Any | float | None | Unset
        if isinstance(self.total_cost, Unset):
            total_cost = UNSET
        else:
            total_cost = self.total_cost

        avg_num_turns: Any | float | None | Unset
        if isinstance(self.avg_num_turns, Unset):
            avg_num_turns = UNSET
        else:
            avg_num_turns = self.avg_num_turns

        slack_enabled: bool | None | Unset
        if isinstance(self.slack_enabled, Unset):
            slack_enabled = UNSET
        else:
            slack_enabled = self.slack_enabled

        email_enabled: bool | None | Unset
        if isinstance(self.email_enabled, Unset):
            email_enabled = UNSET
        else:
            email_enabled = self.email_enabled

        time_created: None | str | Unset
        if isinstance(self.time_created, Unset):
            time_created = UNSET
        elif isinstance(self.time_created, datetime.datetime):
            time_created = self.time_created.isoformat()
        else:
            time_created = self.time_created

        time_updated: None | str | Unset
        if isinstance(self.time_updated, Unset):
            time_updated = UNSET
        elif isinstance(self.time_updated, datetime.datetime):
            time_updated = self.time_updated.isoformat()
        else:
            time_updated = self.time_updated

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filters": filters,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if checks is not UNSET:
            field_dict["checks"] = checks
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if filter_group_id is not UNSET:
            field_dict["filter_group_id"] = filter_group_id
        if latest_test_run is not UNSET:
            field_dict["latest_test_run"] = latest_test_run
        if datapoint_count is not UNSET:
            field_dict["datapoint_count"] = datapoint_count
        if issue_count is not UNSET:
            field_dict["issue_count"] = issue_count
        if error_count is not UNSET:
            field_dict["error_count"] = error_count
        if average_metrics is not UNSET:
            field_dict["average_metrics"] = average_metrics
        if failed_checks is not UNSET:
            field_dict["failed_checks"] = failed_checks
        if avg_latency is not UNSET:
            field_dict["avg_latency"] = avg_latency
        if total_cost is not UNSET:
            field_dict["total_cost"] = total_cost
        if avg_num_turns is not UNSET:
            field_dict["avg_num_turns"] = avg_num_turns
        if slack_enabled is not UNSET:
            field_dict["slack_enabled"] = slack_enabled
        if email_enabled is not UNSET:
            field_dict["email_enabled"] = email_enabled
        if time_created is not UNSET:
            field_dict["time_created"] = time_created
        if time_updated is not UNSET:
            field_dict["time_updated"] = time_updated

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.datapoint_filter_item_average_metrics_type_0 import DatapointFilterItemAverageMetricsType0
        from ..models.datapoint_filter_item_latest_test_run_type_0 import DatapointFilterItemLatestTestRunType0
        from ..models.filter_condition import FilterCondition

        d = dict(src_dict)
        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = FilterCondition.from_dict(filters_item_data)

            filters.append(filters_item)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_checks(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                checks_type_0 = cast(list[str], data)

                return checks_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        checks = _parse_checks(d.pop("checks", UNSET))

        def _parse_project_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

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

        def _parse_latest_test_run(data: object) -> Any | DatapointFilterItemLatestTestRunType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                latest_test_run_type_0 = DatapointFilterItemLatestTestRunType0.from_dict(data)

                return latest_test_run_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Any | DatapointFilterItemLatestTestRunType0 | None | Unset, data)

        latest_test_run = _parse_latest_test_run(d.pop("latest_test_run", UNSET))

        def _parse_datapoint_count(data: object) -> Any | int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | int | None | Unset, data)

        datapoint_count = _parse_datapoint_count(d.pop("datapoint_count", UNSET))

        def _parse_issue_count(data: object) -> Any | int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | int | None | Unset, data)

        issue_count = _parse_issue_count(d.pop("issue_count", UNSET))

        def _parse_error_count(data: object) -> Any | int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | int | None | Unset, data)

        error_count = _parse_error_count(d.pop("error_count", UNSET))

        def _parse_average_metrics(data: object) -> Any | DatapointFilterItemAverageMetricsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                average_metrics_type_0 = DatapointFilterItemAverageMetricsType0.from_dict(data)

                return average_metrics_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Any | DatapointFilterItemAverageMetricsType0 | None | Unset, data)

        average_metrics = _parse_average_metrics(d.pop("average_metrics", UNSET))

        failed_checks = d.pop("failed_checks", UNSET)

        def _parse_avg_latency(data: object) -> Any | float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | float | None | Unset, data)

        avg_latency = _parse_avg_latency(d.pop("avg_latency", UNSET))

        def _parse_total_cost(data: object) -> Any | float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | float | None | Unset, data)

        total_cost = _parse_total_cost(d.pop("total_cost", UNSET))

        def _parse_avg_num_turns(data: object) -> Any | float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | float | None | Unset, data)

        avg_num_turns = _parse_avg_num_turns(d.pop("avg_num_turns", UNSET))

        def _parse_slack_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        slack_enabled = _parse_slack_enabled(d.pop("slack_enabled", UNSET))

        def _parse_email_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        email_enabled = _parse_email_enabled(d.pop("email_enabled", UNSET))

        def _parse_time_created(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                time_created_type_0 = isoparse(data)

                return time_created_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        time_created = _parse_time_created(d.pop("time_created", UNSET))

        def _parse_time_updated(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                time_updated_type_0 = isoparse(data)

                return time_updated_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        time_updated = _parse_time_updated(d.pop("time_updated", UNSET))

        datapoint_filter_item = cls(
            filters=filters,
            name=name,
            description=description,
            checks=checks,
            project_id=project_id,
            filter_group_id=filter_group_id,
            latest_test_run=latest_test_run,
            datapoint_count=datapoint_count,
            issue_count=issue_count,
            error_count=error_count,
            average_metrics=average_metrics,
            failed_checks=failed_checks,
            avg_latency=avg_latency,
            total_cost=total_cost,
            avg_num_turns=avg_num_turns,
            slack_enabled=slack_enabled,
            email_enabled=email_enabled,
            time_created=time_created,
            time_updated=time_updated,
        )

        datapoint_filter_item.additional_properties = d
        return datapoint_filter_item

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
