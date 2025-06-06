import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_run_item_model_metrics import TestRunItemModelMetrics


T = TypeVar("T", bound="TestRunItem")


@_attrs_define
class TestRunItem:
    """
    Attributes:
        id (str):
        project_id (str):
        mut_id (Union[Unset, str]):
        scenario_set_id (Union[Unset, str]):
        filter_group_id (Union[Unset, str]):
        name (Union[Unset, str]):
        tags (Union[Unset, List[str]]):
        type (Union[Unset, str]):
        start_time (Union[Unset, datetime.datetime]):
        end_time (Union[Unset, None, datetime.datetime]):
        test_data_point_count (Union[Unset, int]):
        model_metrics (Union[Unset, TestRunItemModelMetrics]):
        error_matrix (Union[Unset, List[Any]]):
        status (Union[Unset, str]):
        failure_message (Union[Unset, str]):
        progress (Union[Unset, int]): Number in percent of progress of test run
        app_link (Union[Unset, str]): This URL links to the Okareo webpage for this test run Default: ''.
    """

    id: str
    project_id: str
    mut_id: Union[Unset, str] = UNSET
    scenario_set_id: Union[Unset, str] = UNSET
    filter_group_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    type: Union[Unset, str] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    end_time: Union[Unset, None, datetime.datetime] = UNSET
    test_data_point_count: Union[Unset, int] = UNSET
    model_metrics: Union[Unset, "TestRunItemModelMetrics"] = UNSET
    error_matrix: Union[Unset, List[Any]] = UNSET
    status: Union[Unset, str] = UNSET
    failure_message: Union[Unset, str] = UNSET
    progress: Union[Unset, int] = 0
    app_link: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        project_id = self.project_id
        mut_id = self.mut_id
        scenario_set_id = self.scenario_set_id
        filter_group_id = self.filter_group_id
        name = self.name
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        type = self.type
        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        end_time: Union[Unset, None, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat() if self.end_time else None

        test_data_point_count = self.test_data_point_count
        model_metrics: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.model_metrics, Unset):
            model_metrics = self.model_metrics.to_dict()

        error_matrix: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.error_matrix, Unset):
            error_matrix = self.error_matrix

        status = self.status
        failure_message = self.failure_message
        progress = self.progress
        app_link = self.app_link

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
            }
        )
        if mut_id is not UNSET:
            field_dict["mut_id"] = mut_id
        if scenario_set_id is not UNSET:
            field_dict["scenario_set_id"] = scenario_set_id
        if filter_group_id is not UNSET:
            field_dict["filter_group_id"] = filter_group_id
        if name is not UNSET:
            field_dict["name"] = name
        if tags is not UNSET:
            field_dict["tags"] = tags
        if type is not UNSET:
            field_dict["type"] = type
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if test_data_point_count is not UNSET:
            field_dict["test_data_point_count"] = test_data_point_count
        if model_metrics is not UNSET:
            field_dict["model_metrics"] = model_metrics
        if error_matrix is not UNSET:
            field_dict["error_matrix"] = error_matrix
        if status is not UNSET:
            field_dict["status"] = status
        if failure_message is not UNSET:
            field_dict["failure_message"] = failure_message
        if progress is not UNSET:
            field_dict["progress"] = progress
        if app_link is not UNSET:
            field_dict["app_link"] = app_link

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_run_item_model_metrics import TestRunItemModelMetrics

        d = src_dict.copy()
        id = d.pop("id")

        project_id = d.pop("project_id")

        mut_id = d.pop("mut_id", UNSET)

        scenario_set_id = d.pop("scenario_set_id", UNSET)

        filter_group_id = d.pop("filter_group_id", UNSET)

        name = d.pop("name", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        type = d.pop("type", UNSET)

        _start_time = d.pop("start_time", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        _end_time = d.pop("end_time", UNSET)
        end_time: Union[Unset, None, datetime.datetime]
        if _end_time is None:
            end_time = None
        elif isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = isoparse(_end_time)

        test_data_point_count = d.pop("test_data_point_count", UNSET)

        _model_metrics = d.pop("model_metrics", UNSET)
        model_metrics: Union[Unset, TestRunItemModelMetrics]
        if isinstance(_model_metrics, Unset):
            model_metrics = UNSET
        else:
            model_metrics = TestRunItemModelMetrics.from_dict(_model_metrics)

        error_matrix = cast(List[Any], d.pop("error_matrix", UNSET))

        status = d.pop("status", UNSET)

        failure_message = d.pop("failure_message", UNSET)

        progress = d.pop("progress", UNSET)

        app_link = d.pop("app_link", UNSET)

        test_run_item = cls(
            id=id,
            project_id=project_id,
            mut_id=mut_id,
            scenario_set_id=scenario_set_id,
            filter_group_id=filter_group_id,
            name=name,
            tags=tags,
            type=type,
            start_time=start_time,
            end_time=end_time,
            test_data_point_count=test_data_point_count,
            model_metrics=model_metrics,
            error_matrix=error_matrix,
            status=status,
            failure_message=failure_message,
            progress=progress,
            app_link=app_link,
        )

        test_run_item.additional_properties = d
        return test_run_item

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
