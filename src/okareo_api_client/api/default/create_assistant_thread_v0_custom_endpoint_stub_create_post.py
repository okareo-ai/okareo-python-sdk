from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.assistant_thread_response import AssistantThreadResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    return {
        "method": "post",
        "url": "/v0/custom_endpoint_stub/create",
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AssistantThreadResponse, ErrorResponse]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = AssistantThreadResponse.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[AssistantThreadResponse, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Response[Union[AssistantThreadResponse, ErrorResponse]]:
    """Create Assistant Thread

     Creates a new OpenAI Assistant thread with an initial system message.

    Returns:
        AssistantThreadResponse: Contains the thread_id for future messages

    Args:
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AssistantThreadResponse, ErrorResponse]]
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
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Optional[Union[AssistantThreadResponse, ErrorResponse]]:
    """Create Assistant Thread

     Creates a new OpenAI Assistant thread with an initial system message.

    Returns:
        AssistantThreadResponse: Contains the thread_id for future messages

    Args:
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AssistantThreadResponse, ErrorResponse]
    """

    return sync_detailed(
        client=client,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Response[Union[AssistantThreadResponse, ErrorResponse]]:
    """Create Assistant Thread

     Creates a new OpenAI Assistant thread with an initial system message.

    Returns:
        AssistantThreadResponse: Contains the thread_id for future messages

    Args:
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AssistantThreadResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Optional[Union[AssistantThreadResponse, ErrorResponse]]:
    """Create Assistant Thread

     Creates a new OpenAI Assistant thread with an initial system message.

    Returns:
        AssistantThreadResponse: Contains the thread_id for future messages

    Args:
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AssistantThreadResponse, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            api_key=api_key,
        )
    ).parsed
