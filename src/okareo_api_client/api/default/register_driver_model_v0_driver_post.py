from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.driver_model_response import DriverModelResponse
from ...models.driver_model_schema import DriverModelSchema
from ...models.error_response import ErrorResponse
from ...models.voice_driver_model_response import VoiceDriverModelResponse
from ...types import Response


def _get_kwargs(
    *,
    body: DriverModelSchema,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v0/driver",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DriverModelResponse | VoiceDriverModelResponse | ErrorResponse | None:
    if response.status_code == 201:

        def _parse_response_201(data: object) -> DriverModelResponse | VoiceDriverModelResponse:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_201_type_0 = VoiceDriverModelResponse.from_dict(data)

                return response_201_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_201_type_1 = DriverModelResponse.from_dict(data)

            return response_201_type_1

        response_201 = _parse_response_201(response.json())

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
) -> Response[DriverModelResponse | VoiceDriverModelResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DriverModelSchema,
    api_key: str,
) -> Response[DriverModelResponse | VoiceDriverModelResponse | ErrorResponse]:
    """Register Driver Model

    Args:
        api_key (str):
        body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DriverModelResponse | VoiceDriverModelResponse | ErrorResponse]
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
    body: DriverModelSchema,
    api_key: str,
) -> DriverModelResponse | VoiceDriverModelResponse | ErrorResponse | None:
    """Register Driver Model

    Args:
        api_key (str):
        body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DriverModelResponse | VoiceDriverModelResponse | ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DriverModelSchema,
    api_key: str,
) -> Response[DriverModelResponse | VoiceDriverModelResponse | ErrorResponse]:
    """Register Driver Model

    Args:
        api_key (str):
        body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DriverModelResponse | VoiceDriverModelResponse | ErrorResponse]
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
    body: DriverModelSchema,
    api_key: str,
) -> DriverModelResponse | VoiceDriverModelResponse | ErrorResponse | None:
    """Register Driver Model

    Args:
        api_key (str):
        body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DriverModelResponse | VoiceDriverModelResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key=api_key,
        )
    ).parsed
