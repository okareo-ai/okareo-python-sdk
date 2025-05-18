from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_under_test_response_models_type_0 import ModelUnderTestResponseModelsType0


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
        models (Union['ModelUnderTestResponseModelsType0', None, Unset]):
        datapoint_count (Union[None, Unset, int]):
        app_link (Union[Unset, str]): This URL links to the Okareo webpage for this model Default: ''.
        warning (Union[None, Unset, str]):
    """

    id: UUID
    project_id: UUID
    name: str
    tags: list[str]
    time_created: str
    models: Union["ModelUnderTestResponseModelsType0", None, Unset] = UNSET
    datapoint_count: Union[None, Unset, int] = UNSET
    app_link: Union[Unset, str] = ""
    warning: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.model_under_test_response_models_type_0 import ModelUnderTestResponseModelsType0

        id = str(self.id)

        project_id = str(self.project_id)

        name = self.name

        tags = self.tags

        time_created = self.time_created

        models: Union[None, Unset, dict[str, Any]]
        if isinstance(self.models, Unset):
            models = UNSET
        elif isinstance(self.models, ModelUnderTestResponseModelsType0):
            models = self.models.to_dict()
        else:
            models = self.models

        datapoint_count: Union[None, Unset, int]
        if isinstance(self.datapoint_count, Unset):
            datapoint_count = UNSET
        else:
            datapoint_count = self.datapoint_count

        app_link = self.app_link

        warning: Union[None, Unset, str]
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
        if models is not UNSET:
            field_dict["models"] = models
        if datapoint_count is not UNSET:
            field_dict["datapoint_count"] = datapoint_count
        if app_link is not UNSET:
            field_dict["app_link"] = app_link
        if warning is not UNSET:
            field_dict["warning"] = warning

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_under_test_response_models_type_0 import ModelUnderTestResponseModelsType0

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        project_id = UUID(d.pop("project_id"))

        name = d.pop("name")

        tags = cast(list[str], d.pop("tags"))

        time_created = d.pop("time_created")

        def _parse_models(data: object) -> Union["ModelUnderTestResponseModelsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                models_type_0 = ModelUnderTestResponseModelsType0.from_dict(data)

                return models_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ModelUnderTestResponseModelsType0", None, Unset], data)

        models = _parse_models(d.pop("models", UNSET))

        def _parse_datapoint_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        datapoint_count = _parse_datapoint_count(d.pop("datapoint_count", UNSET))

        app_link = d.pop("app_link", UNSET)

        def _parse_warning(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        warning = _parse_warning(d.pop("warning", UNSET))

        model_under_test_response = cls(
            id=id,
            project_id=project_id,
            name=name,
            tags=tags,
            time_created=time_created,
            models=models,
            datapoint_count=datapoint_count,
            app_link=app_link,
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
