from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_custom_endpoint_request_next_message_params import TestCustomEndpointRequestNextMessageParams
    from ..models.test_custom_endpoint_request_start_session_params import TestCustomEndpointRequestStartSessionParams


T = TypeVar("T", bound="TestCustomEndpointRequest")


@_attrs_define
class TestCustomEndpointRequest:
    """
    Attributes:
        start_session_params (TestCustomEndpointRequestStartSessionParams): API parameters to start a session.
        next_message_params (Union[Unset, TestCustomEndpointRequestNextMessageParams]): API parameters to get the next
            message in the session. Optional.
    """

    start_session_params: "TestCustomEndpointRequestStartSessionParams"
    next_message_params: Union[Unset, "TestCustomEndpointRequestNextMessageParams"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start_session_params = self.start_session_params.to_dict()

        next_message_params: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.next_message_params, Unset):
            next_message_params = self.next_message_params.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_session_params": start_session_params,
            }
        )
        if next_message_params is not UNSET:
            field_dict["next_message_params"] = next_message_params

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_custom_endpoint_request_next_message_params import TestCustomEndpointRequestNextMessageParams
        from ..models.test_custom_endpoint_request_start_session_params import (
            TestCustomEndpointRequestStartSessionParams,
        )

        d = src_dict.copy()
        start_session_params = TestCustomEndpointRequestStartSessionParams.from_dict(d.pop("start_session_params"))

        _next_message_params = d.pop("next_message_params", UNSET)
        next_message_params: Union[Unset, TestCustomEndpointRequestNextMessageParams]
        if isinstance(_next_message_params, Unset):
            next_message_params = UNSET
        else:
            next_message_params = TestCustomEndpointRequestNextMessageParams.from_dict(_next_message_params)

        test_custom_endpoint_request = cls(
            start_session_params=start_session_params,
            next_message_params=next_message_params,
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
