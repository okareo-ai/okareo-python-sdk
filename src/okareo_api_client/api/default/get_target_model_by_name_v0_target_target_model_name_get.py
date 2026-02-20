from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.target_model_response import TargetModelResponse
from ...types import Response


def _get_kwargs(
    target_model_name: str,
    *,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v0/target/{target_model_name}".format(
            target_model_name=quote(str(target_model_name), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | TargetModelResponse | None:
    if response.status_code == 200:
        response_200 = TargetModelResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | TargetModelResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    target_model_name: str,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> Response[HTTPValidationError | TargetModelResponse]:
    """Get Target Model By Name

    Args:
        target_model_name (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TargetModelResponse]
    """

    kwargs = _get_kwargs(
        target_model_name=target_model_name,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    target_model_name: str,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> HTTPValidationError | TargetModelResponse | None:
    """Get Target Model By Name

    Args:
        target_model_name (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TargetModelResponse
    """

    return sync_detailed(
        target_model_name=target_model_name,
        client=client,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    target_model_name: str,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> Response[HTTPValidationError | TargetModelResponse]:
    """Get Target Model By Name

    Args:
        target_model_name (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TargetModelResponse]
    """

    kwargs = _get_kwargs(
        target_model_name=target_model_name,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    target_model_name: str,
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> HTTPValidationError | TargetModelResponse | None:
    """Get Target Model By Name

    Args:
        target_model_name (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TargetModelResponse
    """

    return (
        await asyncio_detailed(
            target_model_name=target_model_name,
            client=client,
            api_key=api_key,
        )
    ).parsed
