from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_run_type import TestRunType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_run_payload_v2_api_keys import TestRunPayloadV2ApiKeys
    from ..models.test_run_payload_v2_metrics_kwargs import TestRunPayloadV2MetricsKwargs
    from ..models.test_run_payload_v2_model_results import TestRunPayloadV2ModelResults


T = TypeVar("T", bound="TestRunPayloadV2")


@_attrs_define
class TestRunPayloadV2:
    """
    Attributes:
        mut_id (str): ID of the model
        scenario_id (str): ID of the scenario set
        api_keys (Union[Unset, TestRunPayloadV2ApiKeys]): Dictionary that maps model type to the respective API keys
        metrics_kwargs (Union[Unset, TestRunPayloadV2MetricsKwargs]): Dictionary of metrics to be measured
        name (Union[Unset, str]): Name of the test run
        type (Union[Unset, TestRunType]): An enumeration. Default: TestRunType.MULTI_CLASS_CLASSIFICATION.
        calculate_metrics (Union[Unset, bool]): Boolean value indicating if metrics should be calculated for the test
            run Default: True.
        tags (Union[Unset, List[str]]): Tags are strings that can be used to filter test runs in the Okareo app
        model_results (Union[Unset, TestRunPayloadV2ModelResults]):
        checks (Union[Unset, List[str]]): List of checks to include in the test run.
    """

    mut_id: str
    scenario_id: str
    api_keys: Union[Unset, "TestRunPayloadV2ApiKeys"] = UNSET
    metrics_kwargs: Union[Unset, "TestRunPayloadV2MetricsKwargs"] = UNSET
    name: Union[Unset, str] = UNSET
    type: Union[Unset, TestRunType] = TestRunType.MULTI_CLASS_CLASSIFICATION
    calculate_metrics: Union[Unset, bool] = True
    tags: Union[Unset, List[str]] = UNSET
    model_results: Union[Unset, "TestRunPayloadV2ModelResults"] = UNSET
    checks: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mut_id = self.mut_id
        scenario_id = self.scenario_id
        api_keys: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.api_keys, Unset):
            api_keys = self.api_keys.to_dict()

        metrics_kwargs: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metrics_kwargs, Unset):
            metrics_kwargs = self.metrics_kwargs.to_dict()

        name = self.name
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        calculate_metrics = self.calculate_metrics
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        model_results: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.model_results, Unset):
            model_results = self.model_results.to_dict()

        checks: Union[Unset, List[str]] = UNSET
        if not isinstance(self.checks, Unset):
            checks = self.checks

        field_dict: Dict[str, Any] = {}
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
        if type is not UNSET:
            field_dict["type"] = type
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
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_run_payload_v2_api_keys import TestRunPayloadV2ApiKeys
        from ..models.test_run_payload_v2_metrics_kwargs import TestRunPayloadV2MetricsKwargs
        from ..models.test_run_payload_v2_model_results import TestRunPayloadV2ModelResults

        d = src_dict.copy()
        mut_id = d.pop("mut_id")

        scenario_id = d.pop("scenario_id")

        _api_keys = d.pop("api_keys", UNSET)
        api_keys: Union[Unset, TestRunPayloadV2ApiKeys]
        if isinstance(_api_keys, Unset):
            api_keys = UNSET
        else:
            api_keys = TestRunPayloadV2ApiKeys.from_dict(_api_keys)

        _metrics_kwargs = d.pop("metrics_kwargs", UNSET)
        metrics_kwargs: Union[Unset, TestRunPayloadV2MetricsKwargs]
        if isinstance(_metrics_kwargs, Unset):
            metrics_kwargs = UNSET
        else:
            metrics_kwargs = TestRunPayloadV2MetricsKwargs.from_dict(_metrics_kwargs)

        name = d.pop("name", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, TestRunType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = TestRunType(_type)

        calculate_metrics = d.pop("calculate_metrics", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        _model_results = d.pop("model_results", UNSET)
        model_results: Union[Unset, TestRunPayloadV2ModelResults]
        if isinstance(_model_results, Unset):
            model_results = UNSET
        else:
            model_results = TestRunPayloadV2ModelResults.from_dict(_model_results)

        checks = cast(List[str], d.pop("checks", UNSET))

        test_run_payload_v2 = cls(
            mut_id=mut_id,
            scenario_id=scenario_id,
            api_keys=api_keys,
            metrics_kwargs=metrics_kwargs,
            name=name,
            type=type,
            calculate_metrics=calculate_metrics,
            tags=tags,
            model_results=model_results,
            checks=checks,
        )

        test_run_payload_v2.additional_properties = d
        return test_run_payload_v2

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
