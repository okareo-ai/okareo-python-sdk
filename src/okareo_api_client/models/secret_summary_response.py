from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.secret_summary_response_statuses import SecretSummaryResponseStatuses


T = TypeVar("T", bound="SecretSummaryResponse")


@_attrs_define
class SecretSummaryResponse:
    """
    Attributes:
        secret_names (list[str]):
        statuses (SecretSummaryResponseStatuses):
    """

    secret_names: list[str]
    statuses: SecretSummaryResponseStatuses

    def to_dict(self) -> dict[str, Any]:
        secret_names = self.secret_names

        statuses = self.statuses.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "secret_names": secret_names,
                "statuses": statuses,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.secret_summary_response_statuses import SecretSummaryResponseStatuses

        d = dict(src_dict)
        secret_names = cast(list[str], d.pop("secret_names"))

        statuses = SecretSummaryResponseStatuses.from_dict(d.pop("statuses"))

        secret_summary_response = cls(
            secret_names=secret_names,
            statuses=statuses,
        )

        return secret_summary_response
