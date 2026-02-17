from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.driver_model_response import DriverModelResponse
from ...models.driver_model_schema import DriverModelSchema
from ...models.error_response import ErrorResponse
from ...models.voice_driver_model_response import VoiceDriverModelResponse
from ...types import Response


def _get_kwargs(
    driver_id: UUID,
    *,
    body: DriverModelSchema,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v0/driver/{driver_id}".format(
            driver_id=quote(str(driver_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DriverModelResponse | VoiceDriverModelResponse | ErrorResponse | None:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> DriverModelResponse | VoiceDriverModelResponse:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = VoiceDriverModelResponse.from_dict(data)

                return response_200_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = DriverModelResponse.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

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
) -> Response[DriverModelResponse | VoiceDriverModelResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    driver_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: DriverModelSchema,
    api_key: str,
) -> Response[DriverModelResponse | VoiceDriverModelResponse | ErrorResponse]:
    """Update Driver Model

    Args:
        driver_id (UUID):
        api_key (str):
        body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DriverModelResponse | VoiceDriverModelResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        driver_id=driver_id,
        body=body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    driver_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: DriverModelSchema,
    api_key: str,
) -> DriverModelResponse | VoiceDriverModelResponse | ErrorResponse | None:
    """Update Driver Model

    Args:
        driver_id (UUID):
        api_key (str):
        body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DriverModelResponse | VoiceDriverModelResponse | ErrorResponse
    """

    return sync_detailed(
        driver_id=driver_id,
        client=client,
        body=body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    driver_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: DriverModelSchema,
    api_key: str,
) -> Response[DriverModelResponse | VoiceDriverModelResponse | ErrorResponse]:
    """Update Driver Model

    Args:
        driver_id (UUID):
        api_key (str):
        body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DriverModelResponse | VoiceDriverModelResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        driver_id=driver_id,
        body=body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    driver_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: DriverModelSchema,
    api_key: str,
) -> DriverModelResponse | VoiceDriverModelResponse | ErrorResponse | None:
    """Update Driver Model

    Args:
        driver_id (UUID):
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
            driver_id=driver_id,
            client=client,
            body=body,
            api_key=api_key,
        )
    ).parsed
