from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.datapoint_filter_item import DatapointFilterItem
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    lookback_start: Union[Unset, int] = 90,
    lookback_end: Union[Unset, int] = 0,
    get_baseline_metrics: Union[Unset, bool] = False,
    timezone: Union[Unset, str] = "Etc/UTC",
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    params: dict[str, Any] = {}

    params["lookback_start"] = lookback_start

    params["lookback_end"] = lookback_end

    params["get_baseline_metrics"] = get_baseline_metrics

    params["timezone"] = timezone

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v0/filters",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, list["DatapointFilterItem"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = DatapointFilterItem.from_dict(response_200_item_data)

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
) -> Response[Union[ErrorResponse, list["DatapointFilterItem"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    lookback_start: Union[Unset, int] = 90,
    lookback_end: Union[Unset, int] = 0,
    get_baseline_metrics: Union[Unset, bool] = False,
    timezone: Union[Unset, str] = "Etc/UTC",
    api_key: str,
) -> Response[Union[ErrorResponse, list["DatapointFilterItem"]]]:
    """Get Filters

     Get all datapoint filters for a project.
    Defaults to a 90-day lookback window.

    Args:
        request: The FastAPI request object
        project_id: UUID of the project to get filters for

    Returns:
        List of filter items for the project

    Args:
        lookback_start (Union[Unset, int]):  Default: 90.
        lookback_end (Union[Unset, int]):  Default: 0.
        get_baseline_metrics (Union[Unset, bool]):  Default: False.
        timezone (Union[Unset, str]):  Default: 'Etc/UTC'.
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, list['DatapointFilterItem']]]
    """

    kwargs = _get_kwargs(
        lookback_start=lookback_start,
        lookback_end=lookback_end,
        get_baseline_metrics=get_baseline_metrics,
        timezone=timezone,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    lookback_start: Union[Unset, int] = 90,
    lookback_end: Union[Unset, int] = 0,
    get_baseline_metrics: Union[Unset, bool] = False,
    timezone: Union[Unset, str] = "Etc/UTC",
    api_key: str,
) -> Optional[Union[ErrorResponse, list["DatapointFilterItem"]]]:
    """Get Filters

     Get all datapoint filters for a project.
    Defaults to a 90-day lookback window.

    Args:
        request: The FastAPI request object
        project_id: UUID of the project to get filters for

    Returns:
        List of filter items for the project

    Args:
        lookback_start (Union[Unset, int]):  Default: 90.
        lookback_end (Union[Unset, int]):  Default: 0.
        get_baseline_metrics (Union[Unset, bool]):  Default: False.
        timezone (Union[Unset, str]):  Default: 'Etc/UTC'.
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, list['DatapointFilterItem']]
    """

    return sync_detailed(
        client=client,
        lookback_start=lookback_start,
        lookback_end=lookback_end,
        get_baseline_metrics=get_baseline_metrics,
        timezone=timezone,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    lookback_start: Union[Unset, int] = 90,
    lookback_end: Union[Unset, int] = 0,
    get_baseline_metrics: Union[Unset, bool] = False,
    timezone: Union[Unset, str] = "Etc/UTC",
    api_key: str,
) -> Response[Union[ErrorResponse, list["DatapointFilterItem"]]]:
    """Get Filters

     Get all datapoint filters for a project.
    Defaults to a 90-day lookback window.

    Args:
        request: The FastAPI request object
        project_id: UUID of the project to get filters for

    Returns:
        List of filter items for the project

    Args:
        lookback_start (Union[Unset, int]):  Default: 90.
        lookback_end (Union[Unset, int]):  Default: 0.
        get_baseline_metrics (Union[Unset, bool]):  Default: False.
        timezone (Union[Unset, str]):  Default: 'Etc/UTC'.
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, list['DatapointFilterItem']]]
    """

    kwargs = _get_kwargs(
        lookback_start=lookback_start,
        lookback_end=lookback_end,
        get_baseline_metrics=get_baseline_metrics,
        timezone=timezone,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    lookback_start: Union[Unset, int] = 90,
    lookback_end: Union[Unset, int] = 0,
    get_baseline_metrics: Union[Unset, bool] = False,
    timezone: Union[Unset, str] = "Etc/UTC",
    api_key: str,
) -> Optional[Union[ErrorResponse, list["DatapointFilterItem"]]]:
    """Get Filters

     Get all datapoint filters for a project.
    Defaults to a 90-day lookback window.

    Args:
        request: The FastAPI request object
        project_id: UUID of the project to get filters for

    Returns:
        List of filter items for the project

    Args:
        lookback_start (Union[Unset, int]):  Default: 90.
        lookback_end (Union[Unset, int]):  Default: 0.
        get_baseline_metrics (Union[Unset, bool]):  Default: False.
        timezone (Union[Unset, str]):  Default: 'Etc/UTC'.
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, list['DatapointFilterItem']]
    """

    return (
        await asyncio_detailed(
            client=client,
            lookback_start=lookback_start,
            lookback_end=lookback_end,
            get_baseline_metrics=get_baseline_metrics,
            timezone=timezone,
            api_key=api_key,
        )
    ).parsed
