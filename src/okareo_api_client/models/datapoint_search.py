import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatapointSearch")


@_attrs_define
class DatapointSearch:
    """
    Attributes:
        tags (Union[Unset, List[str]]): Tags are strings that can be used to filter datapoints in the Okareo app
        from_date (Union[Unset, datetime.datetime]): Earliest date Default: isoparse('2022-12-31T23:59:59.999999').
        to_date (Union[Unset, datetime.datetime]): Latest date
        feedback (Union[Unset, float]): Feedback is a 0 to 1 float value that captures user feedback range for related
            datapoint results
        error_code (Union[Unset, str]):
        context_token (Union[Unset, str]): Context token is a unique token to link various datapoints which originate
            from the same context
        project_id (Union[Unset, str]): Project ID
        mut_id (Union[Unset, str]): Model ID
        test_run_id (Union[Unset, str]): Test run ID
    """

    tags: Union[Unset, List[str]] = UNSET
    from_date: Union[Unset, datetime.datetime] = isoparse("2022-12-31T23:59:59.999999")
    to_date: Union[Unset, datetime.datetime] = UNSET
    feedback: Union[Unset, float] = UNSET
    error_code: Union[Unset, str] = UNSET
    context_token: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    mut_id: Union[Unset, str] = UNSET
    test_run_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        from_date: Union[Unset, str] = UNSET
        if not isinstance(self.from_date, Unset):
            from_date = self.from_date.isoformat()

        to_date: Union[Unset, str] = UNSET
        if not isinstance(self.to_date, Unset):
            to_date = self.to_date.isoformat()

        feedback = self.feedback
        error_code = self.error_code
        context_token = self.context_token
        project_id = self.project_id
        mut_id = self.mut_id
        test_run_id = self.test_run_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tags is not UNSET:
            field_dict["tags"] = tags
        if from_date is not UNSET:
            field_dict["from_date"] = from_date
        if to_date is not UNSET:
            field_dict["to_date"] = to_date
        if feedback is not UNSET:
            field_dict["feedback"] = feedback
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if context_token is not UNSET:
            field_dict["context_token"] = context_token
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if mut_id is not UNSET:
            field_dict["mut_id"] = mut_id
        if test_run_id is not UNSET:
            field_dict["test_run_id"] = test_run_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tags = cast(List[str], d.pop("tags", UNSET))

        _from_date = d.pop("from_date", UNSET)
        from_date: Union[Unset, datetime.datetime]
        if isinstance(_from_date, Unset):
            from_date = UNSET
        else:
            from_date = isoparse(_from_date)

        _to_date = d.pop("to_date", UNSET)
        to_date: Union[Unset, datetime.datetime]
        if isinstance(_to_date, Unset):
            to_date = UNSET
        else:
            to_date = isoparse(_to_date)

        feedback = d.pop("feedback", UNSET)

        error_code = d.pop("error_code", UNSET)

        context_token = d.pop("context_token", UNSET)

        project_id = d.pop("project_id", UNSET)

        mut_id = d.pop("mut_id", UNSET)

        test_run_id = d.pop("test_run_id", UNSET)

        datapoint_search = cls(
            tags=tags,
            from_date=from_date,
            to_date=to_date,
            feedback=feedback,
            error_code=error_code,
            context_token=context_token,
            project_id=project_id,
            mut_id=mut_id,
            test_run_id=test_run_id,
        )

        datapoint_search.additional_properties = d
        return datapoint_search

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
