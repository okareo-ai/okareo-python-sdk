import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

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
        filters (List['FilterCondition']): List of filter conditions to apply
        name (Union[Unset, str]): Optional name describing this filter
        description (Union[Unset, str]): Optional description for this filter
        checks (Union[Unset, List[str]]): Checks to apply to datapoints in the filter.
        project_id (Union[Unset, str]): Project ID these filters belong to
        filter_group_id (Union[Unset, str]): Group ID for filter
        latest_test_run (Union['DatapointFilterItemLatestTestRunType0', Any, Unset]): Group ID for filter
        datapoint_count (Union[Any, Unset, int]): Group ID for filter
        issue_count (Union[Any, Unset, int]): Count of issues for this filter
        error_count (Union[Any, Unset, int]): Count of errors for this filter
        average_metrics (Union['DatapointFilterItemAverageMetricsType0', Any, Unset]): Metrics for checks in this filter
        failed_checks (Union[Unset, Any]): Array of failed cheßck names
        avg_latency (Union[Any, Unset, float]): Average latency for completions
        total_cost (Union[Any, Unset, float]): Total dollar cost of all completions
        avg_num_turns (Union[Any, Unset, float]): Average number of turns for completions
        slack_enabled (Union[Unset, bool]): Whether Slack notifications are enabled for this filter group
        email_enabled (Union[Unset, bool]): Whether Email notifications are enabled for this filter group
        time_created (Union[Unset, datetime.datetime]): Created datetime for this filter group
        time_updated (Union[Unset, datetime.datetime]): Last updated datetime for this filter group
    """

    filters: List["FilterCondition"]
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    checks: Union[Unset, List[str]] = UNSET
    project_id: Union[Unset, str] = UNSET
    filter_group_id: Union[Unset, str] = UNSET
    latest_test_run: Union["DatapointFilterItemLatestTestRunType0", Any, Unset] = UNSET
    datapoint_count: Union[Any, Unset, int] = UNSET
    issue_count: Union[Any, Unset, int] = UNSET
    error_count: Union[Any, Unset, int] = UNSET
    average_metrics: Union["DatapointFilterItemAverageMetricsType0", Any, Unset] = UNSET
    failed_checks: Union[Unset, Any] = UNSET
    avg_latency: Union[Any, Unset, float] = UNSET
    total_cost: Union[Any, Unset, float] = UNSET
    avg_num_turns: Union[Any, Unset, float] = UNSET
    slack_enabled: Union[Unset, bool] = UNSET
    email_enabled: Union[Unset, bool] = UNSET
    time_created: Union[Unset, datetime.datetime] = UNSET
    time_updated: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.datapoint_filter_item_average_metrics_type_0 import DatapointFilterItemAverageMetricsType0
        from ..models.datapoint_filter_item_latest_test_run_type_0 import DatapointFilterItemLatestTestRunType0

        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()

            filters.append(filters_item)

        name = self.name
        description = self.description
        checks: Union[Unset, List[str]] = UNSET
        if not isinstance(self.checks, Unset):
            checks = self.checks

        project_id = self.project_id
        filter_group_id = self.filter_group_id
        latest_test_run: Union[Any, Dict[str, Any], Unset]
        if isinstance(self.latest_test_run, Unset):
            latest_test_run = UNSET

        elif isinstance(self.latest_test_run, DatapointFilterItemLatestTestRunType0):
            latest_test_run = UNSET
            if not isinstance(self.latest_test_run, Unset):
                latest_test_run = self.latest_test_run.to_dict()

        else:
            latest_test_run = self.latest_test_run

        datapoint_count: Union[Any, Unset, int]
        if isinstance(self.datapoint_count, Unset):
            datapoint_count = UNSET

        else:
            datapoint_count = self.datapoint_count

        issue_count: Union[Any, Unset, int]
        if isinstance(self.issue_count, Unset):
            issue_count = UNSET

        else:
            issue_count = self.issue_count

        error_count: Union[Any, Unset, int]
        if isinstance(self.error_count, Unset):
            error_count = UNSET

        else:
            error_count = self.error_count

        average_metrics: Union[Any, Dict[str, Any], Unset]
        if isinstance(self.average_metrics, Unset):
            average_metrics = UNSET

        elif isinstance(self.average_metrics, DatapointFilterItemAverageMetricsType0):
            average_metrics = UNSET
            if not isinstance(self.average_metrics, Unset):
                average_metrics = self.average_metrics.to_dict()

        else:
            average_metrics = self.average_metrics

        failed_checks = self.failed_checks
        avg_latency: Union[Any, Unset, float]
        if isinstance(self.avg_latency, Unset):
            avg_latency = UNSET

        else:
            avg_latency = self.avg_latency

        total_cost: Union[Any, Unset, float]
        if isinstance(self.total_cost, Unset):
            total_cost = UNSET

        else:
            total_cost = self.total_cost

        avg_num_turns: Union[Any, Unset, float]
        if isinstance(self.avg_num_turns, Unset):
            avg_num_turns = UNSET

        else:
            avg_num_turns = self.avg_num_turns

        slack_enabled = self.slack_enabled
        email_enabled = self.email_enabled
        time_created: Union[Unset, str] = UNSET
        if not isinstance(self.time_created, Unset):
            time_created = self.time_created.isoformat()

        time_updated: Union[Unset, str] = UNSET
        if not isinstance(self.time_updated, Unset):
            time_updated = self.time_updated.isoformat()

        field_dict: Dict[str, Any] = {}
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
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.datapoint_filter_item_average_metrics_type_0 import DatapointFilterItemAverageMetricsType0
        from ..models.datapoint_filter_item_latest_test_run_type_0 import DatapointFilterItemLatestTestRunType0
        from ..models.filter_condition import FilterCondition

        d = src_dict.copy()
        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = FilterCondition.from_dict(filters_item_data)

            filters.append(filters_item)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        checks = cast(List[str], d.pop("checks", UNSET))

        project_id = d.pop("project_id", UNSET)

        filter_group_id = d.pop("filter_group_id", UNSET)

        def _parse_latest_test_run(data: object) -> Union["DatapointFilterItemLatestTestRunType0", Any, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _latest_test_run_type_0 = data
                latest_test_run_type_0: Union[Unset, DatapointFilterItemLatestTestRunType0]
                if isinstance(_latest_test_run_type_0, Unset):
                    latest_test_run_type_0 = UNSET
                else:
                    latest_test_run_type_0 = DatapointFilterItemLatestTestRunType0.from_dict(_latest_test_run_type_0)

                return latest_test_run_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatapointFilterItemLatestTestRunType0", Any, Unset], data)

        latest_test_run = _parse_latest_test_run(d.pop("latest_test_run", UNSET))

        def _parse_datapoint_count(data: object) -> Union[Any, Unset, int]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Any, Unset, int], data)

        datapoint_count = _parse_datapoint_count(d.pop("datapoint_count", UNSET))

        def _parse_issue_count(data: object) -> Union[Any, Unset, int]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Any, Unset, int], data)

        issue_count = _parse_issue_count(d.pop("issue_count", UNSET))

        def _parse_error_count(data: object) -> Union[Any, Unset, int]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Any, Unset, int], data)

        error_count = _parse_error_count(d.pop("error_count", UNSET))

        def _parse_average_metrics(data: object) -> Union["DatapointFilterItemAverageMetricsType0", Any, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _average_metrics_type_0 = data
                average_metrics_type_0: Union[Unset, DatapointFilterItemAverageMetricsType0]
                if isinstance(_average_metrics_type_0, Unset):
                    average_metrics_type_0 = UNSET
                else:
                    average_metrics_type_0 = DatapointFilterItemAverageMetricsType0.from_dict(_average_metrics_type_0)

                return average_metrics_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatapointFilterItemAverageMetricsType0", Any, Unset], data)

        average_metrics = _parse_average_metrics(d.pop("average_metrics", UNSET))

        failed_checks = d.pop("failed_checks", UNSET)

        def _parse_avg_latency(data: object) -> Union[Any, Unset, float]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Any, Unset, float], data)

        avg_latency = _parse_avg_latency(d.pop("avg_latency", UNSET))

        def _parse_total_cost(data: object) -> Union[Any, Unset, float]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Any, Unset, float], data)

        total_cost = _parse_total_cost(d.pop("total_cost", UNSET))

        def _parse_avg_num_turns(data: object) -> Union[Any, Unset, float]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Any, Unset, float], data)

        avg_num_turns = _parse_avg_num_turns(d.pop("avg_num_turns", UNSET))

        slack_enabled = d.pop("slack_enabled", UNSET)

        email_enabled = d.pop("email_enabled", UNSET)

        _time_created = d.pop("time_created", UNSET)
        time_created: Union[Unset, datetime.datetime]
        if isinstance(_time_created, Unset):
            time_created = UNSET
        else:
            time_created = isoparse(_time_created)

        _time_updated = d.pop("time_updated", UNSET)
        time_updated: Union[Unset, datetime.datetime]
        if isinstance(_time_updated, Unset):
            time_updated = UNSET
        else:
            time_updated = isoparse(_time_updated)

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
