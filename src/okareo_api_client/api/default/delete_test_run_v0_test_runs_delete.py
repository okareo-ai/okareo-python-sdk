from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response


def _get_kwargs(
    *,
    test_run_ids: List[str],
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    params: Dict[str, Any] = {}
    json_test_run_ids = test_run_ids

    params["test_run_ids"] = json_test_run_ids

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
        "url": "/v0/test_runs",
        "params": params,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ErrorResponse]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
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
) -> Response[Union[Any, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    test_run_ids: List[str],
    api_key: str,
) -> Response[Union[Any, ErrorResponse]]:
    """Delete Test Run

     Deletes one or more test runs and cascades deletes to all related entities, including datapoints.

    !! Use With Caution !!

    Args:
        test_run_ids: List of UUIDs to delete

    Raises:
        HTTPException: 404 if any test_run_id is not found
        HTTPException: 422 if test_run_ids list is empty or invalid

    Returns: 204 status code on successful deletion

    Args:
        test_run_ids (List[str]): List of Test Run IDs to delete
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        test_run_ids=test_run_ids,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    test_run_ids: List[str],
    api_key: str,
) -> Optional[Union[Any, ErrorResponse]]:
    """Delete Test Run

     Deletes one or more test runs and cascades deletes to all related entities, including datapoints.

    !! Use With Caution !!

    Args:
        test_run_ids: List of UUIDs to delete

    Raises:
        HTTPException: 404 if any test_run_id is not found
        HTTPException: 422 if test_run_ids list is empty or invalid

    Returns: 204 status code on successful deletion

    Args:
        test_run_ids (List[str]): List of Test Run IDs to delete
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return sync_detailed(
        client=client,
        test_run_ids=test_run_ids,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    test_run_ids: List[str],
    api_key: str,
) -> Response[Union[Any, ErrorResponse]]:
    """Delete Test Run

     Deletes one or more test runs and cascades deletes to all related entities, including datapoints.

    !! Use With Caution !!

    Args:
        test_run_ids: List of UUIDs to delete

    Raises:
        HTTPException: 404 if any test_run_id is not found
        HTTPException: 422 if test_run_ids list is empty or invalid

    Returns: 204 status code on successful deletion

    Args:
        test_run_ids (List[str]): List of Test Run IDs to delete
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        test_run_ids=test_run_ids,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    test_run_ids: List[str],
    api_key: str,
) -> Optional[Union[Any, ErrorResponse]]:
    """Delete Test Run

     Deletes one or more test runs and cascades deletes to all related entities, including datapoints.

    !! Use With Caution !!

    Args:
        test_run_ids: List of UUIDs to delete

    Raises:
        HTTPException: 404 if any test_run_id is not found
        HTTPException: 422 if test_run_ids list is empty or invalid

    Returns: 204 status code on successful deletion

    Args:
        test_run_ids (List[str]): List of Test Run IDs to delete
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            test_run_ids=test_run_ids,
            api_key=api_key,
        )
    ).parsed
