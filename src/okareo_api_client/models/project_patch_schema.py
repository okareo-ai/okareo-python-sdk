"""Hand-written model for PATCH /v0/projects/{project_id}.

NOT generated: regenerating the client wholesale is destructive (see the
project-separation plan §7). Mirrors the backend's ProjectPatchSchema — all fields
optional; only the keys actually set are sent (the backend applies exclude_unset
semantics, and refuses explicit nulls with a 400).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectPatchSchema")


@_attrs_define
class ProjectPatchSchema:
    """
    Attributes:
        name (str | Unset): Name of the project
        tags (list[str] | Unset): Tags are strings that can be used to filter projects in the Okareo app
        is_archived (bool | Unset): Archive state. Archived projects are hidden from the project
            picker but remain fully usable.
    """

    name: str | Unset = UNSET
    tags: list[str] | Unset = UNSET
    is_archived: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        if not isinstance(self.name, Unset):
            field_dict["name"] = self.name
        if not isinstance(self.tags, Unset):
            field_dict["tags"] = self.tags
        if not isinstance(self.is_archived, Unset):
            field_dict["is_archived"] = self.is_archived
        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = cast("str | Unset", d.pop("name", UNSET))
        tags = cast("list[str] | Unset", d.pop("tags", UNSET))
        is_archived = cast("bool | Unset", d.pop("is_archived", UNSET))

        project_patch_schema = cls(
            name=name,
            tags=tags,
            is_archived=is_archived,
        )
        project_patch_schema.additional_properties = d
        return project_patch_schema

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
