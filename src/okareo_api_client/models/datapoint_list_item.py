import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.datapoint_list_item_input_type_0 import DatapointListItemInputType0
    from ..models.datapoint_list_item_result_type_0 import DatapointListItemResultType0


T = TypeVar("T", bound="DatapointListItem")


@_attrs_define
class DatapointListItem:
    """
    Attributes:
        id (str):
        tags (Union[Unset, List[str]]):
        input_ (Union['DatapointListItemInputType0', List[Any], Unset, str]):
        input_datetime (Union[Unset, datetime.datetime]):
        result (Union['DatapointListItemResultType0', List[Any], Unset, str]):
        result_datetime (Union[Unset, datetime.datetime]):
        feedback (Union[Unset, float]):
        error_message (Union[Unset, str]):
        error_code (Union[Unset, str]):
        time_created (Union[Unset, datetime.datetime]):
        context_token (Union[Unset, str]):
        mut_id (Union[Unset, str]):
        project_id (Union[Unset, str]):
        test_run_id (Union[Unset, str]):
    """

    id: str
    tags: Union[Unset, List[str]] = UNSET
    input_: Union["DatapointListItemInputType0", List[Any], Unset, str] = UNSET
    input_datetime: Union[Unset, datetime.datetime] = UNSET
    result: Union["DatapointListItemResultType0", List[Any], Unset, str] = UNSET
    result_datetime: Union[Unset, datetime.datetime] = UNSET
    feedback: Union[Unset, float] = UNSET
    error_message: Union[Unset, str] = UNSET
    error_code: Union[Unset, str] = UNSET
    time_created: Union[Unset, datetime.datetime] = UNSET
    context_token: Union[Unset, str] = UNSET
    mut_id: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    test_run_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.datapoint_list_item_input_type_0 import DatapointListItemInputType0
        from ..models.datapoint_list_item_result_type_0 import DatapointListItemResultType0

        id = self.id
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        input_: Union[Dict[str, Any], List[Any], Unset, str]
        if isinstance(self.input_, Unset):
            input_ = UNSET

        elif isinstance(self.input_, DatapointListItemInputType0):
            input_ = UNSET
            if not isinstance(self.input_, Unset):
                input_ = self.input_.to_dict()

        elif isinstance(self.input_, list):
            input_ = UNSET
            if not isinstance(self.input_, Unset):
                input_ = self.input_

        else:
            input_ = self.input_

        input_datetime: Union[Unset, str] = UNSET
        if not isinstance(self.input_datetime, Unset):
            input_datetime = self.input_datetime.isoformat()

        result: Union[Dict[str, Any], List[Any], Unset, str]
        if isinstance(self.result, Unset):
            result = UNSET

        elif isinstance(self.result, DatapointListItemResultType0):
            result = UNSET
            if not isinstance(self.result, Unset):
                result = self.result.to_dict()

        elif isinstance(self.result, list):
            result = UNSET
            if not isinstance(self.result, Unset):
                result = self.result

        else:
            result = self.result

        result_datetime: Union[Unset, str] = UNSET
        if not isinstance(self.result_datetime, Unset):
            result_datetime = self.result_datetime.isoformat()

        feedback = self.feedback
        error_message = self.error_message
        error_code = self.error_code
        time_created: Union[Unset, str] = UNSET
        if not isinstance(self.time_created, Unset):
            time_created = self.time_created.isoformat()

        context_token = self.context_token
        mut_id = self.mut_id
        project_id = self.project_id
        test_run_id = self.test_run_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags
        if input_ is not UNSET:
            field_dict["input"] = input_
        if input_datetime is not UNSET:
            field_dict["input_datetime"] = input_datetime
        if result is not UNSET:
            field_dict["result"] = result
        if result_datetime is not UNSET:
            field_dict["result_datetime"] = result_datetime
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
        if test_run_id is not UNSET:
            field_dict["test_run_id"] = test_run_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.datapoint_list_item_input_type_0 import DatapointListItemInputType0
        from ..models.datapoint_list_item_result_type_0 import DatapointListItemResultType0

        d = src_dict.copy()
        id = d.pop("id")

        tags = cast(List[str], d.pop("tags", UNSET))

        def _parse_input_(data: object) -> Union["DatapointListItemInputType0", List[Any], Unset, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _input_type_0 = data
                input_type_0: Union[Unset, DatapointListItemInputType0]
                if isinstance(_input_type_0, Unset):
                    input_type_0 = UNSET
                else:
                    input_type_0 = DatapointListItemInputType0.from_dict(_input_type_0)

                return input_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_1 = cast(List[Any], data)

                return input_type_1
            except:  # noqa: E722
                pass
            return cast(Union["DatapointListItemInputType0", List[Any], Unset, str], data)

        input_ = _parse_input_(d.pop("input", UNSET))

        _input_datetime = d.pop("input_datetime", UNSET)
        input_datetime: Union[Unset, datetime.datetime]
        if isinstance(_input_datetime, Unset):
            input_datetime = UNSET
        else:
            input_datetime = isoparse(_input_datetime)

        def _parse_result(data: object) -> Union["DatapointListItemResultType0", List[Any], Unset, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _result_type_0 = data
                result_type_0: Union[Unset, DatapointListItemResultType0]
                if isinstance(_result_type_0, Unset):
                    result_type_0 = UNSET
                else:
                    result_type_0 = DatapointListItemResultType0.from_dict(_result_type_0)

                return result_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                result_type_1 = cast(List[Any], data)

                return result_type_1
            except:  # noqa: E722
                pass
            return cast(Union["DatapointListItemResultType0", List[Any], Unset, str], data)

        result = _parse_result(d.pop("result", UNSET))

        _result_datetime = d.pop("result_datetime", UNSET)
        result_datetime: Union[Unset, datetime.datetime]
        if isinstance(_result_datetime, Unset):
            result_datetime = UNSET
        else:
            result_datetime = isoparse(_result_datetime)

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

        test_run_id = d.pop("test_run_id", UNSET)

        datapoint_list_item = cls(
            id=id,
            tags=tags,
            input_=input_,
            input_datetime=input_datetime,
            result=result,
            result_datetime=result_datetime,
            feedback=feedback,
            error_message=error_message,
            error_code=error_code,
            time_created=time_created,
            context_token=context_token,
            mut_id=mut_id,
            project_id=project_id,
            test_run_id=test_run_id,
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
