from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GeneralFindPayload")


@_attrs_define
class GeneralFindPayload:
    """
    Attributes:
        id (Union[Unset, UUID]): ID for the testrun
        project_id (Union[Unset, UUID]): ID for the project
        mut_id (Union[Unset, UUID]): ID of the model
        scenario_set_id (Union[Unset, UUID]): ID of the scenario set
        tags (Union[Unset, list[str]]): Tags are strings that can be used to filter test runs in the Okareo app
        return_model_metrics (Union[Unset, bool]): Boolean value indicating if model metrics should be returned. This
            increases the response size. Default: False.
        return_error_matrix (Union[Unset, bool]): Boolean value indicating if error matrix should be returned. This
            increases the response size. Default: False.
    """

    id: Union[Unset, UUID] = UNSET
    project_id: Union[Unset, UUID] = UNSET
    mut_id: Union[Unset, UUID] = UNSET
    scenario_set_id: Union[Unset, UUID] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    return_model_metrics: Union[Unset, bool] = False
    return_error_matrix: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        project_id: Union[Unset, str] = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        mut_id: Union[Unset, str] = UNSET
        if not isinstance(self.mut_id, Unset):
            mut_id = str(self.mut_id)

        scenario_set_id: Union[Unset, str] = UNSET
        if not isinstance(self.scenario_set_id, Unset):
            scenario_set_id = str(self.scenario_set_id)

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        return_model_metrics = self.return_model_metrics

        return_error_matrix = self.return_error_matrix

        field_dict: dict[str, Any] = {}
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        _project_id = d.pop("project_id", UNSET)
        project_id: Union[Unset, UUID]
        if isinstance(_project_id, Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)

        _mut_id = d.pop("mut_id", UNSET)
        mut_id: Union[Unset, UUID]
        if isinstance(_mut_id, Unset):
            mut_id = UNSET
        else:
            mut_id = UUID(_mut_id)

        _scenario_set_id = d.pop("scenario_set_id", UNSET)
        scenario_set_id: Union[Unset, UUID]
        if isinstance(_scenario_set_id, Unset):
            scenario_set_id = UNSET
        else:
            scenario_set_id = UUID(_scenario_set_id)

        tags = cast(list[str], d.pop("tags", UNSET))

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
