from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_condition import FilterCondition


T = TypeVar("T", bound="DatapointFilterCreate")


@_attrs_define
class DatapointFilterCreate:
    """
    Attributes:
        filters (list['FilterCondition']): List of filter conditions to apply
        name (Union[None, Unset, str]): Optional name describing this filter
        description (Union[None, Unset, str]): Optional description of the filter
        checks (Union[None, Unset, list[str]]): Optional list of checks to apply to datapoints in the filter
        slack_enabled (Union[None, Unset, bool]): Whether to enable Slack notifications for this filter group. Default
            is False (off). Default: False.
        email_enabled (Union[None, Unset, bool]): Whether to enable Email notifications for this filter group. Default
            is False (off). Default: False.
        project_id (Union[None, UUID, Unset]): Project ID these filters belong to
    """

    filters: list["FilterCondition"]
    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    checks: Union[None, Unset, list[str]] = UNSET
    slack_enabled: Union[None, Unset, bool] = False
    email_enabled: Union[None, Unset, bool] = False
    project_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()
            filters.append(filters_item)

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        checks: Union[None, Unset, list[str]]
        if isinstance(self.checks, Unset):
            checks = UNSET
        elif isinstance(self.checks, list):
            checks = self.checks

        else:
            checks = self.checks

        slack_enabled: Union[None, Unset, bool]
        if isinstance(self.slack_enabled, Unset):
            slack_enabled = UNSET
        else:
            slack_enabled = self.slack_enabled

        email_enabled: Union[None, Unset, bool]
        if isinstance(self.email_enabled, Unset):
            email_enabled = UNSET
        else:
            email_enabled = self.email_enabled

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

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
        if slack_enabled is not UNSET:
            field_dict["slack_enabled"] = slack_enabled
        if email_enabled is not UNSET:
            field_dict["email_enabled"] = email_enabled
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

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

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_checks(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                checks_type_0 = cast(list[str], data)

                return checks_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        checks = _parse_checks(d.pop("checks", UNSET))

        def _parse_slack_enabled(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        slack_enabled = _parse_slack_enabled(d.pop("slack_enabled", UNSET))

        def _parse_email_enabled(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        email_enabled = _parse_email_enabled(d.pop("email_enabled", UNSET))

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

        datapoint_filter_create = cls(
            filters=filters,
            name=name,
            description=description,
            checks=checks,
            slack_enabled=slack_enabled,
            email_enabled=email_enabled,
            project_id=project_id,
        )

        datapoint_filter_create.additional_properties = d
        return datapoint_filter_create

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
