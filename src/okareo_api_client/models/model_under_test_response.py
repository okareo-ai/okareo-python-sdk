from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

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
        datapoint_count (Union[Unset, int]):
    """

    id: str
    project_id: str
    name: str
    tags: List[str]
    time_created: str
    datapoint_count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        project_id = self.project_id
        name = self.name
        tags = self.tags

        time_created = self.time_created
        datapoint_count = self.datapoint_count

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
        if datapoint_count is not UNSET:
            field_dict["datapoint_count"] = datapoint_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        project_id = d.pop("project_id")

        name = d.pop("name")

        tags = cast(List[str], d.pop("tags"))

        time_created = d.pop("time_created")

        datapoint_count = d.pop("datapoint_count", UNSET)

        model_under_test_response = cls(
            id=id,
            project_id=project_id,
            name=name,
            tags=tags,
            time_created=time_created,
            datapoint_count=datapoint_count,
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
