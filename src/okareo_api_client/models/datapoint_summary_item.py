import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.feedback_range_summary import FeedbackRangeSummary


T = TypeVar("T", bound="DatapointSummaryItem")


@_attrs_define
class DatapointSummaryItem:
    """
    Attributes:
        date (datetime.datetime): The date for the data summary.
        feedback_ranges (Union[Unset, List['FeedbackRangeSummary']]): List of feedback range summaries for the date.
    """

    date: datetime.datetime
    feedback_ranges: Union[Unset, List["FeedbackRangeSummary"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        date = self.date.isoformat()

        feedback_ranges: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.feedback_ranges, Unset):
            feedback_ranges = []
            for feedback_ranges_item_data in self.feedback_ranges:
                feedback_ranges_item = feedback_ranges_item_data.to_dict()

                feedback_ranges.append(feedback_ranges_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
            }
        )
        if feedback_ranges is not UNSET:
            field_dict["feedback_ranges"] = feedback_ranges

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.feedback_range_summary import FeedbackRangeSummary

        d = src_dict.copy()
        date = isoparse(d.pop("date"))

        feedback_ranges = []
        _feedback_ranges = d.pop("feedback_ranges", UNSET)
        for feedback_ranges_item_data in _feedback_ranges or []:
            feedback_ranges_item = FeedbackRangeSummary.from_dict(feedback_ranges_item_data)

            feedback_ranges.append(feedback_ranges_item)

        datapoint_summary_item = cls(
            date=date,
            feedback_ranges=feedback_ranges,
        )

        datapoint_summary_item.additional_properties = d
        return datapoint_summary_item

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
