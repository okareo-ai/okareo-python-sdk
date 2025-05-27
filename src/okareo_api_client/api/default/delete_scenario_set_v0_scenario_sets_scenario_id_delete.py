from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response


def _get_kwargs(
    scenario_id: UUID,
    *,
    name: str,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    params: dict[str, Any] = {}

    params["name"] = name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/v0/scenario_sets/{scenario_id}",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ErrorResponse]]:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
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
) -> Response[Union[Any, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    scenario_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    name: str,
    api_key: str,
) -> Response[Union[Any, ErrorResponse]]:
    """Delete Scenario Set

     Deletes the scenario set and cascades deletes to all related entities.
    Namely, Evaluations, Evaluation Datapoints, and  Model Datapoints

    !! Use With Caution !!

    Raises:
        HTTPException: 404 if scenario_id is not found

    Returns: 204 status code on successful deletion

    Args:
        scenario_id (UUID): The ID of the Scenario Set to delete
        name (str): Name of the Scenario Set to delete
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        scenario_id=scenario_id,
        name=name,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    scenario_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    name: str,
    api_key: str,
) -> Optional[Union[Any, ErrorResponse]]:
    """Delete Scenario Set

     Deletes the scenario set and cascades deletes to all related entities.
    Namely, Evaluations, Evaluation Datapoints, and  Model Datapoints

    !! Use With Caution !!

    Raises:
        HTTPException: 404 if scenario_id is not found

    Returns: 204 status code on successful deletion

    Args:
        scenario_id (UUID): The ID of the Scenario Set to delete
        name (str): Name of the Scenario Set to delete
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return sync_detailed(
        scenario_id=scenario_id,
        client=client,
        name=name,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    scenario_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    name: str,
    api_key: str,
) -> Response[Union[Any, ErrorResponse]]:
    """Delete Scenario Set

     Deletes the scenario set and cascades deletes to all related entities.
    Namely, Evaluations, Evaluation Datapoints, and  Model Datapoints

    !! Use With Caution !!

    Raises:
        HTTPException: 404 if scenario_id is not found

    Returns: 204 status code on successful deletion

    Args:
        scenario_id (UUID): The ID of the Scenario Set to delete
        name (str): Name of the Scenario Set to delete
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        scenario_id=scenario_id,
        name=name,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    scenario_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    name: str,
    api_key: str,
) -> Optional[Union[Any, ErrorResponse]]:
    """Delete Scenario Set

     Deletes the scenario set and cascades deletes to all related entities.
    Namely, Evaluations, Evaluation Datapoints, and  Model Datapoints

    !! Use With Caution !!

    Raises:
        HTTPException: 404 if scenario_id is not found

    Returns: 204 status code on successful deletion

    Args:
        scenario_id (UUID): The ID of the Scenario Set to delete
        name (str): Name of the Scenario Set to delete
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            scenario_id=scenario_id,
            client=client,
            name=name,
            api_key=api_key,
        )
    ).parsed
