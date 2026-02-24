from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.evaluator_detailed_response import EvaluatorDetailedResponse
from ...types import Response


def _get_kwargs(
    check_id: UUID,
    *,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v0/check/{check_id}".format(
            check_id=quote(str(check_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | EvaluatorDetailedResponse | None:
    if response.status_code == 201:
        response_201 = EvaluatorDetailedResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | EvaluatorDetailedResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    check_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> Response[ErrorResponse | EvaluatorDetailedResponse]:
    """Get Check

     Get a check

    Raises:
        HTTPException: 404 if check_id is not found

    Returns: the check

    Args:
        check_id (UUID): The ID of the Check to get
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | EvaluatorDetailedResponse]
    """

    kwargs = _get_kwargs(
        check_id=check_id,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    check_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> ErrorResponse | EvaluatorDetailedResponse | None:
    """Get Check

     Get a check

    Raises:
        HTTPException: 404 if check_id is not found

    Returns: the check

    Args:
        check_id (UUID): The ID of the Check to get
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | EvaluatorDetailedResponse
    """

    return sync_detailed(
        check_id=check_id,
        client=client,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    check_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> Response[ErrorResponse | EvaluatorDetailedResponse]:
    """Get Check

     Get a check

    Raises:
        HTTPException: 404 if check_id is not found

    Returns: the check

    Args:
        check_id (UUID): The ID of the Check to get
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | EvaluatorDetailedResponse]
    """

    kwargs = _get_kwargs(
        check_id=check_id,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    check_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> ErrorResponse | EvaluatorDetailedResponse | None:
    """Get Check

     Get a check

    Raises:
        HTTPException: 404 if check_id is not found

    Returns: the check

    Args:
        check_id (UUID): The ID of the Check to get
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | EvaluatorDetailedResponse
    """

    return (
        await asyncio_detailed(
            check_id=check_id,
            client=client,
            api_key=api_key,
        )
    ).parsed
