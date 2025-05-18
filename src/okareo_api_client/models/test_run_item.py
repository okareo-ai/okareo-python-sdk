import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_run_item_model_metrics_type_0 import TestRunItemModelMetricsType0


T = TypeVar("T", bound="TestRunItem")


@_attrs_define
class TestRunItem:
    """
    Attributes:
        id (UUID):
        project_id (UUID):
        mut_id (Union[None, UUID, Unset]):
        scenario_set_id (Union[None, UUID, Unset]):
        filter_group_id (Union[None, UUID, Unset]):
        name (Union[None, Unset, str]):
        tags (Union[None, Unset, list[str]]):
        type_ (Union[None, Unset, str]):
        start_time (Union[None, Unset, datetime.datetime]):
        end_time (Union[None, Unset, datetime.datetime]):
        test_data_point_count (Union[None, Unset, int]):
        model_metrics (Union['TestRunItemModelMetricsType0', None, Unset]):
        error_matrix (Union[None, Unset, list[Any]]):
        app_link (Union[Unset, str]): This URL links to the Okareo webpage for this test run Default: ''.
    """

    id: UUID
    project_id: UUID
    mut_id: Union[None, UUID, Unset] = UNSET
    scenario_set_id: Union[None, UUID, Unset] = UNSET
    filter_group_id: Union[None, UUID, Unset] = UNSET
    name: Union[None, Unset, str] = UNSET
    tags: Union[None, Unset, list[str]] = UNSET
    type_: Union[None, Unset, str] = UNSET
    start_time: Union[None, Unset, datetime.datetime] = UNSET
    end_time: Union[None, Unset, datetime.datetime] = UNSET
    test_data_point_count: Union[None, Unset, int] = UNSET
    model_metrics: Union["TestRunItemModelMetricsType0", None, Unset] = UNSET
    error_matrix: Union[None, Unset, list[Any]] = UNSET
    app_link: Union[Unset, str] = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.test_run_item_model_metrics_type_0 import TestRunItemModelMetricsType0

        id = str(self.id)

        project_id = str(self.project_id)

        mut_id: Union[None, Unset, str]
        if isinstance(self.mut_id, Unset):
            mut_id = UNSET
        elif isinstance(self.mut_id, UUID):
            mut_id = str(self.mut_id)
        else:
            mut_id = self.mut_id

        scenario_set_id: Union[None, Unset, str]
        if isinstance(self.scenario_set_id, Unset):
            scenario_set_id = UNSET
        elif isinstance(self.scenario_set_id, UUID):
            scenario_set_id = str(self.scenario_set_id)
        else:
            scenario_set_id = self.scenario_set_id

        filter_group_id: Union[None, Unset, str]
        if isinstance(self.filter_group_id, Unset):
            filter_group_id = UNSET
        elif isinstance(self.filter_group_id, UUID):
            filter_group_id = str(self.filter_group_id)
        else:
            filter_group_id = self.filter_group_id

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        tags: Union[None, Unset, list[str]]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        type_: Union[None, Unset, str]
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

        start_time: Union[None, Unset, str]
        if isinstance(self.start_time, Unset):
            start_time = UNSET
        elif isinstance(self.start_time, datetime.datetime):
            start_time = self.start_time.isoformat()
        else:
            start_time = self.start_time

        end_time: Union[None, Unset, str]
        if isinstance(self.end_time, Unset):
            end_time = UNSET
        elif isinstance(self.end_time, datetime.datetime):
            end_time = self.end_time.isoformat()
        else:
            end_time = self.end_time

        test_data_point_count: Union[None, Unset, int]
        if isinstance(self.test_data_point_count, Unset):
            test_data_point_count = UNSET
        else:
            test_data_point_count = self.test_data_point_count

        model_metrics: Union[None, Unset, dict[str, Any]]
        if isinstance(self.model_metrics, Unset):
            model_metrics = UNSET
        elif isinstance(self.model_metrics, TestRunItemModelMetricsType0):
            model_metrics = self.model_metrics.to_dict()
        else:
            model_metrics = self.model_metrics

        error_matrix: Union[None, Unset, list[Any]]
        if isinstance(self.error_matrix, Unset):
            error_matrix = UNSET
        elif isinstance(self.error_matrix, list):
            error_matrix = self.error_matrix

        else:
            error_matrix = self.error_matrix

        app_link = self.app_link

        field_dict: dict[str, Any] = {}
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
        if type_ is not UNSET:
            field_dict["type"] = type_
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
        if app_link is not UNSET:
            field_dict["app_link"] = app_link

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.test_run_item_model_metrics_type_0 import TestRunItemModelMetricsType0

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        project_id = UUID(d.pop("project_id"))

        def _parse_mut_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mut_id_type_0 = UUID(data)

                return mut_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        mut_id = _parse_mut_id(d.pop("mut_id", UNSET))

        def _parse_scenario_set_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scenario_set_id_type_0 = UUID(data)

                return scenario_set_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        scenario_set_id = _parse_scenario_set_id(d.pop("scenario_set_id", UNSET))

        def _parse_filter_group_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                filter_group_id_type_0 = UUID(data)

                return filter_group_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        filter_group_id = _parse_filter_group_id(d.pop("filter_group_id", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_tags(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_type_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        type_ = _parse_type_(d.pop("type", UNSET))

        def _parse_start_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0 = isoparse(data)

                return start_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        start_time = _parse_start_time(d.pop("start_time", UNSET))

        def _parse_end_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_time_type_0 = isoparse(data)

                return end_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        end_time = _parse_end_time(d.pop("end_time", UNSET))

        def _parse_test_data_point_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        test_data_point_count = _parse_test_data_point_count(d.pop("test_data_point_count", UNSET))

        def _parse_model_metrics(data: object) -> Union["TestRunItemModelMetricsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_metrics_type_0 = TestRunItemModelMetricsType0.from_dict(data)

                return model_metrics_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TestRunItemModelMetricsType0", None, Unset], data)

        model_metrics = _parse_model_metrics(d.pop("model_metrics", UNSET))

        def _parse_error_matrix(data: object) -> Union[None, Unset, list[Any]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                error_matrix_type_0 = cast(list[Any], data)

                return error_matrix_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Any]], data)

        error_matrix = _parse_error_matrix(d.pop("error_matrix", UNSET))

        app_link = d.pop("app_link", UNSET)

        test_run_item = cls(
            id=id,
            project_id=project_id,
            mut_id=mut_id,
            scenario_set_id=scenario_set_id,
            filter_group_id=filter_group_id,
            name=name,
            tags=tags,
            type_=type_,
            start_time=start_time,
            end_time=end_time,
            test_data_point_count=test_data_point_count,
            model_metrics=model_metrics,
            error_matrix=error_matrix,
            app_link=app_link,
        )

        test_run_item.additional_properties = d
        return test_run_item

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
