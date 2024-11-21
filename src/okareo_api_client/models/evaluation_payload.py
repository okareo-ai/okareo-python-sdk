import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.test_run_type import TestRunType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.evaluation_payload_metrics_kwargs import EvaluationPayloadMetricsKwargs


T = TypeVar("T", bound="EvaluationPayload")


@_attrs_define
class EvaluationPayload:
    """
    Attributes:
        scenario_id (Union[Unset, str]): ID of the scenario set
        metrics_kwargs (Union[Unset, EvaluationPayloadMetricsKwargs]): Dictionary of metrics to be measured
        name (Union[Unset, str]): Name of the test run
        type (Union[Unset, TestRunType]): An enumeration. Default: TestRunType.MULTI_CLASS_CLASSIFICATION.
        evaluation_tags (Union[Unset, List[str]]): Tags are strings that can be used to filter test runs in the Okareo
            app
        checks (Union[Unset, List[str]]): List of checks to include in the test run.
        tags (Union[Unset, List[str]]): Tags are strings that can be used to filter datapoints in the Okareo app
        from_date (Union[Unset, datetime.datetime]): Earliest date Default: isoparse('2022-12-31T23:59:59.999999').
        to_date (Union[Unset, datetime.datetime]): Latest date
        feedback (Union[Unset, float]): Feedback is a 0 to 1 float value that captures user feedback range for related
            datapoint results
        error_code (Union[Unset, str]):
        context_token (Union[Unset, str]): Context token is a unique token to link various datapoints which originate
            from the same context
        project_id (Union[Unset, str]): Project ID
        mut_id (Union[Unset, str]): Model ID
        test_run_id (Union[Unset, str]): Test run ID
        search_value (Union[Unset, str]): Search substring that is matched against input, result, context_token, tags,
            or time_created fields
        offset (Union[Unset, int]): Offset for pagination
        limit (Union[Unset, int]): Limit for pagination
        datapoint_ids (Union[Unset, List[str]]): List of datapoint IDs to filter by
    """

    scenario_id: Union[Unset, str] = UNSET
    metrics_kwargs: Union[Unset, "EvaluationPayloadMetricsKwargs"] = UNSET
    name: Union[Unset, str] = UNSET
    type: Union[Unset, TestRunType] = TestRunType.MULTI_CLASS_CLASSIFICATION
    evaluation_tags: Union[Unset, List[str]] = UNSET
    checks: Union[Unset, List[str]] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    from_date: Union[Unset, datetime.datetime] = isoparse("2022-12-31T23:59:59.999999")
    to_date: Union[Unset, datetime.datetime] = UNSET
    feedback: Union[Unset, float] = UNSET
    error_code: Union[Unset, str] = UNSET
    context_token: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    mut_id: Union[Unset, str] = UNSET
    test_run_id: Union[Unset, str] = UNSET
    search_value: Union[Unset, str] = UNSET
    offset: Union[Unset, int] = UNSET
    limit: Union[Unset, int] = UNSET
    datapoint_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scenario_id = self.scenario_id
        metrics_kwargs: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metrics_kwargs, Unset):
            metrics_kwargs = self.metrics_kwargs.to_dict()

        name = self.name
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        evaluation_tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.evaluation_tags, Unset):
            evaluation_tags = self.evaluation_tags

        checks: Union[Unset, List[str]] = UNSET
        if not isinstance(self.checks, Unset):
            checks = self.checks

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        from_date: Union[Unset, str] = UNSET
        if not isinstance(self.from_date, Unset):
            from_date = self.from_date.isoformat()

        to_date: Union[Unset, str] = UNSET
        if not isinstance(self.to_date, Unset):
            to_date = self.to_date.isoformat()

        feedback = self.feedback
        error_code = self.error_code
        context_token = self.context_token
        project_id = self.project_id
        mut_id = self.mut_id
        test_run_id = self.test_run_id
        search_value = self.search_value
        offset = self.offset
        limit = self.limit
        datapoint_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.datapoint_ids, Unset):
            datapoint_ids = self.datapoint_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if scenario_id is not UNSET:
            field_dict["scenario_id"] = scenario_id
        if metrics_kwargs is not UNSET:
            field_dict["metrics_kwargs"] = metrics_kwargs
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type
        if evaluation_tags is not UNSET:
            field_dict["evaluation_tags"] = evaluation_tags
        if checks is not UNSET:
            field_dict["checks"] = checks
        if tags is not UNSET:
            field_dict["tags"] = tags
        if from_date is not UNSET:
            field_dict["from_date"] = from_date
        if to_date is not UNSET:
            field_dict["to_date"] = to_date
        if feedback is not UNSET:
            field_dict["feedback"] = feedback
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if context_token is not UNSET:
            field_dict["context_token"] = context_token
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if mut_id is not UNSET:
            field_dict["mut_id"] = mut_id
        if test_run_id is not UNSET:
            field_dict["test_run_id"] = test_run_id
        if search_value is not UNSET:
            field_dict["search_value"] = search_value
        if offset is not UNSET:
            field_dict["offset"] = offset
        if limit is not UNSET:
            field_dict["limit"] = limit
        if datapoint_ids is not UNSET:
            field_dict["datapoint_ids"] = datapoint_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.evaluation_payload_metrics_kwargs import EvaluationPayloadMetricsKwargs

        d = src_dict.copy()
        scenario_id = d.pop("scenario_id", UNSET)

        _metrics_kwargs = d.pop("metrics_kwargs", UNSET)
        metrics_kwargs: Union[Unset, EvaluationPayloadMetricsKwargs]
        if isinstance(_metrics_kwargs, Unset):
            metrics_kwargs = UNSET
        else:
            metrics_kwargs = EvaluationPayloadMetricsKwargs.from_dict(_metrics_kwargs)

        name = d.pop("name", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, TestRunType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = TestRunType(_type)

        evaluation_tags = cast(List[str], d.pop("evaluation_tags", UNSET))

        checks = cast(List[str], d.pop("checks", UNSET))

        tags = cast(List[str], d.pop("tags", UNSET))

        _from_date = d.pop("from_date", UNSET)
        from_date: Union[Unset, datetime.datetime]
        if isinstance(_from_date, Unset):
            from_date = UNSET
        else:
            from_date = isoparse(_from_date)

        _to_date = d.pop("to_date", UNSET)
        to_date: Union[Unset, datetime.datetime]
        if isinstance(_to_date, Unset):
            to_date = UNSET
        else:
            to_date = isoparse(_to_date)

        feedback = d.pop("feedback", UNSET)

        error_code = d.pop("error_code", UNSET)

        context_token = d.pop("context_token", UNSET)

        project_id = d.pop("project_id", UNSET)

        mut_id = d.pop("mut_id", UNSET)

        test_run_id = d.pop("test_run_id", UNSET)

        search_value = d.pop("search_value", UNSET)

        offset = d.pop("offset", UNSET)

        limit = d.pop("limit", UNSET)

        datapoint_ids = cast(List[str], d.pop("datapoint_ids", UNSET))

        evaluation_payload = cls(
            scenario_id=scenario_id,
            metrics_kwargs=metrics_kwargs,
            name=name,
            type=type,
            evaluation_tags=evaluation_tags,
            checks=checks,
            tags=tags,
            from_date=from_date,
            to_date=to_date,
            feedback=feedback,
            error_code=error_code,
            context_token=context_token,
            project_id=project_id,
            mut_id=mut_id,
            test_run_id=test_run_id,
            search_value=search_value,
            offset=offset,
            limit=limit,
            datapoint_ids=datapoint_ids,
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
