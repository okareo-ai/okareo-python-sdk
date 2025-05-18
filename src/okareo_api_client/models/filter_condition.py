from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.comparison_operator import ComparisonOperator
from ..models.datapoint_field import DatapointField
from ..types import UNSET, Unset

T = TypeVar("T", bound="FilterCondition")


@_attrs_define
class FilterCondition:
    """
    Attributes:
        field (DatapointField):
        operator (ComparisonOperator):
        value (str): Value to compare against
        field_key (Union[None, Unset, str]): Key of the User Metadata field to filter on. Ignored for other 'field'
            values
    """

    field: DatapointField
    operator: ComparisonOperator
    value: str
    field_key: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field = self.field.value

        operator = self.operator.value

        value = self.value

        field_key: Union[None, Unset, str]
        if isinstance(self.field_key, Unset):
            field_key = UNSET
        else:
            field_key = self.field_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field": field,
                "operator": operator,
                "value": value,
            }
        )
        if field_key is not UNSET:
            field_dict["field_key"] = field_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field = DatapointField(d.pop("field"))

        operator = ComparisonOperator(d.pop("operator"))

        value = d.pop("value")

        def _parse_field_key(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        field_key = _parse_field_key(d.pop("field_key", UNSET))

        filter_condition = cls(
            field=field,
            operator=operator,
            value=value,
            field_key=field_key,
        )

        filter_condition.additional_properties = d
        return filter_condition

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
