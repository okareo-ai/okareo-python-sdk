from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FeedbackRangeSummary")


@_attrs_define
class FeedbackRangeSummary:
    """
    Attributes:
        count (int): The total count of feedbacks in the specified range for the given date.
        feedback_range_start (Union[Unset, float]): The start of the feedback range.
    """

    count: int
    feedback_range_start: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        count = self.count
        feedback_range_start = self.feedback_range_start

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
            }
        )
        if feedback_range_start is not UNSET:
            field_dict["feedback_range_start"] = feedback_range_start

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        count = d.pop("count")

        feedback_range_start = d.pop("feedback_range_start", UNSET)

        feedback_range_summary = cls(
            count=count,
            feedback_range_start=feedback_range_start,
        )

        feedback_range_summary.additional_properties = d
        return feedback_range_summary

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
