from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_trace_eval_v0_groups_group_id_trace_eval_post_response_create_trace_eval_v0_groups_group_id_trace_eval_post import (
    CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost,
)
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response


def _get_kwargs(
    group_id: UUID,
    *,
    context_token: str,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    params: dict[str, Any] = {}

    params["context_token"] = context_token

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v0/groups/{group_id}/trace_eval".format(
            group_id=quote(str(group_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost
    | ErrorResponse
    | None
):
    if response.status_code == 201:
        response_201 = (
            CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost.from_dict(
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
) -> Response[
    CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost | ErrorResponse
]:
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
    context_token: str,
    api_key: str,
) -> Response[
    CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost | ErrorResponse
]:
    """Create Trace Eval

     Create a trace evaluation for a group

    Returns:
        The created trace evaluation details

    Args:
        group_id (UUID): The ID of the group
        context_token (str): The context token for the trace
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost | ErrorResponse]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        context_token=context_token,
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
    context_token: str,
    api_key: str,
) -> (
    CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost
    | ErrorResponse
    | None
):
    """Create Trace Eval

     Create a trace evaluation for a group

    Returns:
        The created trace evaluation details

    Args:
        group_id (UUID): The ID of the group
        context_token (str): The context token for the trace
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost | ErrorResponse
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
        context_token=context_token,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    group_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    context_token: str,
    api_key: str,
) -> Response[
    CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost | ErrorResponse
]:
    """Create Trace Eval

     Create a trace evaluation for a group

    Returns:
        The created trace evaluation details

    Args:
        group_id (UUID): The ID of the group
        context_token (str): The context token for the trace
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost | ErrorResponse]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        context_token=context_token,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    context_token: str,
    api_key: str,
) -> (
    CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost
    | ErrorResponse
    | None
):
    """Create Trace Eval

     Create a trace evaluation for a group

    Returns:
        The created trace evaluation details

    Args:
        group_id (UUID): The ID of the group
        context_token (str): The context token for the trace
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost | ErrorResponse
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
            context_token=context_token,
            api_key=api_key,
        )
    ).parsed
