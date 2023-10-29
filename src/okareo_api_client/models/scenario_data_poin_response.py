from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scenario_data_poin_response_result_type_0 import ScenarioDataPoinResponseResultType0


T = TypeVar("T", bound="ScenarioDataPoinResponse")


@_attrs_define
class ScenarioDataPoinResponse:
    """
    Attributes:
        id (str):
        input_ (str):
        result (Union['ScenarioDataPoinResponseResultType0', List[Any], str]):
        meta_data (Union[Unset, str]):
    """

    id: str
    input_: str
    result: Union["ScenarioDataPoinResponseResultType0", List[Any], str]
    meta_data: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.scenario_data_poin_response_result_type_0 import ScenarioDataPoinResponseResultType0

        id = self.id
        input_ = self.input_
        result: Union[Dict[str, Any], List[Any], str]

        if isinstance(self.result, ScenarioDataPoinResponseResultType0):
            result = self.result.to_dict()

        elif isinstance(self.result, list):
            result = self.result

        else:
            result = self.result

        meta_data = self.meta_data

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "input": input_,
                "result": result,
            }
        )
        if meta_data is not UNSET:
            field_dict["meta_data"] = meta_data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.scenario_data_poin_response_result_type_0 import ScenarioDataPoinResponseResultType0

        d = src_dict.copy()
        id = d.pop("id")

        input_ = d.pop("input")

        def _parse_result(data: object) -> Union["ScenarioDataPoinResponseResultType0", List[Any], str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = ScenarioDataPoinResponseResultType0.from_dict(data)

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
            return cast(Union["ScenarioDataPoinResponseResultType0", List[Any], str], data)

        result = _parse_result(d.pop("result"))

        meta_data = d.pop("meta_data", UNSET)

        scenario_data_poin_response = cls(
            id=id,
            input_=input_,
            result=result,
            meta_data=meta_data,
        )

        scenario_data_poin_response.additional_properties = d
        return scenario_data_poin_response

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
