from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_driver_voices_v0_driver_voices_get_response_200_item import (
    GetDriverVoicesV0DriverVoicesGetResponse200Item,
)
from ...types import Response


def _get_kwargs(
    *,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v0/driver_voices",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[GetDriverVoicesV0DriverVoicesGetResponse200Item] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetDriverVoicesV0DriverVoicesGetResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

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
) -> Response[ErrorResponse | list[GetDriverVoicesV0DriverVoicesGetResponse200Item]]:
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
) -> Response[ErrorResponse | list[GetDriverVoicesV0DriverVoicesGetResponse200Item]]:
    r"""Get Driver Voices

     Get the list of available voices for driver models with metadata.

    Returns:
        List of voice dictionaries with:
        - id: Voice ID (UUID)
        - name: Full voice name (e.g., \"Ray - Conversationalist\", used when creating driver)
        - language: Language code (BCP-47 format)
        - gender: Gender (\"feminine\" or \"masculine\")
        - description: Voice description

    Args:
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[GetDriverVoicesV0DriverVoicesGetResponse200Item]]
    """

    kwargs = _get_kwargs(
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> ErrorResponse | list[GetDriverVoicesV0DriverVoicesGetResponse200Item] | None:
    r"""Get Driver Voices

     Get the list of available voices for driver models with metadata.

    Returns:
        List of voice dictionaries with:
        - id: Voice ID (UUID)
        - name: Full voice name (e.g., \"Ray - Conversationalist\", used when creating driver)
        - language: Language code (BCP-47 format)
        - gender: Gender (\"feminine\" or \"masculine\")
        - description: Voice description

    Args:
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[GetDriverVoicesV0DriverVoicesGetResponse200Item]
    """

    return sync_detailed(
        client=client,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> Response[ErrorResponse | list[GetDriverVoicesV0DriverVoicesGetResponse200Item]]:
    r"""Get Driver Voices

     Get the list of available voices for driver models with metadata.

    Returns:
        List of voice dictionaries with:
        - id: Voice ID (UUID)
        - name: Full voice name (e.g., \"Ray - Conversationalist\", used when creating driver)
        - language: Language code (BCP-47 format)
        - gender: Gender (\"feminine\" or \"masculine\")
        - description: Voice description

    Args:
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[GetDriverVoicesV0DriverVoicesGetResponse200Item]]
    """

    kwargs = _get_kwargs(
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> ErrorResponse | list[GetDriverVoicesV0DriverVoicesGetResponse200Item] | None:
    r"""Get Driver Voices

     Get the list of available voices for driver models with metadata.

    Returns:
        List of voice dictionaries with:
        - id: Voice ID (UUID)
        - name: Full voice name (e.g., \"Ray - Conversationalist\", used when creating driver)
        - language: Language code (BCP-47 format)
        - gender: Gender (\"feminine\" or \"masculine\")
        - description: Voice description

    Args:
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[GetDriverVoicesV0DriverVoicesGetResponse200Item]
    """

    return (
        await asyncio_detailed(
            client=client,
            api_key=api_key,
        )
    ).parsed
