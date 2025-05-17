from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.datapoint_summary_item_user_metadata_type_0 import DatapointSummaryItemUserMetadataType0
    from ..models.feedback_range_summary import FeedbackRangeSummary


T = TypeVar("T", bound="DatapointSummaryItem")


@_attrs_define
class DatapointSummaryItem:
    """
    Attributes:
        group (str): The group name or datetime for the data summary.
        datapoints (int): The total count of datapoints for the group.
        issues (int): The total count of issues for the group.
        errors (int): The total count of errors for the group.
        feedback_ranges (Union[Unset, List['FeedbackRangeSummary']]): List of feedback range summaries for the date.
        avg_latency (Union[Unset, float]): The average latency for the group.
        sum_cost (Union[Unset, float]): The total cost for the group.
        user_metadata (Union['DatapointSummaryItemUserMetadataType0', Any, Unset]): Number of distinct values found for
            each key in user metadata for the group.
    """

    group: str
    datapoints: int
    issues: int
    errors: int
    feedback_ranges: Union[Unset, List["FeedbackRangeSummary"]] = UNSET
    avg_latency: Union[Unset, float] = UNSET
    sum_cost: Union[Unset, float] = UNSET
    user_metadata: Union["DatapointSummaryItemUserMetadataType0", Any, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.datapoint_summary_item_user_metadata_type_0 import DatapointSummaryItemUserMetadataType0

        group = self.group
        datapoints = self.datapoints
        issues = self.issues
        errors = self.errors
        feedback_ranges: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.feedback_ranges, Unset):
            feedback_ranges = []
            for feedback_ranges_item_data in self.feedback_ranges:
                feedback_ranges_item = feedback_ranges_item_data.to_dict()

                feedback_ranges.append(feedback_ranges_item)

        avg_latency = self.avg_latency
        sum_cost = self.sum_cost
        user_metadata: Union[Any, Dict[str, Any], Unset]
        if isinstance(self.user_metadata, Unset):
            user_metadata = UNSET

        elif isinstance(self.user_metadata, DatapointSummaryItemUserMetadataType0):
            user_metadata = UNSET
            if not isinstance(self.user_metadata, Unset):
                user_metadata = self.user_metadata.to_dict()

        else:
            user_metadata = self.user_metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "group": group,
                "datapoints": datapoints,
                "issues": issues,
                "errors": errors,
            }
        )
        if feedback_ranges is not UNSET:
            field_dict["feedback_ranges"] = feedback_ranges
        if avg_latency is not UNSET:
            field_dict["avg_latency"] = avg_latency
        if sum_cost is not UNSET:
            field_dict["sum_cost"] = sum_cost
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.datapoint_summary_item_user_metadata_type_0 import DatapointSummaryItemUserMetadataType0
        from ..models.feedback_range_summary import FeedbackRangeSummary

        d = src_dict.copy()
        group = d.pop("group")

        datapoints = d.pop("datapoints")

        issues = d.pop("issues")

        errors = d.pop("errors")

        feedback_ranges = []
        _feedback_ranges = d.pop("feedback_ranges", UNSET)
        for feedback_ranges_item_data in _feedback_ranges or []:
            feedback_ranges_item = FeedbackRangeSummary.from_dict(feedback_ranges_item_data)

            feedback_ranges.append(feedback_ranges_item)

        avg_latency = d.pop("avg_latency", UNSET)

        sum_cost = d.pop("sum_cost", UNSET)

        def _parse_user_metadata(data: object) -> Union["DatapointSummaryItemUserMetadataType0", Any, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _user_metadata_type_0 = data
                user_metadata_type_0: Union[Unset, DatapointSummaryItemUserMetadataType0]
                if isinstance(_user_metadata_type_0, Unset):
                    user_metadata_type_0 = UNSET
                else:
                    user_metadata_type_0 = DatapointSummaryItemUserMetadataType0.from_dict(_user_metadata_type_0)

                return user_metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatapointSummaryItemUserMetadataType0", Any, Unset], data)

        user_metadata = _parse_user_metadata(d.pop("user_metadata", UNSET))

        datapoint_summary_item = cls(
            group=group,
            datapoints=datapoints,
            issues=issues,
            errors=errors,
            feedback_ranges=feedback_ranges,
            avg_latency=avg_latency,
            sum_cost=sum_cost,
            user_metadata=user_metadata,
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
