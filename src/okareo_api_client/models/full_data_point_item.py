from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.full_data_point_item_metric_value import FullDataPointItemMetricValue
    from ..models.full_data_point_item_model_metadata import FullDataPointItemModelMetadata
    from ..models.full_data_point_item_scenario_input_type_0 import FullDataPointItemScenarioInputType0
    from ..models.full_data_point_item_scenario_result_type_0 import FullDataPointItemScenarioResultType0


T = TypeVar("T", bound="FullDataPointItem")


@_attrs_define
class FullDataPointItem:
    """
    Attributes:
        id (str):
        scenario_data_point_id (str):
        test_run_id (str):
        metric_type (str):
        metric_value (FullDataPointItemMetricValue):
        scenario_input (Union['FullDataPointItemScenarioInputType0', List[Any], str]):
        scenario_result (Union['FullDataPointItemScenarioResultType0', List[Any], str]):
        tags (Union[Unset, List[str]]):
        model_input (Union[Unset, Any]):
        model_result (Union[Unset, Any]):
        model_metadata (Union[Unset, FullDataPointItemModelMetadata]):
    """

    id: str
    scenario_data_point_id: str
    test_run_id: str
    metric_type: str
    metric_value: "FullDataPointItemMetricValue"
    scenario_input: Union["FullDataPointItemScenarioInputType0", List[Any], str]
    scenario_result: Union["FullDataPointItemScenarioResultType0", List[Any], str]
    tags: Union[Unset, List[str]] = UNSET
    model_input: Union[Unset, Any] = UNSET
    model_result: Union[Unset, Any] = UNSET
    model_metadata: Union[Unset, "FullDataPointItemModelMetadata"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.full_data_point_item_scenario_input_type_0 import FullDataPointItemScenarioInputType0
        from ..models.full_data_point_item_scenario_result_type_0 import FullDataPointItemScenarioResultType0

        id = self.id
        scenario_data_point_id = self.scenario_data_point_id
        test_run_id = self.test_run_id
        metric_type = self.metric_type
        metric_value = self.metric_value.to_dict()

        scenario_input: Union[Dict[str, Any], List[Any], str]

        if isinstance(self.scenario_input, FullDataPointItemScenarioInputType0):
            scenario_input = self.scenario_input.to_dict()

        elif isinstance(self.scenario_input, list):
            scenario_input = self.scenario_input

        else:
            scenario_input = self.scenario_input

        scenario_result: Union[Dict[str, Any], List[Any], str]

        if isinstance(self.scenario_result, FullDataPointItemScenarioResultType0):
            scenario_result = self.scenario_result.to_dict()

        elif isinstance(self.scenario_result, list):
            scenario_result = self.scenario_result

        else:
            scenario_result = self.scenario_result

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        model_input = self.model_input
        model_result = self.model_result
        model_metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.model_metadata, Unset):
            model_metadata = self.model_metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "scenario_data_point_id": scenario_data_point_id,
                "test_run_id": test_run_id,
                "metric_type": metric_type,
                "metric_value": metric_value,
                "scenario_input": scenario_input,
                "scenario_result": scenario_result,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags
        if model_input is not UNSET:
            field_dict["model_input"] = model_input
        if model_result is not UNSET:
            field_dict["model_result"] = model_result
        if model_metadata is not UNSET:
            field_dict["model_metadata"] = model_metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.full_data_point_item_metric_value import FullDataPointItemMetricValue
        from ..models.full_data_point_item_model_metadata import FullDataPointItemModelMetadata
        from ..models.full_data_point_item_scenario_input_type_0 import FullDataPointItemScenarioInputType0
        from ..models.full_data_point_item_scenario_result_type_0 import FullDataPointItemScenarioResultType0

        d = src_dict.copy()
        id = d.pop("id")

        scenario_data_point_id = d.pop("scenario_data_point_id")

        test_run_id = d.pop("test_run_id")

        metric_type = d.pop("metric_type")

        metric_value = FullDataPointItemMetricValue.from_dict(d.pop("metric_value"))

        def _parse_scenario_input(data: object) -> Union["FullDataPointItemScenarioInputType0", List[Any], str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scenario_input_type_0 = FullDataPointItemScenarioInputType0.from_dict(data)

                return scenario_input_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scenario_input_type_1 = cast(List[Any], data)

                return scenario_input_type_1
            except:  # noqa: E722
                pass
            return cast(Union["FullDataPointItemScenarioInputType0", List[Any], str], data)

        scenario_input = _parse_scenario_input(d.pop("scenario_input"))

        def _parse_scenario_result(data: object) -> Union["FullDataPointItemScenarioResultType0", List[Any], str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scenario_result_type_0 = FullDataPointItemScenarioResultType0.from_dict(data)

                return scenario_result_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scenario_result_type_1 = cast(List[Any], data)

                return scenario_result_type_1
            except:  # noqa: E722
                pass
            return cast(Union["FullDataPointItemScenarioResultType0", List[Any], str], data)

        scenario_result = _parse_scenario_result(d.pop("scenario_result"))

        tags = cast(List[str], d.pop("tags", UNSET))

        model_input = d.pop("model_input", UNSET)

        model_result = d.pop("model_result", UNSET)

        _model_metadata = d.pop("model_metadata", UNSET)
        model_metadata: Union[Unset, FullDataPointItemModelMetadata]
        if isinstance(_model_metadata, Unset):
            model_metadata = UNSET
        else:
            model_metadata = FullDataPointItemModelMetadata.from_dict(_model_metadata)

        full_data_point_item = cls(
            id=id,
            scenario_data_point_id=scenario_data_point_id,
            test_run_id=test_run_id,
            metric_type=metric_type,
            metric_value=metric_value,
            scenario_input=scenario_input,
            scenario_result=scenario_result,
            tags=tags,
            model_input=model_input,
            model_result=model_result,
            model_metadata=model_metadata,
        )

        full_data_point_item.additional_properties = d
        return full_data_point_item

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
