from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_under_test_response_models import ModelUnderTestResponseModels


T = TypeVar("T", bound="ModelUnderTestResponse")


@_attrs_define
class ModelUnderTestResponse:
    """
    Attributes:
        id (str):
        project_id (str):
        name (str):
        tags (List[str]):
        time_created (str):
        models (Union[Unset, ModelUnderTestResponseModels]):
        sensitive_fields (Union[Unset, List[str]]):
        datapoint_count (Union[Unset, int]):
        app_link (Union[Unset, str]): This URL links to the Okareo webpage for this model Default: ''.
        warning (Union[Unset, str]):
    """

    id: str
    project_id: str
    name: str
    tags: List[str]
    time_created: str
    models: Union[Unset, "ModelUnderTestResponseModels"] = UNSET
    sensitive_fields: Union[Unset, List[str]] = UNSET
    datapoint_count: Union[Unset, int] = UNSET
    app_link: Union[Unset, str] = ""
    warning: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        project_id = self.project_id
        name = self.name
        tags = self.tags

        time_created = self.time_created
        models: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.models, Unset):
            models = self.models.to_dict()

        sensitive_fields: Union[Unset, List[str]] = UNSET
        if not isinstance(self.sensitive_fields, Unset):
            sensitive_fields = self.sensitive_fields

        datapoint_count = self.datapoint_count
        app_link = self.app_link
        warning = self.warning

        field_dict: Dict[str, Any] = {}
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
        if sensitive_fields is not UNSET:
            field_dict["sensitive_fields"] = sensitive_fields
        if datapoint_count is not UNSET:
            field_dict["datapoint_count"] = datapoint_count
        if app_link is not UNSET:
            field_dict["app_link"] = app_link
        if warning is not UNSET:
            field_dict["warning"] = warning

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_under_test_response_models import ModelUnderTestResponseModels

        d = src_dict.copy()
        id = d.pop("id")

        project_id = d.pop("project_id")

        name = d.pop("name")

        tags = cast(List[str], d.pop("tags"))

        time_created = d.pop("time_created")

        _models = d.pop("models", UNSET)
        models: Union[Unset, ModelUnderTestResponseModels]
        if isinstance(_models, Unset):
            models = UNSET
        else:
            models = ModelUnderTestResponseModels.from_dict(_models)

        sensitive_fields = cast(List[str], d.pop("sensitive_fields", UNSET))

        datapoint_count = d.pop("datapoint_count", UNSET)

        app_link = d.pop("app_link", UNSET)

        warning = d.pop("warning", UNSET)

        model_under_test_response = cls(
            id=id,
            project_id=project_id,
            name=name,
            tags=tags,
            time_created=time_created,
            models=models,
            sensitive_fields=sensitive_fields,
            datapoint_count=datapoint_count,
            app_link=app_link,
            warning=warning,
        )

        model_under_test_response.additional_properties = d
        return model_under_test_response

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
