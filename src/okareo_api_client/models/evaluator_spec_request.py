from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EvaluatorSpecRequest")


@_attrs_define
class EvaluatorSpecRequest:
    """
    Attributes:
        project_id (None | UUID): ID for the project
        name (None | str | Unset): Name of the evaluator
        user_input (None | str | Unset): Primary user instruction for generation. When set, used instead of description
            for the LLM prompt.
        description (None | str | Unset): Description for the evaluator.
                        When this request is sent to generate an evaluator, this field will be used to generate it (or
            user_input if set).
        requires_scenario_input (bool | Unset): Whether the evaluator requires scenario input Default: False.
        requires_scenario_result (bool | Unset): Whether the evaluator requires scenario expected result Default: False.
        output_data_type (str | Unset): Evaluator output data type (i.e., bool, int, float)
        check_type (None | str | Unset): model or code based check Default: 'code'.
        prior_code (None | str | Unset): Existing code to refine (code branch). When set, LLM is asked to modify/improve
            it.
        prior_prompt (None | str | Unset): Existing prompt to refine (model branch). When set, LLM is asked to revise
            it.
    """

    project_id: None | UUID
    name: None | str | Unset = UNSET
    user_input: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    requires_scenario_input: bool | Unset = False
    requires_scenario_result: bool | Unset = False
    output_data_type: str | Unset = UNSET
    check_type: None | str | Unset = "code"
    prior_code: None | str | Unset = UNSET
    prior_prompt: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id: None | str
        if isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        user_input: None | str | Unset
        if isinstance(self.user_input, Unset):
            user_input = UNSET
        else:
            user_input = self.user_input

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        requires_scenario_input = self.requires_scenario_input

        requires_scenario_result = self.requires_scenario_result

        output_data_type = self.output_data_type

        check_type: None | str | Unset
        if isinstance(self.check_type, Unset):
            check_type = UNSET
        else:
            check_type = self.check_type

        prior_code: None | str | Unset
        if isinstance(self.prior_code, Unset):
            prior_code = UNSET
        else:
            prior_code = self.prior_code

        prior_prompt: None | str | Unset
        if isinstance(self.prior_prompt, Unset):
            prior_prompt = UNSET
        else:
            prior_prompt = self.prior_prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if user_input is not UNSET:
            field_dict["user_input"] = user_input
        if description is not UNSET:
            field_dict["description"] = description
        if requires_scenario_input is not UNSET:
            field_dict["requires_scenario_input"] = requires_scenario_input
        if requires_scenario_result is not UNSET:
            field_dict["requires_scenario_result"] = requires_scenario_result
        if output_data_type is not UNSET:
            field_dict["output_data_type"] = output_data_type
        if check_type is not UNSET:
            field_dict["check_type"] = check_type
        if prior_code is not UNSET:
            field_dict["prior_code"] = prior_code
        if prior_prompt is not UNSET:
            field_dict["prior_prompt"] = prior_prompt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_project_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        project_id = _parse_project_id(d.pop("project_id"))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_user_input(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user_input = _parse_user_input(d.pop("user_input", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        requires_scenario_input = d.pop("requires_scenario_input", UNSET)

        requires_scenario_result = d.pop("requires_scenario_result", UNSET)

        output_data_type = d.pop("output_data_type", UNSET)

        def _parse_check_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        check_type = _parse_check_type(d.pop("check_type", UNSET))

        def _parse_prior_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prior_code = _parse_prior_code(d.pop("prior_code", UNSET))

        def _parse_prior_prompt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prior_prompt = _parse_prior_prompt(d.pop("prior_prompt", UNSET))

        evaluator_spec_request = cls(
            project_id=project_id,
            name=name,
            user_input=user_input,
            description=description,
            requires_scenario_input=requires_scenario_input,
            requires_scenario_result=requires_scenario_result,
            output_data_type=output_data_type,
            check_type=check_type,
            prior_code=prior_code,
            prior_prompt=prior_prompt,
        )

        evaluator_spec_request.additional_properties = d
        return evaluator_spec_request

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
