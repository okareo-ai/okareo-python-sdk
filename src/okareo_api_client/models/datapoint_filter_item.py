from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

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
        average_metrics (Union['DatapointFilterItemAverageMetricsType0', Any, Unset]): Metrics for checks in this filter
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
    average_metrics: Union["DatapointFilterItemAverageMetricsType0", Any, Unset] = UNSET
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

        average_metrics: Union[Any, Dict[str, Any], Unset]
        if isinstance(self.average_metrics, Unset):
            average_metrics = UNSET

        elif isinstance(self.average_metrics, DatapointFilterItemAverageMetricsType0):
            average_metrics = UNSET
            if not isinstance(self.average_metrics, Unset):
                average_metrics = self.average_metrics.to_dict()

        else:
            average_metrics = self.average_metrics

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
        if average_metrics is not UNSET:
            field_dict["average_metrics"] = average_metrics

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
            average_metrics=average_metrics,
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
