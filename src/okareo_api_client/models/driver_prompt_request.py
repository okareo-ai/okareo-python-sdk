from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DriverPromptRequest")


@_attrs_define
class DriverPromptRequest:
    """
    Attributes:
        user_input (str):
        prior_prompt (None | str | Unset):
        language (None | str | Unset): BCP-47 language code (e.g., 'en', 'es', 'fr-CA', 'ja') for the driver prompt.
            Specifies what language the driver should always and only respond to. Defaults to 'en' (English) if not
            provided.
    """

    user_input: str
    prior_prompt: None | str | Unset = UNSET
    language: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        user_input = self.user_input

        prior_prompt: None | str | Unset
        if isinstance(self.prior_prompt, Unset):
            prior_prompt = UNSET
        else:
            prior_prompt = self.prior_prompt

        language: None | str | Unset
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "user_input": user_input,
            }
        )
        if prior_prompt is not UNSET:
            field_dict["prior_prompt"] = prior_prompt
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_input = d.pop("user_input")

        def _parse_prior_prompt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prior_prompt = _parse_prior_prompt(d.pop("prior_prompt", UNSET))

        def _parse_language(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        language = _parse_language(d.pop("language", UNSET))

        driver_prompt_request = cls(
            user_input=user_input,
            prior_prompt=prior_prompt,
            language=language,
        )

        return driver_prompt_request
