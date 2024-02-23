from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TestRunPayloadV2MetricsKwargs")


@_attrs_define
class TestRunPayloadV2MetricsKwargs:
    """Dictionary of metrics to be measured"""

    additional_properties: Dict[str, Union[List[int], List[str]]] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        test_run_payload_v2_metrics_kwargs = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(data: object) -> Union[List[int], List[str]]:
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_0 = cast(List[int], data)

                    return additional_property_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, list):
                    raise TypeError()
                additional_property_type_1 = cast(List[str], data)

                return additional_property_type_1

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        test_run_payload_v2_metrics_kwargs.additional_properties = additional_properties
        return test_run_payload_v2_metrics_kwargs

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union[List[int], List[str]]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Union[List[int], List[str]]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
