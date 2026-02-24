from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.assistant_thread_response import AssistantThreadResponse
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    if not isinstance(authorization, Unset):
        headers["authorization"] = authorization

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v0/custom_endpoint_stub/create",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AssistantThreadResponse | ErrorResponse | None:
    if response.status_code == 201:
        response_201 = AssistantThreadResponse.from_dict(response.json())

        return response_201

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


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AssistantThreadResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> Response[AssistantThreadResponse | ErrorResponse]:
    """Create Assistant Thread

     Creates a new Assistant thread with an initial system message.

    Returns:
        AssistantThreadResponse: Contains the thread_id for future messages

    Args:
        api_key (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssistantThreadResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        api_key=api_key,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> AssistantThreadResponse | ErrorResponse | None:
    """Create Assistant Thread

     Creates a new Assistant thread with an initial system message.

    Returns:
        AssistantThreadResponse: Contains the thread_id for future messages

    Args:
        api_key (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssistantThreadResponse | ErrorResponse
    """

    return sync_detailed(
        client=client,
        api_key=api_key,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> Response[AssistantThreadResponse | ErrorResponse]:
    """Create Assistant Thread

     Creates a new Assistant thread with an initial system message.

    Returns:
        AssistantThreadResponse: Contains the thread_id for future messages

    Args:
        api_key (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssistantThreadResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        api_key=api_key,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> AssistantThreadResponse | ErrorResponse | None:
    """Create Assistant Thread

     Creates a new Assistant thread with an initial system message.

    Returns:
        AssistantThreadResponse: Contains the thread_id for future messages

    Args:
        api_key (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssistantThreadResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            api_key=api_key,
            authorization=authorization,
        )
    ).parsed
