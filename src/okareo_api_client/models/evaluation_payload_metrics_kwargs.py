from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EvaluationPayloadMetricsKwargs")


@_attrs_define
class EvaluationPayloadMetricsKwargs:
    """Dictionary of metrics to be measured"""

    additional_properties: dict[str, Union[list[int], list[str]]] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        evaluation_payload_metrics_kwargs = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(data: object) -> Union[list[int], list[str]]:
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_0 = cast(list[int], data)

                    return additional_property_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, list):
                    raise TypeError()
                additional_property_type_1 = cast(list[str], data)

                return additional_property_type_1

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        evaluation_payload_metrics_kwargs.additional_properties = additional_properties
        return evaluation_payload_metrics_kwargs

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union[list[int], list[str]]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Union[list[int], list[str]]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
