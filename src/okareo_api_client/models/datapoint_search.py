from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatapointSearch")


@_attrs_define
class DatapointSearch:
    """
    Attributes:
        tags (list[str] | None | Unset): Tags are strings that can be used to filter datapoints in the Okareo app
        from_date (datetime.datetime | None | Unset): Earliest date Default: isoparse('2022-12-31T23:59:59.999999').
        to_date (datetime.datetime | None | Unset): Latest date
        feedback (float | None | Unset): Feedback is a 0 to 1 float value that captures user feedback range for related
            datapoint results
        error_code (None | str | Unset):
        context_token (None | str | Unset): Context token is a unique token to link various datapoints which originate
            from the same context
        project_id (None | str | Unset): Project ID
        mut_id (None | Unset | UUID): Model ID
        test_run_id (None | Unset | UUID): Test run ID
        search_value (None | str | Unset): Search substring that is matched against input, result, context_token, tags,
            or time_created fields
        offset (int | None | Unset): Offset for pagination
        limit (int | None | Unset): Limit for pagination
        datapoint_ids (list[UUID] | None | Unset): List of datapoint IDs to filter by
    """

    tags: list[str] | None | Unset = UNSET
    from_date: datetime.datetime | None | Unset = isoparse("2022-12-31T23:59:59.999999")
    to_date: datetime.datetime | None | Unset = UNSET
    feedback: float | None | Unset = UNSET
    error_code: None | str | Unset = UNSET
    context_token: None | str | Unset = UNSET
    project_id: None | str | Unset = UNSET
    mut_id: None | Unset | UUID = UNSET
    test_run_id: None | Unset | UUID = UNSET
    search_value: None | str | Unset = UNSET
    offset: int | None | Unset = UNSET
    limit: int | None | Unset = UNSET
    datapoint_ids: list[UUID] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        from_date: None | str | Unset
        if isinstance(self.from_date, Unset):
            from_date = UNSET
        elif isinstance(self.from_date, datetime.datetime):
            from_date = self.from_date.isoformat()
        else:
            from_date = self.from_date

        to_date: None | str | Unset
        if isinstance(self.to_date, Unset):
            to_date = UNSET
        elif isinstance(self.to_date, datetime.datetime):
            to_date = self.to_date.isoformat()
        else:
            to_date = self.to_date

        feedback: float | None | Unset
        if isinstance(self.feedback, Unset):
            feedback = UNSET
        else:
            feedback = self.feedback

        error_code: None | str | Unset
        if isinstance(self.error_code, Unset):
            error_code = UNSET
        else:
            error_code = self.error_code

        context_token: None | str | Unset
        if isinstance(self.context_token, Unset):
            context_token = UNSET
        else:
            context_token = self.context_token

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        mut_id: None | str | Unset
        if isinstance(self.mut_id, Unset):
            mut_id = UNSET
        elif isinstance(self.mut_id, UUID):
            mut_id = str(self.mut_id)
        else:
            mut_id = self.mut_id

        test_run_id: None | str | Unset
        if isinstance(self.test_run_id, Unset):
            test_run_id = UNSET
        elif isinstance(self.test_run_id, UUID):
            test_run_id = str(self.test_run_id)
        else:
            test_run_id = self.test_run_id

        search_value: None | str | Unset
        if isinstance(self.search_value, Unset):
            search_value = UNSET
        else:
            search_value = self.search_value

        offset: int | None | Unset
        if isinstance(self.offset, Unset):
            offset = UNSET
        else:
            offset = self.offset

        limit: int | None | Unset
        if isinstance(self.limit, Unset):
            limit = UNSET
        else:
            limit = self.limit

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_from_date(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                from_date_type_0 = isoparse(data)

                return from_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        from_date = _parse_from_date(d.pop("from_date", UNSET))

        def _parse_to_date(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                to_date_type_0 = isoparse(data)

                return to_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        to_date = _parse_to_date(d.pop("to_date", UNSET))

        def _parse_feedback(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        feedback = _parse_feedback(d.pop("feedback", UNSET))

        def _parse_error_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_code = _parse_error_code(d.pop("error_code", UNSET))

        def _parse_context_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        context_token = _parse_context_token(d.pop("context_token", UNSET))

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_mut_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mut_id_type_0 = UUID(data)

                return mut_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        mut_id = _parse_mut_id(d.pop("mut_id", UNSET))

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

        def _parse_search_value(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        search_value = _parse_search_value(d.pop("search_value", UNSET))

        def _parse_offset(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        offset = _parse_offset(d.pop("offset", UNSET))

        def _parse_limit(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        limit = _parse_limit(d.pop("limit", UNSET))

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

        datapoint_search = cls(
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

        datapoint_search.additional_properties = d
        return datapoint_search

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
