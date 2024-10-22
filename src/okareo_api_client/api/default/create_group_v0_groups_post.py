from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_group_v0_groups_post_response_create_group_v0_groups_post import (
    CreateGroupV0GroupsPostResponseCreateGroupV0GroupsPost,
)
from ...models.create_group_v0_groups_post_source import CreateGroupV0GroupsPostSource
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    json_body: CreateGroupV0GroupsPostSource,
    name: str,
    tags: Union[Unset, None, List[str]] = UNSET,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    params: Dict[str, Any] = {}
    params["name"] = name

    json_tags: Union[Unset, None, List[str]] = UNSET
    if not isinstance(tags, Unset):
        if tags is None:
            json_tags = None
        else:
            json_tags = tags

    params["tags"] = json_tags

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v0/groups",
        "json": json_json_body,
        "params": params,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateGroupV0GroupsPostResponseCreateGroupV0GroupsPost, ErrorResponse]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = CreateGroupV0GroupsPostResponseCreateGroupV0GroupsPost.from_dict(response.json())

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
) -> Response[Union[CreateGroupV0GroupsPostResponseCreateGroupV0GroupsPost, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateGroupV0GroupsPostSource,
    name: str,
    tags: Union[Unset, None, List[str]] = UNSET,
    api_key: str,
) -> Response[Union[CreateGroupV0GroupsPostResponseCreateGroupV0GroupsPost, ErrorResponse]]:
    """Create Group

     Create a new group for models under test or return existing group with the same name.

    Returns:
        The group's details (either newly created or existing)

    Args:
        name (str): The name of the group
        tags (Union[Unset, None, List[str]]): Tags for the group
        api_key (str):
        json_body (CreateGroupV0GroupsPostSource): Log source of the group

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateGroupV0GroupsPostResponseCreateGroupV0GroupsPost, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        name=name,
        tags=tags,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateGroupV0GroupsPostSource,
    name: str,
    tags: Union[Unset, None, List[str]] = UNSET,
    api_key: str,
) -> Optional[Union[CreateGroupV0GroupsPostResponseCreateGroupV0GroupsPost, ErrorResponse]]:
    """Create Group

     Create a new group for models under test or return existing group with the same name.

    Returns:
        The group's details (either newly created or existing)

    Args:
        name (str): The name of the group
        tags (Union[Unset, None, List[str]]): Tags for the group
        api_key (str):
        json_body (CreateGroupV0GroupsPostSource): Log source of the group

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateGroupV0GroupsPostResponseCreateGroupV0GroupsPost, ErrorResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        name=name,
        tags=tags,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateGroupV0GroupsPostSource,
    name: str,
    tags: Union[Unset, None, List[str]] = UNSET,
    api_key: str,
) -> Response[Union[CreateGroupV0GroupsPostResponseCreateGroupV0GroupsPost, ErrorResponse]]:
    """Create Group

     Create a new group for models under test or return existing group with the same name.

    Returns:
        The group's details (either newly created or existing)

    Args:
        name (str): The name of the group
        tags (Union[Unset, None, List[str]]): Tags for the group
        api_key (str):
        json_body (CreateGroupV0GroupsPostSource): Log source of the group

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateGroupV0GroupsPostResponseCreateGroupV0GroupsPost, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        name=name,
        tags=tags,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateGroupV0GroupsPostSource,
    name: str,
    tags: Union[Unset, None, List[str]] = UNSET,
    api_key: str,
) -> Optional[Union[CreateGroupV0GroupsPostResponseCreateGroupV0GroupsPost, ErrorResponse]]:
    """Create Group

     Create a new group for models under test or return existing group with the same name.

    Returns:
        The group's details (either newly created or existing)

    Args:
        name (str): The name of the group
        tags (Union[Unset, None, List[str]]): Tags for the group
        api_key (str):
        json_body (CreateGroupV0GroupsPostSource): Log source of the group

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateGroupV0GroupsPostResponseCreateGroupV0GroupsPost, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            name=name,
            tags=tags,
            api_key=api_key,
        )
    ).parsed
