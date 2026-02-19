from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.datapoint_filter_delete import DatapointFilterDelete
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    body: DatapointFilterDelete,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v0/filters",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorResponse | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DatapointFilterDelete,
    api_key: str,
) -> Response[Any | ErrorResponse]:
    """Delete Filter

     Delete a datapoint filter.

    Args:
        request: The FastAPI request object
        payload: Filter deletion payload containing filter ID

    Args:
        api_key (str):
        body (DatapointFilterDelete):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
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
    body: DatapointFilterDelete,
    api_key: str,
) -> Any | ErrorResponse | None:
    """Delete Filter

     Delete a datapoint filter.

    Args:
        request: The FastAPI request object
        payload: Filter deletion payload containing filter ID

    Args:
        api_key (str):
        body (DatapointFilterDelete):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DatapointFilterDelete,
    api_key: str,
) -> Response[Any | ErrorResponse]:
    """Delete Filter

     Delete a datapoint filter.

    Args:
        request: The FastAPI request object
        payload: Filter deletion payload containing filter ID

    Args:
        api_key (str):
        body (DatapointFilterDelete):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
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
    body: DatapointFilterDelete,
    api_key: str,
) -> Any | ErrorResponse | None:
    """Delete Filter

     Delete a datapoint filter.

    Args:
        request: The FastAPI request object
        payload: Filter deletion payload containing filter ID

    Args:
        api_key (str):
        body (DatapointFilterDelete):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key=api_key,
        )
    ).parsed
