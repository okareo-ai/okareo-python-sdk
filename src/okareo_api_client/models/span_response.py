from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.span_response_attributes_type_0 import SpanResponseAttributesType0
    from ..models.span_response_metadata_type_0 import SpanResponseMetadataType0


T = TypeVar("T", bound="SpanResponse")


@_attrs_define
class SpanResponse:
    """
    Attributes:
        id (UUID):
        span_name (str): Name of the span
        span_kind (str): Kind of the span
        otel_span_id (str): OpenTelemetry Span ID
        otel_trace_id (str): OpenTelemetry Trace ID
        start_time (int): Span start time in epoch nanoseconds
        end_time (int): Span end time in epoch nanoseconds
        otel_trace_depth (int | None | Unset): Depth of the span in the trace hierarchy
        datapoint_id (None | Unset | UUID): Associated Datapoint ID
        attributes (None | SpanResponseAttributesType0 | Unset): Span attributes
        metadata (None | SpanResponseMetadataType0 | Unset): Span metadata
    """

    id: UUID
    span_name: str
    span_kind: str
    otel_span_id: str
    otel_trace_id: str
    start_time: int
    end_time: int
    otel_trace_depth: int | None | Unset = UNSET
    datapoint_id: None | Unset | UUID = UNSET
    attributes: None | SpanResponseAttributesType0 | Unset = UNSET
    metadata: None | SpanResponseMetadataType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.span_response_attributes_type_0 import SpanResponseAttributesType0
        from ..models.span_response_metadata_type_0 import SpanResponseMetadataType0

        id = str(self.id)

        span_name = self.span_name

        span_kind = self.span_kind

        otel_span_id = self.otel_span_id

        otel_trace_id = self.otel_trace_id

        start_time = self.start_time

        end_time = self.end_time

        otel_trace_depth: int | None | Unset
        if isinstance(self.otel_trace_depth, Unset):
            otel_trace_depth = UNSET
        else:
            otel_trace_depth = self.otel_trace_depth

        datapoint_id: None | str | Unset
        if isinstance(self.datapoint_id, Unset):
            datapoint_id = UNSET
        elif isinstance(self.datapoint_id, UUID):
            datapoint_id = str(self.datapoint_id)
        else:
            datapoint_id = self.datapoint_id

        attributes: dict[str, Any] | None | Unset
        if isinstance(self.attributes, Unset):
            attributes = UNSET
        elif isinstance(self.attributes, SpanResponseAttributesType0):
            attributes = self.attributes.to_dict()
        else:
            attributes = self.attributes

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, SpanResponseMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "span_name": span_name,
                "span_kind": span_kind,
                "otel_span_id": otel_span_id,
                "otel_trace_id": otel_trace_id,
                "start_time": start_time,
                "end_time": end_time,
            }
        )
        if otel_trace_depth is not UNSET:
            field_dict["otel_trace_depth"] = otel_trace_depth
        if datapoint_id is not UNSET:
            field_dict["datapoint_id"] = datapoint_id
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.span_response_attributes_type_0 import SpanResponseAttributesType0
        from ..models.span_response_metadata_type_0 import SpanResponseMetadataType0

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        span_name = d.pop("span_name")

        span_kind = d.pop("span_kind")

        otel_span_id = d.pop("otel_span_id")

        otel_trace_id = d.pop("otel_trace_id")

        start_time = d.pop("start_time")

        end_time = d.pop("end_time")

        def _parse_otel_trace_depth(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        otel_trace_depth = _parse_otel_trace_depth(d.pop("otel_trace_depth", UNSET))

        def _parse_datapoint_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                datapoint_id_type_0 = UUID(data)

                return datapoint_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        datapoint_id = _parse_datapoint_id(d.pop("datapoint_id", UNSET))

        def _parse_attributes(data: object) -> None | SpanResponseAttributesType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                attributes_type_0 = SpanResponseAttributesType0.from_dict(data)

                return attributes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SpanResponseAttributesType0 | Unset, data)

        attributes = _parse_attributes(d.pop("attributes", UNSET))

        def _parse_metadata(data: object) -> None | SpanResponseMetadataType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = SpanResponseMetadataType0.from_dict(data)

                return metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SpanResponseMetadataType0 | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        span_response = cls(
            id=id,
            span_name=span_name,
            span_kind=span_kind,
            otel_span_id=otel_span_id,
            otel_trace_id=otel_trace_id,
            start_time=start_time,
            end_time=end_time,
            otel_trace_depth=otel_trace_depth,
            datapoint_id=datapoint_id,
            attributes=attributes,
            metadata=metadata,
        )

        span_response.additional_properties = d
        return span_response

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
