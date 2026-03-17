from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.check_validate_request_check_type import CheckValidateRequestCheckType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.check_validate_request_check_config import CheckValidateRequestCheckConfig


T = TypeVar("T", bound="CheckValidateRequest")


@_attrs_define
class CheckValidateRequest:
    """Request body for POST /check_validate. Validates check code or prompt without persisting.

    Attributes:
        check_type (CheckValidateRequestCheckType): Type of check: code (code-based), model (model-based judge prompt),
            or audio (LLM audio judge).
        check_config (CheckValidateRequestCheckConfig): Check config: code_contents for code-based, prompt_template for
            model-based or audio.
        output_data_type (None | str | Unset): Output data type (e.g. pass_fail, score, analysis). Used for frontend
            symmetry.
    """

    check_type: CheckValidateRequestCheckType
    check_config: CheckValidateRequestCheckConfig
    output_data_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        check_type = self.check_type.value

        check_config = self.check_config.to_dict()

        output_data_type: None | str | Unset
        if isinstance(self.output_data_type, Unset):
            output_data_type = UNSET
        else:
            output_data_type = self.output_data_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "check_type": check_type,
                "check_config": check_config,
            }
        )
        if output_data_type is not UNSET:
            field_dict["output_data_type"] = output_data_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.check_validate_request_check_config import CheckValidateRequestCheckConfig

        d = dict(src_dict)
        check_type = CheckValidateRequestCheckType(d.pop("check_type"))

        check_config = CheckValidateRequestCheckConfig.from_dict(d.pop("check_config"))

        def _parse_output_data_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_data_type = _parse_output_data_type(d.pop("output_data_type", UNSET))

        check_validate_request = cls(
            check_type=check_type,
            check_config=check_config,
            output_data_type=output_data_type,
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
