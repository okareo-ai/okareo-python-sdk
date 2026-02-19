from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_run_type import TestRunType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_run_payload_v2_api_keys import TestRunPayloadV2ApiKeys
    from ..models.test_run_payload_v2_metrics_kwargs import TestRunPayloadV2MetricsKwargs
    from ..models.test_run_payload_v2_model_results import TestRunPayloadV2ModelResults
    from ..models.test_run_payload_v2_simulation_params import TestRunPayloadV2SimulationParams


T = TypeVar("T", bound="TestRunPayloadV2")


@_attrs_define
class TestRunPayloadV2:
    """
    Attributes:
        mut_id (UUID): ID of the model
        scenario_id (UUID): ID of the scenario set
        api_keys (None | TestRunPayloadV2ApiKeys | Unset): Dictionary that maps model type to the respective API keys
        metrics_kwargs (TestRunPayloadV2MetricsKwargs | Unset): Dictionary of metrics to be measured
        name (None | str | Unset): Name of the test run
        type_ (TestRunType | Unset): An enumeration. Default: TestRunType.MULTI_CLASS_CLASSIFICATION.
        calculate_metrics (bool | Unset): Boolean value indicating if metrics should be calculated for the test run
            Default: True.
        tags (list[str] | Unset): Tags are strings that can be used to filter test runs in the Okareo app
        model_results (None | TestRunPayloadV2ModelResults | Unset):
        checks (list[str] | None | Unset): List of checks to include in the test run.
        simulation_params (None | TestRunPayloadV2SimulationParams | Unset): Simulation parameters for the test run.
        driver_id (None | Unset | UUID): ID of the driver model to use, if applicable.
        nats_invoke_id (None | str | Unset): Optional custom NATS invoke ID for the mut evaluation.
    """

    mut_id: UUID
    scenario_id: UUID
    api_keys: None | TestRunPayloadV2ApiKeys | Unset = UNSET
    metrics_kwargs: TestRunPayloadV2MetricsKwargs | Unset = UNSET
    name: None | str | Unset = UNSET
    type_: TestRunType | Unset = TestRunType.MULTI_CLASS_CLASSIFICATION
    calculate_metrics: bool | Unset = True
    tags: list[str] | Unset = UNSET
    model_results: None | TestRunPayloadV2ModelResults | Unset = UNSET
    checks: list[str] | None | Unset = UNSET
    simulation_params: None | TestRunPayloadV2SimulationParams | Unset = UNSET
    driver_id: None | Unset | UUID = UNSET
    nats_invoke_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.test_run_payload_v2_api_keys import TestRunPayloadV2ApiKeys
        from ..models.test_run_payload_v2_model_results import TestRunPayloadV2ModelResults
        from ..models.test_run_payload_v2_simulation_params import TestRunPayloadV2SimulationParams

        mut_id = str(self.mut_id)

        scenario_id = str(self.scenario_id)

        api_keys: dict[str, Any] | None | Unset
        if isinstance(self.api_keys, Unset):
            api_keys = UNSET
        elif isinstance(self.api_keys, TestRunPayloadV2ApiKeys):
            api_keys = self.api_keys.to_dict()
        else:
            api_keys = self.api_keys

        metrics_kwargs: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metrics_kwargs, Unset):
            metrics_kwargs = self.metrics_kwargs.to_dict()

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        calculate_metrics = self.calculate_metrics

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        model_results: dict[str, Any] | None | Unset
        if isinstance(self.model_results, Unset):
            model_results = UNSET
        elif isinstance(self.model_results, TestRunPayloadV2ModelResults):
            model_results = self.model_results.to_dict()
        else:
            model_results = self.model_results

        checks: list[str] | None | Unset
        if isinstance(self.checks, Unset):
            checks = UNSET
        elif isinstance(self.checks, list):
            checks = self.checks

        else:
            checks = self.checks

        simulation_params: dict[str, Any] | None | Unset
        if isinstance(self.simulation_params, Unset):
            simulation_params = UNSET
        elif isinstance(self.simulation_params, TestRunPayloadV2SimulationParams):
            simulation_params = self.simulation_params.to_dict()
        else:
            simulation_params = self.simulation_params

        driver_id: None | str | Unset
        if isinstance(self.driver_id, Unset):
            driver_id = UNSET
        elif isinstance(self.driver_id, UUID):
            driver_id = str(self.driver_id)
        else:
            driver_id = self.driver_id

        nats_invoke_id: None | str | Unset
        if isinstance(self.nats_invoke_id, Unset):
            nats_invoke_id = UNSET
        else:
            nats_invoke_id = self.nats_invoke_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mut_id": mut_id,
                "scenario_id": scenario_id,
            }
        )
        if api_keys is not UNSET:
            field_dict["api_keys"] = api_keys
        if metrics_kwargs is not UNSET:
            field_dict["metrics_kwargs"] = metrics_kwargs
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_
        if calculate_metrics is not UNSET:
            field_dict["calculate_metrics"] = calculate_metrics
        if tags is not UNSET:
            field_dict["tags"] = tags
        if model_results is not UNSET:
            field_dict["model_results"] = model_results
        if checks is not UNSET:
            field_dict["checks"] = checks
        if simulation_params is not UNSET:
            field_dict["simulation_params"] = simulation_params
        if driver_id is not UNSET:
            field_dict["driver_id"] = driver_id
        if nats_invoke_id is not UNSET:
            field_dict["nats_invoke_id"] = nats_invoke_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.test_run_payload_v2_api_keys import TestRunPayloadV2ApiKeys
        from ..models.test_run_payload_v2_metrics_kwargs import TestRunPayloadV2MetricsKwargs
        from ..models.test_run_payload_v2_model_results import TestRunPayloadV2ModelResults
        from ..models.test_run_payload_v2_simulation_params import TestRunPayloadV2SimulationParams

        d = dict(src_dict)
        mut_id = UUID(d.pop("mut_id"))

        scenario_id = UUID(d.pop("scenario_id"))

        def _parse_api_keys(data: object) -> None | TestRunPayloadV2ApiKeys | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                api_keys_type_0 = TestRunPayloadV2ApiKeys.from_dict(data)

                return api_keys_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TestRunPayloadV2ApiKeys | Unset, data)

        api_keys = _parse_api_keys(d.pop("api_keys", UNSET))

        _metrics_kwargs = d.pop("metrics_kwargs", UNSET)
        metrics_kwargs: TestRunPayloadV2MetricsKwargs | Unset
        if isinstance(_metrics_kwargs, Unset):
            metrics_kwargs = UNSET
        else:
            metrics_kwargs = TestRunPayloadV2MetricsKwargs.from_dict(_metrics_kwargs)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        _type_ = d.pop("type", UNSET)
        type_: TestRunType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = TestRunType(_type_)

        calculate_metrics = d.pop("calculate_metrics", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_model_results(data: object) -> None | TestRunPayloadV2ModelResults | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_results_type_0 = TestRunPayloadV2ModelResults.from_dict(data)

                return model_results_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TestRunPayloadV2ModelResults | Unset, data)

        model_results = _parse_model_results(d.pop("model_results", UNSET))

        def _parse_checks(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                checks_type_0 = cast(list[str], data)

                return checks_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        checks = _parse_checks(d.pop("checks", UNSET))

        def _parse_simulation_params(data: object) -> None | TestRunPayloadV2SimulationParams | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                simulation_params_type_0 = TestRunPayloadV2SimulationParams.from_dict(data)

                return simulation_params_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TestRunPayloadV2SimulationParams | Unset, data)

        simulation_params = _parse_simulation_params(d.pop("simulation_params", UNSET))

        def _parse_driver_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                driver_id_type_0 = UUID(data)

                return driver_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        driver_id = _parse_driver_id(d.pop("driver_id", UNSET))

        def _parse_nats_invoke_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        nats_invoke_id = _parse_nats_invoke_id(d.pop("nats_invoke_id", UNSET))

        test_run_payload_v2 = cls(
            mut_id=mut_id,
            scenario_id=scenario_id,
            api_keys=api_keys,
            metrics_kwargs=metrics_kwargs,
            name=name,
            type_=type_,
            calculate_metrics=calculate_metrics,
            tags=tags,
            model_results=model_results,
            checks=checks,
            simulation_params=simulation_params,
            driver_id=driver_id,
            nats_invoke_id=nats_invoke_id,
        )

        test_run_payload_v2.additional_properties = d
        return test_run_payload_v2

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
