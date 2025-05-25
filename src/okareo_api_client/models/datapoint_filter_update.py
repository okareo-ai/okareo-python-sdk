from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_condition import FilterCondition


T = TypeVar("T", bound="DatapointFilterUpdate")


@_attrs_define
class DatapointFilterUpdate:
    """
    Attributes:
        filters (Union[Unset, list['FilterCondition']]): List of filter conditions to apply
        name (Union[Unset, str]): Optional name describing this filter
        description (Union[Unset, str]): Optional description of the filter
        checks (Union[Unset, list[str]]): Optional list of checks to apply to datapoints in the filter
        slack_enabled (Union[Unset, bool]): Whether to enable Slack notifications for this filter group.
        email_enabled (Union[Unset, bool]): Whether to enable Email notifications for this filter group.
        project_id (Union[Unset, UUID]): Project ID these filters belong to
    """

    filters: Union[Unset, list["FilterCondition"]] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    checks: Union[Unset, list[str]] = UNSET
    slack_enabled: Union[Unset, bool] = UNSET
    email_enabled: Union[Unset, bool] = UNSET
    project_id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()
                filters.append(filters_item)

        name = self.name

        description = self.description

        checks: Union[Unset, list[str]] = UNSET
        if not isinstance(self.checks, Unset):
            checks = self.checks

        slack_enabled = self.slack_enabled

        email_enabled = self.email_enabled

        project_id: Union[Unset, str] = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filters is not UNSET:
            field_dict["filters"] = filters
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
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:
            filters_item = FilterCondition.from_dict(filters_item_data)

            filters.append(filters_item)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        checks = cast(list[str], d.pop("checks", UNSET))

        slack_enabled = d.pop("slack_enabled", UNSET)

        email_enabled = d.pop("email_enabled", UNSET)

        _project_id = d.pop("project_id", UNSET)
        project_id: Union[Unset, UUID]
        if isinstance(_project_id, Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)

        datapoint_filter_update = cls(
            filters=filters,
            name=name,
            description=description,
            checks=checks,
            slack_enabled=slack_enabled,
            email_enabled=email_enabled,
            project_id=project_id,
        )

        datapoint_filter_update.additional_properties = d
        return datapoint_filter_update

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
