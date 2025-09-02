from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DriverModelResponse")


@_attrs_define
class DriverModelResponse:
    """
    Attributes:
        id (str):
        name (str):
        temperature (float):
        prompt_template (str):
        time_created (str):
        model_id (Union[Unset, str]):
        project_id (Union[Unset, str]):
    """

    id: str
    name: str
    temperature: float
    prompt_template: str
    time_created: str
    model_id: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        temperature = self.temperature
        prompt_template = self.prompt_template
        time_created = self.time_created
        model_id = self.model_id
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "temperature": temperature,
                "prompt_template": prompt_template,
                "time_created": time_created,
            }
        )
        if model_id is not UNSET:
            field_dict["model_id"] = model_id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        temperature = d.pop("temperature")

        prompt_template = d.pop("prompt_template")

        time_created = d.pop("time_created")

        model_id = d.pop("model_id", UNSET)

        project_id = d.pop("project_id", UNSET)

        driver_model_response = cls(
            id=id,
            name=name,
            temperature=temperature,
            prompt_template=prompt_template,
            time_created=time_created,
            model_id=model_id,
            project_id=project_id,
        )

        driver_model_response.additional_properties = d
        return driver_model_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
