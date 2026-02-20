from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.find_test_data_point_payload import FindTestDataPointPayload
from ...models.full_data_point_item import FullDataPointItem
from ...models.test_data_point_item import TestDataPointItem
from ...types import Response


def _get_kwargs(
    *,
    body: FindTestDataPointPayload,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v0/find_test_data_points",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[FullDataPointItem | TestDataPointItem] | None:
    if response.status_code == 201:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:

            def _parse_response_201_item(data: object) -> FullDataPointItem | TestDataPointItem:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    response_201_item_type_0 = FullDataPointItem.from_dict(data)

                    return response_201_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                response_201_item_type_1 = TestDataPointItem.from_dict(data)

                return response_201_item_type_1

            response_201_item = _parse_response_201_item(response_201_item_data)

            response_201.append(response_201_item)

        return response_201

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
) -> Response[ErrorResponse | list[FullDataPointItem | TestDataPointItem]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: FindTestDataPointPayload,
    api_key: str,
) -> Response[ErrorResponse | list[FullDataPointItem | TestDataPointItem]]:
    """Find Test Data Points

     Find Test Data Point

    Returns:
        a list of Test Data Points

    Args:
        api_key (str):
        body (FindTestDataPointPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[FullDataPointItem | TestDataPointItem]]
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
    body: FindTestDataPointPayload,
    api_key: str,
) -> ErrorResponse | list[FullDataPointItem | TestDataPointItem] | None:
    """Find Test Data Points

     Find Test Data Point

    Returns:
        a list of Test Data Points

    Args:
        api_key (str):
        body (FindTestDataPointPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[FullDataPointItem | TestDataPointItem]
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: FindTestDataPointPayload,
    api_key: str,
) -> Response[ErrorResponse | list[FullDataPointItem | TestDataPointItem]]:
    """Find Test Data Points

     Find Test Data Point

    Returns:
        a list of Test Data Points

    Args:
        api_key (str):
        body (FindTestDataPointPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[FullDataPointItem | TestDataPointItem]]
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
    body: FindTestDataPointPayload,
    api_key: str,
) -> ErrorResponse | list[FullDataPointItem | TestDataPointItem] | None:
    """Find Test Data Points

     Find Test Data Point

    Returns:
        a list of Test Data Points

    Args:
        api_key (str):
        body (FindTestDataPointPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[FullDataPointItem | TestDataPointItem]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key=api_key,
        )
    ).parsed
