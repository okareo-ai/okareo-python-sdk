from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.provider_integration_response import ProviderIntegrationResponse
from ...models.update_provider_integration_request import UpdateProviderIntegrationRequest
from ...types import Response


def _get_kwargs(
    integration_id: UUID,
    *,
    body: UpdateProviderIntegrationRequest,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v0/integration/{integration_id}".format(
            integration_id=quote(str(integration_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ProviderIntegrationResponse | None:
    if response.status_code == 200:
        response_200 = ProviderIntegrationResponse.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | ProviderIntegrationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    integration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateProviderIntegrationRequest,
    api_key: str,
) -> Response[HTTPValidationError | ProviderIntegrationResponse]:
    """Update Provider Integration

    Args:
        integration_id (UUID):
        api_key (str):
        body (UpdateProviderIntegrationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProviderIntegrationResponse]
    """

    kwargs = _get_kwargs(
        integration_id=integration_id,
        body=body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    integration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateProviderIntegrationRequest,
    api_key: str,
) -> HTTPValidationError | ProviderIntegrationResponse | None:
    """Update Provider Integration

    Args:
        integration_id (UUID):
        api_key (str):
        body (UpdateProviderIntegrationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProviderIntegrationResponse
    """

    return sync_detailed(
        integration_id=integration_id,
        client=client,
        body=body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    integration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateProviderIntegrationRequest,
    api_key: str,
) -> Response[HTTPValidationError | ProviderIntegrationResponse]:
    """Update Provider Integration

    Args:
        integration_id (UUID):
        api_key (str):
        body (UpdateProviderIntegrationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProviderIntegrationResponse]
    """

    kwargs = _get_kwargs(
        integration_id=integration_id,
        body=body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    integration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateProviderIntegrationRequest,
    api_key: str,
) -> HTTPValidationError | ProviderIntegrationResponse | None:
    """Update Provider Integration

    Args:
        integration_id (UUID):
        api_key (str):
        body (UpdateProviderIntegrationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProviderIntegrationResponse
    """

    return (
        await asyncio_detailed(
            integration_id=integration_id,
            client=client,
            body=body,
            api_key=api_key,
        )
    ).parsed
