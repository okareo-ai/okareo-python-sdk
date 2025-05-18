from http import HTTPStatus
from typing import Any, Optional, Union

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

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, list["DatapointSummaryItem"]]]:
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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponse, list["DatapointSummaryItem"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: SummaryDatapointSearch,
    api_key: str,
) -> Response[Union[ErrorResponse, list["DatapointSummaryItem"]]]:
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
        Response[Union[ErrorResponse, list['DatapointSummaryItem']]]
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
    client: Union[AuthenticatedClient, Client],
    body: SummaryDatapointSearch,
    api_key: str,
) -> Optional[Union[ErrorResponse, list["DatapointSummaryItem"]]]:
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
        Union[ErrorResponse, list['DatapointSummaryItem']]
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: SummaryDatapointSearch,
    api_key: str,
) -> Response[Union[ErrorResponse, list["DatapointSummaryItem"]]]:
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
        Response[Union[ErrorResponse, list['DatapointSummaryItem']]]
    """

    kwargs = _get_kwargs(
        body=body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: SummaryDatapointSearch,
    api_key: str,
) -> Optional[Union[ErrorResponse, list["DatapointSummaryItem"]]]:
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
        Union[ErrorResponse, list['DatapointSummaryItem']]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key=api_key,
        )
    ).parsed
