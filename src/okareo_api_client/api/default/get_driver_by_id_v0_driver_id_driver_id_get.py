from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    driver_id: str,
    *,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    return {
        "method": "get",
        "url": "/v0/driver_id/{driver_id}".format(
            driver_id=driver_id,
        ),
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = response.json()
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
) -> Response[Union[Any, HTTPValidationError]]:
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
    api_key: str,
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Driver By Id

     Retrieve a driver model by its name.

    Args:
        driver_name: The unique name of the driver model to retrieve
        request: FastAPI request object containing database session

    Returns:
        DriverModelResponse with the driver model details

    Raises:
        HTTPException: 404 if driver model is not found

    Args:
        driver_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        driver_id=driver_id,
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
    api_key: str,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Driver By Id

     Retrieve a driver model by its name.

    Args:
        driver_name: The unique name of the driver model to retrieve
        request: FastAPI request object containing database session

    Returns:
        DriverModelResponse with the driver model details

    Raises:
        HTTPException: 404 if driver model is not found

    Args:
        driver_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        driver_id=driver_id,
        client=client,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    driver_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Driver By Id

     Retrieve a driver model by its name.

    Args:
        driver_name: The unique name of the driver model to retrieve
        request: FastAPI request object containing database session

    Returns:
        DriverModelResponse with the driver model details

    Raises:
        HTTPException: 404 if driver model is not found

    Args:
        driver_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        driver_id=driver_id,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    driver_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Driver By Id

     Retrieve a driver model by its name.

    Args:
        driver_name: The unique name of the driver model to retrieve
        request: FastAPI request object containing database session

    Returns:
        DriverModelResponse with the driver model details

    Raises:
        HTTPException: 404 if driver model is not found

    Args:
        driver_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            driver_id=driver_id,
            client=client,
            api_key=api_key,
        )
    ).parsed
