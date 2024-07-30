from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

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
    json_body: FindTestDataPointPayload,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v0/find_test_data_points",
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, List[Union["FullDataPointItem", "TestDataPointItem"]]]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:

            def _parse_response_201_item(data: object) -> Union["FullDataPointItem", "TestDataPointItem"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    response_201_item_type_0 = FullDataPointItem.from_dict(data)

                    return response_201_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                response_201_item_type_1 = TestDataPointItem.from_dict(data)

                return response_201_item_type_1

            response_201_item = _parse_response_201_item(response_201_item_data)

            response_201.append(response_201_item)

        return response_201
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
) -> Response[Union[ErrorResponse, List[Union["FullDataPointItem", "TestDataPointItem"]]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: FindTestDataPointPayload,
    api_key: str,
) -> Response[Union[ErrorResponse, List[Union["FullDataPointItem", "TestDataPointItem"]]]]:
    """Find Test Data Points

     Find Test Data Point

    Returns:
        a list of Test Data Points

    Args:
        api_key (str):
        json_body (FindTestDataPointPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List[Union['FullDataPointItem', 'TestDataPointItem']]]]
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
    json_body: FindTestDataPointPayload,
    api_key: str,
) -> Optional[Union[ErrorResponse, List[Union["FullDataPointItem", "TestDataPointItem"]]]]:
    """Find Test Data Points

     Find Test Data Point

    Returns:
        a list of Test Data Points

    Args:
        api_key (str):
        json_body (FindTestDataPointPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List[Union['FullDataPointItem', 'TestDataPointItem']]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: FindTestDataPointPayload,
    api_key: str,
) -> Response[Union[ErrorResponse, List[Union["FullDataPointItem", "TestDataPointItem"]]]]:
    """Find Test Data Points

     Find Test Data Point

    Returns:
        a list of Test Data Points

    Args:
        api_key (str):
        json_body (FindTestDataPointPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List[Union['FullDataPointItem', 'TestDataPointItem']]]]
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
    json_body: FindTestDataPointPayload,
    api_key: str,
) -> Optional[Union[ErrorResponse, List[Union["FullDataPointItem", "TestDataPointItem"]]]]:
    """Find Test Data Points

     Find Test Data Point

    Returns:
        a list of Test Data Points

    Args:
        api_key (str):
        json_body (FindTestDataPointPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List[Union['FullDataPointItem', 'TestDataPointItem']]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
