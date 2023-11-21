from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TestRunPayloadV2MetricsKwargs")


@_attrs_define
class TestRunPayloadV2MetricsKwargs:
    """ """

    additional_properties: Dict[str, List[int]] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        test_run_payload_v2_metrics_kwargs = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = cast(List[int], prop_dict)

            additional_properties[prop_name] = additional_property

        test_run_payload_v2_metrics_kwargs.additional_properties = additional_properties
        return test_run_payload_v2_metrics_kwargs

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> List[int]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: List[int]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
