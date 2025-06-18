from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_under_test_schema_models import ModelUnderTestSchemaModels


T = TypeVar("T", bound="ModelUnderTestSchema")


@_attrs_define
class ModelUnderTestSchema:
    """
    Attributes:
        name (Union[Unset, str]): Name of the model
        models (Union[Unset, ModelUnderTestSchemaModels]): Models to be added for testing
        sensitive_fields (Union[Unset, List[str]]): List of sensitive fields in the model to redact. Should include
            nested fields, e.g. ['headers.authorization', 'body.password']
        tags (Union[Unset, List[str]]): Tags are strings that can be used to filter models in the Okareo app
        project_id (Union[Unset, str]): ID of the project
        update (Union[Unset, bool]): If set to true, the model will be updated instead of returning the existing model
    """

    name: Union[Unset, str] = UNSET
    models: Union[Unset, "ModelUnderTestSchemaModels"] = UNSET
    sensitive_fields: Union[Unset, List[str]] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    project_id: Union[Unset, str] = UNSET
    update: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        models: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.models, Unset):
            models = self.models.to_dict()

        sensitive_fields: Union[Unset, List[str]] = UNSET
        if not isinstance(self.sensitive_fields, Unset):
            sensitive_fields = self.sensitive_fields

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        project_id = self.project_id
        update = self.update

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if models is not UNSET:
            field_dict["models"] = models
        if sensitive_fields is not UNSET:
            field_dict["sensitive_fields"] = sensitive_fields
        if tags is not UNSET:
            field_dict["tags"] = tags
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if update is not UNSET:
            field_dict["update"] = update

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_under_test_schema_models import ModelUnderTestSchemaModels

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _models = d.pop("models", UNSET)
        models: Union[Unset, ModelUnderTestSchemaModels]
        if isinstance(_models, Unset):
            models = UNSET
        else:
            models = ModelUnderTestSchemaModels.from_dict(_models)

        sensitive_fields = cast(List[str], d.pop("sensitive_fields", UNSET))

        tags = cast(List[str], d.pop("tags", UNSET))

        project_id = d.pop("project_id", UNSET)

        update = d.pop("update", UNSET)

        model_under_test_schema = cls(
            name=name,
            models=models,
            sensitive_fields=sensitive_fields,
            tags=tags,
            project_id=project_id,
            update=update,
        )

        model_under_test_schema.additional_properties = d
        return model_under_test_schema

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
