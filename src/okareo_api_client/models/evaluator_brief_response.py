import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.evaluator_brief_response_check_config import EvaluatorBriefResponseCheckConfig


T = TypeVar("T", bound="EvaluatorBriefResponse")


@_attrs_define
class EvaluatorBriefResponse:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):  Default: ''.
        output_data_type (Union[Unset, str]):  Default: ''.
        time_created (Union[Unset, datetime.datetime]):
        check_config (Union[Unset, EvaluatorBriefResponseCheckConfig]):
        is_predefined (Union[Unset, bool]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = ""
    output_data_type: Union[Unset, str] = ""
    time_created: Union[Unset, datetime.datetime] = UNSET
    check_config: Union[Unset, "EvaluatorBriefResponseCheckConfig"] = UNSET
    is_predefined: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        description = self.description
        output_data_type = self.output_data_type
        time_created: Union[Unset, str] = UNSET
        if not isinstance(self.time_created, Unset):
            time_created = self.time_created.isoformat()

        check_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.check_config, Unset):
            check_config = self.check_config.to_dict()

        is_predefined = self.is_predefined

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if output_data_type is not UNSET:
            field_dict["output_data_type"] = output_data_type
        if time_created is not UNSET:
            field_dict["time_created"] = time_created
        if check_config is not UNSET:
            field_dict["check_config"] = check_config
        if is_predefined is not UNSET:
            field_dict["is_predefined"] = is_predefined

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.evaluator_brief_response_check_config import EvaluatorBriefResponseCheckConfig

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        output_data_type = d.pop("output_data_type", UNSET)

        _time_created = d.pop("time_created", UNSET)
        time_created: Union[Unset, datetime.datetime]
        if isinstance(_time_created, Unset):
            time_created = UNSET
        else:
            time_created = isoparse(_time_created)

        _check_config = d.pop("check_config", UNSET)
        check_config: Union[Unset, EvaluatorBriefResponseCheckConfig]
        if isinstance(_check_config, Unset):
            check_config = UNSET
        else:
            check_config = EvaluatorBriefResponseCheckConfig.from_dict(_check_config)

        is_predefined = d.pop("is_predefined", UNSET)

        evaluator_brief_response = cls(
            id=id,
            name=name,
            description=description,
            output_data_type=output_data_type,
            time_created=time_created,
            check_config=check_config,
            is_predefined=is_predefined,
        )

        evaluator_brief_response.additional_properties = d
        return evaluator_brief_response

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
