from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EvaluatorGenerateResponse")


@_attrs_define
class EvaluatorGenerateResponse:
    """
    Attributes:
        name (None | str | Unset):
        description (None | str | Unset):
        requires_scenario_input (bool | None | Unset):
        requires_scenario_result (bool | None | Unset):
        output_data_type (None | str | Unset):
        generated_code (None | str | Unset):
        generated_prompt (None | str | Unset):
        warning (None | str | Unset):
    """

    name: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    requires_scenario_input: bool | None | Unset = UNSET
    requires_scenario_result: bool | None | Unset = UNSET
    output_data_type: None | str | Unset = UNSET
    generated_code: None | str | Unset = UNSET
    generated_prompt: None | str | Unset = UNSET
    warning: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        requires_scenario_input: bool | None | Unset
        if isinstance(self.requires_scenario_input, Unset):
            requires_scenario_input = UNSET
        else:
            requires_scenario_input = self.requires_scenario_input

        requires_scenario_result: bool | None | Unset
        if isinstance(self.requires_scenario_result, Unset):
            requires_scenario_result = UNSET
        else:
            requires_scenario_result = self.requires_scenario_result

        output_data_type: None | str | Unset
        if isinstance(self.output_data_type, Unset):
            output_data_type = UNSET
        else:
            output_data_type = self.output_data_type

        generated_code: None | str | Unset
        if isinstance(self.generated_code, Unset):
            generated_code = UNSET
        else:
            generated_code = self.generated_code

        generated_prompt: None | str | Unset
        if isinstance(self.generated_prompt, Unset):
            generated_prompt = UNSET
        else:
            generated_prompt = self.generated_prompt

        warning: None | str | Unset
        if isinstance(self.warning, Unset):
            warning = UNSET
        else:
            warning = self.warning

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if requires_scenario_input is not UNSET:
            field_dict["requires_scenario_input"] = requires_scenario_input
        if requires_scenario_result is not UNSET:
            field_dict["requires_scenario_result"] = requires_scenario_result
        if output_data_type is not UNSET:
            field_dict["output_data_type"] = output_data_type
        if generated_code is not UNSET:
            field_dict["generated_code"] = generated_code
        if generated_prompt is not UNSET:
            field_dict["generated_prompt"] = generated_prompt
        if warning is not UNSET:
            field_dict["warning"] = warning

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_requires_scenario_input(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        requires_scenario_input = _parse_requires_scenario_input(d.pop("requires_scenario_input", UNSET))

        def _parse_requires_scenario_result(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        requires_scenario_result = _parse_requires_scenario_result(d.pop("requires_scenario_result", UNSET))

        def _parse_output_data_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_data_type = _parse_output_data_type(d.pop("output_data_type", UNSET))

        def _parse_generated_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        generated_code = _parse_generated_code(d.pop("generated_code", UNSET))

        def _parse_generated_prompt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        generated_prompt = _parse_generated_prompt(d.pop("generated_prompt", UNSET))

        def _parse_warning(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        warning = _parse_warning(d.pop("warning", UNSET))

        evaluator_generate_response = cls(
            name=name,
            description=description,
            requires_scenario_input=requires_scenario_input,
            requires_scenario_result=requires_scenario_result,
            output_data_type=output_data_type,
            generated_code=generated_code,
            generated_prompt=generated_prompt,
            warning=warning,
        )

        evaluator_generate_response.additional_properties = d
        return evaluator_generate_response

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
