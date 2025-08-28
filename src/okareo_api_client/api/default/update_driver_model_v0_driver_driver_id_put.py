from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.driver_model_schema import DriverModelSchema
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    driver_id: str,
    *,
    json_body: DriverModelSchema,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/v0/driver/{driver_id}".format(
            driver_id=driver_id,
        ),
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ErrorResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = response.json()
        return response_200
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
) -> Response[Union[Any, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    driver_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DriverModelSchema,
    api_key: str,
) -> Response[Union[Any, ErrorResponse]]:
    """Update Driver Model

     Update an existing driver model by ID

    Args:
        driver_id: UUID of the driver model to update
        request: FastAPI request object containing database session and organization info
        payload: Updated driver model data

    Returns:
        The updated driver model

    Raises:
        HTTPException: 404 if driver model is not found

    Args:
        driver_id (str):
        api_key (str):
        json_body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        driver_id=driver_id,
        json_body=json_body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    driver_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DriverModelSchema,
    api_key: str,
) -> Optional[Union[Any, ErrorResponse]]:
    """Update Driver Model

     Update an existing driver model by ID

    Args:
        driver_id: UUID of the driver model to update
        request: FastAPI request object containing database session and organization info
        payload: Updated driver model data

    Returns:
        The updated driver model

    Raises:
        HTTPException: 404 if driver model is not found

    Args:
        driver_id (str):
        api_key (str):
        json_body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return sync_detailed(
        driver_id=driver_id,
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    driver_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DriverModelSchema,
    api_key: str,
) -> Response[Union[Any, ErrorResponse]]:
    """Update Driver Model

     Update an existing driver model by ID

    Args:
        driver_id: UUID of the driver model to update
        request: FastAPI request object containing database session and organization info
        payload: Updated driver model data

    Returns:
        The updated driver model

    Raises:
        HTTPException: 404 if driver model is not found

    Args:
        driver_id (str):
        api_key (str):
        json_body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        driver_id=driver_id,
        json_body=json_body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    driver_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DriverModelSchema,
    api_key: str,
) -> Optional[Union[Any, ErrorResponse]]:
    """Update Driver Model

     Update an existing driver model by ID

    Args:
        driver_id: UUID of the driver model to update
        request: FastAPI request object containing database session and organization info
        payload: Updated driver model data

    Returns:
        The updated driver model

    Raises:
        HTTPException: 404 if driver model is not found

    Args:
        driver_id (str):
        api_key (str):
        json_body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            driver_id=driver_id,
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
