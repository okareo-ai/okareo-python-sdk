from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.connection_check import ConnectionCheck


T = TypeVar("T", bound="ConnectionTestResponse")


@_attrs_define
class ConnectionTestResponse:
    """
    Attributes:
        ok (bool):
        checks (list[ConnectionCheck]):
    """

    ok: bool
    checks: list[ConnectionCheck]

    def to_dict(self) -> dict[str, Any]:
        ok = self.ok

        checks = []
        for checks_item_data in self.checks:
            checks_item = checks_item_data.to_dict()
            checks.append(checks_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "ok": ok,
                "checks": checks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.connection_check import ConnectionCheck

        d = dict(src_dict)
        ok = d.pop("ok")

        checks = []
        _checks = d.pop("checks")
        for checks_item_data in _checks:
            checks_item = ConnectionCheck.from_dict(checks_item_data)

            checks.append(checks_item)

        connection_test_response = cls(
            ok=ok,
            checks=checks,
        )

        return connection_test_response
