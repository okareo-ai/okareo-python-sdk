from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FindTracesRequest")


@_attrs_define
class FindTracesRequest:
    """
    Attributes:
        project_id (str): Project UUID to fetch traces from
        otel_trace_id (Union[Unset, str]): Trace ID to fetch
    """

    project_id: str
    otel_trace_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        project_id = self.project_id
        otel_trace_id = self.otel_trace_id

        field_dict: Dict[str, Any] = {}
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
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_id = d.pop("project_id")

        otel_trace_id = d.pop("otel_trace_id", UNSET)

        find_traces_request = cls(
            project_id=project_id,
            otel_trace_id=otel_trace_id,
        )

        find_traces_request.additional_properties = d
        return find_traces_request

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
