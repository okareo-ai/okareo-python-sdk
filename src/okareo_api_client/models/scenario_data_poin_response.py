from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scenario_data_poin_response_meta_data import ScenarioDataPoinResponseMetaData


T = TypeVar("T", bound="ScenarioDataPoinResponse")


@_attrs_define
class ScenarioDataPoinResponse:
    """
    Attributes:
        id (str):
        input_ (Union[Unset, Any]):
        result (Union[Unset, Any]):
        meta_data (Union[Unset, ScenarioDataPoinResponseMetaData]):
    """

    id: str
    input_: Union[Unset, Any] = UNSET
    result: Union[Unset, Any] = UNSET
    meta_data: Union[Unset, "ScenarioDataPoinResponseMetaData"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        input_ = self.input_
        result = self.result
        meta_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.meta_data, Unset):
            meta_data = self.meta_data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if input_ is not UNSET:
            field_dict["input"] = input_
        if result is not UNSET:
            field_dict["result"] = result
        if meta_data is not UNSET:
            field_dict["meta_data"] = meta_data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.scenario_data_poin_response_meta_data import ScenarioDataPoinResponseMetaData

        d = src_dict.copy()
        id = d.pop("id")

        input_ = d.pop("input", UNSET)

        result = d.pop("result", UNSET)

        _meta_data = d.pop("meta_data", UNSET)
        meta_data: Union[Unset, ScenarioDataPoinResponseMetaData]
        if isinstance(_meta_data, Unset):
            meta_data = UNSET
        else:
            meta_data = ScenarioDataPoinResponseMetaData.from_dict(_meta_data)

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
