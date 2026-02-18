from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_custom_endpoint_response_end_session_raw_response_type_0 import (
        TestCustomEndpointResponseEndSessionRawResponseType0,
    )
    from ..models.test_custom_endpoint_response_next_message_raw_response import (
        TestCustomEndpointResponseNextMessageRawResponse,
    )
    from ..models.test_custom_endpoint_response_start_session_raw_response_type_0 import (
        TestCustomEndpointResponseStartSessionRawResponseType0,
    )


T = TypeVar("T", bound="TestCustomEndpointResponse")


@_attrs_define
class TestCustomEndpointResponse:
    """
    Attributes:
        start_session_raw_response (None | TestCustomEndpointResponseStartSessionRawResponseType0 | Unset): Raw response
            from the start session endpoint, if applicable.
        next_message_raw_response (TestCustomEndpointResponseNextMessageRawResponse | Unset): Raw response from the next
            message endpoint.
        end_session_raw_response (None | TestCustomEndpointResponseEndSessionRawResponseType0 | Unset): Raw response
            from the end session endpoint, if applicable.
    """

    start_session_raw_response: None | TestCustomEndpointResponseStartSessionRawResponseType0 | Unset = UNSET
    next_message_raw_response: TestCustomEndpointResponseNextMessageRawResponse | Unset = UNSET
    end_session_raw_response: None | TestCustomEndpointResponseEndSessionRawResponseType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.test_custom_endpoint_response_end_session_raw_response_type_0 import (
            TestCustomEndpointResponseEndSessionRawResponseType0,
        )
        from ..models.test_custom_endpoint_response_start_session_raw_response_type_0 import (
            TestCustomEndpointResponseStartSessionRawResponseType0,
        )

        start_session_raw_response: dict[str, Any] | None | Unset
        if isinstance(self.start_session_raw_response, Unset):
            start_session_raw_response = UNSET
        elif isinstance(self.start_session_raw_response, TestCustomEndpointResponseStartSessionRawResponseType0):
            start_session_raw_response = self.start_session_raw_response.to_dict()
        else:
            start_session_raw_response = self.start_session_raw_response

        next_message_raw_response: dict[str, Any] | Unset = UNSET
        if not isinstance(self.next_message_raw_response, Unset):
            next_message_raw_response = self.next_message_raw_response.to_dict()

        end_session_raw_response: dict[str, Any] | None | Unset
        if isinstance(self.end_session_raw_response, Unset):
            end_session_raw_response = UNSET
        elif isinstance(self.end_session_raw_response, TestCustomEndpointResponseEndSessionRawResponseType0):
            end_session_raw_response = self.end_session_raw_response.to_dict()
        else:
            end_session_raw_response = self.end_session_raw_response

        field_dict: dict[str, Any] = {}
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.test_custom_endpoint_response_end_session_raw_response_type_0 import (
            TestCustomEndpointResponseEndSessionRawResponseType0,
        )
        from ..models.test_custom_endpoint_response_next_message_raw_response import (
            TestCustomEndpointResponseNextMessageRawResponse,
        )
        from ..models.test_custom_endpoint_response_start_session_raw_response_type_0 import (
            TestCustomEndpointResponseStartSessionRawResponseType0,
        )

        d = dict(src_dict)

        def _parse_start_session_raw_response(
            data: object,
        ) -> None | TestCustomEndpointResponseStartSessionRawResponseType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                start_session_raw_response_type_0 = TestCustomEndpointResponseStartSessionRawResponseType0.from_dict(
                    data
                )

                return start_session_raw_response_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TestCustomEndpointResponseStartSessionRawResponseType0 | Unset, data)

        start_session_raw_response = _parse_start_session_raw_response(d.pop("start_session_raw_response", UNSET))

        _next_message_raw_response = d.pop("next_message_raw_response", UNSET)
        next_message_raw_response: TestCustomEndpointResponseNextMessageRawResponse | Unset
        if isinstance(_next_message_raw_response, Unset):
            next_message_raw_response = UNSET
        else:
            next_message_raw_response = TestCustomEndpointResponseNextMessageRawResponse.from_dict(
                _next_message_raw_response
            )

        def _parse_end_session_raw_response(
            data: object,
        ) -> None | TestCustomEndpointResponseEndSessionRawResponseType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                end_session_raw_response_type_0 = TestCustomEndpointResponseEndSessionRawResponseType0.from_dict(data)

                return end_session_raw_response_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TestCustomEndpointResponseEndSessionRawResponseType0 | Unset, data)

        end_session_raw_response = _parse_end_session_raw_response(d.pop("end_session_raw_response", UNSET))

        test_custom_endpoint_response = cls(
            start_session_raw_response=start_session_raw_response,
            next_message_raw_response=next_message_raw_response,
            end_session_raw_response=end_session_raw_response,
        )

        test_custom_endpoint_response.additional_properties = d
        return test_custom_endpoint_response

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
