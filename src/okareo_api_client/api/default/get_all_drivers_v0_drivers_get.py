from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.driver_model_response import DriverModelResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.voice_driver_model_response import VoiceDriverModelResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    project_id: UUID | Unset = UNSET,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    params: dict[str, Any] = {}

    json_project_id: str | Unset = UNSET
    if not isinstance(project_id, Unset):
        json_project_id = str(project_id)
    params["project_id"] = json_project_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v0/drivers",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[DriverModelResponse | VoiceDriverModelResponse] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:

            def _parse_response_200_item(data: object) -> DriverModelResponse | VoiceDriverModelResponse:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    response_200_item_type_0 = VoiceDriverModelResponse.from_dict(data)

                    return response_200_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_item_type_1 = DriverModelResponse.from_dict(data)

                return response_200_item_type_1

            response_200_item = _parse_response_200_item(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[HTTPValidationError | list[DriverModelResponse | VoiceDriverModelResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    project_id: UUID | Unset = UNSET,
    api_key: str,
) -> Response[HTTPValidationError | list[DriverModelResponse | VoiceDriverModelResponse]]:
    """Get All Drivers

    Args:
        project_id (UUID | Unset): The ID of the project
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[DriverModelResponse | VoiceDriverModelResponse]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    project_id: UUID | Unset = UNSET,
    api_key: str,
) -> HTTPValidationError | list[DriverModelResponse | VoiceDriverModelResponse] | None:
    """Get All Drivers

    Args:
        project_id (UUID | Unset): The ID of the project
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[DriverModelResponse | VoiceDriverModelResponse]
    """

    return sync_detailed(
        client=client,
        project_id=project_id,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    project_id: UUID | Unset = UNSET,
    api_key: str,
) -> Response[HTTPValidationError | list[DriverModelResponse | VoiceDriverModelResponse]]:
    """Get All Drivers

    Args:
        project_id (UUID | Unset): The ID of the project
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[DriverModelResponse | VoiceDriverModelResponse]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    project_id: UUID | Unset = UNSET,
    api_key: str,
) -> HTTPValidationError | list[DriverModelResponse | VoiceDriverModelResponse] | None:
    """Get All Drivers

    Args:
        project_id (UUID | Unset): The ID of the project
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[DriverModelResponse | VoiceDriverModelResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            project_id=project_id,
            api_key=api_key,
        )
    ).parsed
