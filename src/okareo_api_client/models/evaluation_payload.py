from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

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
        scenario_id (Union[Unset, UUID]): ID of the scenario set to evaluate
        datapoint_ids (Union[Unset, list[UUID]]): List of datapoint IDs to filter by
        metrics_kwargs (Union[Unset, EvaluationPayloadMetricsKwargs]): Dictionary of metrics to be measured
        filter_group_id (Union[Unset, UUID]): ID of the datapoint filter group to apply
        tags (Union[Unset, list[str]]): Tags are strings that can be used to filter test runs in the Okareo app
        checks (Union[Unset, list[str]]): List of checks to include in the test run.
        type_ (Union[Unset, TestRunType]): An enumeration. Default: TestRunType.MULTI_CLASS_CLASSIFICATION.
        name (Union[Unset, str]): Name of the test run
        project_id (Union[Unset, UUID]): Project ID
    """

    scenario_id: Union[Unset, UUID] = UNSET
    datapoint_ids: Union[Unset, list[UUID]] = UNSET
    metrics_kwargs: Union[Unset, "EvaluationPayloadMetricsKwargs"] = UNSET
    filter_group_id: Union[Unset, UUID] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    checks: Union[Unset, list[str]] = UNSET
    type_: Union[Unset, TestRunType] = TestRunType.MULTI_CLASS_CLASSIFICATION
    name: Union[Unset, str] = UNSET
    project_id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scenario_id: Union[Unset, str] = UNSET
        if not isinstance(self.scenario_id, Unset):
            scenario_id = str(self.scenario_id)

        datapoint_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.datapoint_ids, Unset):
            datapoint_ids = []
            for datapoint_ids_item_data in self.datapoint_ids:
                datapoint_ids_item = str(datapoint_ids_item_data)
                datapoint_ids.append(datapoint_ids_item)

        metrics_kwargs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics_kwargs, Unset):
            metrics_kwargs = self.metrics_kwargs.to_dict()

        filter_group_id: Union[Unset, str] = UNSET
        if not isinstance(self.filter_group_id, Unset):
            filter_group_id = str(self.filter_group_id)

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        checks: Union[Unset, list[str]] = UNSET
        if not isinstance(self.checks, Unset):
            checks = self.checks

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        name = self.name

        project_id: Union[Unset, str] = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        field_dict: dict[str, Any] = {}
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
        if type_ is not UNSET:
            field_dict["type"] = type_
        if name is not UNSET:
            field_dict["name"] = name
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluation_payload_metrics_kwargs import EvaluationPayloadMetricsKwargs

        d = dict(src_dict)
        _scenario_id = d.pop("scenario_id", UNSET)
        scenario_id: Union[Unset, UUID]
        if isinstance(_scenario_id, Unset):
            scenario_id = UNSET
        else:
            scenario_id = UUID(_scenario_id)

        datapoint_ids = []
        _datapoint_ids = d.pop("datapoint_ids", UNSET)
        for datapoint_ids_item_data in _datapoint_ids or []:
            datapoint_ids_item = UUID(datapoint_ids_item_data)

            datapoint_ids.append(datapoint_ids_item)

        _metrics_kwargs = d.pop("metrics_kwargs", UNSET)
        metrics_kwargs: Union[Unset, EvaluationPayloadMetricsKwargs]
        if isinstance(_metrics_kwargs, Unset):
            metrics_kwargs = UNSET
        else:
            metrics_kwargs = EvaluationPayloadMetricsKwargs.from_dict(_metrics_kwargs)

        _filter_group_id = d.pop("filter_group_id", UNSET)
        filter_group_id: Union[Unset, UUID]
        if isinstance(_filter_group_id, Unset):
            filter_group_id = UNSET
        else:
            filter_group_id = UUID(_filter_group_id)

        tags = cast(list[str], d.pop("tags", UNSET))

        checks = cast(list[str], d.pop("checks", UNSET))

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, TestRunType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = TestRunType(_type_)

        name = d.pop("name", UNSET)

        _project_id = d.pop("project_id", UNSET)
        project_id: Union[Unset, UUID]
        if isinstance(_project_id, Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)

        evaluation_payload = cls(
            scenario_id=scenario_id,
            datapoint_ids=datapoint_ids,
            metrics_kwargs=metrics_kwargs,
            filter_group_id=filter_group_id,
            tags=tags,
            checks=checks,
            type_=type_,
            name=name,
            project_id=project_id,
        )

        evaluation_payload.additional_properties = d
        return evaluation_payload

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
