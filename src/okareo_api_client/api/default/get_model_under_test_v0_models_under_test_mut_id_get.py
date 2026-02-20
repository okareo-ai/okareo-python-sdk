from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.model_under_test_response import ModelUnderTestResponse
from ...types import Response


def _get_kwargs(
    mut_id: UUID,
    *,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v0/models_under_test/{mut_id}".format(
            mut_id=quote(str(mut_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | ModelUnderTestResponse | None:
    if response.status_code == 201:
        response_201 = ModelUnderTestResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | ModelUnderTestResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    mut_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> Response[ErrorResponse | ModelUnderTestResponse]:
    """Get Model Under Test

     Get a model under test

    Returns:
        the requested model under test

    Args:
        mut_id (UUID): The ID of the model
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ModelUnderTestResponse]
    """

    kwargs = _get_kwargs(
        mut_id=mut_id,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    mut_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> ErrorResponse | ModelUnderTestResponse | None:
    """Get Model Under Test

     Get a model under test

    Returns:
        the requested model under test

    Args:
        mut_id (UUID): The ID of the model
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ModelUnderTestResponse
    """

    return sync_detailed(
        mut_id=mut_id,
        client=client,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    mut_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> Response[ErrorResponse | ModelUnderTestResponse]:
    """Get Model Under Test

     Get a model under test

    Returns:
        the requested model under test

    Args:
        mut_id (UUID): The ID of the model
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ModelUnderTestResponse]
    """

    kwargs = _get_kwargs(
        mut_id=mut_id,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    mut_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> ErrorResponse | ModelUnderTestResponse | None:
    """Get Model Under Test

     Get a model under test

    Returns:
        the requested model under test

    Args:
        mut_id (UUID): The ID of the model
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ModelUnderTestResponse
    """

    return (
        await asyncio_detailed(
            mut_id=mut_id,
            client=client,
            api_key=api_key,
        )
    ).parsed
