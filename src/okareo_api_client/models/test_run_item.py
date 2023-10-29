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
        mut_id (str):
        scenario_set_id (str):
        name (Union[Unset, str]):
        tags (Union[Unset, List[str]]):
        type (Union[Unset, str]):
        start_time (Union[Unset, datetime.datetime]):
        end_time (Union[Unset, datetime.datetime]):
        test_data_point_count (Union[Unset, int]):
        model_metrics (Union[Unset, TestRunItemModelMetrics]):
        error_matrix (Union[Unset, List[Any]]):
    """

    id: str
    project_id: str
    mut_id: str
    scenario_set_id: str
    name: Union[Unset, str] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    type: Union[Unset, str] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    end_time: Union[Unset, datetime.datetime] = UNSET
    test_data_point_count: Union[Unset, int] = UNSET
    model_metrics: Union[Unset, "TestRunItemModelMetrics"] = UNSET
    error_matrix: Union[Unset, List[Any]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        project_id = self.project_id
        mut_id = self.mut_id
        scenario_set_id = self.scenario_set_id
        name = self.name
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        type = self.type
        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        end_time: Union[Unset, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat()

        test_data_point_count = self.test_data_point_count
        model_metrics: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.model_metrics, Unset):
            model_metrics = self.model_metrics.to_dict()

        error_matrix: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.error_matrix, Unset):
            error_matrix = self.error_matrix

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "mut_id": mut_id,
                "scenario_set_id": scenario_set_id,
            }
        )
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_run_item_model_metrics import TestRunItemModelMetrics

        d = src_dict.copy()
        id = d.pop("id")

        project_id = d.pop("project_id")

        mut_id = d.pop("mut_id")

        scenario_set_id = d.pop("scenario_set_id")

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
        end_time: Union[Unset, datetime.datetime]
        if isinstance(_end_time, Unset):
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

        test_run_item = cls(
            id=id,
            project_id=project_id,
            mut_id=mut_id,
            scenario_set_id=scenario_set_id,
            name=name,
            tags=tags,
            type=type,
            start_time=start_time,
            end_time=end_time,
            test_data_point_count=test_data_point_count,
            model_metrics=model_metrics,
            error_matrix=error_matrix,
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
