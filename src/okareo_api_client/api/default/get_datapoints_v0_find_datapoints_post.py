from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.datapoint_list_item import DatapointListItem
from ...models.datapoint_search import DatapointSearch
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    json_body: DatapointSearch,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v0/find_datapoints",
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, List["DatapointListItem"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = DatapointListItem.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, List["DatapointListItem"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DatapointSearch,
    api_key: str,
) -> Response[Union[HTTPValidationError, List["DatapointListItem"]]]:
    """Get Datapoints

     gets all the datapoints created by a given token.

    Returns:
        list: An array of datapoint objects.

    Args:
        api_key (str):
        json_body (DatapointSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, List['DatapointListItem']]]
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
    json_body: DatapointSearch,
    api_key: str,
) -> Optional[Union[HTTPValidationError, List["DatapointListItem"]]]:
    """Get Datapoints

     gets all the datapoints created by a given token.

    Returns:
        list: An array of datapoint objects.

    Args:
        api_key (str):
        json_body (DatapointSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, List['DatapointListItem']]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DatapointSearch,
    api_key: str,
) -> Response[Union[HTTPValidationError, List["DatapointListItem"]]]:
    """Get Datapoints

     gets all the datapoints created by a given token.

    Returns:
        list: An array of datapoint objects.

    Args:
        api_key (str):
        json_body (DatapointSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, List['DatapointListItem']]]
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
    json_body: DatapointSearch,
    api_key: str,
) -> Optional[Union[HTTPValidationError, List["DatapointListItem"]]]:
    """Get Datapoints

     gets all the datapoints created by a given token.

    Returns:
        list: An array of datapoint objects.

    Args:
        api_key (str):
        json_body (DatapointSearch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, List['DatapointListItem']]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
