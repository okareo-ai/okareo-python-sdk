from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BodyOauthTokenV0CustomEndpointStubTokenPost")


@_attrs_define
class BodyOauthTokenV0CustomEndpointStubTokenPost:
    """
    Attributes:
        grant_type (str):
        client_id (str | Unset):  Default: ''.
        client_secret (str | Unset):  Default: ''.
        scope (str | Unset):  Default: ''.
    """

    grant_type: str
    client_id: str | Unset = ""
    client_secret: str | Unset = ""
    scope: str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        grant_type = self.grant_type

        client_id = self.client_id

        client_secret = self.client_secret

        scope = self.scope

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "grant_type": grant_type,
            }
        )
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_secret is not UNSET:
            field_dict["client_secret"] = client_secret
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        grant_type = d.pop("grant_type")

        client_id = d.pop("client_id", UNSET)

        client_secret = d.pop("client_secret", UNSET)

        scope = d.pop("scope", UNSET)

        body_oauth_token_v0_custom_endpoint_stub_token_post = cls(
            grant_type=grant_type,
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
        )

        body_oauth_token_v0_custom_endpoint_stub_token_post.additional_properties = d
        return body_oauth_token_v0_custom_endpoint_stub_token_post

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
