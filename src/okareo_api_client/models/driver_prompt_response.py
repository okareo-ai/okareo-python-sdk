from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DriverPromptResponse")


@_attrs_define
class DriverPromptResponse:
    """
    Attributes:
        driver_prompt (str):
        suggested_name (str):
    """

    driver_prompt: str
    suggested_name: str

    def to_dict(self) -> Dict[str, Any]:
        driver_prompt = self.driver_prompt
        suggested_name = self.suggested_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "driver_prompt": driver_prompt,
                "suggested_name": suggested_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        driver_prompt = d.pop("driver_prompt")

        suggested_name = d.pop("suggested_name")

        driver_prompt_response = cls(
            driver_prompt=driver_prompt,
            suggested_name=suggested_name,
        )

        return driver_prompt_response
