from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.span_response import SpanResponse


T = TypeVar("T", bound="FindTracesResponse")


@_attrs_define
class FindTracesResponse:
    """
    Attributes:
        id (UUID): Trace UUID
        otel_trace_id (str): Trace ID from OpenTelemetry
        datapoint_ids (list[UUID]): List of associated datapoint IDs
        span_ids (list[str]): List of associated span OpenTelemetry IDs
        spans (list[SpanResponse]): List of spans associated with the trace
        start_time (datetime.datetime): Trace start time
        end_time (datetime.datetime): Trace end time
        time_created (datetime.datetime): Trace creation time
    """

    id: UUID
    otel_trace_id: str
    datapoint_ids: list[UUID]
    span_ids: list[str]
    spans: list[SpanResponse]
    start_time: datetime.datetime
    end_time: datetime.datetime
    time_created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        otel_trace_id = self.otel_trace_id

        datapoint_ids = []
        for datapoint_ids_item_data in self.datapoint_ids:
            datapoint_ids_item = str(datapoint_ids_item_data)
            datapoint_ids.append(datapoint_ids_item)

        span_ids = self.span_ids

        spans = []
        for spans_item_data in self.spans:
            spans_item = spans_item_data.to_dict()
            spans.append(spans_item)

        start_time = self.start_time.isoformat()

        end_time = self.end_time.isoformat()

        time_created = self.time_created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "otel_trace_id": otel_trace_id,
                "datapoint_ids": datapoint_ids,
                "span_ids": span_ids,
                "spans": spans,
                "start_time": start_time,
                "end_time": end_time,
                "time_created": time_created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.span_response import SpanResponse

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        otel_trace_id = d.pop("otel_trace_id")

        datapoint_ids = []
        _datapoint_ids = d.pop("datapoint_ids")
        for datapoint_ids_item_data in _datapoint_ids:
            datapoint_ids_item = UUID(datapoint_ids_item_data)

            datapoint_ids.append(datapoint_ids_item)

        span_ids = cast(list[str], d.pop("span_ids"))

        spans = []
        _spans = d.pop("spans")
        for spans_item_data in _spans:
            spans_item = SpanResponse.from_dict(spans_item_data)

            spans.append(spans_item)

        start_time = isoparse(d.pop("start_time"))

        end_time = isoparse(d.pop("end_time"))

        time_created = isoparse(d.pop("time_created"))

        find_traces_response = cls(
            id=id,
            otel_trace_id=otel_trace_id,
            datapoint_ids=datapoint_ids,
            span_ids=span_ids,
            spans=spans,
            start_time=start_time,
            end_time=end_time,
            time_created=time_created,
        )

        find_traces_response.additional_properties = d
        return find_traces_response

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
