from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.check_value_item_check_metadata_type_0 import CheckValueItemCheckMetadataType0


T = TypeVar("T", bound="CheckValueItem")


@_attrs_define
class CheckValueItem:
    """
    Attributes:
        name (str):
        value (bool | float):
        value_type (str):
        check_id (UUID):
        is_issue (bool | None | Unset):
        explanation (None | str | Unset):
        check_metadata (CheckValueItemCheckMetadataType0 | None | Unset):
    """

    name: str
    value: bool | float
    value_type: str
    check_id: UUID
    is_issue: bool | None | Unset = UNSET
    explanation: None | str | Unset = UNSET
    check_metadata: CheckValueItemCheckMetadataType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.check_value_item_check_metadata_type_0 import CheckValueItemCheckMetadataType0

        name = self.name

        value: bool | float
        value = self.value

        value_type = self.value_type

        check_id = str(self.check_id)

        is_issue: bool | None | Unset
        if isinstance(self.is_issue, Unset):
            is_issue = UNSET
        else:
            is_issue = self.is_issue

        explanation: None | str | Unset
        if isinstance(self.explanation, Unset):
            explanation = UNSET
        else:
            explanation = self.explanation

        check_metadata: dict[str, Any] | None | Unset
        if isinstance(self.check_metadata, Unset):
            check_metadata = UNSET
        elif isinstance(self.check_metadata, CheckValueItemCheckMetadataType0):
            check_metadata = self.check_metadata.to_dict()
        else:
            check_metadata = self.check_metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "value": value,
                "value_type": value_type,
                "check_id": check_id,
            }
        )
        if is_issue is not UNSET:
            field_dict["is_issue"] = is_issue
        if explanation is not UNSET:
            field_dict["explanation"] = explanation
        if check_metadata is not UNSET:
            field_dict["check_metadata"] = check_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.check_value_item_check_metadata_type_0 import CheckValueItemCheckMetadataType0

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_value(data: object) -> bool | float:
            return cast(bool | float, data)

        value = _parse_value(d.pop("value"))

        value_type = d.pop("value_type")

        check_id = UUID(d.pop("check_id"))

        def _parse_is_issue(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_issue = _parse_is_issue(d.pop("is_issue", UNSET))

        def _parse_explanation(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        explanation = _parse_explanation(d.pop("explanation", UNSET))

        def _parse_check_metadata(data: object) -> CheckValueItemCheckMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                check_metadata_type_0 = CheckValueItemCheckMetadataType0.from_dict(data)

                return check_metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CheckValueItemCheckMetadataType0 | None | Unset, data)

        check_metadata = _parse_check_metadata(d.pop("check_metadata", UNSET))

        check_value_item = cls(
            name=name,
            value=value,
            value_type=value_type,
            check_id=check_id,
            is_issue=is_issue,
            explanation=explanation,
            check_metadata=check_metadata,
        )

        check_value_item.additional_properties = d
        return check_value_item

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
