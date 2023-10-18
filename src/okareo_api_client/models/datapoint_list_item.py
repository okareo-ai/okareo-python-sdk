import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatapointListItem")


@_attrs_define
class DatapointListItem:
    """
    Attributes:
        id (str):
        tags (Union[Unset, List[str]]):
        feedback (Union[Unset, int]):
        error_message (Union[Unset, str]):
        error_code (Union[Unset, str]):
        time_created (Union[Unset, datetime.datetime]):
        context_token (Union[Unset, str]):
        mut_id (Union[Unset, str]):
        project_id (Union[Unset, str]):
    """

    id: str
    tags: Union[Unset, List[str]] = UNSET
    feedback: Union[Unset, int] = UNSET
    error_message: Union[Unset, str] = UNSET
    error_code: Union[Unset, str] = UNSET
    time_created: Union[Unset, datetime.datetime] = UNSET
    context_token: Union[Unset, str] = UNSET
    mut_id: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        feedback = self.feedback
        error_message = self.error_message
        error_code = self.error_code
        time_created: Union[Unset, str] = UNSET
        if not isinstance(self.time_created, Unset):
            time_created = self.time_created.isoformat()

        context_token = self.context_token
        mut_id = self.mut_id
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags
        if feedback is not UNSET:
            field_dict["feedback"] = feedback
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if time_created is not UNSET:
            field_dict["time_created"] = time_created
        if context_token is not UNSET:
            field_dict["context_token"] = context_token
        if mut_id is not UNSET:
            field_dict["mut_id"] = mut_id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        tags = cast(List[str], d.pop("tags", UNSET))

        feedback = d.pop("feedback", UNSET)

        error_message = d.pop("error_message", UNSET)

        error_code = d.pop("error_code", UNSET)

        _time_created = d.pop("time_created", UNSET)
        time_created: Union[Unset, datetime.datetime]
        if isinstance(_time_created, Unset):
            time_created = UNSET
        else:
            time_created = isoparse(_time_created)

        context_token = d.pop("context_token", UNSET)

        mut_id = d.pop("mut_id", UNSET)

        project_id = d.pop("project_id", UNSET)

        datapoint_list_item = cls(
            id=id,
            tags=tags,
            feedback=feedback,
            error_message=error_message,
            error_code=error_code,
            time_created=time_created,
            context_token=context_token,
            mut_id=mut_id,
            project_id=project_id,
        )

        datapoint_list_item.additional_properties = d
        return datapoint_list_item

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
