from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.check_value_item import CheckValueItem
    from ..models.test_data_point_item_metric_value import TestDataPointItemMetricValue


T = TypeVar("T", bound="TestDataPointItem")


@_attrs_define
class TestDataPointItem:
    """
    Attributes:
        id (UUID):
        scenario_data_point_id (UUID):
        test_run_id (UUID):
        metric_type (str):
        metric_value (TestDataPointItemMetricValue):
        tags (list[str] | None | Unset):
        checks (Any | Unset):
        check_values (list[CheckValueItem] | None | Unset):
    """

    id: UUID
    scenario_data_point_id: UUID
    test_run_id: UUID
    metric_type: str
    metric_value: TestDataPointItemMetricValue
    tags: list[str] | None | Unset = UNSET
    checks: Any | Unset = UNSET
    check_values: list[CheckValueItem] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        scenario_data_point_id = str(self.scenario_data_point_id)

        test_run_id = str(self.test_run_id)

        metric_type = self.metric_type

        metric_value = self.metric_value.to_dict()

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        checks = self.checks

        check_values: list[dict[str, Any]] | None | Unset
        if isinstance(self.check_values, Unset):
            check_values = UNSET
        elif isinstance(self.check_values, list):
            check_values = []
            for check_values_type_0_item_data in self.check_values:
                check_values_type_0_item = check_values_type_0_item_data.to_dict()
                check_values.append(check_values_type_0_item)

        else:
            check_values = self.check_values

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "scenario_data_point_id": scenario_data_point_id,
                "test_run_id": test_run_id,
                "metric_type": metric_type,
                "metric_value": metric_value,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags
        if checks is not UNSET:
            field_dict["checks"] = checks
        if check_values is not UNSET:
            field_dict["check_values"] = check_values

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.check_value_item import CheckValueItem
        from ..models.test_data_point_item_metric_value import TestDataPointItemMetricValue

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        scenario_data_point_id = UUID(d.pop("scenario_data_point_id"))

        test_run_id = UUID(d.pop("test_run_id"))

        metric_type = d.pop("metric_type")

        metric_value = TestDataPointItemMetricValue.from_dict(d.pop("metric_value"))

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        checks = d.pop("checks", UNSET)

        def _parse_check_values(data: object) -> list[CheckValueItem] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                check_values_type_0 = []
                _check_values_type_0 = data
                for check_values_type_0_item_data in _check_values_type_0:
                    check_values_type_0_item = CheckValueItem.from_dict(check_values_type_0_item_data)

                    check_values_type_0.append(check_values_type_0_item)

                return check_values_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CheckValueItem] | None | Unset, data)

        check_values = _parse_check_values(d.pop("check_values", UNSET))

        test_data_point_item = cls(
            id=id,
            scenario_data_point_id=scenario_data_point_id,
            test_run_id=test_run_id,
            metric_type=metric_type,
            metric_value=metric_value,
            tags=tags,
            checks=checks,
            check_values=check_values,
        )

        test_data_point_item.additional_properties = d
        return test_data_point_item

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
