from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

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
        feedback_ranges (list[FeedbackRangeSummary] | None | Unset): List of feedback range summaries for the date.
        avg_latency (float | None | Unset): The average latency for the group.
        sum_cost (float | None | Unset): The total cost for the group.
        user_metadata (Any | DatapointSummaryItemUserMetadataType0 | None | Unset): Number of distinct values found for
            each key in user metadata for the group.
    """

    group: str
    datapoints: int
    issues: int
    errors: int
    feedback_ranges: list[FeedbackRangeSummary] | None | Unset = UNSET
    avg_latency: float | None | Unset = UNSET
    sum_cost: float | None | Unset = UNSET
    user_metadata: Any | DatapointSummaryItemUserMetadataType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.datapoint_summary_item_user_metadata_type_0 import DatapointSummaryItemUserMetadataType0

        group = self.group

        datapoints = self.datapoints

        issues = self.issues

        errors = self.errors

        feedback_ranges: list[dict[str, Any]] | None | Unset
        if isinstance(self.feedback_ranges, Unset):
            feedback_ranges = UNSET
        elif isinstance(self.feedback_ranges, list):
            feedback_ranges = []
            for feedback_ranges_type_0_item_data in self.feedback_ranges:
                feedback_ranges_type_0_item = feedback_ranges_type_0_item_data.to_dict()
                feedback_ranges.append(feedback_ranges_type_0_item)

        else:
            feedback_ranges = self.feedback_ranges

        avg_latency: float | None | Unset
        if isinstance(self.avg_latency, Unset):
            avg_latency = UNSET
        else:
            avg_latency = self.avg_latency

        sum_cost: float | None | Unset
        if isinstance(self.sum_cost, Unset):
            sum_cost = UNSET
        else:
            sum_cost = self.sum_cost

        user_metadata: Any | dict[str, Any] | None | Unset
        if isinstance(self.user_metadata, Unset):
            user_metadata = UNSET
        elif isinstance(self.user_metadata, DatapointSummaryItemUserMetadataType0):
            user_metadata = self.user_metadata.to_dict()
        else:
            user_metadata = self.user_metadata

        field_dict: dict[str, Any] = {}
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.datapoint_summary_item_user_metadata_type_0 import DatapointSummaryItemUserMetadataType0
        from ..models.feedback_range_summary import FeedbackRangeSummary

        d = dict(src_dict)
        group = d.pop("group")

        datapoints = d.pop("datapoints")

        issues = d.pop("issues")

        errors = d.pop("errors")

        def _parse_feedback_ranges(data: object) -> list[FeedbackRangeSummary] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                feedback_ranges_type_0 = []
                _feedback_ranges_type_0 = data
                for feedback_ranges_type_0_item_data in _feedback_ranges_type_0:
                    feedback_ranges_type_0_item = FeedbackRangeSummary.from_dict(feedback_ranges_type_0_item_data)

                    feedback_ranges_type_0.append(feedback_ranges_type_0_item)

                return feedback_ranges_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[FeedbackRangeSummary] | None | Unset, data)

        feedback_ranges = _parse_feedback_ranges(d.pop("feedback_ranges", UNSET))

        def _parse_avg_latency(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        avg_latency = _parse_avg_latency(d.pop("avg_latency", UNSET))

        def _parse_sum_cost(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        sum_cost = _parse_sum_cost(d.pop("sum_cost", UNSET))

        def _parse_user_metadata(data: object) -> Any | DatapointSummaryItemUserMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                user_metadata_type_0 = DatapointSummaryItemUserMetadataType0.from_dict(data)

                return user_metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Any | DatapointSummaryItemUserMetadataType0 | None | Unset, data)

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
