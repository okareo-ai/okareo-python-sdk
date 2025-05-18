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
        id (Union[None, UUID, Unset]): ID for the testrun
        project_id (Union[None, UUID, Unset]): ID for the project
        mut_id (Union[None, UUID, Unset]): ID of the model
        scenario_set_id (Union[None, UUID, Unset]): ID of the scenario set
        tags (Union[None, Unset, list[str]]): Tags are strings that can be used to filter test runs in the Okareo app
        return_model_metrics (Union[None, Unset, bool]): Boolean value indicating if model metrics should be returned.
            This increases the response size. Default: False.
        return_error_matrix (Union[None, Unset, bool]): Boolean value indicating if error matrix should be returned.
            This increases the response size. Default: False.
    """

    id: Union[None, UUID, Unset] = UNSET
    project_id: Union[None, UUID, Unset] = UNSET
    mut_id: Union[None, UUID, Unset] = UNSET
    scenario_set_id: Union[None, UUID, Unset] = UNSET
    tags: Union[None, Unset, list[str]] = UNSET
    return_model_metrics: Union[None, Unset, bool] = False
    return_error_matrix: Union[None, Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        elif isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        mut_id: Union[None, Unset, str]
        if isinstance(self.mut_id, Unset):
            mut_id = UNSET
        elif isinstance(self.mut_id, UUID):
            mut_id = str(self.mut_id)
        else:
            mut_id = self.mut_id

        scenario_set_id: Union[None, Unset, str]
        if isinstance(self.scenario_set_id, Unset):
            scenario_set_id = UNSET
        elif isinstance(self.scenario_set_id, UUID):
            scenario_set_id = str(self.scenario_set_id)
        else:
            scenario_set_id = self.scenario_set_id

        tags: Union[None, Unset, list[str]]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        return_model_metrics: Union[None, Unset, bool]
        if isinstance(self.return_model_metrics, Unset):
            return_model_metrics = UNSET
        else:
            return_model_metrics = self.return_model_metrics

        return_error_matrix: Union[None, Unset, bool]
        if isinstance(self.return_error_matrix, Unset):
            return_error_matrix = UNSET
        else:
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

        def _parse_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                id_type_0 = UUID(data)

                return id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_project_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_mut_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mut_id_type_0 = UUID(data)

                return mut_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        mut_id = _parse_mut_id(d.pop("mut_id", UNSET))

        def _parse_scenario_set_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scenario_set_id_type_0 = UUID(data)

                return scenario_set_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        scenario_set_id = _parse_scenario_set_id(d.pop("scenario_set_id", UNSET))

        def _parse_tags(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_return_model_metrics(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        return_model_metrics = _parse_return_model_metrics(d.pop("return_model_metrics", UNSET))

        def _parse_return_error_matrix(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        return_error_matrix = _parse_return_error_matrix(d.pop("return_error_matrix", UNSET))

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
