from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

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
        start_session_params (None | TestCustomEndpointRequestStartSessionParams | Unset): API parameters to start a
            session. Optional
        end_session_params (None | TestCustomEndpointRequestEndSessionParams | Unset): API parameters to end a session.
            Optional.
        mut_id (None | Unset | UUID): ID of the model to use for the custom endpoint. Optional.
        sensitive_fields (list[str] | None | Unset): List of sensitive fields to redact in the response. Optional.
    """

    next_message_params: TestCustomEndpointRequestNextMessageParams
    start_session_params: None | TestCustomEndpointRequestStartSessionParams | Unset = UNSET
    end_session_params: None | TestCustomEndpointRequestEndSessionParams | Unset = UNSET
    mut_id: None | Unset | UUID = UNSET
    sensitive_fields: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.test_custom_endpoint_request_end_session_params import TestCustomEndpointRequestEndSessionParams
        from ..models.test_custom_endpoint_request_start_session_params import (
            TestCustomEndpointRequestStartSessionParams,
        )

        next_message_params = self.next_message_params.to_dict()

        start_session_params: dict[str, Any] | None | Unset
        if isinstance(self.start_session_params, Unset):
            start_session_params = UNSET
        elif isinstance(self.start_session_params, TestCustomEndpointRequestStartSessionParams):
            start_session_params = self.start_session_params.to_dict()
        else:
            start_session_params = self.start_session_params

        end_session_params: dict[str, Any] | None | Unset
        if isinstance(self.end_session_params, Unset):
            end_session_params = UNSET
        elif isinstance(self.end_session_params, TestCustomEndpointRequestEndSessionParams):
            end_session_params = self.end_session_params.to_dict()
        else:
            end_session_params = self.end_session_params

        mut_id: None | str | Unset
        if isinstance(self.mut_id, Unset):
            mut_id = UNSET
        elif isinstance(self.mut_id, UUID):
            mut_id = str(self.mut_id)
        else:
            mut_id = self.mut_id

        sensitive_fields: list[str] | None | Unset
        if isinstance(self.sensitive_fields, Unset):
            sensitive_fields = UNSET
        elif isinstance(self.sensitive_fields, list):
            sensitive_fields = self.sensitive_fields

        else:
            sensitive_fields = self.sensitive_fields

        field_dict: dict[str, Any] = {}
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.test_custom_endpoint_request_end_session_params import TestCustomEndpointRequestEndSessionParams
        from ..models.test_custom_endpoint_request_next_message_params import TestCustomEndpointRequestNextMessageParams
        from ..models.test_custom_endpoint_request_start_session_params import (
            TestCustomEndpointRequestStartSessionParams,
        )

        d = dict(src_dict)
        next_message_params = TestCustomEndpointRequestNextMessageParams.from_dict(d.pop("next_message_params"))

        def _parse_start_session_params(data: object) -> None | TestCustomEndpointRequestStartSessionParams | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                start_session_params_type_0 = TestCustomEndpointRequestStartSessionParams.from_dict(data)

                return start_session_params_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TestCustomEndpointRequestStartSessionParams | Unset, data)

        start_session_params = _parse_start_session_params(d.pop("start_session_params", UNSET))

        def _parse_end_session_params(data: object) -> None | TestCustomEndpointRequestEndSessionParams | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                end_session_params_type_0 = TestCustomEndpointRequestEndSessionParams.from_dict(data)

                return end_session_params_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TestCustomEndpointRequestEndSessionParams | Unset, data)

        end_session_params = _parse_end_session_params(d.pop("end_session_params", UNSET))

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

        def _parse_sensitive_fields(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sensitive_fields_type_0 = cast(list[str], data)

                return sensitive_fields_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        sensitive_fields = _parse_sensitive_fields(d.pop("sensitive_fields", UNSET))

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
