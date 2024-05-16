from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.seed_data_input_type_0 import SeedDataInputType0
    from ..models.seed_data_result_type_0 import SeedDataResultType0


T = TypeVar("T", bound="SeedData")


@_attrs_define
class SeedData:
    """
    Attributes:
        input_ (Union['SeedDataInputType0', List[Any], str]):
        result (Union['SeedDataResultType0', List[Any], str]):
    """

    input_: Union["SeedDataInputType0", List[Any], str]
    result: Union["SeedDataResultType0", List[Any], str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.seed_data_input_type_0 import SeedDataInputType0
        from ..models.seed_data_result_type_0 import SeedDataResultType0

        input_: Union[Dict[str, Any], List[Any], str]

        if isinstance(self.input_, SeedDataInputType0):
            input_ = self.input_.to_dict()

        elif isinstance(self.input_, list):
            input_ = self.input_

        else:
            input_ = self.input_

        result: Union[Dict[str, Any], List[Any], str]

        if isinstance(self.result, SeedDataResultType0):
            result = self.result.to_dict()

        elif isinstance(self.result, list):
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
        from ..models.seed_data_input_type_0 import SeedDataInputType0
        from ..models.seed_data_result_type_0 import SeedDataResultType0

        d = src_dict.copy()

        def _parse_input_(data: object) -> Union["SeedDataInputType0", List[Any], str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_type_0 = SeedDataInputType0.from_dict(data)

                return input_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_1 = cast(List[Any], data)

                return input_type_1
            except:  # noqa: E722
                pass
            return cast(Union["SeedDataInputType0", List[Any], str], data)

        input_ = _parse_input_(d.pop("input"))

        def _parse_result(data: object) -> Union["SeedDataResultType0", List[Any], str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = SeedDataResultType0.from_dict(data)

                return result_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                result_type_1 = cast(List[Any], data)

                return result_type_1
            except:  # noqa: E722
                pass
            return cast(Union["SeedDataResultType0", List[Any], str], data)

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
