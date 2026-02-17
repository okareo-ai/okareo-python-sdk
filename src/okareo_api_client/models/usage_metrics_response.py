from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metric_detail import MetricDetail
    from ..models.metrics import Metrics
    from ..models.usage_metrics_period import UsageMetricsPeriod


T = TypeVar("T", bound="UsageMetricsResponse")


@_attrs_define
class UsageMetricsResponse:
    """Complete response for usage metrics request.

    Example:
        {'organization_id': '123e4567-e89b-12d3-a456-426614174000', 'period': {'start_date': '2026-01-01T00:00:00Z',
            'end_date': '2026-01-31T11:59:59Z'}, 'totals': {'voice_minutes': 1234.56, 'simulations': 450, 'datapoints':
            12500, 'checks': 5600}, 'details': [{'period_start': '2026-01-01T00:00:00Z', 'period_end':
            '2026-01-01T23:59:59Z', 'voice_minutes': 42.5, 'simulations': 15, 'datapoints': 420, 'checks': 180},
            {'period_start': '2026-01-02T00:00:00Z', 'period_end': '2026-01-02T23:59:59Z', 'voice_minutes': 38.2,
            'simulations': 12, 'datapoints': 380, 'checks': 165}]}

    Attributes:
        organization_id (UUID):
        period (UsageMetricsPeriod): Period information for metrics response.
        totals (Metrics): Individual usage metrics.
        details (list[MetricDetail]): Breakdown of metrics by time period based on precision
    """

    organization_id: UUID
    period: UsageMetricsPeriod
    totals: Metrics
    details: list[MetricDetail]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        organization_id = str(self.organization_id)

        period = self.period.to_dict()

        totals = self.totals.to_dict()

        details = []
        for details_item_data in self.details:
            details_item = details_item_data.to_dict()
            details.append(details_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "organization_id": organization_id,
                "period": period,
                "totals": totals,
                "details": details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_detail import MetricDetail
        from ..models.metrics import Metrics
        from ..models.usage_metrics_period import UsageMetricsPeriod

        d = dict(src_dict)
        organization_id = UUID(d.pop("organization_id"))

        period = UsageMetricsPeriod.from_dict(d.pop("period"))

        totals = Metrics.from_dict(d.pop("totals"))

        details = []
        _details = d.pop("details")
        for details_item_data in _details:
            details_item = MetricDetail.from_dict(details_item_data)

            details.append(details_item)

        usage_metrics_response = cls(
            organization_id=organization_id,
            period=period,
            totals=totals,
            details=details,
        )

        usage_metrics_response.additional_properties = d
        return usage_metrics_response

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
