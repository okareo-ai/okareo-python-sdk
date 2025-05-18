from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_run_type import TestRunType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_run_payload_v2_api_keys_type_0 import TestRunPayloadV2ApiKeysType0
    from ..models.test_run_payload_v2_metrics_kwargs import TestRunPayloadV2MetricsKwargs
    from ..models.test_run_payload_v2_model_results_type_0 import TestRunPayloadV2ModelResultsType0


T = TypeVar("T", bound="TestRunPayloadV2")


@_attrs_define
class TestRunPayloadV2:
    """
    Attributes:
        mut_id (UUID): ID of the model
        scenario_id (UUID): ID of the scenario set
        api_keys (Union['TestRunPayloadV2ApiKeysType0', None, Unset]): Dictionary that maps model type to the respective
            API keys
        metrics_kwargs (Union[Unset, TestRunPayloadV2MetricsKwargs]): Dictionary of metrics to be measured
        name (Union[None, Unset, str]): Name of the test run
        type_ (Union[Unset, TestRunType]):
        calculate_metrics (Union[Unset, bool]): Boolean value indicating if metrics should be calculated for the test
            run Default: True.
        tags (Union[Unset, list[str]]): Tags are strings that can be used to filter test runs in the Okareo app
        model_results (Union['TestRunPayloadV2ModelResultsType0', None, Unset]):
        checks (Union[None, Unset, list[str]]): List of checks to include in the test run.
    """

    mut_id: UUID
    scenario_id: UUID
    api_keys: Union["TestRunPayloadV2ApiKeysType0", None, Unset] = UNSET
    metrics_kwargs: Union[Unset, "TestRunPayloadV2MetricsKwargs"] = UNSET
    name: Union[None, Unset, str] = UNSET
    type_: Union[Unset, TestRunType] = UNSET
    calculate_metrics: Union[Unset, bool] = True
    tags: Union[Unset, list[str]] = UNSET
    model_results: Union["TestRunPayloadV2ModelResultsType0", None, Unset] = UNSET
    checks: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.test_run_payload_v2_api_keys_type_0 import TestRunPayloadV2ApiKeysType0
        from ..models.test_run_payload_v2_model_results_type_0 import TestRunPayloadV2ModelResultsType0

        mut_id = str(self.mut_id)

        scenario_id = str(self.scenario_id)

        api_keys: Union[None, Unset, dict[str, Any]]
        if isinstance(self.api_keys, Unset):
            api_keys = UNSET
        elif isinstance(self.api_keys, TestRunPayloadV2ApiKeysType0):
            api_keys = self.api_keys.to_dict()
        else:
            api_keys = self.api_keys

        metrics_kwargs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics_kwargs, Unset):
            metrics_kwargs = self.metrics_kwargs.to_dict()

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        calculate_metrics = self.calculate_metrics

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        model_results: Union[None, Unset, dict[str, Any]]
        if isinstance(self.model_results, Unset):
            model_results = UNSET
        elif isinstance(self.model_results, TestRunPayloadV2ModelResultsType0):
            model_results = self.model_results.to_dict()
        else:
            model_results = self.model_results

        checks: Union[None, Unset, list[str]]
        if isinstance(self.checks, Unset):
            checks = UNSET
        elif isinstance(self.checks, list):
            checks = self.checks

        else:
            checks = self.checks

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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.test_run_payload_v2_api_keys_type_0 import TestRunPayloadV2ApiKeysType0
        from ..models.test_run_payload_v2_metrics_kwargs import TestRunPayloadV2MetricsKwargs
        from ..models.test_run_payload_v2_model_results_type_0 import TestRunPayloadV2ModelResultsType0

        d = dict(src_dict)
        mut_id = UUID(d.pop("mut_id"))

        scenario_id = UUID(d.pop("scenario_id"))

        def _parse_api_keys(data: object) -> Union["TestRunPayloadV2ApiKeysType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                api_keys_type_0 = TestRunPayloadV2ApiKeysType0.from_dict(data)

                return api_keys_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TestRunPayloadV2ApiKeysType0", None, Unset], data)

        api_keys = _parse_api_keys(d.pop("api_keys", UNSET))

        _metrics_kwargs = d.pop("metrics_kwargs", UNSET)
        metrics_kwargs: Union[Unset, TestRunPayloadV2MetricsKwargs]
        if isinstance(_metrics_kwargs, Unset):
            metrics_kwargs = UNSET
        else:
            metrics_kwargs = TestRunPayloadV2MetricsKwargs.from_dict(_metrics_kwargs)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, TestRunType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = TestRunType(_type_)

        calculate_metrics = d.pop("calculate_metrics", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_model_results(data: object) -> Union["TestRunPayloadV2ModelResultsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_results_type_0 = TestRunPayloadV2ModelResultsType0.from_dict(data)

                return model_results_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TestRunPayloadV2ModelResultsType0", None, Unset], data)

        model_results = _parse_model_results(d.pop("model_results", UNSET))

        def _parse_checks(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                checks_type_0 = cast(list[str], data)

                return checks_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        checks = _parse_checks(d.pop("checks", UNSET))

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
