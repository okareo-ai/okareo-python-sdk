from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ModelInfo")


@_attrs_define
class ModelInfo:
    """
    Attributes:
        provider_display_name (str): Display name of the provider
        model_name (str): Name of the model
        model_display_name (str): Display name of the model
    """

    provider_display_name: str
    model_name: str
    model_display_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider_display_name = self.provider_display_name

        model_name = self.model_name

        model_display_name = self.model_display_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provider_display_name": provider_display_name,
                "model_name": model_name,
                "model_display_name": model_display_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider_display_name = d.pop("provider_display_name")

        model_name = d.pop("model_name")

        model_display_name = d.pop("model_display_name")

        model_info = cls(
            provider_display_name=provider_display_name,
            model_name=model_name,
            model_display_name=model_display_name,
        )

        model_info.additional_properties = d
        return model_info

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
