from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_model_to_group_v0_groups_group_id_models_post_response_add_model_to_group_v0_groups_group_id_models_post import (
    AddModelToGroupV0GroupsGroupIdModelsPostResponseAddModelToGroupV0GroupsGroupIdModelsPost,
)
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response


def _get_kwargs(
    group_id: UUID,
    *,
    model_id: UUID,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    params: dict[str, Any] = {}

    json_model_id = str(model_id)
    params["model_id"] = json_model_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v0/groups/{group_id}/models".format(
            group_id=quote(str(group_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AddModelToGroupV0GroupsGroupIdModelsPostResponseAddModelToGroupV0GroupsGroupIdModelsPost | ErrorResponse | None:
    if response.status_code == 201:
        response_201 = (
            AddModelToGroupV0GroupsGroupIdModelsPostResponseAddModelToGroupV0GroupsGroupIdModelsPost.from_dict(
                response.json()
            )
        )

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
) -> Response[AddModelToGroupV0GroupsGroupIdModelsPostResponseAddModelToGroupV0GroupsGroupIdModelsPost | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    model_id: UUID,
    api_key: str,
) -> Response[AddModelToGroupV0GroupsGroupIdModelsPostResponseAddModelToGroupV0GroupsGroupIdModelsPost | ErrorResponse]:
    """Add Model To Group

     Add a model to a group.

    Returns:
        A success message

    Args:
        group_id (UUID): The ID of the group
        model_id (UUID): The ID of the model to add
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AddModelToGroupV0GroupsGroupIdModelsPostResponseAddModelToGroupV0GroupsGroupIdModelsPost | ErrorResponse]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        model_id=model_id,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    model_id: UUID,
    api_key: str,
) -> AddModelToGroupV0GroupsGroupIdModelsPostResponseAddModelToGroupV0GroupsGroupIdModelsPost | ErrorResponse | None:
    """Add Model To Group

     Add a model to a group.

    Returns:
        A success message

    Args:
        group_id (UUID): The ID of the group
        model_id (UUID): The ID of the model to add
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AddModelToGroupV0GroupsGroupIdModelsPostResponseAddModelToGroupV0GroupsGroupIdModelsPost | ErrorResponse
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
        model_id=model_id,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    group_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    model_id: UUID,
    api_key: str,
) -> Response[AddModelToGroupV0GroupsGroupIdModelsPostResponseAddModelToGroupV0GroupsGroupIdModelsPost | ErrorResponse]:
    """Add Model To Group

     Add a model to a group.

    Returns:
        A success message

    Args:
        group_id (UUID): The ID of the group
        model_id (UUID): The ID of the model to add
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AddModelToGroupV0GroupsGroupIdModelsPostResponseAddModelToGroupV0GroupsGroupIdModelsPost | ErrorResponse]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        model_id=model_id,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    model_id: UUID,
    api_key: str,
) -> AddModelToGroupV0GroupsGroupIdModelsPostResponseAddModelToGroupV0GroupsGroupIdModelsPost | ErrorResponse | None:
    """Add Model To Group

     Add a model to a group.

    Returns:
        A success message

    Args:
        group_id (UUID): The ID of the group
        model_id (UUID): The ID of the model to add
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AddModelToGroupV0GroupsGroupIdModelsPostResponseAddModelToGroupV0GroupsGroupIdModelsPost | ErrorResponse
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
            model_id=model_id,
            api_key=api_key,
        )
    ).parsed
