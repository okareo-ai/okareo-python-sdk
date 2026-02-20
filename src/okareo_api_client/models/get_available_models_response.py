from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.model_info import ModelInfo


T = TypeVar("T", bound="GetAvailableModelsResponse")


@_attrs_define
class GetAvailableModelsResponse:
    """
    Attributes:
        available_models (list[ModelInfo]): List of available models with provider and display information.
    """

    available_models: list[ModelInfo]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        available_models = []
        for available_models_item_data in self.available_models:
            available_models_item = available_models_item_data.to_dict()
            available_models.append(available_models_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "available_models": available_models,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_info import ModelInfo

        d = dict(src_dict)
        available_models = []
        _available_models = d.pop("available_models")
        for available_models_item_data in _available_models:
            available_models_item = ModelInfo.from_dict(available_models_item_data)

            available_models.append(available_models_item)

        get_available_models_response = cls(
            available_models=available_models,
        )

        get_available_models_response.additional_properties = d
        return get_available_models_response

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
