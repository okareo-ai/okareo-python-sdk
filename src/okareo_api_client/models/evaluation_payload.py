from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_run_type import TestRunType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.evaluation_payload_metrics_kwargs import EvaluationPayloadMetricsKwargs


T = TypeVar("T", bound="EvaluationPayload")


@_attrs_define
class EvaluationPayload:
    """
    Attributes:
        scenario_id (Union[Unset, str]): ID of the scenario set to evaluate
        datapoint_ids (Union[Unset, List[str]]): List of datapoint IDs to filter by
        metrics_kwargs (Union[Unset, EvaluationPayloadMetricsKwargs]): Dictionary of metrics to be measured
        filter_group_id (Union[Unset, str]): ID of the datapoint filter group to apply
        tags (Union[Unset, List[str]]): Tags are strings that can be used to filter test runs in the Okareo app
        checks (Union[Unset, List[str]]): List of checks to include in the test run.
        type (Union[Unset, TestRunType]): An enumeration. Default: TestRunType.MULTI_CLASS_CLASSIFICATION.
        name (Union[Unset, str]): Name of the test run
        project_id (Union[Unset, str]): Project ID
    """

    scenario_id: Union[Unset, str] = UNSET
    datapoint_ids: Union[Unset, List[str]] = UNSET
    metrics_kwargs: Union[Unset, "EvaluationPayloadMetricsKwargs"] = UNSET
    filter_group_id: Union[Unset, str] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    checks: Union[Unset, List[str]] = UNSET
    type: Union[Unset, TestRunType] = TestRunType.MULTI_CLASS_CLASSIFICATION
    name: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scenario_id = self.scenario_id
        datapoint_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.datapoint_ids, Unset):
            datapoint_ids = self.datapoint_ids

        metrics_kwargs: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metrics_kwargs, Unset):
            metrics_kwargs = self.metrics_kwargs.to_dict()

        filter_group_id = self.filter_group_id
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        checks: Union[Unset, List[str]] = UNSET
        if not isinstance(self.checks, Unset):
            checks = self.checks

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        name = self.name
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if scenario_id is not UNSET:
            field_dict["scenario_id"] = scenario_id
        if datapoint_ids is not UNSET:
            field_dict["datapoint_ids"] = datapoint_ids
        if metrics_kwargs is not UNSET:
            field_dict["metrics_kwargs"] = metrics_kwargs
        if filter_group_id is not UNSET:
            field_dict["filter_group_id"] = filter_group_id
        if tags is not UNSET:
            field_dict["tags"] = tags
        if checks is not UNSET:
            field_dict["checks"] = checks
        if type is not UNSET:
            field_dict["type"] = type
        if name is not UNSET:
            field_dict["name"] = name
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.evaluation_payload_metrics_kwargs import EvaluationPayloadMetricsKwargs

        d = src_dict.copy()
        scenario_id = d.pop("scenario_id", UNSET)

        datapoint_ids = cast(List[str], d.pop("datapoint_ids", UNSET))

        _metrics_kwargs = d.pop("metrics_kwargs", UNSET)
        metrics_kwargs: Union[Unset, EvaluationPayloadMetricsKwargs]
        if isinstance(_metrics_kwargs, Unset):
            metrics_kwargs = UNSET
        else:
            metrics_kwargs = EvaluationPayloadMetricsKwargs.from_dict(_metrics_kwargs)

        filter_group_id = d.pop("filter_group_id", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        checks = cast(List[str], d.pop("checks", UNSET))

        _type = d.pop("type", UNSET)
        type: Union[Unset, TestRunType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = TestRunType(_type)

        name = d.pop("name", UNSET)

        project_id = d.pop("project_id", UNSET)

        evaluation_payload = cls(
            scenario_id=scenario_id,
            datapoint_ids=datapoint_ids,
            metrics_kwargs=metrics_kwargs,
            filter_group_id=filter_group_id,
            tags=tags,
            checks=checks,
            type=type,
            name=name,
            project_id=project_id,
        )

        evaluation_payload.additional_properties = d
        return evaluation_payload

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
