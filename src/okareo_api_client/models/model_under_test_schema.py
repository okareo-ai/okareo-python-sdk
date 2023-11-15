from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_run_model_payload import TestRunModelPayload


T = TypeVar("T", bound="ModelUnderTestSchema")


@_attrs_define
class ModelUnderTestSchema:
    """
    Attributes:
        name (Union[Unset, str]):
        model (Union[Unset, TestRunModelPayload]):
        tags (Union[Unset, List[str]]):
        project_id (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    model: Union[Unset, "TestRunModelPayload"] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    project_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.model, Unset):
            model = self.model.to_dict()

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if model is not UNSET:
            field_dict["model"] = model
        if tags is not UNSET:
            field_dict["tags"] = tags
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_run_model_payload import TestRunModelPayload

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _model = d.pop("model", UNSET)
        model: Union[Unset, TestRunModelPayload]
        if isinstance(_model, Unset):
            model = UNSET
        else:
            model = TestRunModelPayload.from_dict(_model)

        tags = cast(List[str], d.pop("tags", UNSET))

        project_id = d.pop("project_id", UNSET)

        model_under_test_schema = cls(
            name=name,
            model=model,
            tags=tags,
            project_id=project_id,
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
