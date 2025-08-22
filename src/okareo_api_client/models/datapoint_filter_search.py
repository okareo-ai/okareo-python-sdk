import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_condition import FilterCondition


T = TypeVar("T", bound="DatapointFilterSearch")


@_attrs_define
class DatapointFilterSearch:
    """
    Attributes:
        filters (List['FilterCondition']): List of filter conditions to apply
        from_date (Union[Unset, datetime.datetime]): Earliest date Default: isoparse('2022-12-31T23:59:59.999999').
        to_date (Union[Unset, datetime.datetime]): Latest date
        project_id (Union[Unset, str]): Project ID to search within
        offset (Union[Unset, int]): Offset for pagination
        limit (Union[Unset, int]): Limit for pagination
        issues_only (Union[Unset, bool]): Only return issues
        errors_only (Union[Unset, bool]): Only return errors
        checks (Union[Unset, List[Any]]): List of checks to only flag issues for
        filter_group_id (Union[Unset, str]): Filter group ID to search with
        timezone (Union[Unset, str]): IANA timezone to use for date filtering/aggregation (e.g., 'America/New_York').
            Defaults to None (i.e., UTC).
        precision (Union[Unset, str]): Time precision for the filter search. Valid values include ['day', 'hour',
            'minute']. Applied to 'from_date'. Defaults to 'day'. Default: 'day'.
    """

    filters: List["FilterCondition"]
    from_date: Union[Unset, datetime.datetime] = isoparse("2022-12-31T23:59:59.999999")
    to_date: Union[Unset, datetime.datetime] = UNSET
    project_id: Union[Unset, str] = UNSET
    offset: Union[Unset, int] = UNSET
    limit: Union[Unset, int] = UNSET
    issues_only: Union[Unset, bool] = False
    errors_only: Union[Unset, bool] = False
    checks: Union[Unset, List[Any]] = UNSET
    filter_group_id: Union[Unset, str] = UNSET
    timezone: Union[Unset, str] = UNSET
    precision: Union[Unset, str] = "day"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()

            filters.append(filters_item)

        from_date: Union[Unset, str] = UNSET
        if not isinstance(self.from_date, Unset):
            from_date = self.from_date.isoformat()

        to_date: Union[Unset, str] = UNSET
        if not isinstance(self.to_date, Unset):
            to_date = self.to_date.isoformat()

        project_id = self.project_id
        offset = self.offset
        limit = self.limit
        issues_only = self.issues_only
        errors_only = self.errors_only
        checks: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.checks, Unset):
            checks = self.checks

        filter_group_id = self.filter_group_id
        timezone = self.timezone
        precision = self.precision

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filters": filters,
            }
        )
        if from_date is not UNSET:
            field_dict["from_date"] = from_date
        if to_date is not UNSET:
            field_dict["to_date"] = to_date
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if offset is not UNSET:
            field_dict["offset"] = offset
        if limit is not UNSET:
            field_dict["limit"] = limit
        if issues_only is not UNSET:
            field_dict["issues_only"] = issues_only
        if errors_only is not UNSET:
            field_dict["errors_only"] = errors_only
        if checks is not UNSET:
            field_dict["checks"] = checks
        if filter_group_id is not UNSET:
            field_dict["filter_group_id"] = filter_group_id
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if precision is not UNSET:
            field_dict["precision"] = precision

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.filter_condition import FilterCondition

        d = src_dict.copy()
        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = FilterCondition.from_dict(filters_item_data)

            filters.append(filters_item)

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

        project_id = d.pop("project_id", UNSET)

        offset = d.pop("offset", UNSET)

        limit = d.pop("limit", UNSET)

        issues_only = d.pop("issues_only", UNSET)

        errors_only = d.pop("errors_only", UNSET)

        checks = cast(List[Any], d.pop("checks", UNSET))

        filter_group_id = d.pop("filter_group_id", UNSET)

        timezone = d.pop("timezone", UNSET)

        precision = d.pop("precision", UNSET)

        datapoint_filter_search = cls(
            filters=filters,
            from_date=from_date,
            to_date=to_date,
            project_id=project_id,
            offset=offset,
            limit=limit,
            issues_only=issues_only,
            errors_only=errors_only,
            checks=checks,
            filter_group_id=filter_group_id,
            timezone=timezone,
            precision=precision,
        )

        datapoint_filter_search.additional_properties = d
        return datapoint_filter_search

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
