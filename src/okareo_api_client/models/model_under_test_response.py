from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_under_test_response_deprecated_params import ModelUnderTestResponseDeprecatedParams
    from ..models.model_under_test_response_models import ModelUnderTestResponseModels


T = TypeVar("T", bound="ModelUnderTestResponse")


@_attrs_define
class ModelUnderTestResponse:
    """
    Attributes:
        id (UUID):
        project_id (UUID):
        name (str):
        tags (list[str]):
        time_created (str):
        version (int | Unset):  Default: 1.
        models (ModelUnderTestResponseModels | None | Unset):
        sensitive_fields (list[str] | None | Unset):
        datapoint_count (int | None | Unset):
        app_link (str | Unset): This URL links to the Okareo webpage for this model Default: ''.
        deprecated_params (ModelUnderTestResponseDeprecatedParams | None | Unset): Deprecated parameters for backward
            compatibility.
        warning (None | str | Unset):
    """

    id: UUID
    project_id: UUID
    name: str
    tags: list[str]
    time_created: str
    version: int | Unset = 1
    models: ModelUnderTestResponseModels | None | Unset = UNSET
    sensitive_fields: list[str] | None | Unset = UNSET
    datapoint_count: int | None | Unset = UNSET
    app_link: str | Unset = ""
    deprecated_params: ModelUnderTestResponseDeprecatedParams | None | Unset = UNSET
    warning: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.model_under_test_response_deprecated_params import ModelUnderTestResponseDeprecatedParams
        from ..models.model_under_test_response_models import ModelUnderTestResponseModels

        id = str(self.id)

        project_id = str(self.project_id)

        name = self.name

        tags = self.tags

        time_created = self.time_created

        version = self.version

        models: dict[str, Any] | None | Unset
        if isinstance(self.models, Unset):
            models = UNSET
        elif isinstance(self.models, ModelUnderTestResponseModels):
            models = self.models.to_dict()
        else:
            models = self.models

        sensitive_fields: list[str] | None | Unset
        if isinstance(self.sensitive_fields, Unset):
            sensitive_fields = UNSET
        elif isinstance(self.sensitive_fields, list):
            sensitive_fields = self.sensitive_fields

        else:
            sensitive_fields = self.sensitive_fields

        datapoint_count: int | None | Unset
        if isinstance(self.datapoint_count, Unset):
            datapoint_count = UNSET
        else:
            datapoint_count = self.datapoint_count

        app_link = self.app_link

        deprecated_params: dict[str, Any] | None | Unset
        if isinstance(self.deprecated_params, Unset):
            deprecated_params = UNSET
        elif isinstance(self.deprecated_params, ModelUnderTestResponseDeprecatedParams):
            deprecated_params = self.deprecated_params.to_dict()
        else:
            deprecated_params = self.deprecated_params

        warning: None | str | Unset
        if isinstance(self.warning, Unset):
            warning = UNSET
        else:
            warning = self.warning

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "name": name,
                "tags": tags,
                "time_created": time_created,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version
        if models is not UNSET:
            field_dict["models"] = models
        if sensitive_fields is not UNSET:
            field_dict["sensitive_fields"] = sensitive_fields
        if datapoint_count is not UNSET:
            field_dict["datapoint_count"] = datapoint_count
        if app_link is not UNSET:
            field_dict["app_link"] = app_link
        if deprecated_params is not UNSET:
            field_dict["deprecated_params"] = deprecated_params
        if warning is not UNSET:
            field_dict["warning"] = warning

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_under_test_response_deprecated_params import ModelUnderTestResponseDeprecatedParams
        from ..models.model_under_test_response_models import ModelUnderTestResponseModels

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        project_id = UUID(d.pop("project_id"))

        name = d.pop("name")

        tags = cast(list[str], d.pop("tags"))

        time_created = d.pop("time_created")

        version = d.pop("version", UNSET)

        def _parse_models(data: object) -> ModelUnderTestResponseModels | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                models_type_0 = ModelUnderTestResponseModels.from_dict(data)

                return models_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ModelUnderTestResponseModels | None | Unset, data)

        models = _parse_models(d.pop("models", UNSET))

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

        def _parse_datapoint_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        datapoint_count = _parse_datapoint_count(d.pop("datapoint_count", UNSET))

        app_link = d.pop("app_link", UNSET)

        def _parse_deprecated_params(data: object) -> ModelUnderTestResponseDeprecatedParams | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                deprecated_params_type_0 = ModelUnderTestResponseDeprecatedParams.from_dict(data)

                return deprecated_params_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ModelUnderTestResponseDeprecatedParams | None | Unset, data)

        deprecated_params = _parse_deprecated_params(d.pop("deprecated_params", UNSET))

        def _parse_warning(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        warning = _parse_warning(d.pop("warning", UNSET))

        model_under_test_response = cls(
            id=id,
            project_id=project_id,
            name=name,
            tags=tags,
            time_created=time_created,
            version=version,
            models=models,
            sensitive_fields=sensitive_fields,
            datapoint_count=datapoint_count,
            app_link=app_link,
            deprecated_params=deprecated_params,
            warning=warning,
        )

        model_under_test_response.additional_properties = d
        return model_under_test_response

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
