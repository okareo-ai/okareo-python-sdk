from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.full_data_point_item_baseline_metrics_type_0 import FullDataPointItemBaselineMetricsType0
    from ..models.full_data_point_item_checks_metadata_type_0 import FullDataPointItemChecksMetadataType0
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
        tags (list[str] | None | Unset):
        scenario_data_point_id (None | Unset | UUID):
        model_input (Any | None | Unset):
        model_result (Any | None | Unset):
        scenario_input (FullDataPointItemScenarioInputType0 | list[Any] | None | str | Unset):
        scenario_result (FullDataPointItemScenarioResultType0 | list[Any] | None | str | Unset):
        model_metadata (Any | FullDataPointItemModelMetadataType0 | None | Unset):
        time_created (None | str | Unset):
        checks (Any | Unset):
        checks_metadata (FullDataPointItemChecksMetadataType0 | None | Unset):
        end_time (Any | None | Unset):
        driver_prompt (None | str | Unset):
        baseline_metrics (FullDataPointItemBaselineMetricsType0 | None | Unset):
        error_message (None | str | Unset):
        error_code (None | str | Unset):
        error_type (None | str | Unset):
        context_token (None | str | Unset):
    """

    id: UUID
    test_run_id: UUID
    metric_type: str
    metric_value: FullDataPointItemMetricValue
    tags: list[str] | None | Unset = UNSET
    scenario_data_point_id: None | Unset | UUID = UNSET
    model_input: Any | None | Unset = UNSET
    model_result: Any | None | Unset = UNSET
    scenario_input: FullDataPointItemScenarioInputType0 | list[Any] | None | str | Unset = UNSET
    scenario_result: FullDataPointItemScenarioResultType0 | list[Any] | None | str | Unset = UNSET
    model_metadata: Any | FullDataPointItemModelMetadataType0 | None | Unset = UNSET
    time_created: None | str | Unset = UNSET
    checks: Any | Unset = UNSET
    checks_metadata: FullDataPointItemChecksMetadataType0 | None | Unset = UNSET
    end_time: Any | None | Unset = UNSET
    driver_prompt: None | str | Unset = UNSET
    baseline_metrics: FullDataPointItemBaselineMetricsType0 | None | Unset = UNSET
    error_message: None | str | Unset = UNSET
    error_code: None | str | Unset = UNSET
    error_type: None | str | Unset = UNSET
    context_token: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.full_data_point_item_baseline_metrics_type_0 import FullDataPointItemBaselineMetricsType0
        from ..models.full_data_point_item_checks_metadata_type_0 import FullDataPointItemChecksMetadataType0
        from ..models.full_data_point_item_model_metadata_type_0 import FullDataPointItemModelMetadataType0
        from ..models.full_data_point_item_scenario_input_type_0 import FullDataPointItemScenarioInputType0
        from ..models.full_data_point_item_scenario_result_type_0 import FullDataPointItemScenarioResultType0

        id = str(self.id)

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

        scenario_data_point_id: None | str | Unset
        if isinstance(self.scenario_data_point_id, Unset):
            scenario_data_point_id = UNSET
        elif isinstance(self.scenario_data_point_id, UUID):
            scenario_data_point_id = str(self.scenario_data_point_id)
        else:
            scenario_data_point_id = self.scenario_data_point_id

        model_input: Any | None | Unset
        if isinstance(self.model_input, Unset):
            model_input = UNSET
        else:
            model_input = self.model_input

        model_result: Any | None | Unset
        if isinstance(self.model_result, Unset):
            model_result = UNSET
        else:
            model_result = self.model_result

        scenario_input: dict[str, Any] | list[Any] | None | str | Unset
        if isinstance(self.scenario_input, Unset):
            scenario_input = UNSET
        elif isinstance(self.scenario_input, FullDataPointItemScenarioInputType0):
            scenario_input = self.scenario_input.to_dict()
        elif isinstance(self.scenario_input, list):
            scenario_input = self.scenario_input

        else:
            scenario_input = self.scenario_input

        scenario_result: dict[str, Any] | list[Any] | None | str | Unset
        if isinstance(self.scenario_result, Unset):
            scenario_result = UNSET
        elif isinstance(self.scenario_result, FullDataPointItemScenarioResultType0):
            scenario_result = self.scenario_result.to_dict()
        elif isinstance(self.scenario_result, list):
            scenario_result = self.scenario_result

        else:
            scenario_result = self.scenario_result

        model_metadata: Any | dict[str, Any] | None | Unset
        if isinstance(self.model_metadata, Unset):
            model_metadata = UNSET
        elif isinstance(self.model_metadata, FullDataPointItemModelMetadataType0):
            model_metadata = self.model_metadata.to_dict()
        else:
            model_metadata = self.model_metadata

        time_created: None | str | Unset
        if isinstance(self.time_created, Unset):
            time_created = UNSET
        else:
            time_created = self.time_created

        checks = self.checks

        checks_metadata: dict[str, Any] | None | Unset
        if isinstance(self.checks_metadata, Unset):
            checks_metadata = UNSET
        elif isinstance(self.checks_metadata, FullDataPointItemChecksMetadataType0):
            checks_metadata = self.checks_metadata.to_dict()
        else:
            checks_metadata = self.checks_metadata

        end_time: Any | None | Unset
        if isinstance(self.end_time, Unset):
            end_time = UNSET
        else:
            end_time = self.end_time

        driver_prompt: None | str | Unset
        if isinstance(self.driver_prompt, Unset):
            driver_prompt = UNSET
        else:
            driver_prompt = self.driver_prompt

        baseline_metrics: dict[str, Any] | None | Unset
        if isinstance(self.baseline_metrics, Unset):
            baseline_metrics = UNSET
        elif isinstance(self.baseline_metrics, FullDataPointItemBaselineMetricsType0):
            baseline_metrics = self.baseline_metrics.to_dict()
        else:
            baseline_metrics = self.baseline_metrics

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        error_code: None | str | Unset
        if isinstance(self.error_code, Unset):
            error_code = UNSET
        else:
            error_code = self.error_code

        error_type: None | str | Unset
        if isinstance(self.error_type, Unset):
            error_type = UNSET
        else:
            error_type = self.error_type

        context_token: None | str | Unset
        if isinstance(self.context_token, Unset):
            context_token = UNSET
        else:
            context_token = self.context_token

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
        if checks_metadata is not UNSET:
            field_dict["checks_metadata"] = checks_metadata
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if driver_prompt is not UNSET:
            field_dict["driver_prompt"] = driver_prompt
        if baseline_metrics is not UNSET:
            field_dict["baseline_metrics"] = baseline_metrics
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if error_type is not UNSET:
            field_dict["error_type"] = error_type
        if context_token is not UNSET:
            field_dict["context_token"] = context_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.full_data_point_item_baseline_metrics_type_0 import FullDataPointItemBaselineMetricsType0
        from ..models.full_data_point_item_checks_metadata_type_0 import FullDataPointItemChecksMetadataType0
        from ..models.full_data_point_item_metric_value import FullDataPointItemMetricValue
        from ..models.full_data_point_item_model_metadata_type_0 import FullDataPointItemModelMetadataType0
        from ..models.full_data_point_item_scenario_input_type_0 import FullDataPointItemScenarioInputType0
        from ..models.full_data_point_item_scenario_result_type_0 import FullDataPointItemScenarioResultType0

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        test_run_id = UUID(d.pop("test_run_id"))

        metric_type = d.pop("metric_type")

        metric_value = FullDataPointItemMetricValue.from_dict(d.pop("metric_value"))

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

        def _parse_scenario_data_point_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scenario_data_point_id_type_0 = UUID(data)

                return scenario_data_point_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        scenario_data_point_id = _parse_scenario_data_point_id(d.pop("scenario_data_point_id", UNSET))

        def _parse_model_input(data: object) -> Any | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | None | Unset, data)

        model_input = _parse_model_input(d.pop("model_input", UNSET))

        def _parse_model_result(data: object) -> Any | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | None | Unset, data)

        model_result = _parse_model_result(d.pop("model_result", UNSET))

        def _parse_scenario_input(data: object) -> FullDataPointItemScenarioInputType0 | list[Any] | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scenario_input_type_0 = FullDataPointItemScenarioInputType0.from_dict(data)

                return scenario_input_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scenario_input_type_1 = cast(list[Any], data)

                return scenario_input_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FullDataPointItemScenarioInputType0 | list[Any] | None | str | Unset, data)

        scenario_input = _parse_scenario_input(d.pop("scenario_input", UNSET))

        def _parse_scenario_result(
            data: object,
        ) -> FullDataPointItemScenarioResultType0 | list[Any] | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scenario_result_type_0 = FullDataPointItemScenarioResultType0.from_dict(data)

                return scenario_result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scenario_result_type_1 = cast(list[Any], data)

                return scenario_result_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FullDataPointItemScenarioResultType0 | list[Any] | None | str | Unset, data)

        scenario_result = _parse_scenario_result(d.pop("scenario_result", UNSET))

        def _parse_model_metadata(data: object) -> Any | FullDataPointItemModelMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_metadata_type_0 = FullDataPointItemModelMetadataType0.from_dict(data)

                return model_metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Any | FullDataPointItemModelMetadataType0 | None | Unset, data)

        model_metadata = _parse_model_metadata(d.pop("model_metadata", UNSET))

        def _parse_time_created(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        time_created = _parse_time_created(d.pop("time_created", UNSET))

        checks = d.pop("checks", UNSET)

        def _parse_checks_metadata(data: object) -> FullDataPointItemChecksMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                checks_metadata_type_0 = FullDataPointItemChecksMetadataType0.from_dict(data)

                return checks_metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FullDataPointItemChecksMetadataType0 | None | Unset, data)

        checks_metadata = _parse_checks_metadata(d.pop("checks_metadata", UNSET))

        def _parse_end_time(data: object) -> Any | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | None | Unset, data)

        end_time = _parse_end_time(d.pop("end_time", UNSET))

        def _parse_driver_prompt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        driver_prompt = _parse_driver_prompt(d.pop("driver_prompt", UNSET))

        def _parse_baseline_metrics(data: object) -> FullDataPointItemBaselineMetricsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                baseline_metrics_type_0 = FullDataPointItemBaselineMetricsType0.from_dict(data)

                return baseline_metrics_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FullDataPointItemBaselineMetricsType0 | None | Unset, data)

        baseline_metrics = _parse_baseline_metrics(d.pop("baseline_metrics", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_error_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_code = _parse_error_code(d.pop("error_code", UNSET))

        def _parse_error_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_type = _parse_error_type(d.pop("error_type", UNSET))

        def _parse_context_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        context_token = _parse_context_token(d.pop("context_token", UNSET))

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
            checks_metadata=checks_metadata,
            end_time=end_time,
            driver_prompt=driver_prompt,
            baseline_metrics=baseline_metrics,
            error_message=error_message,
            error_code=error_code,
            error_type=error_type,
            context_token=context_token,
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
