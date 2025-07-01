from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_custom_endpoint_response_end_session_raw_response import (
        TestCustomEndpointResponseEndSessionRawResponse,
    )
    from ..models.test_custom_endpoint_response_next_message_raw_response import (
        TestCustomEndpointResponseNextMessageRawResponse,
    )
    from ..models.test_custom_endpoint_response_start_session_raw_response import (
        TestCustomEndpointResponseStartSessionRawResponse,
    )


T = TypeVar("T", bound="TestCustomEndpointResponse")


@_attrs_define
class TestCustomEndpointResponse:
    """
    Attributes:
        start_session_raw_response (Union[Unset, TestCustomEndpointResponseStartSessionRawResponse]): Raw response from
            the start session endpoint, if applicable.
        next_message_raw_response (Union[Unset, TestCustomEndpointResponseNextMessageRawResponse]): Raw response from
            the next message endpoint.
        end_session_raw_response (Union[Unset, TestCustomEndpointResponseEndSessionRawResponse]): Raw response from the
            end session endpoint, if applicable.
    """

    start_session_raw_response: Union[Unset, "TestCustomEndpointResponseStartSessionRawResponse"] = UNSET
    next_message_raw_response: Union[Unset, "TestCustomEndpointResponseNextMessageRawResponse"] = UNSET
    end_session_raw_response: Union[Unset, "TestCustomEndpointResponseEndSessionRawResponse"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start_session_raw_response: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.start_session_raw_response, Unset):
            start_session_raw_response = self.start_session_raw_response.to_dict()

        next_message_raw_response: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.next_message_raw_response, Unset):
            next_message_raw_response = self.next_message_raw_response.to_dict()

        end_session_raw_response: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.end_session_raw_response, Unset):
            end_session_raw_response = self.end_session_raw_response.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if start_session_raw_response is not UNSET:
            field_dict["start_session_raw_response"] = start_session_raw_response
        if next_message_raw_response is not UNSET:
            field_dict["next_message_raw_response"] = next_message_raw_response
        if end_session_raw_response is not UNSET:
            field_dict["end_session_raw_response"] = end_session_raw_response

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_custom_endpoint_response_end_session_raw_response import (
            TestCustomEndpointResponseEndSessionRawResponse,
        )
        from ..models.test_custom_endpoint_response_next_message_raw_response import (
            TestCustomEndpointResponseNextMessageRawResponse,
        )
        from ..models.test_custom_endpoint_response_start_session_raw_response import (
            TestCustomEndpointResponseStartSessionRawResponse,
        )

        d = src_dict.copy()
        _start_session_raw_response = d.pop("start_session_raw_response", UNSET)
        start_session_raw_response: Union[Unset, TestCustomEndpointResponseStartSessionRawResponse]
        if isinstance(_start_session_raw_response, Unset):
            start_session_raw_response = UNSET
        else:
            start_session_raw_response = TestCustomEndpointResponseStartSessionRawResponse.from_dict(
                _start_session_raw_response
            )

        _next_message_raw_response = d.pop("next_message_raw_response", UNSET)
        next_message_raw_response: Union[Unset, TestCustomEndpointResponseNextMessageRawResponse]
        if isinstance(_next_message_raw_response, Unset):
            next_message_raw_response = UNSET
        else:
            next_message_raw_response = TestCustomEndpointResponseNextMessageRawResponse.from_dict(
                _next_message_raw_response
            )

        _end_session_raw_response = d.pop("end_session_raw_response", UNSET)
        end_session_raw_response: Union[Unset, TestCustomEndpointResponseEndSessionRawResponse]
        if isinstance(_end_session_raw_response, Unset):
            end_session_raw_response = UNSET
        else:
            end_session_raw_response = TestCustomEndpointResponseEndSessionRawResponse.from_dict(
                _end_session_raw_response
            )

        test_custom_endpoint_response = cls(
            start_session_raw_response=start_session_raw_response,
            next_message_raw_response=next_message_raw_response,
            end_session_raw_response=end_session_raw_response,
        )

        test_custom_endpoint_response.additional_properties = d
        return test_custom_endpoint_response

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
