from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OutboundLineItem")


@_attrs_define
class OutboundLineItem:
    """
    Attributes:
        test_run_id (UUID):
        status (str):
        number (None | str | Unset):
        sip_alias (None | str | Unset):
        armed_at (float | None | Unset):
        max_until (float | None | Unset):
        idle_timeout_s (int | None | Unset):
        calls_received (int | Unset):  Default: 0.
        close_reason (None | str | Unset):
        app_link (None | str | Unset):
    """

    test_run_id: UUID
    status: str
    number: None | str | Unset = UNSET
    sip_alias: None | str | Unset = UNSET
    armed_at: float | None | Unset = UNSET
    max_until: float | None | Unset = UNSET
    idle_timeout_s: int | None | Unset = UNSET
    calls_received: int | Unset = 0
    close_reason: None | str | Unset = UNSET
    app_link: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        test_run_id = str(self.test_run_id)

        status = self.status

        number: None | str | Unset
        if isinstance(self.number, Unset):
            number = UNSET
        else:
            number = self.number

        sip_alias: None | str | Unset
        if isinstance(self.sip_alias, Unset):
            sip_alias = UNSET
        else:
            sip_alias = self.sip_alias

        armed_at: float | None | Unset
        if isinstance(self.armed_at, Unset):
            armed_at = UNSET
        else:
            armed_at = self.armed_at

        max_until: float | None | Unset
        if isinstance(self.max_until, Unset):
            max_until = UNSET
        else:
            max_until = self.max_until

        idle_timeout_s: int | None | Unset
        if isinstance(self.idle_timeout_s, Unset):
            idle_timeout_s = UNSET
        else:
            idle_timeout_s = self.idle_timeout_s

        calls_received = self.calls_received

        close_reason: None | str | Unset
        if isinstance(self.close_reason, Unset):
            close_reason = UNSET
        else:
            close_reason = self.close_reason

        app_link: None | str | Unset
        if isinstance(self.app_link, Unset):
            app_link = UNSET
        else:
            app_link = self.app_link

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_run_id": test_run_id,
                "status": status,
            }
        )
        if number is not UNSET:
            field_dict["number"] = number
        if sip_alias is not UNSET:
            field_dict["sip_alias"] = sip_alias
        if armed_at is not UNSET:
            field_dict["armed_at"] = armed_at
        if max_until is not UNSET:
            field_dict["max_until"] = max_until
        if idle_timeout_s is not UNSET:
            field_dict["idle_timeout_s"] = idle_timeout_s
        if calls_received is not UNSET:
            field_dict["calls_received"] = calls_received
        if close_reason is not UNSET:
            field_dict["close_reason"] = close_reason
        if app_link is not UNSET:
            field_dict["app_link"] = app_link

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        test_run_id = UUID(d.pop("test_run_id"))

        status = d.pop("status")

        def _parse_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        number = _parse_number(d.pop("number", UNSET))

        def _parse_sip_alias(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sip_alias = _parse_sip_alias(d.pop("sip_alias", UNSET))

        def _parse_armed_at(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        armed_at = _parse_armed_at(d.pop("armed_at", UNSET))

        def _parse_max_until(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        max_until = _parse_max_until(d.pop("max_until", UNSET))

        def _parse_idle_timeout_s(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        idle_timeout_s = _parse_idle_timeout_s(d.pop("idle_timeout_s", UNSET))

        calls_received = d.pop("calls_received", UNSET)

        def _parse_close_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        close_reason = _parse_close_reason(d.pop("close_reason", UNSET))

        def _parse_app_link(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        app_link = _parse_app_link(d.pop("app_link", UNSET))

        outbound_line_item = cls(
            test_run_id=test_run_id,
            status=status,
            number=number,
            sip_alias=sip_alias,
            armed_at=armed_at,
            max_until=max_until,
            idle_timeout_s=idle_timeout_s,
            calls_received=calls_received,
            close_reason=close_reason,
            app_link=app_link,
        )

        outbound_line_item.additional_properties = d
        return outbound_line_item

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
