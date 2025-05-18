import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatapointSchema")


@_attrs_define
class DatapointSchema:
    """
    Attributes:
        input_ (str): Inputted value into the model
        result (str): Outputted value from the model based on the input
        mut_id (Union[None, UUID, Unset]): Model ID
        input_datetime (Union[None, Unset, datetime.datetime]): Datetime for the input
        result_datetime (Union[None, Unset, datetime.datetime]): Datetime for the result
        tags (Union[None, Unset, list[str]]): Tags are strings that can be used to filter datapoints in the Okareo app
        feedback (Union[None, Unset, float]): Feedback is a 0 to 1 float value that captures user feedback range for
            related datapoint results
        error_message (Union[None, Unset, str]):
        error_code (Union[None, Unset, str]):
        context_token (Union[None, Unset, str]): Context token is a unique token to link various datapoints which
            originate from the same context
        test_run_id (Union[None, UUID, Unset]): ID of testrun
        group_id (Union[None, UUID, Unset]): ID of the group
        model_metadata (Union[None, Unset, str]): Additional metadata about the model used for this datapoint
        input_metadata (Union[None, Unset, str]): Metadata about the input
        result_metadata (Union[None, Unset, str]): Metadata about the result
    """

    input_: str
    result: str
    mut_id: Union[None, UUID, Unset] = UNSET
    input_datetime: Union[None, Unset, datetime.datetime] = UNSET
    result_datetime: Union[None, Unset, datetime.datetime] = UNSET
    tags: Union[None, Unset, list[str]] = UNSET
    feedback: Union[None, Unset, float] = UNSET
    error_message: Union[None, Unset, str] = UNSET
    error_code: Union[None, Unset, str] = UNSET
    context_token: Union[None, Unset, str] = UNSET
    test_run_id: Union[None, UUID, Unset] = UNSET
    group_id: Union[None, UUID, Unset] = UNSET
    model_metadata: Union[None, Unset, str] = UNSET
    input_metadata: Union[None, Unset, str] = UNSET
    result_metadata: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_ = self.input_

        result = self.result

        mut_id: Union[None, Unset, str]
        if isinstance(self.mut_id, Unset):
            mut_id = UNSET
        elif isinstance(self.mut_id, UUID):
            mut_id = str(self.mut_id)
        else:
            mut_id = self.mut_id

        input_datetime: Union[None, Unset, str]
        if isinstance(self.input_datetime, Unset):
            input_datetime = UNSET
        elif isinstance(self.input_datetime, datetime.datetime):
            input_datetime = self.input_datetime.isoformat()
        else:
            input_datetime = self.input_datetime

        result_datetime: Union[None, Unset, str]
        if isinstance(self.result_datetime, Unset):
            result_datetime = UNSET
        elif isinstance(self.result_datetime, datetime.datetime):
            result_datetime = self.result_datetime.isoformat()
        else:
            result_datetime = self.result_datetime

        tags: Union[None, Unset, list[str]]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        feedback: Union[None, Unset, float]
        if isinstance(self.feedback, Unset):
            feedback = UNSET
        else:
            feedback = self.feedback

        error_message: Union[None, Unset, str]
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        error_code: Union[None, Unset, str]
        if isinstance(self.error_code, Unset):
            error_code = UNSET
        else:
            error_code = self.error_code

        context_token: Union[None, Unset, str]
        if isinstance(self.context_token, Unset):
            context_token = UNSET
        else:
            context_token = self.context_token

        test_run_id: Union[None, Unset, str]
        if isinstance(self.test_run_id, Unset):
            test_run_id = UNSET
        elif isinstance(self.test_run_id, UUID):
            test_run_id = str(self.test_run_id)
        else:
            test_run_id = self.test_run_id

        group_id: Union[None, Unset, str]
        if isinstance(self.group_id, Unset):
            group_id = UNSET
        elif isinstance(self.group_id, UUID):
            group_id = str(self.group_id)
        else:
            group_id = self.group_id

        model_metadata: Union[None, Unset, str]
        if isinstance(self.model_metadata, Unset):
            model_metadata = UNSET
        else:
            model_metadata = self.model_metadata

        input_metadata: Union[None, Unset, str]
        if isinstance(self.input_metadata, Unset):
            input_metadata = UNSET
        else:
            input_metadata = self.input_metadata

        result_metadata: Union[None, Unset, str]
        if isinstance(self.result_metadata, Unset):
            result_metadata = UNSET
        else:
            result_metadata = self.result_metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input": input_,
                "result": result,
            }
        )
        if mut_id is not UNSET:
            field_dict["mut_id"] = mut_id
        if input_datetime is not UNSET:
            field_dict["input_datetime"] = input_datetime
        if result_datetime is not UNSET:
            field_dict["result_datetime"] = result_datetime
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
        if group_id is not UNSET:
            field_dict["group_id"] = group_id
        if model_metadata is not UNSET:
            field_dict["model_metadata"] = model_metadata
        if input_metadata is not UNSET:
            field_dict["input_metadata"] = input_metadata
        if result_metadata is not UNSET:
            field_dict["result_metadata"] = result_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_ = d.pop("input")

        result = d.pop("result")

        def _parse_mut_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mut_id_type_0 = UUID(data)

                return mut_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        mut_id = _parse_mut_id(d.pop("mut_id", UNSET))

        def _parse_input_datetime(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                input_datetime_type_0 = isoparse(data)

                return input_datetime_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        input_datetime = _parse_input_datetime(d.pop("input_datetime", UNSET))

        def _parse_result_datetime(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                result_datetime_type_0 = isoparse(data)

                return result_datetime_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        result_datetime = _parse_result_datetime(d.pop("result_datetime", UNSET))

        def _parse_tags(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_feedback(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        feedback = _parse_feedback(d.pop("feedback", UNSET))

        def _parse_error_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_error_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_code = _parse_error_code(d.pop("error_code", UNSET))

        def _parse_context_token(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        context_token = _parse_context_token(d.pop("context_token", UNSET))

        def _parse_test_run_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                test_run_id_type_0 = UUID(data)

                return test_run_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        test_run_id = _parse_test_run_id(d.pop("test_run_id", UNSET))

        def _parse_group_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                group_id_type_0 = UUID(data)

                return group_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        group_id = _parse_group_id(d.pop("group_id", UNSET))

        def _parse_model_metadata(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model_metadata = _parse_model_metadata(d.pop("model_metadata", UNSET))

        def _parse_input_metadata(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        input_metadata = _parse_input_metadata(d.pop("input_metadata", UNSET))

        def _parse_result_metadata(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        result_metadata = _parse_result_metadata(d.pop("result_metadata", UNSET))

        datapoint_schema = cls(
            input_=input_,
            result=result,
            mut_id=mut_id,
            input_datetime=input_datetime,
            result_datetime=result_datetime,
            tags=tags,
            feedback=feedback,
            error_message=error_message,
            error_code=error_code,
            context_token=context_token,
            test_run_id=test_run_id,
            group_id=group_id,
            model_metadata=model_metadata,
            input_metadata=input_metadata,
            result_metadata=result_metadata,
        )

        datapoint_schema.additional_properties = d
        return datapoint_schema

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
