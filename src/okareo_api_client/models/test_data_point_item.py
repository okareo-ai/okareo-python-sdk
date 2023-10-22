from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.test_data_point_item_metric_value import TestDataPointItemMetricValue


T = TypeVar("T", bound="TestDataPointItem")


@_attrs_define
class TestDataPointItem:
    """
    Attributes:
        id (str):
        scenario_data_point_id (str):
        test_run_id (str):
        metric_type (str):
        metric_value (TestDataPointItemMetricValue):
    """

    id: str
    scenario_data_point_id: str
    test_run_id: str
    metric_type: str
    metric_value: "TestDataPointItemMetricValue"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        scenario_data_point_id = self.scenario_data_point_id
        test_run_id = self.test_run_id
        metric_type = self.metric_type
        metric_value = self.metric_value.to_dict()

        field_dict: Dict[str, Any] = {}
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_data_point_item_metric_value import TestDataPointItemMetricValue

        d = src_dict.copy()
        id = d.pop("id")

        scenario_data_point_id = d.pop("scenario_data_point_id")

        test_run_id = d.pop("test_run_id")

        metric_type = d.pop("metric_type")

        metric_value = TestDataPointItemMetricValue.from_dict(d.pop("metric_value"))

        test_data_point_item = cls(
            id=id,
            scenario_data_point_id=scenario_data_point_id,
            test_run_id=test_run_id,
            metric_type=metric_type,
            metric_value=metric_value,
        )

        test_data_point_item.additional_properties = d
        return test_data_point_item

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
