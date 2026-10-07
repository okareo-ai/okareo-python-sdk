from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.connection_test_request import ConnectionTestRequest
from ...models.connection_test_response import ConnectionTestResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    body: ConnectionTestRequest,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v0/voice/integration/test",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ConnectionTestResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = ConnectionTestResponse.from_dict(response.json())

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
) -> Response[ConnectionTestResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ConnectionTestRequest,
    api_key: str,
) -> Response[ConnectionTestResponse | HTTPValidationError]:
    """Check Unsaved Integration Connection

     Check settings before they are saved. Nothing is stored.

    Args:
        api_key (str):
        body (ConnectionTestRequest): Unsaved settings to check before creating an integration.
            Nothing is stored.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectionTestResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ConnectionTestRequest,
    api_key: str,
) -> ConnectionTestResponse | HTTPValidationError | None:
    """Check Unsaved Integration Connection

     Check settings before they are saved. Nothing is stored.

    Args:
        api_key (str):
        body (ConnectionTestRequest): Unsaved settings to check before creating an integration.
            Nothing is stored.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectionTestResponse | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ConnectionTestRequest,
    api_key: str,
) -> Response[ConnectionTestResponse | HTTPValidationError]:
    """Check Unsaved Integration Connection

     Check settings before they are saved. Nothing is stored.

    Args:
        api_key (str):
        body (ConnectionTestRequest): Unsaved settings to check before creating an integration.
            Nothing is stored.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectionTestResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ConnectionTestRequest,
    api_key: str,
) -> ConnectionTestResponse | HTTPValidationError | None:
    """Check Unsaved Integration Connection

     Check settings before they are saved. Nothing is stored.

    Args:
        api_key (str):
        body (ConnectionTestRequest): Unsaved settings to check before creating an integration.
            Nothing is stored.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectionTestResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key=api_key,
        )
    ).parsed
