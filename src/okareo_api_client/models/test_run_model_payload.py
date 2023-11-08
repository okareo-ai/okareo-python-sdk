from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_run_model_payload_type import TestRunModelPayloadType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_run_model_payload_params import TestRunModelPayloadParams


T = TypeVar("T", bound="TestRunModelPayload")


@_attrs_define
class TestRunModelPayload:
    """
    Attributes:
        type (TestRunModelPayloadType):
        url (Union[Unset, str]):
        params (Union[Unset, TestRunModelPayloadParams]):
    """

    type: TestRunModelPayloadType
    url: Union[Unset, str] = UNSET
    params: Union[Unset, "TestRunModelPayloadParams"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        url = self.url
        params: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if url is not UNSET:
            field_dict["url"] = url
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_run_model_payload_params import TestRunModelPayloadParams

        d = src_dict.copy()
        type = TestRunModelPayloadType(d.pop("type"))

        url = d.pop("url", UNSET)

        _params = d.pop("params", UNSET)
        params: Union[Unset, TestRunModelPayloadParams]
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = TestRunModelPayloadParams.from_dict(_params)

        test_run_model_payload = cls(
            type=type,
            url=url,
            params=params,
        )

        test_run_model_payload.additional_properties = d
        return test_run_model_payload

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
