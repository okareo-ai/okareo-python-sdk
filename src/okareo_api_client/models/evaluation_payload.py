from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
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
        scenario_id (None | Unset | UUID): ID of the scenario set to evaluate
        datapoint_ids (list[UUID] | None | Unset): List of datapoint IDs to filter by
        metrics_kwargs (EvaluationPayloadMetricsKwargs | Unset): Dictionary of metrics to be measured
        filter_group_id (None | Unset | UUID): ID of the datapoint filter group to apply
        tags (list[str] | Unset): Tags are strings that can be used to filter test runs in the Okareo app
        checks (list[str] | None | Unset): List of checks to include in the test run.
        type_ (TestRunType | Unset): An enumeration. Default: TestRunType.MULTI_CLASS_CLASSIFICATION.
        name (None | str | Unset): Name of the test run
        project_id (None | Unset | UUID): Project ID
        test_run_id (None | Unset | UUID): ID for the test run. Used when 'submit_test' has already been called.
    """

    scenario_id: None | Unset | UUID = UNSET
    datapoint_ids: list[UUID] | None | Unset = UNSET
    metrics_kwargs: EvaluationPayloadMetricsKwargs | Unset = UNSET
    filter_group_id: None | Unset | UUID = UNSET
    tags: list[str] | Unset = UNSET
    checks: list[str] | None | Unset = UNSET
    type_: TestRunType | Unset = TestRunType.MULTI_CLASS_CLASSIFICATION
    name: None | str | Unset = UNSET
    project_id: None | Unset | UUID = UNSET
    test_run_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scenario_id: None | str | Unset
        if isinstance(self.scenario_id, Unset):
            scenario_id = UNSET
        elif isinstance(self.scenario_id, UUID):
            scenario_id = str(self.scenario_id)
        else:
            scenario_id = self.scenario_id

        datapoint_ids: list[str] | None | Unset
        if isinstance(self.datapoint_ids, Unset):
            datapoint_ids = UNSET
        elif isinstance(self.datapoint_ids, list):
            datapoint_ids = []
            for datapoint_ids_type_0_item_data in self.datapoint_ids:
                datapoint_ids_type_0_item = str(datapoint_ids_type_0_item_data)
                datapoint_ids.append(datapoint_ids_type_0_item)

        else:
            datapoint_ids = self.datapoint_ids

        metrics_kwargs: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metrics_kwargs, Unset):
            metrics_kwargs = self.metrics_kwargs.to_dict()

        filter_group_id: None | str | Unset
        if isinstance(self.filter_group_id, Unset):
            filter_group_id = UNSET
        elif isinstance(self.filter_group_id, UUID):
            filter_group_id = str(self.filter_group_id)
        else:
            filter_group_id = self.filter_group_id

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        checks: list[str] | None | Unset
        if isinstance(self.checks, Unset):
            checks = UNSET
        elif isinstance(self.checks, list):
            checks = self.checks

        else:
            checks = self.checks

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        test_run_id: None | str | Unset
        if isinstance(self.test_run_id, Unset):
            test_run_id = UNSET
        elif isinstance(self.test_run_id, UUID):
            test_run_id = str(self.test_run_id)
        else:
            test_run_id = self.test_run_id

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
        if test_run_id is not UNSET:
            field_dict["test_run_id"] = test_run_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluation_payload_metrics_kwargs import EvaluationPayloadMetricsKwargs

        d = dict(src_dict)

        def _parse_scenario_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scenario_id_type_0 = UUID(data)

                return scenario_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        scenario_id = _parse_scenario_id(d.pop("scenario_id", UNSET))

        def _parse_datapoint_ids(data: object) -> list[UUID] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                datapoint_ids_type_0 = []
                _datapoint_ids_type_0 = data
                for datapoint_ids_type_0_item_data in _datapoint_ids_type_0:
                    datapoint_ids_type_0_item = UUID(datapoint_ids_type_0_item_data)

                    datapoint_ids_type_0.append(datapoint_ids_type_0_item)

                return datapoint_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UUID] | None | Unset, data)

        datapoint_ids = _parse_datapoint_ids(d.pop("datapoint_ids", UNSET))

        _metrics_kwargs = d.pop("metrics_kwargs", UNSET)
        metrics_kwargs: EvaluationPayloadMetricsKwargs | Unset
        if isinstance(_metrics_kwargs, Unset):
            metrics_kwargs = UNSET
        else:
            metrics_kwargs = EvaluationPayloadMetricsKwargs.from_dict(_metrics_kwargs)

        def _parse_filter_group_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                filter_group_id_type_0 = UUID(data)

                return filter_group_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        filter_group_id = _parse_filter_group_id(d.pop("filter_group_id", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

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

        _type_ = d.pop("type", UNSET)
        type_: TestRunType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = TestRunType(_type_)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_project_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_test_run_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                test_run_id_type_0 = UUID(data)

                return test_run_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        test_run_id = _parse_test_run_id(d.pop("test_run_id", UNSET))

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
            test_run_id=test_run_id,
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
