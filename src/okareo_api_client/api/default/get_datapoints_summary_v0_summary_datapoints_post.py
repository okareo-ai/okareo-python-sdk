from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.datapoint_summary_item import DatapointSummaryItem
from ...models.error_response import ErrorResponse
from ...models.summary_datapoint_search import SummaryDatapointSearch
from ...types import Response


def _get_kwargs(
    *,
    body: SummaryDatapointSearch,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v0/summary_datapoints",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[DatapointSummaryItem] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = DatapointSummaryItem.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[ErrorResponse | list[DatapointSummaryItem]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SummaryDatapointSearch,
    api_key: str,
) -> Response[ErrorResponse | list[DatapointSummaryItem]]:
    """Get Datapoints Summary

     Expects a date range and returns a summary of datapoint counts by group and feedback range.
    Defaults to 90-day lookback window.

    Returns:
        list: An array of datapoint objects.

    Args:
        api_key (str):
        body (SummaryDatapointSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[DatapointSummaryItem]]
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
    body: SummaryDatapointSearch,
    api_key: str,
) -> ErrorResponse | list[DatapointSummaryItem] | None:
    """Get Datapoints Summary

     Expects a date range and returns a summary of datapoint counts by group and feedback range.
    Defaults to 90-day lookback window.

    Returns:
        list: An array of datapoint objects.

    Args:
        api_key (str):
        body (SummaryDatapointSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[DatapointSummaryItem]
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SummaryDatapointSearch,
    api_key: str,
) -> Response[ErrorResponse | list[DatapointSummaryItem]]:
    """Get Datapoints Summary

     Expects a date range and returns a summary of datapoint counts by group and feedback range.
    Defaults to 90-day lookback window.

    Returns:
        list: An array of datapoint objects.

    Args:
        api_key (str):
        body (SummaryDatapointSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[DatapointSummaryItem]]
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
    body: SummaryDatapointSearch,
    api_key: str,
) -> ErrorResponse | list[DatapointSummaryItem] | None:
    """Get Datapoints Summary

     Expects a date range and returns a summary of datapoint counts by group and feedback range.
    Defaults to 90-day lookback window.

    Returns:
        list: An array of datapoint objects.

    Args:
        api_key (str):
        body (SummaryDatapointSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[DatapointSummaryItem]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key=api_key,
        )
    ).parsed
