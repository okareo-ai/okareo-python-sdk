from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.test_run_item import TestRunItem
from ...models.test_run_payload import TestRunPayload
from ...types import Response


def _get_kwargs(
    test_run_id: str,
    *,
    json_body: TestRunPayload,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/v0/test_runs/{test_run_id}".format(
            test_run_id=test_run_id,
        ),
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, TestRunItem]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = TestRunItem.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
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
) -> Response[Union[ErrorResponse, TestRunItem]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    test_run_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: TestRunPayload,
    api_key: str,
) -> Response[Union[ErrorResponse, TestRunItem]]:
    """Update Test Run

     Update a Test Run

    Returns:
        the updated Test Run

    Args:
        test_run_id (str): The ID of the test run to modify
        api_key (str):
        json_body (TestRunPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TestRunItem]]
    """

    kwargs = _get_kwargs(
        test_run_id=test_run_id,
        json_body=json_body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    test_run_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: TestRunPayload,
    api_key: str,
) -> Optional[Union[ErrorResponse, TestRunItem]]:
    """Update Test Run

     Update a Test Run

    Returns:
        the updated Test Run

    Args:
        test_run_id (str): The ID of the test run to modify
        api_key (str):
        json_body (TestRunPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TestRunItem]
    """

    return sync_detailed(
        test_run_id=test_run_id,
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    test_run_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: TestRunPayload,
    api_key: str,
) -> Response[Union[ErrorResponse, TestRunItem]]:
    """Update Test Run

     Update a Test Run

    Returns:
        the updated Test Run

    Args:
        test_run_id (str): The ID of the test run to modify
        api_key (str):
        json_body (TestRunPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TestRunItem]]
    """

    kwargs = _get_kwargs(
        test_run_id=test_run_id,
        json_body=json_body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    test_run_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: TestRunPayload,
    api_key: str,
) -> Optional[Union[ErrorResponse, TestRunItem]]:
    """Update Test Run

     Update a Test Run

    Returns:
        the updated Test Run

    Args:
        test_run_id (str): The ID of the test run to modify
        api_key (str):
        json_body (TestRunPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TestRunItem]
    """

    return (
        await asyncio_detailed(
            test_run_id=test_run_id,
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
