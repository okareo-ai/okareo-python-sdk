from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.datapoint_filter_item import DatapointFilterItem
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    lookback_start: Union[Unset, None, int] = 90,
    lookback_end: Union[Unset, None, int] = 0,
    get_baseline_metrics: Union[Unset, None, bool] = False,
    timezone: Union[Unset, None, str] = "Etc/UTC",
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    params: Dict[str, Any] = {}
    params["lookback_start"] = lookback_start

    params["lookback_end"] = lookback_end

    params["get_baseline_metrics"] = get_baseline_metrics

    params["timezone"] = timezone

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/v0/filters",
        "params": params,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, List["DatapointFilterItem"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = DatapointFilterItem.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
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
) -> Response[Union[ErrorResponse, List["DatapointFilterItem"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    lookback_start: Union[Unset, None, int] = 90,
    lookback_end: Union[Unset, None, int] = 0,
    get_baseline_metrics: Union[Unset, None, bool] = False,
    timezone: Union[Unset, None, str] = "Etc/UTC",
    api_key: str,
) -> Response[Union[ErrorResponse, List["DatapointFilterItem"]]]:
    """Get Filters

     Get all datapoint filters for a project.
    Defaults to a 90-day lookback window.

    Args:
        request: The FastAPI request object
        project_id: UUID of the project to get filters for

    Returns:
        List of filter items for the project

    Args:
        lookback_start (Union[Unset, None, int]):  Default: 90.
        lookback_end (Union[Unset, None, int]):
        get_baseline_metrics (Union[Unset, None, bool]):
        timezone (Union[Unset, None, str]):  Default: 'Etc/UTC'.
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['DatapointFilterItem']]]
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
    lookback_start: Union[Unset, None, int] = 90,
    lookback_end: Union[Unset, None, int] = 0,
    get_baseline_metrics: Union[Unset, None, bool] = False,
    timezone: Union[Unset, None, str] = "Etc/UTC",
    api_key: str,
) -> Optional[Union[ErrorResponse, List["DatapointFilterItem"]]]:
    """Get Filters

     Get all datapoint filters for a project.
    Defaults to a 90-day lookback window.

    Args:
        request: The FastAPI request object
        project_id: UUID of the project to get filters for

    Returns:
        List of filter items for the project

    Args:
        lookback_start (Union[Unset, None, int]):  Default: 90.
        lookback_end (Union[Unset, None, int]):
        get_baseline_metrics (Union[Unset, None, bool]):
        timezone (Union[Unset, None, str]):  Default: 'Etc/UTC'.
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['DatapointFilterItem']]
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
    lookback_start: Union[Unset, None, int] = 90,
    lookback_end: Union[Unset, None, int] = 0,
    get_baseline_metrics: Union[Unset, None, bool] = False,
    timezone: Union[Unset, None, str] = "Etc/UTC",
    api_key: str,
) -> Response[Union[ErrorResponse, List["DatapointFilterItem"]]]:
    """Get Filters

     Get all datapoint filters for a project.
    Defaults to a 90-day lookback window.

    Args:
        request: The FastAPI request object
        project_id: UUID of the project to get filters for

    Returns:
        List of filter items for the project

    Args:
        lookback_start (Union[Unset, None, int]):  Default: 90.
        lookback_end (Union[Unset, None, int]):
        get_baseline_metrics (Union[Unset, None, bool]):
        timezone (Union[Unset, None, str]):  Default: 'Etc/UTC'.
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['DatapointFilterItem']]]
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
    lookback_start: Union[Unset, None, int] = 90,
    lookback_end: Union[Unset, None, int] = 0,
    get_baseline_metrics: Union[Unset, None, bool] = False,
    timezone: Union[Unset, None, str] = "Etc/UTC",
    api_key: str,
) -> Optional[Union[ErrorResponse, List["DatapointFilterItem"]]]:
    """Get Filters

     Get all datapoint filters for a project.
    Defaults to a 90-day lookback window.

    Args:
        request: The FastAPI request object
        project_id: UUID of the project to get filters for

    Returns:
        List of filter items for the project

    Args:
        lookback_start (Union[Unset, None, int]):  Default: 90.
        lookback_end (Union[Unset, None, int]):
        get_baseline_metrics (Union[Unset, None, bool]):
        timezone (Union[Unset, None, str]):  Default: 'Etc/UTC'.
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['DatapointFilterItem']]
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
