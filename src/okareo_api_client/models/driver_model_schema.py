from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DriverModelSchema")


@_attrs_define
class DriverModelSchema:
    """
    Attributes:
        name (str): Name of the driver model
        temperature (float): Temperature of the driver model
        prompt_template (str): Prompt template for the driver model
        id (Union[Unset, str]): ID of the driver model
        model_id (Union[Unset, str]): Model ID of the driver model
        project_id (Union[Unset, str]): ID for project
    """

    name: str
    temperature: float
    prompt_template: str
    id: Union[Unset, str] = UNSET
    model_id: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        temperature = self.temperature
        prompt_template = self.prompt_template
        id = self.id
        model_id = self.model_id
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "temperature": temperature,
                "prompt_template": prompt_template,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if model_id is not UNSET:
            field_dict["model_id"] = model_id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        temperature = d.pop("temperature")

        prompt_template = d.pop("prompt_template")

        id = d.pop("id", UNSET)

        model_id = d.pop("model_id", UNSET)

        project_id = d.pop("project_id", UNSET)

        driver_model_schema = cls(
            name=name,
            temperature=temperature,
            prompt_template=prompt_template,
            id=id,
            model_id=model_id,
            project_id=project_id,
        )

        driver_model_schema.additional_properties = d
        return driver_model_schema

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
