from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vector_db_payload_type import VectorDbPayloadType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vector_db_payload_params import VectorDbPayloadParams


T = TypeVar("T", bound="VectorDbPayload")


@_attrs_define
class VectorDbPayload:
    """
    Attributes:
        type (VectorDbPayloadType):
        api_key (str):
        params (Union[Unset, VectorDbPayloadParams]):
    """

    type: VectorDbPayloadType
    api_key: str
    params: Union[Unset, "VectorDbPayloadParams"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        api_key = self.api_key
        params: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "api_key": api_key,
            }
        )
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.vector_db_payload_params import VectorDbPayloadParams

        d = src_dict.copy()
        type = VectorDbPayloadType(d.pop("type"))

        api_key = d.pop("api_key")

        _params = d.pop("params", UNSET)
        params: Union[Unset, VectorDbPayloadParams]
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = VectorDbPayloadParams.from_dict(_params)

        vector_db_payload = cls(
            type=type,
            api_key=api_key,
            params=params,
        )

        vector_db_payload.additional_properties = d
        return vector_db_payload

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
