from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.compare_test_runs_payload import CompareTestRunsPayload
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    body: CompareTestRunsPayload,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v0/test_runs/compare",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorResponse | None:
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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CompareTestRunsPayload,
    api_key: str,
) -> Response[ErrorResponse]:
    """Compare Test Runs

     Compare one or two test runs.

    Send both IDs for a side-by-side comparison.
    Send only one ID for single-run stats.
    Statistical tests are only computed when both runs are provided
    and the type is generation/multi-turn.

    Checks are always paired by their immutable check_id UUID.

    Args:
        api_key (str):
        body (CompareTestRunsPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse]
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
    body: CompareTestRunsPayload,
    api_key: str,
) -> ErrorResponse | None:
    """Compare Test Runs

     Compare one or two test runs.

    Send both IDs for a side-by-side comparison.
    Send only one ID for single-run stats.
    Statistical tests are only computed when both runs are provided
    and the type is generation/multi-turn.

    Checks are always paired by their immutable check_id UUID.

    Args:
        api_key (str):
        body (CompareTestRunsPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CompareTestRunsPayload,
    api_key: str,
) -> Response[ErrorResponse]:
    """Compare Test Runs

     Compare one or two test runs.

    Send both IDs for a side-by-side comparison.
    Send only one ID for single-run stats.
    Statistical tests are only computed when both runs are provided
    and the type is generation/multi-turn.

    Checks are always paired by their immutable check_id UUID.

    Args:
        api_key (str):
        body (CompareTestRunsPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse]
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
    body: CompareTestRunsPayload,
    api_key: str,
) -> ErrorResponse | None:
    """Compare Test Runs

     Compare one or two test runs.

    Send both IDs for a side-by-side comparison.
    Send only one ID for single-run stats.
    Statistical tests are only computed when both runs are provided
    and the type is generation/multi-turn.

    Checks are always paired by their immutable check_id UUID.

    Args:
        api_key (str):
        body (CompareTestRunsPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key=api_key,
        )
    ).parsed
