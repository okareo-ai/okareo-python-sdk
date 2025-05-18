from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
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
        tags (Union[None, Unset, list[str]]):
        checks (Union[Unset, Any]):
    """

    id: UUID
    scenario_data_point_id: UUID
    test_run_id: UUID
    metric_type: str
    metric_value: "TestDataPointItemMetricValue"
    tags: Union[None, Unset, list[str]] = UNSET
    checks: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        scenario_data_point_id = str(self.scenario_data_point_id)

        test_run_id = str(self.test_run_id)

        metric_type = self.metric_type

        metric_value = self.metric_value.to_dict()

        tags: Union[None, Unset, list[str]]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        checks = self.checks

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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.test_data_point_item_metric_value import TestDataPointItemMetricValue

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        scenario_data_point_id = UUID(d.pop("scenario_data_point_id"))

        test_run_id = UUID(d.pop("test_run_id"))

        metric_type = d.pop("metric_type")

        metric_value = TestDataPointItemMetricValue.from_dict(d.pop("metric_value"))

        def _parse_tags(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        tags = _parse_tags(d.pop("tags", UNSET))

        checks = d.pop("checks", UNSET)

        test_data_point_item = cls(
            id=id,
            scenario_data_point_id=scenario_data_point_id,
            test_run_id=test_run_id,
            metric_type=metric_type,
            metric_value=metric_value,
            tags=tags,
            checks=checks,
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
