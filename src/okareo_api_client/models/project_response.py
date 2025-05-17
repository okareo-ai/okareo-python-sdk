from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectResponse")


@_attrs_define
class ProjectResponse:
    """
    Attributes:
        id (str):
        name (str):
        onboarding_status (str):
        tags (Union[Unset, List[str]]):
        num_evals (Union[Unset, int]):
    """

    id: str
    name: str
    onboarding_status: str
    tags: Union[Unset, List[str]] = UNSET
    num_evals: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        onboarding_status = self.onboarding_status
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        num_evals = self.num_evals

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "onboarding_status": onboarding_status,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags
        if num_evals is not UNSET:
            field_dict["num_evals"] = num_evals

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        onboarding_status = d.pop("onboarding_status")

        tags = cast(List[str], d.pop("tags", UNSET))

        num_evals = d.pop("num_evals", UNSET)

        project_response = cls(
            id=id,
            name=name,
            onboarding_status=onboarding_status,
            tags=tags,
            num_evals=num_evals,
        )

        project_response.additional_properties = d
        return project_response

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
