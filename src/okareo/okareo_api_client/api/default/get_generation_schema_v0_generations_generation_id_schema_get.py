from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    generation_id: str,
    *,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    return {
        "method": "get",
        "url": "/v0/generations/{generation_id}/schema".format(
            generation_id=generation_id,
        ),
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, str]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(str, response.json())
        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    generation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Response[Union[HTTPValidationError, str]]:
    """Get Generation Schema

     gets a specific generation by id/hash for the given user.

    Returns:
        list: An array of generation' objects.

    Args:
        generation_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, str]]
    """

    kwargs = _get_kwargs(
        generation_id=generation_id,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    generation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Optional[Union[HTTPValidationError, str]]:
    """Get Generation Schema

     gets a specific generation by id/hash for the given user.

    Returns:
        list: An array of generation' objects.

    Args:
        generation_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, str]
    """

    return sync_detailed(
        generation_id=generation_id,
        client=client,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    generation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Response[Union[HTTPValidationError, str]]:
    """Get Generation Schema

     gets a specific generation by id/hash for the given user.

    Returns:
        list: An array of generation' objects.

    Args:
        generation_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, str]]
    """

    kwargs = _get_kwargs(
        generation_id=generation_id,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    generation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Optional[Union[HTTPValidationError, str]]:
    """Get Generation Schema

     gets a specific generation by id/hash for the given user.

    Returns:
        list: An array of generation' objects.

    Args:
        generation_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, str]
    """

    return (
        await asyncio_detailed(
            generation_id=generation_id,
            client=client,
            api_key=api_key,
        )
    ).parsed
