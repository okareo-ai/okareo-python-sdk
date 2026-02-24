from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.assistant_end_thread_request import AssistantEndThreadRequest
from ...models.assistant_end_thread_response import AssistantEndThreadResponse
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: AssistantEndThreadRequest,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    if not isinstance(authorization, Unset):
        headers["authorization"] = authorization

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v0/custom_endpoint_stub/end",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AssistantEndThreadResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = AssistantEndThreadResponse.from_dict(response.json())

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
) -> Response[AssistantEndThreadResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AssistantEndThreadRequest,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> Response[AssistantEndThreadResponse | ErrorResponse]:
    """End Assistant Thread

     Ends an OpenAI Assistant thread and returns a thread summary.

    Args:
        thread_id: The ID of the thread to end

    Returns:
        A confirmation message

    Args:
        api_key (str):
        authorization (None | str | Unset):
        body (AssistantEndThreadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssistantEndThreadResponse | ErrorResponse]
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
    body: AssistantEndThreadRequest,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> AssistantEndThreadResponse | ErrorResponse | None:
    """End Assistant Thread

     Ends an OpenAI Assistant thread and returns a thread summary.

    Args:
        thread_id: The ID of the thread to end

    Returns:
        A confirmation message

    Args:
        api_key (str):
        authorization (None | str | Unset):
        body (AssistantEndThreadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssistantEndThreadResponse | ErrorResponse
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
    body: AssistantEndThreadRequest,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> Response[AssistantEndThreadResponse | ErrorResponse]:
    """End Assistant Thread

     Ends an OpenAI Assistant thread and returns a thread summary.

    Args:
        thread_id: The ID of the thread to end

    Returns:
        A confirmation message

    Args:
        api_key (str):
        authorization (None | str | Unset):
        body (AssistantEndThreadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssistantEndThreadResponse | ErrorResponse]
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
    body: AssistantEndThreadRequest,
    api_key: str,
    authorization: None | str | Unset = UNSET,
) -> AssistantEndThreadResponse | ErrorResponse | None:
    """End Assistant Thread

     Ends an OpenAI Assistant thread and returns a thread summary.

    Args:
        thread_id: The ID of the thread to end

    Returns:
        A confirmation message

    Args:
        api_key (str):
        authorization (None | str | Unset):
        body (AssistantEndThreadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssistantEndThreadResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key=api_key,
            authorization=authorization,
        )
    ).parsed
