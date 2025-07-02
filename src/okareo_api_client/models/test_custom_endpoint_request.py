from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_custom_endpoint_request_end_session_params import TestCustomEndpointRequestEndSessionParams
    from ..models.test_custom_endpoint_request_next_message_params import TestCustomEndpointRequestNextMessageParams
    from ..models.test_custom_endpoint_request_start_session_params import TestCustomEndpointRequestStartSessionParams


T = TypeVar("T", bound="TestCustomEndpointRequest")


@_attrs_define
class TestCustomEndpointRequest:
    """
    Attributes:
        next_message_params (TestCustomEndpointRequestNextMessageParams): API parameters to get the next message in the
            session.
        start_session_params (Union[Unset, TestCustomEndpointRequestStartSessionParams]): API parameters to start a
            session. Optional
        end_session_params (Union[Unset, TestCustomEndpointRequestEndSessionParams]): API parameters to end a session.
            Optional.
        mut_id (Union[Unset, str]): ID of the model to use for the custom endpoint. Optional.
        sensitive_fields (Union[Unset, List[str]]): List of sensitive fields to redact in the response. Optional.
    """

    next_message_params: "TestCustomEndpointRequestNextMessageParams"
    start_session_params: Union[Unset, "TestCustomEndpointRequestStartSessionParams"] = UNSET
    end_session_params: Union[Unset, "TestCustomEndpointRequestEndSessionParams"] = UNSET
    mut_id: Union[Unset, str] = UNSET
    sensitive_fields: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        next_message_params = self.next_message_params.to_dict()

        start_session_params: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.start_session_params, Unset):
            start_session_params = self.start_session_params.to_dict()

        end_session_params: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.end_session_params, Unset):
            end_session_params = self.end_session_params.to_dict()

        mut_id = self.mut_id
        sensitive_fields: Union[Unset, List[str]] = UNSET
        if not isinstance(self.sensitive_fields, Unset):
            sensitive_fields = self.sensitive_fields

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "next_message_params": next_message_params,
            }
        )
        if start_session_params is not UNSET:
            field_dict["start_session_params"] = start_session_params
        if end_session_params is not UNSET:
            field_dict["end_session_params"] = end_session_params
        if mut_id is not UNSET:
            field_dict["mut_id"] = mut_id
        if sensitive_fields is not UNSET:
            field_dict["sensitive_fields"] = sensitive_fields

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_custom_endpoint_request_end_session_params import TestCustomEndpointRequestEndSessionParams
        from ..models.test_custom_endpoint_request_next_message_params import TestCustomEndpointRequestNextMessageParams
        from ..models.test_custom_endpoint_request_start_session_params import (
            TestCustomEndpointRequestStartSessionParams,
        )

        d = src_dict.copy()
        next_message_params = TestCustomEndpointRequestNextMessageParams.from_dict(d.pop("next_message_params"))

        _start_session_params = d.pop("start_session_params", UNSET)
        start_session_params: Union[Unset, TestCustomEndpointRequestStartSessionParams]
        if isinstance(_start_session_params, Unset):
            start_session_params = UNSET
        else:
            start_session_params = TestCustomEndpointRequestStartSessionParams.from_dict(_start_session_params)

        _end_session_params = d.pop("end_session_params", UNSET)
        end_session_params: Union[Unset, TestCustomEndpointRequestEndSessionParams]
        if isinstance(_end_session_params, Unset):
            end_session_params = UNSET
        else:
            end_session_params = TestCustomEndpointRequestEndSessionParams.from_dict(_end_session_params)

        mut_id = d.pop("mut_id", UNSET)

        sensitive_fields = cast(List[str], d.pop("sensitive_fields", UNSET))

        test_custom_endpoint_request = cls(
            next_message_params=next_message_params,
            start_session_params=start_session_params,
            end_session_params=end_session_params,
            mut_id=mut_id,
            sensitive_fields=sensitive_fields,
        )

        test_custom_endpoint_request.additional_properties = d
        return test_custom_endpoint_request

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
