from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.datapoint_filter_search import DatapointFilterSearch
from ...models.error_response import ErrorResponse
from ...models.get_datapoint_counts_v0_filter_counts_post_response_get_datapoint_counts_v0_filter_counts_post import (
    GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost,
)
from ...types import Response


def _get_kwargs(
    *,
    body: DatapointFilterSearch,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v0/filter_counts",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost | None:
    if response.status_code == 200:
        response_200 = GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost.from_dict(
            response.json()
        )

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
) -> Response[ErrorResponse | GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DatapointFilterSearch,
    api_key: str,
) -> Response[ErrorResponse | GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]:
    """Get Datapoint Counts

     Gets only the counts for datapoints matching given filter criteria without retrieving the actual
    data.

    Returns:
        dict: Object containing filtered_count and total_count

    Args:
        api_key (str):
        body (DatapointFilterSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]
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
    body: DatapointFilterSearch,
    api_key: str,
) -> ErrorResponse | GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost | None:
    """Get Datapoint Counts

     Gets only the counts for datapoints matching given filter criteria without retrieving the actual
    data.

    Returns:
        dict: Object containing filtered_count and total_count

    Args:
        api_key (str):
        body (DatapointFilterSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DatapointFilterSearch,
    api_key: str,
) -> Response[ErrorResponse | GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]:
    """Get Datapoint Counts

     Gets only the counts for datapoints matching given filter criteria without retrieving the actual
    data.

    Returns:
        dict: Object containing filtered_count and total_count

    Args:
        api_key (str):
        body (DatapointFilterSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]
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
    body: DatapointFilterSearch,
    api_key: str,
) -> ErrorResponse | GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost | None:
    """Get Datapoint Counts

     Gets only the counts for datapoints matching given filter criteria without retrieving the actual
    data.

    Returns:
        dict: Object containing filtered_count and total_count

    Args:
        api_key (str):
        body (DatapointFilterSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key=api_key,
        )
    ).parsed
