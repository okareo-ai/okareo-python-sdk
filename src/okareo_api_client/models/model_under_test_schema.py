from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_under_test_schema_models_type_0 import ModelUnderTestSchemaModelsType0


T = TypeVar("T", bound="ModelUnderTestSchema")


@_attrs_define
class ModelUnderTestSchema:
    """
    Attributes:
        name (Union[None, Unset, str]): Name of the model
        models (Union['ModelUnderTestSchemaModelsType0', None, Unset]): Models to be added for testing
        tags (Union[Unset, list[str]]): Tags are strings that can be used to filter models in the Okareo app
        project_id (Union[None, UUID, Unset]): ID of the project
        update (Union[None, Unset, bool]): If set to true, the model will be updated instead of returning the existing
            model Default: False.
    """

    name: Union[None, Unset, str] = UNSET
    models: Union["ModelUnderTestSchemaModelsType0", None, Unset] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    project_id: Union[None, UUID, Unset] = UNSET
    update: Union[None, Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.model_under_test_schema_models_type_0 import ModelUnderTestSchemaModelsType0

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        models: Union[None, Unset, dict[str, Any]]
        if isinstance(self.models, Unset):
            models = UNSET
        elif isinstance(self.models, ModelUnderTestSchemaModelsType0):
            models = self.models.to_dict()
        else:
            models = self.models

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        update: Union[None, Unset, bool]
        if isinstance(self.update, Unset):
            update = UNSET
        else:
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
        from ..models.model_under_test_schema_models_type_0 import ModelUnderTestSchemaModelsType0

        d = dict(src_dict)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_models(data: object) -> Union["ModelUnderTestSchemaModelsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                models_type_0 = ModelUnderTestSchemaModelsType0.from_dict(data)

                return models_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ModelUnderTestSchemaModelsType0", None, Unset], data)

        models = _parse_models(d.pop("models", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_project_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_update(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        update = _parse_update(d.pop("update", UNSET))

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
