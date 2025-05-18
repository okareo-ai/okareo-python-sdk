from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_condition import FilterCondition


T = TypeVar("T", bound="DatapointFilterSearch")


@_attrs_define
class DatapointFilterSearch:
    """
    Attributes:
        filters (list['FilterCondition']): List of filter conditions to apply
        project_id (Union[None, UUID, Unset]): Project ID to search within
        offset (Union[None, Unset, int]): Offset for pagination
        limit (Union[None, Unset, int]): Limit for pagination
        issues_only (Union[None, Unset, bool]): Only return issues Default: False.
        errors_only (Union[None, Unset, bool]): Only return errors Default: False.
        checks (Union[None, Unset, list[Any]]): List of checks to only flag issues for
        filter_group_id (Union[None, UUID, Unset]): Filter group ID to search with
    """

    filters: list["FilterCondition"]
    project_id: Union[None, UUID, Unset] = UNSET
    offset: Union[None, Unset, int] = UNSET
    limit: Union[None, Unset, int] = UNSET
    issues_only: Union[None, Unset, bool] = False
    errors_only: Union[None, Unset, bool] = False
    checks: Union[None, Unset, list[Any]] = UNSET
    filter_group_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()
            filters.append(filters_item)

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        offset: Union[None, Unset, int]
        if isinstance(self.offset, Unset):
            offset = UNSET
        else:
            offset = self.offset

        limit: Union[None, Unset, int]
        if isinstance(self.limit, Unset):
            limit = UNSET
        else:
            limit = self.limit

        issues_only: Union[None, Unset, bool]
        if isinstance(self.issues_only, Unset):
            issues_only = UNSET
        else:
            issues_only = self.issues_only

        errors_only: Union[None, Unset, bool]
        if isinstance(self.errors_only, Unset):
            errors_only = UNSET
        else:
            errors_only = self.errors_only

        checks: Union[None, Unset, list[Any]]
        if isinstance(self.checks, Unset):
            checks = UNSET
        elif isinstance(self.checks, list):
            checks = self.checks

        else:
            checks = self.checks

        filter_group_id: Union[None, Unset, str]
        if isinstance(self.filter_group_id, Unset):
            filter_group_id = UNSET
        elif isinstance(self.filter_group_id, UUID):
            filter_group_id = str(self.filter_group_id)
        else:
            filter_group_id = self.filter_group_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filters": filters,
            }
        )
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

        def _parse_project_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_offset(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        offset = _parse_offset(d.pop("offset", UNSET))

        def _parse_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        limit = _parse_limit(d.pop("limit", UNSET))

        def _parse_issues_only(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        issues_only = _parse_issues_only(d.pop("issues_only", UNSET))

        def _parse_errors_only(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        errors_only = _parse_errors_only(d.pop("errors_only", UNSET))

        def _parse_checks(data: object) -> Union[None, Unset, list[Any]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                checks_type_0 = cast(list[Any], data)

                return checks_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Any]], data)

        checks = _parse_checks(d.pop("checks", UNSET))

        def _parse_filter_group_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                filter_group_id_type_0 = UUID(data)

                return filter_group_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        filter_group_id = _parse_filter_group_id(d.pop("filter_group_id", UNSET))

        datapoint_filter_search = cls(
            filters=filters,
            project_id=project_id,
            offset=offset,
            limit=limit,
            issues_only=issues_only,
            errors_only=errors_only,
            checks=checks,
            filter_group_id=filter_group_id,
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
