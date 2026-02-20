from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scenario_data_poin_response_meta_data_type_0 import ScenarioDataPoinResponseMetaDataType0


T = TypeVar("T", bound="ScenarioDataPoinResponse")


@_attrs_define
class ScenarioDataPoinResponse:
    """
    Attributes:
        id (UUID):
        input_ (Any):
        result (Any):
        meta_data (None | ScenarioDataPoinResponseMetaDataType0 | Unset):
    """

    id: UUID
    input_: Any
    result: Any
    meta_data: None | ScenarioDataPoinResponseMetaDataType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.scenario_data_poin_response_meta_data_type_0 import ScenarioDataPoinResponseMetaDataType0

        id = str(self.id)

        input_ = self.input_

        result = self.result

        meta_data: dict[str, Any] | None | Unset
        if isinstance(self.meta_data, Unset):
            meta_data = UNSET
        elif isinstance(self.meta_data, ScenarioDataPoinResponseMetaDataType0):
            meta_data = self.meta_data.to_dict()
        else:
            meta_data = self.meta_data

        field_dict: dict[str, Any] = {}
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scenario_data_poin_response_meta_data_type_0 import ScenarioDataPoinResponseMetaDataType0

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        input_ = d.pop("input")

        result = d.pop("result")

        def _parse_meta_data(data: object) -> None | ScenarioDataPoinResponseMetaDataType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                meta_data_type_0 = ScenarioDataPoinResponseMetaDataType0.from_dict(data)

                return meta_data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ScenarioDataPoinResponseMetaDataType0 | Unset, data)

        meta_data = _parse_meta_data(d.pop("meta_data", UNSET))

        scenario_data_poin_response = cls(
            id=id,
            input_=input_,
            result=result,
            meta_data=meta_data,
        )

        scenario_data_poin_response.additional_properties = d
        return scenario_data_poin_response

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
