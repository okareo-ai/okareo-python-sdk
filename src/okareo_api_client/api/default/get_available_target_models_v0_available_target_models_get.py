from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_available_models_response import GetAvailableModelsResponse
from ...types import Response


def _get_kwargs(
    *,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v0/available_target_models",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | GetAvailableModelsResponse | None:
    if response.status_code == 200:
        response_200 = GetAvailableModelsResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | GetAvailableModelsResponse]:
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
) -> Response[ErrorResponse | GetAvailableModelsResponse]:
    r"""Get Available Target Models

     Get a list of available target models from the model configuration registry.

    Returns models from the target_models section in provider/name format (e.g., \"azure/gpt-4o-mini\")
    that can be used in driver_model_id, target_model, or other model configuration fields.

    These models have pre-configured api_base and api_version settings that will be
    automatically applied when the model is used.

    Args:
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetAvailableModelsResponse]
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
) -> ErrorResponse | GetAvailableModelsResponse | None:
    r"""Get Available Target Models

     Get a list of available target models from the model configuration registry.

    Returns models from the target_models section in provider/name format (e.g., \"azure/gpt-4o-mini\")
    that can be used in driver_model_id, target_model, or other model configuration fields.

    These models have pre-configured api_base and api_version settings that will be
    automatically applied when the model is used.

    Args:
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetAvailableModelsResponse
    """

    return sync_detailed(
        client=client,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    api_key: str,
) -> Response[ErrorResponse | GetAvailableModelsResponse]:
    r"""Get Available Target Models

     Get a list of available target models from the model configuration registry.

    Returns models from the target_models section in provider/name format (e.g., \"azure/gpt-4o-mini\")
    that can be used in driver_model_id, target_model, or other model configuration fields.

    These models have pre-configured api_base and api_version settings that will be
    automatically applied when the model is used.

    Args:
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetAvailableModelsResponse]
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
) -> ErrorResponse | GetAvailableModelsResponse | None:
    r"""Get Available Target Models

     Get a list of available target models from the model configuration registry.

    Returns models from the target_models section in provider/name format (e.g., \"azure/gpt-4o-mini\")
    that can be used in driver_model_id, target_model, or other model configuration fields.

    These models have pre-configured api_base and api_version settings that will be
    automatically applied when the model is used.

    Args:
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetAvailableModelsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            api_key=api_key,
        )
    ).parsed
