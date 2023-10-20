from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.general_find_payload import GeneralFindPayload
from ...models.http_validation_error import HTTPValidationError
from ...models.test_run_item import TestRunItem
from ...types import Response


def _get_kwargs(
    *,
    json_body: GeneralFindPayload,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v0/find_test_runs",
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, List["TestRunItem"]]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = TestRunItem.from_dict(response_201_item_data)

            response_201.append(response_201_item)

        return response_201
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, List["TestRunItem"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: GeneralFindPayload,
    api_key: str,
) -> Response[Union[HTTPValidationError, List["TestRunItem"]]]:
    """Find Test Run

     Find Test Runs

    Returns:
        a list of Test Runs

    Args:
        api_key (str):
        json_body (GeneralFindPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, List['TestRunItem']]]
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
    json_body: GeneralFindPayload,
    api_key: str,
) -> Optional[Union[HTTPValidationError, List["TestRunItem"]]]:
    """Find Test Run

     Find Test Runs

    Returns:
        a list of Test Runs

    Args:
        api_key (str):
        json_body (GeneralFindPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, List['TestRunItem']]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: GeneralFindPayload,
    api_key: str,
) -> Response[Union[HTTPValidationError, List["TestRunItem"]]]:
    """Find Test Run

     Find Test Runs

    Returns:
        a list of Test Runs

    Args:
        api_key (str):
        json_body (GeneralFindPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, List['TestRunItem']]]
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
    json_body: GeneralFindPayload,
    api_key: str,
) -> Optional[Union[HTTPValidationError, List["TestRunItem"]]]:
    """Find Test Run

     Find Test Runs

    Returns:
        a list of Test Runs

    Args:
        api_key (str):
        json_body (GeneralFindPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, List['TestRunItem']]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
