from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

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
        filters (List['FilterCondition']): List of filter conditions to apply
        name (Union[Unset, str]): Optional name describing this filter
        description (Union[Unset, str]): Optional description of the filter
        checks (Union[Unset, List[str]]): Optional list of checks to apply to datapoints in the filter
        project_id (Union[Unset, str]): Project ID these filters belong to
    """

    filters: List["FilterCondition"]
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    checks: Union[Unset, List[str]] = UNSET
    project_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
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

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        checks = cast(List[str], d.pop("checks", UNSET))

        project_id = d.pop("project_id", UNSET)

        datapoint_filter_create = cls(
            filters=filters,
            name=name,
            description=description,
            checks=checks,
            project_id=project_id,
        )

        datapoint_filter_create.additional_properties = d
        return datapoint_filter_create

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
