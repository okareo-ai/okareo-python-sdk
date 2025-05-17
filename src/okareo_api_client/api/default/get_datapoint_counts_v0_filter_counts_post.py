from http import HTTPStatus
from typing import Any, Dict, Optional, Union

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
    json_body: DatapointFilterSearch,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v0/filter_counts",
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost.from_dict(
            response.json()
        )

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
) -> Response[Union[ErrorResponse, GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DatapointFilterSearch,
    api_key: str,
) -> Response[Union[ErrorResponse, GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]]:
    """Get Datapoint Counts

     Gets only the counts for datapoints matching given filter criteria without retrieving the actual
    data.

    Returns:
        dict: Object containing filtered_count and total_count

    Args:
        api_key (str):
        json_body (DatapointFilterSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DatapointFilterSearch,
    api_key: str,
) -> Optional[Union[ErrorResponse, GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]]:
    """Get Datapoint Counts

     Gets only the counts for datapoints matching given filter criteria without retrieving the actual
    data.

    Returns:
        dict: Object containing filtered_count and total_count

    Args:
        api_key (str):
        json_body (DatapointFilterSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DatapointFilterSearch,
    api_key: str,
) -> Response[Union[ErrorResponse, GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]]:
    """Get Datapoint Counts

     Gets only the counts for datapoints matching given filter criteria without retrieving the actual
    data.

    Returns:
        dict: Object containing filtered_count and total_count

    Args:
        api_key (str):
        json_body (DatapointFilterSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DatapointFilterSearch,
    api_key: str,
) -> Optional[Union[ErrorResponse, GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]]:
    """Get Datapoint Counts

     Gets only the counts for datapoints matching given filter criteria without retrieving the actual
    data.

    Returns:
        dict: Object containing filtered_count and total_count

    Args:
        api_key (str):
        json_body (DatapointFilterSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, GetDatapointCountsV0FilterCountsPostResponseGetDatapointCountsV0FilterCountsPost]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
