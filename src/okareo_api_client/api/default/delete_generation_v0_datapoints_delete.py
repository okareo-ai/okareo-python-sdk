from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    mut_id: Union[Unset, None, str] = UNSET,
    test_run_id: Union[Unset, None, str] = UNSET,
    scenario_set_id: Union[Unset, None, str] = UNSET,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    params: Dict[str, Any] = {}
    params["mut_id"] = mut_id

    params["test_run_id"] = test_run_id

    params["scenario_set_id"] = scenario_set_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
        "url": "/v0/datapoints",
        "params": params,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ErrorResponse]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = cast(Any, response.json())
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
    mut_id: Union[Unset, None, str] = UNSET,
    test_run_id: Union[Unset, None, str] = UNSET,
    scenario_set_id: Union[Unset, None, str] = UNSET,
    api_key: str,
) -> Response[Union[Any, ErrorResponse]]:
    """Delete Generation

     Deletes the datapoint object from db

    Args:
        mut_id (Union[Unset, None, str]): The ID of the model
        test_run_id (Union[Unset, None, str]): The ID of the test run
        scenario_set_id (Union[Unset, None, str]): The ID of the scenario set
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        mut_id=mut_id,
        test_run_id=test_run_id,
        scenario_set_id=scenario_set_id,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    mut_id: Union[Unset, None, str] = UNSET,
    test_run_id: Union[Unset, None, str] = UNSET,
    scenario_set_id: Union[Unset, None, str] = UNSET,
    api_key: str,
) -> Optional[Union[Any, ErrorResponse]]:
    """Delete Generation

     Deletes the datapoint object from db

    Args:
        mut_id (Union[Unset, None, str]): The ID of the model
        test_run_id (Union[Unset, None, str]): The ID of the test run
        scenario_set_id (Union[Unset, None, str]): The ID of the scenario set
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return sync_detailed(
        client=client,
        mut_id=mut_id,
        test_run_id=test_run_id,
        scenario_set_id=scenario_set_id,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    mut_id: Union[Unset, None, str] = UNSET,
    test_run_id: Union[Unset, None, str] = UNSET,
    scenario_set_id: Union[Unset, None, str] = UNSET,
    api_key: str,
) -> Response[Union[Any, ErrorResponse]]:
    """Delete Generation

     Deletes the datapoint object from db

    Args:
        mut_id (Union[Unset, None, str]): The ID of the model
        test_run_id (Union[Unset, None, str]): The ID of the test run
        scenario_set_id (Union[Unset, None, str]): The ID of the scenario set
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        mut_id=mut_id,
        test_run_id=test_run_id,
        scenario_set_id=scenario_set_id,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    mut_id: Union[Unset, None, str] = UNSET,
    test_run_id: Union[Unset, None, str] = UNSET,
    scenario_set_id: Union[Unset, None, str] = UNSET,
    api_key: str,
) -> Optional[Union[Any, ErrorResponse]]:
    """Delete Generation

     Deletes the datapoint object from db

    Args:
        mut_id (Union[Unset, None, str]): The ID of the model
        test_run_id (Union[Unset, None, str]): The ID of the test run
        scenario_set_id (Union[Unset, None, str]): The ID of the scenario set
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
            mut_id=mut_id,
            test_run_id=test_run_id,
            scenario_set_id=scenario_set_id,
            api_key=api_key,
        )
    ).parsed
