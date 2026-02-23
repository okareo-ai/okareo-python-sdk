from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.assistant_message_request import AssistantMessageRequest
from ...models.assistant_message_response import AssistantMessageResponse
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: AssistantMessageRequest,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    if not isinstance(authorization, Unset):
        headers["authorization"] = authorization

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v0/custom_endpoint_stub/message",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AssistantMessageResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = AssistantMessageResponse.from_dict(response.json())

        return response_200

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
) -> Response[AssistantMessageResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AssistantMessageRequest,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> Response[AssistantMessageResponse | ErrorResponse]:
    """Send Assistant Message

     Sends a new message to an existing OpenAI Assistant thread and returns the response.

    Args:
        payload: Contains thread_id and the user message

    Returns:
        AssistantMessageResponse: Contains the assistant's response

    Args:
        api_key (str):
        authorization (None | str | Unset):
        body (AssistantMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssistantMessageResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        api_key=api_key,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: AssistantMessageRequest,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> AssistantMessageResponse | ErrorResponse | None:
    """Send Assistant Message

     Sends a new message to an existing OpenAI Assistant thread and returns the response.

    Args:
        payload: Contains thread_id and the user message

    Returns:
        AssistantMessageResponse: Contains the assistant's response

    Args:
        api_key (str):
        authorization (None | str | Unset):
        body (AssistantMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssistantMessageResponse | ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key=api_key,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AssistantMessageRequest,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> Response[AssistantMessageResponse | ErrorResponse]:
    """Send Assistant Message

     Sends a new message to an existing OpenAI Assistant thread and returns the response.

    Args:
        payload: Contains thread_id and the user message

    Returns:
        AssistantMessageResponse: Contains the assistant's response

    Args:
        api_key (str):
        authorization (None | str | Unset):
        body (AssistantMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssistantMessageResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        api_key=api_key,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: AssistantMessageRequest,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> AssistantMessageResponse | ErrorResponse | None:
    """Send Assistant Message

     Sends a new message to an existing OpenAI Assistant thread and returns the response.

    Args:
        payload: Contains thread_id and the user message

    Returns:
        AssistantMessageResponse: Contains the assistant's response

    Args:
        api_key (str):
        authorization (None | str | Unset):
        body (AssistantMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssistantMessageResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key=api_key,
            authorization=authorization,
        )
    ).parsed
