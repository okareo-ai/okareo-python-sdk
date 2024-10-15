from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_datapoints_in_group_v0_groups_group_id_datapoints_get_response_201_item import (
    GetDatapointsInGroupV0GroupsGroupIdDatapointsGetResponse201Item,
)
from ...types import Response


def _get_kwargs(
    group_id: str,
    *,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    return {
        "method": "get",
        "url": "/v0/groups/{group_id}/datapoints".format(
            group_id=group_id,
        ),
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, List["GetDatapointsInGroupV0GroupsGroupIdDatapointsGetResponse201Item"]]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = GetDatapointsInGroupV0GroupsGroupIdDatapointsGetResponse201Item.from_dict(
                response_201_item_data
            )

            response_201.append(response_201_item)

        return response_201
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
) -> Response[Union[ErrorResponse, List["GetDatapointsInGroupV0GroupsGroupIdDatapointsGetResponse201Item"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Response[Union[ErrorResponse, List["GetDatapointsInGroupV0GroupsGroupIdDatapointsGetResponse201Item"]]]:
    """Get Datapoints In Group

     Get all datapoints in a specific group.

    Returns:
        A list of datapoints in the group

    Args:
        group_id (str): The ID of the group
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['GetDatapointsInGroupV0GroupsGroupIdDatapointsGetResponse201Item']]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Optional[Union[ErrorResponse, List["GetDatapointsInGroupV0GroupsGroupIdDatapointsGetResponse201Item"]]]:
    """Get Datapoints In Group

     Get all datapoints in a specific group.

    Returns:
        A list of datapoints in the group

    Args:
        group_id (str): The ID of the group
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['GetDatapointsInGroupV0GroupsGroupIdDatapointsGetResponse201Item']]
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Response[Union[ErrorResponse, List["GetDatapointsInGroupV0GroupsGroupIdDatapointsGetResponse201Item"]]]:
    """Get Datapoints In Group

     Get all datapoints in a specific group.

    Returns:
        A list of datapoints in the group

    Args:
        group_id (str): The ID of the group
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['GetDatapointsInGroupV0GroupsGroupIdDatapointsGetResponse201Item']]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Optional[Union[ErrorResponse, List["GetDatapointsInGroupV0GroupsGroupIdDatapointsGetResponse201Item"]]]:
    """Get Datapoints In Group

     Get all datapoints in a specific group.

    Returns:
        A list of datapoints in the group

    Args:
        group_id (str): The ID of the group
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['GetDatapointsInGroupV0GroupsGroupIdDatapointsGetResponse201Item']]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
            api_key=api_key,
        )
    ).parsed
