import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatapointSchema")


@_attrs_define
class DatapointSchema:
    """
    Attributes:
        tags (List[str]):
        input_ (str):
        result (str):
        feedback (int):
        error_message (str):
        error_code (str):
        context_token (str):
        input_datetime (Union[Unset, None, datetime.datetime]):  Default: isoparse('2023-10-05T20:47:16.651689').
        result_datetime (Union[Unset, None, datetime.datetime]):  Default: isoparse('2023-10-05T20:47:16.651734').
        project_id (Union[Unset, None, int]):
    """

    tags: List[str]
    input_: str
    result: str
    feedback: int
    error_message: str
    error_code: str
    context_token: str
    input_datetime: Union[Unset, None, datetime.datetime] = isoparse(
        "2023-10-05T20:47:16.651689"
    )
    result_datetime: Union[Unset, None, datetime.datetime] = isoparse(
        "2023-10-05T20:47:16.651734"
    )
    project_id: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tags = self.tags

        input_ = self.input_
        result = self.result
        feedback = self.feedback
        error_message = self.error_message
        error_code = self.error_code
        context_token = self.context_token
        input_datetime: Union[Unset, None, str] = UNSET
        if not isinstance(self.input_datetime, Unset):
            input_datetime = (
                self.input_datetime.isoformat() if self.input_datetime else None
            )

        result_datetime: Union[Unset, None, str] = UNSET
        if not isinstance(self.result_datetime, Unset):
            result_datetime = (
                self.result_datetime.isoformat() if self.result_datetime else None
            )

        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tags": tags,
                "input": input_,
                "result": result,
                "feedback": feedback,
                "error_message": error_message,
                "error_code": error_code,
                "context_token": context_token,
            }
        )
        if input_datetime is not UNSET:
            field_dict["input_datetime"] = input_datetime
        if result_datetime is not UNSET:
            field_dict["result_datetime"] = result_datetime
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tags = cast(List[str], d.pop("tags"))

        input_ = d.pop("input")

        result = d.pop("result")

        feedback = d.pop("feedback")

        error_message = d.pop("error_message")

        error_code = d.pop("error_code")

        context_token = d.pop("context_token")

        _input_datetime = d.pop("input_datetime", UNSET)
        input_datetime: Union[Unset, None, datetime.datetime]
        if _input_datetime is None:
            input_datetime = None
        elif isinstance(_input_datetime, Unset):
            input_datetime = UNSET
        else:
            input_datetime = isoparse(_input_datetime)

        _result_datetime = d.pop("result_datetime", UNSET)
        result_datetime: Union[Unset, None, datetime.datetime]
        if _result_datetime is None:
            result_datetime = None
        elif isinstance(_result_datetime, Unset):
            result_datetime = UNSET
        else:
            result_datetime = isoparse(_result_datetime)

        project_id = d.pop("project_id", UNSET)

        datapoint_schema = cls(
            tags=tags,
            input_=input_,
            result=result,
            feedback=feedback,
            error_message=error_message,
            error_code=error_code,
            context_token=context_token,
            input_datetime=input_datetime,
            result_datetime=result_datetime,
            project_id=project_id,
        )

        datapoint_schema.additional_properties = d
        return datapoint_schema

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
