from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
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
        name (None | str | Unset): Name of the model
        models (ModelUnderTestSchemaModelsType0 | None | Unset): Models to be added for testing
        version (int | Unset): Version of the model under test. Defaults to 1 if not provided. Default: 1.
        sensitive_fields (list[str] | None | Unset): List of sensitive fields in the model to redact. Should include
            nested fields, e.g. ['headers.authorization', 'body.password']
        tags (list[str] | Unset): Tags are strings that can be used to filter models in the Okareo app
        project_id (None | Unset | UUID): ID of the project
        update (bool | None | Unset): If set to true, the model will be updated instead of returning the existing model
            Default: False.
    """

    name: None | str | Unset = UNSET
    models: ModelUnderTestSchemaModelsType0 | None | Unset = UNSET
    version: int | Unset = 1
    sensitive_fields: list[str] | None | Unset = UNSET
    tags: list[str] | Unset = UNSET
    project_id: None | Unset | UUID = UNSET
    update: bool | None | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.model_under_test_schema_models_type_0 import ModelUnderTestSchemaModelsType0

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        models: dict[str, Any] | None | Unset
        if isinstance(self.models, Unset):
            models = UNSET
        elif isinstance(self.models, ModelUnderTestSchemaModelsType0):
            models = self.models.to_dict()
        else:
            models = self.models

        version = self.version

        sensitive_fields: list[str] | None | Unset
        if isinstance(self.sensitive_fields, Unset):
            sensitive_fields = UNSET
        elif isinstance(self.sensitive_fields, list):
            sensitive_fields = self.sensitive_fields

        else:
            sensitive_fields = self.sensitive_fields

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        update: bool | None | Unset
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
        if version is not UNSET:
            field_dict["version"] = version
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_under_test_schema_models_type_0 import ModelUnderTestSchemaModelsType0

        d = dict(src_dict)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_models(data: object) -> ModelUnderTestSchemaModelsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                models_type_0 = ModelUnderTestSchemaModelsType0.from_dict(data)

                return models_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ModelUnderTestSchemaModelsType0 | None | Unset, data)

        models = _parse_models(d.pop("models", UNSET))

        version = d.pop("version", UNSET)

        def _parse_sensitive_fields(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sensitive_fields_type_0 = cast(list[str], data)

                return sensitive_fields_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        sensitive_fields = _parse_sensitive_fields(d.pop("sensitive_fields", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_project_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_update(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        update = _parse_update(d.pop("update", UNSET))

        model_under_test_schema = cls(
            name=name,
            models=models,
            version=version,
            sensitive_fields=sensitive_fields,
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
