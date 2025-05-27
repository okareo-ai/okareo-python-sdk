from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

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
        tags (Union[Unset, list[str]]): Tags are strings that can be used to filter models in the Okareo app
        project_id (Union[Unset, UUID]): ID of the project
        update (Union[Unset, bool]): If set to true, the model will be updated instead of returning the existing model
            Default: False.
    """

    name: Union[Unset, str] = UNSET
    models: Union[Unset, "ModelUnderTestSchemaModels"] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    project_id: Union[Unset, UUID] = UNSET
    update: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        models: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.models, Unset):
            models = self.models.to_dict()

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        project_id: Union[Unset, str] = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        update = self.update

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if models is not UNSET:
            field_dict["models"] = models
        if tags is not UNSET:
            field_dict["tags"] = tags
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if update is not UNSET:
            field_dict["update"] = update

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_under_test_schema_models import ModelUnderTestSchemaModels

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _models = d.pop("models", UNSET)
        models: Union[Unset, ModelUnderTestSchemaModels]
        if isinstance(_models, Unset):
            models = UNSET
        else:
            models = ModelUnderTestSchemaModels.from_dict(_models)

        tags = cast(list[str], d.pop("tags", UNSET))

        _project_id = d.pop("project_id", UNSET)
        project_id: Union[Unset, UUID]
        if isinstance(_project_id, Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)

        update = d.pop("update", UNSET)

        model_under_test_schema = cls(
            name=name,
            models=models,
            tags=tags,
            project_id=project_id,
            update=update,
        )

        model_under_test_schema.additional_properties = d
        return model_under_test_schema

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
