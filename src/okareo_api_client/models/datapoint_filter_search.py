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
    from ..models.filter_condition import FilterCondition


T = TypeVar("T", bound="DatapointFilterSearch")


@_attrs_define
class DatapointFilterSearch:
    """
    Attributes:
        filters (list[FilterCondition]): List of filter conditions to apply
        from_date (datetime.datetime | Unset): Earliest date Default: isoparse('2022-12-31T23:59:59.999999').
        to_date (datetime.datetime | None | Unset): Latest date
        project_id (None | Unset | UUID): Project ID to search within
        offset (int | None | Unset): Offset for pagination
        limit (int | None | Unset): Limit for pagination
        issues_only (bool | Unset): Only return issues Default: False.
        errors_only (bool | Unset): Only return errors Default: False.
        checks (list[Any] | None | Unset): List of checks to only flag issues for
        filter_group_id (None | Unset | UUID): Filter group ID to search with
        timezone (None | str | Unset): IANA timezone to use for date filtering/aggregation (e.g., 'America/New_York').
            Defaults to None (i.e., UTC).
        precision (str | Unset): Time precision for the filter search. Valid values include ['day', 'hour', 'minute'].
            Applied to 'from_date'. Defaults to 'day'. Default: 'day'.
    """

    filters: list[FilterCondition]
    from_date: datetime.datetime | Unset = isoparse("2022-12-31T23:59:59.999999")
    to_date: datetime.datetime | None | Unset = UNSET
    project_id: None | Unset | UUID = UNSET
    offset: int | None | Unset = UNSET
    limit: int | None | Unset = UNSET
    issues_only: bool | Unset = False
    errors_only: bool | Unset = False
    checks: list[Any] | None | Unset = UNSET
    filter_group_id: None | Unset | UUID = UNSET
    timezone: None | str | Unset = UNSET
    precision: str | Unset = "day"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()
            filters.append(filters_item)

        from_date: str | Unset = UNSET
        if not isinstance(self.from_date, Unset):
            from_date = self.from_date.isoformat()

        to_date: None | str | Unset
        if isinstance(self.to_date, Unset):
            to_date = UNSET
        elif isinstance(self.to_date, datetime.datetime):
            to_date = self.to_date.isoformat()
        else:
            to_date = self.to_date

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        offset: int | None | Unset
        if isinstance(self.offset, Unset):
            offset = UNSET
        else:
            offset = self.offset

        limit: int | None | Unset
        if isinstance(self.limit, Unset):
            limit = UNSET
        else:
            limit = self.limit

        issues_only = self.issues_only

        errors_only = self.errors_only

        checks: list[Any] | None | Unset
        if isinstance(self.checks, Unset):
            checks = UNSET
        elif isinstance(self.checks, list):
            checks = self.checks

        else:
            checks = self.checks

        filter_group_id: None | str | Unset
        if isinstance(self.filter_group_id, Unset):
            filter_group_id = UNSET
        elif isinstance(self.filter_group_id, UUID):
            filter_group_id = str(self.filter_group_id)
        else:
            filter_group_id = self.filter_group_id

        timezone: None | str | Unset
        if isinstance(self.timezone, Unset):
            timezone = UNSET
        else:
            timezone = self.timezone

        precision = self.precision

        field_dict: dict[str, Any] = {}
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_condition import FilterCondition

        d = dict(src_dict)
        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = FilterCondition.from_dict(filters_item_data)

            filters.append(filters_item)

        _from_date = d.pop("from_date", UNSET)
        from_date: datetime.datetime | Unset
        if isinstance(_from_date, Unset):
            from_date = UNSET
        else:
            from_date = isoparse(_from_date)

        def _parse_to_date(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                to_date_type_0 = isoparse(data)

                return to_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        to_date = _parse_to_date(d.pop("to_date", UNSET))

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

        def _parse_offset(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        offset = _parse_offset(d.pop("offset", UNSET))

        def _parse_limit(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        limit = _parse_limit(d.pop("limit", UNSET))

        issues_only = d.pop("issues_only", UNSET)

        errors_only = d.pop("errors_only", UNSET)

        def _parse_checks(data: object) -> list[Any] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                checks_type_0 = cast(list[Any], data)

                return checks_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Any] | None | Unset, data)

        checks = _parse_checks(d.pop("checks", UNSET))

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

        def _parse_timezone(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        timezone = _parse_timezone(d.pop("timezone", UNSET))

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
