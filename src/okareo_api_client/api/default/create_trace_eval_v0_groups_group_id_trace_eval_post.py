from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_trace_eval_v0_groups_group_id_trace_eval_post_response_create_trace_eval_v0_groups_group_id_trace_eval_post import (
    CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost,
)
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response


def _get_kwargs(
    group_id: str,
    *,
    context_token: str,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    params: Dict[str, Any] = {}
    params["context_token"] = context_token

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": "/v0/groups/{group_id}/trace_eval".format(
            group_id=group_id,
        ),
        "params": params,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost, ErrorResponse]
]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = (
            CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost.from_dict(
                response.json()
            )
        )

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
) -> Response[
    Union[CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost, ErrorResponse]
]:
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
    context_token: str,
    api_key: str,
) -> Response[
    Union[CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost, ErrorResponse]
]:
    """Create Trace Eval

     Create a trace evaluation for a group

    Returns:
        The created trace evaluation details

    Args:
        group_id (str): The ID of the group
        context_token (str): The context token for the trace
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost, ErrorResponse]]
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
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    context_token: str,
    api_key: str,
) -> Optional[
    Union[CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost, ErrorResponse]
]:
    """Create Trace Eval

     Create a trace evaluation for a group

    Returns:
        The created trace evaluation details

    Args:
        group_id (str): The ID of the group
        context_token (str): The context token for the trace
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost, ErrorResponse]
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
        context_token=context_token,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    context_token: str,
    api_key: str,
) -> Response[
    Union[CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost, ErrorResponse]
]:
    """Create Trace Eval

     Create a trace evaluation for a group

    Returns:
        The created trace evaluation details

    Args:
        group_id (str): The ID of the group
        context_token (str): The context token for the trace
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        context_token=context_token,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    context_token: str,
    api_key: str,
) -> Optional[
    Union[CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost, ErrorResponse]
]:
    """Create Trace Eval

     Create a trace evaluation for a group

    Returns:
        The created trace evaluation details

    Args:
        group_id (str): The ID of the group
        context_token (str): The context token for the trace
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateTraceEvalV0GroupsGroupIdTraceEvalPostResponseCreateTraceEvalV0GroupsGroupIdTraceEvalPost, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
            context_token=context_token,
            api_key=api_key,
        )
    ).parsed
