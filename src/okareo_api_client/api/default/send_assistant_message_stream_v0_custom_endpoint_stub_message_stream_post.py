from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.assistant_message_request import AssistantMessageRequest
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
        "url": "/v0/custom_endpoint_stub/message/stream",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = response.json()
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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ErrorResponse]:
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
) -> Response[Any | ErrorResponse]:
    r"""Send Assistant Message Stream

     SSE stream stub that emits chunks with mixed roles (agent / system).

    This is a **parse-only test stub**: the full LLM response is generated eagerly
    and then split into word-level SSE chunks with no inter-chunk delay.

    Chunk format::

        {\"thread_id\": ..., \"message_id\": ..., \"role\": \"agent\"|\"system\",
         \"assistant_response\": token, \"is_final\": false}

    The stream starts with a ``role: \"system\"`` chunk (useful for testing
    ``select`` conditions that filter by role), followed by ``role: \"agent\"``
    content chunks, and ends with an ``is_final: true`` agent chunk.

    The ``assistant_response`` content key matches the default
    ``response_message_path`` (``response.assistant_response``) so existing
    integration tests work without change.

    Args:
        api_key (str):
        authorization (None | str | Unset):
        body (AssistantMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
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
) -> Any | ErrorResponse | None:
    r"""Send Assistant Message Stream

     SSE stream stub that emits chunks with mixed roles (agent / system).

    This is a **parse-only test stub**: the full LLM response is generated eagerly
    and then split into word-level SSE chunks with no inter-chunk delay.

    Chunk format::

        {\"thread_id\": ..., \"message_id\": ..., \"role\": \"agent\"|\"system\",
         \"assistant_response\": token, \"is_final\": false}

    The stream starts with a ``role: \"system\"`` chunk (useful for testing
    ``select`` conditions that filter by role), followed by ``role: \"agent\"``
    content chunks, and ends with an ``is_final: true`` agent chunk.

    The ``assistant_response`` content key matches the default
    ``response_message_path`` (``response.assistant_response``) so existing
    integration tests work without change.

    Args:
        api_key (str):
        authorization (None | str | Unset):
        body (AssistantMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
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
) -> Response[Any | ErrorResponse]:
    r"""Send Assistant Message Stream

     SSE stream stub that emits chunks with mixed roles (agent / system).

    This is a **parse-only test stub**: the full LLM response is generated eagerly
    and then split into word-level SSE chunks with no inter-chunk delay.

    Chunk format::

        {\"thread_id\": ..., \"message_id\": ..., \"role\": \"agent\"|\"system\",
         \"assistant_response\": token, \"is_final\": false}

    The stream starts with a ``role: \"system\"`` chunk (useful for testing
    ``select`` conditions that filter by role), followed by ``role: \"agent\"``
    content chunks, and ends with an ``is_final: true`` agent chunk.

    The ``assistant_response`` content key matches the default
    ``response_message_path`` (``response.assistant_response``) so existing
    integration tests work without change.

    Args:
        api_key (str):
        authorization (None | str | Unset):
        body (AssistantMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
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
) -> Any | ErrorResponse | None:
    r"""Send Assistant Message Stream

     SSE stream stub that emits chunks with mixed roles (agent / system).

    This is a **parse-only test stub**: the full LLM response is generated eagerly
    and then split into word-level SSE chunks with no inter-chunk delay.

    Chunk format::

        {\"thread_id\": ..., \"message_id\": ..., \"role\": \"agent\"|\"system\",
         \"assistant_response\": token, \"is_final\": false}

    The stream starts with a ``role: \"system\"`` chunk (useful for testing
    ``select`` conditions that filter by role), followed by ``role: \"agent\"``
    content chunks, and ends with an ``is_final: true`` agent chunk.

    The ``assistant_response`` content key matches the default
    ``response_message_path`` (``response.assistant_response``) so existing
    integration tests work without change.

    Args:
        api_key (str):
        authorization (None | str | Unset):
        body (AssistantMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key=api_key,
            authorization=authorization,
        )
    ).parsed
