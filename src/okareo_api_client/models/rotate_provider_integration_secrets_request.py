from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.rotate_provider_integration_secrets_request_secrets import (
        RotateProviderIntegrationSecretsRequestSecrets,
    )


T = TypeVar("T", bound="RotateProviderIntegrationSecretsRequest")


@_attrs_define
class RotateProviderIntegrationSecretsRequest:
    """
    Attributes:
        secrets (RotateProviderIntegrationSecretsRequestSecrets):
    """

    secrets: RotateProviderIntegrationSecretsRequestSecrets

    def to_dict(self) -> dict[str, Any]:
        secrets = self.secrets.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "secrets": secrets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rotate_provider_integration_secrets_request_secrets import (
            RotateProviderIntegrationSecretsRequestSecrets,
        )

        d = dict(src_dict)
        secrets = RotateProviderIntegrationSecretsRequestSecrets.from_dict(d.pop("secrets"))

        rotate_provider_integration_secrets_request = cls(
            secrets=secrets,
        )

        return rotate_provider_integration_secrets_request
