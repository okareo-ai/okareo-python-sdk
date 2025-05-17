import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_condition import FilterCondition


T = TypeVar("T", bound="SummaryDatapointSearch")


@_attrs_define
class SummaryDatapointSearch:
    """
    Attributes:
        project_id (Union[Unset, str]): Project ID
        mut_id (Union[Unset, str]): Model ID
        from_date (Union[Unset, datetime.datetime]): Earliest date Default: isoparse('2022-12-31T23:59:59.999999').
        to_date (Union[Unset, datetime.datetime]): Latest date
        filters (Union[Unset, List['FilterCondition']]): List of filter conditions to apply. Defaults to None (i.e., all
            datapoints).
        checks (Union[Unset, List[Any]]): List of checks to only flag issues for. Defaults to None (i.e., all checks).
        timezone (Union[Unset, str]): IANA timezone to use for date filtering/aggregation (e.g., 'America/New_York').
            Defaults to None (i.e., UTC).
        precision (Union[Unset, str]): Time precision for the summary. Valid values include ['day', 'hour', 'minute'].
            Defaults to 'day'. Default: 'day'.
        filter_group_id (Union[Unset, str]): Filter group ID to search with
        group_column (Union[Unset, str]): Column to group by for the summary. Overwrites the default time-based grouping
            for the summary.
    """

    project_id: Union[Unset, str] = UNSET
    mut_id: Union[Unset, str] = UNSET
    from_date: Union[Unset, datetime.datetime] = isoparse("2022-12-31T23:59:59.999999")
    to_date: Union[Unset, datetime.datetime] = UNSET
    filters: Union[Unset, List["FilterCondition"]] = UNSET
    checks: Union[Unset, List[Any]] = UNSET
    timezone: Union[Unset, str] = UNSET
    precision: Union[Unset, str] = "day"
    filter_group_id: Union[Unset, str] = UNSET
    group_column: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        project_id = self.project_id
        mut_id = self.mut_id
        from_date: Union[Unset, str] = UNSET
        if not isinstance(self.from_date, Unset):
            from_date = self.from_date.isoformat()

        to_date: Union[Unset, str] = UNSET
        if not isinstance(self.to_date, Unset):
            to_date = self.to_date.isoformat()

        filters: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        checks: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.checks, Unset):
            checks = self.checks

        timezone = self.timezone
        precision = self.precision
        filter_group_id = self.filter_group_id
        group_column = self.group_column

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if mut_id is not UNSET:
            field_dict["mut_id"] = mut_id
        if from_date is not UNSET:
            field_dict["from_date"] = from_date
        if to_date is not UNSET:
            field_dict["to_date"] = to_date
        if filters is not UNSET:
            field_dict["filters"] = filters
        if checks is not UNSET:
            field_dict["checks"] = checks
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if precision is not UNSET:
            field_dict["precision"] = precision
        if filter_group_id is not UNSET:
            field_dict["filter_group_id"] = filter_group_id
        if group_column is not UNSET:
            field_dict["group_column"] = group_column

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.filter_condition import FilterCondition

        d = src_dict.copy()
        project_id = d.pop("project_id", UNSET)

        mut_id = d.pop("mut_id", UNSET)

        _from_date = d.pop("from_date", UNSET)
        from_date: Union[Unset, datetime.datetime]
        if isinstance(_from_date, Unset):
            from_date = UNSET
        else:
            from_date = isoparse(_from_date)

        _to_date = d.pop("to_date", UNSET)
        to_date: Union[Unset, datetime.datetime]
        if isinstance(_to_date, Unset):
            to_date = UNSET
        else:
            to_date = isoparse(_to_date)

        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:
            filters_item = FilterCondition.from_dict(filters_item_data)

            filters.append(filters_item)

        checks = cast(List[Any], d.pop("checks", UNSET))

        timezone = d.pop("timezone", UNSET)

        precision = d.pop("precision", UNSET)

        filter_group_id = d.pop("filter_group_id", UNSET)

        group_column = d.pop("group_column", UNSET)

        summary_datapoint_search = cls(
            project_id=project_id,
            mut_id=mut_id,
            from_date=from_date,
            to_date=to_date,
            filters=filters,
            checks=checks,
            timezone=timezone,
            precision=precision,
            filter_group_id=filter_group_id,
            group_column=group_column,
        )

        summary_datapoint_search.additional_properties = d
        return summary_datapoint_search

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
