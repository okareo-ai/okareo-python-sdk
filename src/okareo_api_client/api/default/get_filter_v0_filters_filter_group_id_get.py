from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.datapoint_filter_item import DatapointFilterItem
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    filter_group_id: str,
    *,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    return {
        "method": "get",
        "url": "/v0/filters/{filter_group_id}".format(
            filter_group_id=filter_group_id,
        ),
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DatapointFilterItem, ErrorResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DatapointFilterItem.from_dict(response.json())

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
) -> Response[Union[DatapointFilterItem, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    filter_group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Response[Union[DatapointFilterItem, ErrorResponse]]:
    """Get Filter

     Get a specific datapoint filter.

    Args:
        request: The FastAPI request object
        project_id: UUID of the project the filter belongs to
        filter_group_id: UUID of the specific filter group to retrieve

    Returns:
        The requested filter item

    Args:
        filter_group_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DatapointFilterItem, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        filter_group_id=filter_group_id,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    filter_group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Optional[Union[DatapointFilterItem, ErrorResponse]]:
    """Get Filter

     Get a specific datapoint filter.

    Args:
        request: The FastAPI request object
        project_id: UUID of the project the filter belongs to
        filter_group_id: UUID of the specific filter group to retrieve

    Returns:
        The requested filter item

    Args:
        filter_group_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DatapointFilterItem, ErrorResponse]
    """

    return sync_detailed(
        filter_group_id=filter_group_id,
        client=client,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    filter_group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Response[Union[DatapointFilterItem, ErrorResponse]]:
    """Get Filter

     Get a specific datapoint filter.

    Args:
        request: The FastAPI request object
        project_id: UUID of the project the filter belongs to
        filter_group_id: UUID of the specific filter group to retrieve

    Returns:
        The requested filter item

    Args:
        filter_group_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DatapointFilterItem, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        filter_group_id=filter_group_id,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    filter_group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Optional[Union[DatapointFilterItem, ErrorResponse]]:
    """Get Filter

     Get a specific datapoint filter.

    Args:
        request: The FastAPI request object
        project_id: UUID of the project the filter belongs to
        filter_group_id: UUID of the specific filter group to retrieve

    Returns:
        The requested filter item

    Args:
        filter_group_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DatapointFilterItem, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            filter_group_id=filter_group_id,
            client=client,
            api_key=api_key,
        )
    ).parsed
