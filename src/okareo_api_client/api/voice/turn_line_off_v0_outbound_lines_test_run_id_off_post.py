from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.outbound_line_item import OutboundLineItem
from ...types import Response


def _get_kwargs(
    test_run_id: UUID,
    *,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v0/outbound/lines/{test_run_id}/off".format(
            test_run_id=quote(str(test_run_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | OutboundLineItem | None:
    if response.status_code == 200:
        response_200 = OutboundLineItem.from_dict(response.json())

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
) -> Response[HTTPValidationError | OutboundLineItem]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    test_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> Response[HTTPValidationError | OutboundLineItem]:
    """Turn Line Off

    Args:
        test_run_id (UUID):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | OutboundLineItem]
    """

    kwargs = _get_kwargs(
        test_run_id=test_run_id,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    test_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> HTTPValidationError | OutboundLineItem | None:
    """Turn Line Off

    Args:
        test_run_id (UUID):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | OutboundLineItem
    """

    return sync_detailed(
        test_run_id=test_run_id,
        client=client,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    test_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> Response[HTTPValidationError | OutboundLineItem]:
    """Turn Line Off

    Args:
        test_run_id (UUID):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | OutboundLineItem]
    """

    kwargs = _get_kwargs(
        test_run_id=test_run_id,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    test_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> HTTPValidationError | OutboundLineItem | None:
    """Turn Line Off

    Args:
        test_run_id (UUID):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | OutboundLineItem
    """

    return (
        await asyncio_detailed(
            test_run_id=test_run_id,
            client=client,
            api_key=api_key,
        )
    ).parsed
