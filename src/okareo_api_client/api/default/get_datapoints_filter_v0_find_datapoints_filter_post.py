from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.datapoint_filter_search import DatapointFilterSearch
from ...models.datapoint_list_item import DatapointListItem
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    json_body: DatapointFilterSearch,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v0/find_datapoints_filter",
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, List["DatapointListItem"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = DatapointListItem.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[ErrorResponse, List["DatapointListItem"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DatapointFilterSearch,
    api_key: str,
) -> Response[Union[ErrorResponse, List["DatapointListItem"]]]:
    """Get Datapoints Filter

     Gets all the datapoints for given search criteria.

    Returns:
        list: An array of datapoint objects.

    Args:
        api_key (str):
        json_body (DatapointFilterSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['DatapointListItem']]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DatapointFilterSearch,
    api_key: str,
) -> Optional[Union[ErrorResponse, List["DatapointListItem"]]]:
    """Get Datapoints Filter

     Gets all the datapoints for given search criteria.

    Returns:
        list: An array of datapoint objects.

    Args:
        api_key (str):
        json_body (DatapointFilterSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['DatapointListItem']]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DatapointFilterSearch,
    api_key: str,
) -> Response[Union[ErrorResponse, List["DatapointListItem"]]]:
    """Get Datapoints Filter

     Gets all the datapoints for given search criteria.

    Returns:
        list: An array of datapoint objects.

    Args:
        api_key (str):
        json_body (DatapointFilterSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['DatapointListItem']]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DatapointFilterSearch,
    api_key: str,
) -> Optional[Union[ErrorResponse, List["DatapointListItem"]]]:
    """Get Datapoints Filter

     Gets all the datapoints for given search criteria.

    Returns:
        list: An array of datapoint objects.

    Args:
        api_key (str):
        json_body (DatapointFilterSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['DatapointListItem']]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
