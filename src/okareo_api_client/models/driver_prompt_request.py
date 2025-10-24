from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DriverPromptRequest")


@_attrs_define
class DriverPromptRequest:
    """
    Attributes:
        user_input (str):
        prior_prompt (Union[Unset, str]):
    """

    user_input: str
    prior_prompt: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        user_input = self.user_input
        prior_prompt = self.prior_prompt

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "user_input": user_input,
            }
        )
        if prior_prompt is not UNSET:
            field_dict["prior_prompt"] = prior_prompt

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_input = d.pop("user_input")

        prior_prompt = d.pop("prior_prompt", UNSET)

        driver_prompt_request = cls(
            user_input=user_input,
            prior_prompt=prior_prompt,
        )

        return driver_prompt_request
