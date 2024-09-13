from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GeneralFindPayload")


@_attrs_define
class GeneralFindPayload:
    """
    Attributes:
        id (Union[Unset, str]): ID for the testrun
        project_id (Union[Unset, str]): ID for the project
        mut_id (Union[Unset, str]): ID of the model
        scenario_set_id (Union[Unset, str]): ID of the scenario set
        tags (Union[Unset, List[str]]): Tags are strings that can be used to filter test runs in the Okareo app
        return_model_metrics (Union[Unset, bool]): Boolean value indicating if model metrics should be returned. This
            increases the response size.
        return_error_matrix (Union[Unset, bool]): Boolean value indicating if error matrix should be returned. This
            increases the response size.
    """

    id: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    mut_id: Union[Unset, str] = UNSET
    scenario_set_id: Union[Unset, str] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    return_model_metrics: Union[Unset, bool] = False
    return_error_matrix: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        project_id = self.project_id
        mut_id = self.mut_id
        scenario_set_id = self.scenario_set_id
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        return_model_metrics = self.return_model_metrics
        return_error_matrix = self.return_error_matrix

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if mut_id is not UNSET:
            field_dict["mut_id"] = mut_id
        if scenario_set_id is not UNSET:
            field_dict["scenario_set_id"] = scenario_set_id
        if tags is not UNSET:
            field_dict["tags"] = tags
        if return_model_metrics is not UNSET:
            field_dict["return_model_metrics"] = return_model_metrics
        if return_error_matrix is not UNSET:
            field_dict["return_error_matrix"] = return_error_matrix

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        project_id = d.pop("project_id", UNSET)

        mut_id = d.pop("mut_id", UNSET)

        scenario_set_id = d.pop("scenario_set_id", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        return_model_metrics = d.pop("return_model_metrics", UNSET)

        return_error_matrix = d.pop("return_error_matrix", UNSET)

        general_find_payload = cls(
            id=id,
            project_id=project_id,
            mut_id=mut_id,
            scenario_set_id=scenario_set_id,
            tags=tags,
            return_model_metrics=return_model_metrics,
            return_error_matrix=return_error_matrix,
        )

        general_find_payload.additional_properties = d
        return general_find_payload

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
