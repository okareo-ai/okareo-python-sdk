from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FindTracesRequest")


@_attrs_define
class FindTracesRequest:
    """
    Attributes:
        project_id (UUID): Project UUID to fetch traces from
        otel_trace_id (None | str | Unset): Trace ID to fetch
    """

    project_id: UUID
    otel_trace_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        otel_trace_id: None | str | Unset
        if isinstance(self.otel_trace_id, Unset):
            otel_trace_id = UNSET
        else:
            otel_trace_id = self.otel_trace_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
            }
        )
        if otel_trace_id is not UNSET:
            field_dict["otel_trace_id"] = otel_trace_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))

        def _parse_otel_trace_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        otel_trace_id = _parse_otel_trace_id(d.pop("otel_trace_id", UNSET))

        find_traces_request = cls(
            project_id=project_id,
            otel_trace_id=otel_trace_id,
        )

        find_traces_request.additional_properties = d
        return find_traces_request

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
