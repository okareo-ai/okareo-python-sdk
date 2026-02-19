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


T = TypeVar("T", bound="SummaryDatapointSearch")


@_attrs_define
class SummaryDatapointSearch:
    """
    Attributes:
        project_id (None | Unset | UUID): Project ID
        mut_id (None | Unset | UUID): Model ID
        from_date (datetime.datetime | Unset): Earliest date Default: isoparse('2022-12-31T23:59:59.999999').
        to_date (datetime.datetime | None | Unset): Latest date
        filters (list[FilterCondition] | None | Unset): List of filter conditions to apply. Defaults to None (i.e., all
            datapoints).
        checks (list[Any] | None | Unset): List of checks to only flag issues for. Defaults to None (i.e., all checks).
        timezone (None | str | Unset): IANA timezone to use for date filtering/aggregation (e.g., 'America/New_York').
            Defaults to None (i.e., UTC).
        precision (str | Unset): Time precision for the summary. Valid values include ['day', 'hour', 'minute'].
            Defaults to 'day'. Default: 'day'.
        filter_group_id (None | Unset | UUID): Filter group ID to search with
        group_column (None | str | Unset): Column to group by for the summary. Overwrites the default time-based
            grouping for the summary.
    """

    project_id: None | Unset | UUID = UNSET
    mut_id: None | Unset | UUID = UNSET
    from_date: datetime.datetime | Unset = isoparse("2022-12-31T23:59:59.999999")
    to_date: datetime.datetime | None | Unset = UNSET
    filters: list[FilterCondition] | None | Unset = UNSET
    checks: list[Any] | None | Unset = UNSET
    timezone: None | str | Unset = UNSET
    precision: str | Unset = "day"
    filter_group_id: None | Unset | UUID = UNSET
    group_column: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        mut_id: None | str | Unset
        if isinstance(self.mut_id, Unset):
            mut_id = UNSET
        elif isinstance(self.mut_id, UUID):
            mut_id = str(self.mut_id)
        else:
            mut_id = self.mut_id

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

        filters: list[dict[str, Any]] | None | Unset
        if isinstance(self.filters, Unset):
            filters = UNSET
        elif isinstance(self.filters, list):
            filters = []
            for filters_type_0_item_data in self.filters:
                filters_type_0_item = filters_type_0_item_data.to_dict()
                filters.append(filters_type_0_item)

        else:
            filters = self.filters

        checks: list[Any] | None | Unset
        if isinstance(self.checks, Unset):
            checks = UNSET
        elif isinstance(self.checks, list):
            checks = self.checks

        else:
            checks = self.checks

        timezone: None | str | Unset
        if isinstance(self.timezone, Unset):
            timezone = UNSET
        else:
            timezone = self.timezone

        precision = self.precision

        filter_group_id: None | str | Unset
        if isinstance(self.filter_group_id, Unset):
            filter_group_id = UNSET
        elif isinstance(self.filter_group_id, UUID):
            filter_group_id = str(self.filter_group_id)
        else:
            filter_group_id = self.filter_group_id

        group_column: None | str | Unset
        if isinstance(self.group_column, Unset):
            group_column = UNSET
        else:
            group_column = self.group_column

        field_dict: dict[str, Any] = {}
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_condition import FilterCondition

        d = dict(src_dict)

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

        def _parse_filters(data: object) -> list[FilterCondition] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                filters_type_0 = []
                _filters_type_0 = data
                for filters_type_0_item_data in _filters_type_0:
                    filters_type_0_item = FilterCondition.from_dict(filters_type_0_item_data)

                    filters_type_0.append(filters_type_0_item)

                return filters_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[FilterCondition] | None | Unset, data)

        filters = _parse_filters(d.pop("filters", UNSET))

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

        def _parse_timezone(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        timezone = _parse_timezone(d.pop("timezone", UNSET))

        precision = d.pop("precision", UNSET)

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

        def _parse_group_column(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        group_column = _parse_group_column(d.pop("group_column", UNSET))

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
