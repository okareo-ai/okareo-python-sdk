from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.check_validate_request_check_type import CheckValidateRequestCheckType

if TYPE_CHECKING:
    from ..models.check_validate_request_check_config import CheckValidateRequestCheckConfig


T = TypeVar("T", bound="CheckValidateRequest")


@_attrs_define
class CheckValidateRequest:
    """Request body for POST /check_validate. Validates check code or prompt without persisting.

    Attributes:
        check_type (CheckValidateRequestCheckType): Type of check: code (code-based) or model (model-based judge
            prompt).
        check_config (CheckValidateRequestCheckConfig): Check config: code_contents for code-based, prompt_template for
            model-based.
    """

    check_type: CheckValidateRequestCheckType
    check_config: CheckValidateRequestCheckConfig
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        check_type = self.check_type.value

        check_config = self.check_config.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "check_type": check_type,
                "check_config": check_config,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.check_validate_request_check_config import CheckValidateRequestCheckConfig

        d = dict(src_dict)
        check_type = CheckValidateRequestCheckType(d.pop("check_type"))

        check_config = CheckValidateRequestCheckConfig.from_dict(d.pop("check_config"))

        check_validate_request = cls(
            check_type=check_type,
            check_config=check_config,
        )

        check_validate_request.additional_properties = d
        return check_validate_request

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
