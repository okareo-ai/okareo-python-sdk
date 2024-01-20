from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SeedData")


@_attrs_define
class SeedData:
    """
    Attributes:
        input_ (str):
        result (Union[List[str], str]):
    """

    input_: str
    result: Union[List[str], str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_ = self.input_
        result: Union[List[str], str]

        if isinstance(self.result, list):
            result = self.result

        else:
            result = self.result

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input": input_,
                "result": result,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        input_ = d.pop("input")

        def _parse_result(data: object) -> Union[List[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                result_type_1 = cast(List[str], data)

                return result_type_1
            except:  # noqa: E722
                pass
            return cast(Union[List[str], str], data)

        result = _parse_result(d.pop("result"))

        seed_data = cls(
            input_=input_,
            result=result,
        )

        seed_data.additional_properties = d
        return seed_data

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
