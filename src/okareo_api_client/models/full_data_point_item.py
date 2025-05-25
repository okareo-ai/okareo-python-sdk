from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.full_data_point_item_metric_value import FullDataPointItemMetricValue
    from ..models.full_data_point_item_model_metadata_type_0 import FullDataPointItemModelMetadataType0
    from ..models.full_data_point_item_scenario_input_type_0 import FullDataPointItemScenarioInputType0
    from ..models.full_data_point_item_scenario_result_type_0 import FullDataPointItemScenarioResultType0


T = TypeVar("T", bound="FullDataPointItem")


@_attrs_define
class FullDataPointItem:
    """
    Attributes:
        id (UUID):
        test_run_id (UUID):
        metric_type (str):
        metric_value (FullDataPointItemMetricValue):
        tags (Union[Unset, list[str]]):
        scenario_data_point_id (Union[Unset, UUID]):
        model_input (Union[Unset, Any]):
        model_result (Union[Unset, Any]):
        scenario_input (Union['FullDataPointItemScenarioInputType0', Unset, list[Any], str]):
        scenario_result (Union['FullDataPointItemScenarioResultType0', Unset, list[Any], str]):
        model_metadata (Union['FullDataPointItemModelMetadataType0', Any, Unset]):
        time_created (Union[Unset, str]):
        checks (Union[Unset, Any]):
        end_time (Union[Unset, Any]):
    """

    id: UUID
    test_run_id: UUID
    metric_type: str
    metric_value: "FullDataPointItemMetricValue"
    tags: Union[Unset, list[str]] = UNSET
    scenario_data_point_id: Union[Unset, UUID] = UNSET
    model_input: Union[Unset, Any] = UNSET
    model_result: Union[Unset, Any] = UNSET
    scenario_input: Union["FullDataPointItemScenarioInputType0", Unset, list[Any], str] = UNSET
    scenario_result: Union["FullDataPointItemScenarioResultType0", Unset, list[Any], str] = UNSET
    model_metadata: Union["FullDataPointItemModelMetadataType0", Any, Unset] = UNSET
    time_created: Union[Unset, str] = UNSET
    checks: Union[Unset, Any] = UNSET
    end_time: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.full_data_point_item_model_metadata_type_0 import FullDataPointItemModelMetadataType0
        from ..models.full_data_point_item_scenario_input_type_0 import FullDataPointItemScenarioInputType0
        from ..models.full_data_point_item_scenario_result_type_0 import FullDataPointItemScenarioResultType0

        id = str(self.id)

        test_run_id = str(self.test_run_id)

        metric_type = self.metric_type

        metric_value = self.metric_value.to_dict()

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        scenario_data_point_id: Union[Unset, str] = UNSET
        if not isinstance(self.scenario_data_point_id, Unset):
            scenario_data_point_id = str(self.scenario_data_point_id)

        model_input = self.model_input

        model_result = self.model_result

        scenario_input: Union[Unset, dict[str, Any], list[Any], str]
        if isinstance(self.scenario_input, Unset):
            scenario_input = UNSET
        elif isinstance(self.scenario_input, FullDataPointItemScenarioInputType0):
            scenario_input = self.scenario_input.to_dict()
        elif isinstance(self.scenario_input, list):
            scenario_input = self.scenario_input

        else:
            scenario_input = self.scenario_input

        scenario_result: Union[Unset, dict[str, Any], list[Any], str]
        if isinstance(self.scenario_result, Unset):
            scenario_result = UNSET
        elif isinstance(self.scenario_result, FullDataPointItemScenarioResultType0):
            scenario_result = self.scenario_result.to_dict()
        elif isinstance(self.scenario_result, list):
            scenario_result = self.scenario_result

        else:
            scenario_result = self.scenario_result

        model_metadata: Union[Any, Unset, dict[str, Any]]
        if isinstance(self.model_metadata, Unset):
            model_metadata = UNSET
        elif isinstance(self.model_metadata, FullDataPointItemModelMetadataType0):
            model_metadata = self.model_metadata.to_dict()
        else:
            model_metadata = self.model_metadata

        time_created = self.time_created

        checks = self.checks

        end_time = self.end_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "test_run_id": test_run_id,
                "metric_type": metric_type,
                "metric_value": metric_value,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags
        if scenario_data_point_id is not UNSET:
            field_dict["scenario_data_point_id"] = scenario_data_point_id
        if model_input is not UNSET:
            field_dict["model_input"] = model_input
        if model_result is not UNSET:
            field_dict["model_result"] = model_result
        if scenario_input is not UNSET:
            field_dict["scenario_input"] = scenario_input
        if scenario_result is not UNSET:
            field_dict["scenario_result"] = scenario_result
        if model_metadata is not UNSET:
            field_dict["model_metadata"] = model_metadata
        if time_created is not UNSET:
            field_dict["time_created"] = time_created
        if checks is not UNSET:
            field_dict["checks"] = checks
        if end_time is not UNSET:
            field_dict["end_time"] = end_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.full_data_point_item_metric_value import FullDataPointItemMetricValue
        from ..models.full_data_point_item_model_metadata_type_0 import FullDataPointItemModelMetadataType0
        from ..models.full_data_point_item_scenario_input_type_0 import FullDataPointItemScenarioInputType0
        from ..models.full_data_point_item_scenario_result_type_0 import FullDataPointItemScenarioResultType0

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        test_run_id = UUID(d.pop("test_run_id"))

        metric_type = d.pop("metric_type")

        metric_value = FullDataPointItemMetricValue.from_dict(d.pop("metric_value"))

        tags = cast(list[str], d.pop("tags", UNSET))

        _scenario_data_point_id = d.pop("scenario_data_point_id", UNSET)
        scenario_data_point_id: Union[Unset, UUID]
        if isinstance(_scenario_data_point_id, Unset):
            scenario_data_point_id = UNSET
        else:
            scenario_data_point_id = UUID(_scenario_data_point_id)

        model_input = d.pop("model_input", UNSET)

        model_result = d.pop("model_result", UNSET)

        def _parse_scenario_input(data: object) -> Union["FullDataPointItemScenarioInputType0", Unset, list[Any], str]:
            if isinstance(data, Unset):
                return data
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
                scenario_input_type_1 = cast(list[Any], data)

                return scenario_input_type_1
            except:  # noqa: E722
                pass
            return cast(Union["FullDataPointItemScenarioInputType0", Unset, list[Any], str], data)

        scenario_input = _parse_scenario_input(d.pop("scenario_input", UNSET))

        def _parse_scenario_result(
            data: object,
        ) -> Union["FullDataPointItemScenarioResultType0", Unset, list[Any], str]:
            if isinstance(data, Unset):
                return data
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
                scenario_result_type_1 = cast(list[Any], data)

                return scenario_result_type_1
            except:  # noqa: E722
                pass
            return cast(Union["FullDataPointItemScenarioResultType0", Unset, list[Any], str], data)

        scenario_result = _parse_scenario_result(d.pop("scenario_result", UNSET))

        def _parse_model_metadata(data: object) -> Union["FullDataPointItemModelMetadataType0", Any, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_metadata_type_0 = FullDataPointItemModelMetadataType0.from_dict(data)

                return model_metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["FullDataPointItemModelMetadataType0", Any, Unset], data)

        model_metadata = _parse_model_metadata(d.pop("model_metadata", UNSET))

        time_created = d.pop("time_created", UNSET)

        checks = d.pop("checks", UNSET)

        end_time = d.pop("end_time", UNSET)

        full_data_point_item = cls(
            id=id,
            test_run_id=test_run_id,
            metric_type=metric_type,
            metric_value=metric_value,
            tags=tags,
            scenario_data_point_id=scenario_data_point_id,
            model_input=model_input,
            model_result=model_result,
            scenario_input=scenario_input,
            scenario_result=scenario_result,
            model_metadata=model_metadata,
            time_created=time_created,
            checks=checks,
            end_time=end_time,
        )

        full_data_point_item.additional_properties = d
        return full_data_point_item

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
