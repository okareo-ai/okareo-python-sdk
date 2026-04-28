from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.conversation_ingest_response import ConversationIngestResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.ingest_payload import IngestPayload
from ...types import Response


def _get_kwargs(
    *,
    body: IngestPayload,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v0/conversations/ingest",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ConversationIngestResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = ConversationIngestResponse.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ConversationIngestResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: IngestPayload,
    api_key: str,
) -> Response[ConversationIngestResponse | HTTPValidationError]:
    """Ingest Conversations

     Ingest voice conversations for monitoring.

    Accepts one or more custom conversations and enqueues them for async
    processing. Each conversation's turns will become Datapoint rows, and
    configured monitors will automatically match and run checks.

    This is the monitoring path, not the simulation path. No ScenarioSets are created.
    The mut_id is optional - when omitted, datapoints are created without MUT association
    and rely entirely on monitor/filter group matching.

    Args:
        payload: Conversation data including project_id and conversation list
        request: FastAPI request object for tenant context

    Returns:
        ConversationIngestResponse with status and conversation identifiers

    Args:
        api_key (str):
        body (IngestPayload): Top-level ingest request with project context.

            This is the monitoring path - conversations are ingested and monitored
            based on filter groups, not associated with a specific MUT like test runs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConversationIngestResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: IngestPayload,
    api_key: str,
) -> ConversationIngestResponse | HTTPValidationError | None:
    """Ingest Conversations

     Ingest voice conversations for monitoring.

    Accepts one or more custom conversations and enqueues them for async
    processing. Each conversation's turns will become Datapoint rows, and
    configured monitors will automatically match and run checks.

    This is the monitoring path, not the simulation path. No ScenarioSets are created.
    The mut_id is optional - when omitted, datapoints are created without MUT association
    and rely entirely on monitor/filter group matching.

    Args:
        payload: Conversation data including project_id and conversation list
        request: FastAPI request object for tenant context

    Returns:
        ConversationIngestResponse with status and conversation identifiers

    Args:
        api_key (str):
        body (IngestPayload): Top-level ingest request with project context.

            This is the monitoring path - conversations are ingested and monitored
            based on filter groups, not associated with a specific MUT like test runs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConversationIngestResponse | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: IngestPayload,
    api_key: str,
) -> Response[ConversationIngestResponse | HTTPValidationError]:
    """Ingest Conversations

     Ingest voice conversations for monitoring.

    Accepts one or more custom conversations and enqueues them for async
    processing. Each conversation's turns will become Datapoint rows, and
    configured monitors will automatically match and run checks.

    This is the monitoring path, not the simulation path. No ScenarioSets are created.
    The mut_id is optional - when omitted, datapoints are created without MUT association
    and rely entirely on monitor/filter group matching.

    Args:
        payload: Conversation data including project_id and conversation list
        request: FastAPI request object for tenant context

    Returns:
        ConversationIngestResponse with status and conversation identifiers

    Args:
        api_key (str):
        body (IngestPayload): Top-level ingest request with project context.

            This is the monitoring path - conversations are ingested and monitored
            based on filter groups, not associated with a specific MUT like test runs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConversationIngestResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: IngestPayload,
    api_key: str,
) -> ConversationIngestResponse | HTTPValidationError | None:
    """Ingest Conversations

     Ingest voice conversations for monitoring.

    Accepts one or more custom conversations and enqueues them for async
    processing. Each conversation's turns will become Datapoint rows, and
    configured monitors will automatically match and run checks.

    This is the monitoring path, not the simulation path. No ScenarioSets are created.
    The mut_id is optional - when omitted, datapoints are created without MUT association
    and rely entirely on monitor/filter group matching.

    Args:
        payload: Conversation data including project_id and conversation list
        request: FastAPI request object for tenant context

    Returns:
        ConversationIngestResponse with status and conversation identifiers

    Args:
        api_key (str):
        body (IngestPayload): Top-level ingest request with project context.

            This is the monitoring path - conversations are ingested and monitored
            based on filter groups, not associated with a specific MUT like test runs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConversationIngestResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key=api_key,
        )
    ).parsed
