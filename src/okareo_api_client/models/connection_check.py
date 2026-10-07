from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ConnectionCheck")


@_attrs_define
class ConnectionCheck:
    """
    Attributes:
        name (str):
        ok (bool):
        detail (str):
    """

    name: str
    ok: bool
    detail: str

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        ok = self.ok

        detail = self.detail

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "ok": ok,
                "detail": detail,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        ok = d.pop("ok")

        detail = d.pop("detail")

        connection_check = cls(
            name=name,
            ok=ok,
            detail=detail,
        )

        return connection_check
