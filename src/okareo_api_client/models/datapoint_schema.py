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
        input_datetime (datetime.datetime):
        result_datetime (datetime.datetime):
        mut_id (Union[Unset, str]):
        input_ (Union[Unset, str]):
        result (Union[Unset, str]):
        tags (Union[Unset, List[str]]):
        feedback (Union[Unset, int]):
        error_message (Union[Unset, str]):
        error_code (Union[Unset, str]):
        context_token (Union[Unset, str]):
        test_run_id (Union[Unset, str]):
    """

    input_datetime: datetime.datetime
    result_datetime: datetime.datetime
    mut_id: Union[Unset, str] = UNSET
    input_: Union[Unset, str] = UNSET
    result: Union[Unset, str] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    feedback: Union[Unset, int] = UNSET
    error_message: Union[Unset, str] = UNSET
    error_code: Union[Unset, str] = UNSET
    context_token: Union[Unset, str] = UNSET
    test_run_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_datetime = self.input_datetime.isoformat()

        result_datetime = self.result_datetime.isoformat()

        mut_id = self.mut_id
        input_ = self.input_
        result = self.result
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        feedback = self.feedback
        error_message = self.error_message
        error_code = self.error_code
        context_token = self.context_token
        test_run_id = self.test_run_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input_datetime": input_datetime,
                "result_datetime": result_datetime,
            }
        )
        if mut_id is not UNSET:
            field_dict["mut_id"] = mut_id
        if input_ is not UNSET:
            field_dict["input"] = input_
        if result is not UNSET:
            field_dict["result"] = result
        if tags is not UNSET:
            field_dict["tags"] = tags
        if feedback is not UNSET:
            field_dict["feedback"] = feedback
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if context_token is not UNSET:
            field_dict["context_token"] = context_token
        if test_run_id is not UNSET:
            field_dict["test_run_id"] = test_run_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        input_datetime = isoparse(d.pop("input_datetime"))

        result_datetime = isoparse(d.pop("result_datetime"))

        mut_id = d.pop("mut_id", UNSET)

        input_ = d.pop("input", UNSET)

        result = d.pop("result", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        feedback = d.pop("feedback", UNSET)

        error_message = d.pop("error_message", UNSET)

        error_code = d.pop("error_code", UNSET)

        context_token = d.pop("context_token", UNSET)

        test_run_id = d.pop("test_run_id", UNSET)

        datapoint_schema = cls(
            input_datetime=input_datetime,
            result_datetime=result_datetime,
            mut_id=mut_id,
            input_=input_,
            result=result,
            tags=tags,
            feedback=feedback,
            error_message=error_message,
            error_code=error_code,
            context_token=context_token,
            test_run_id=test_run_id,
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
