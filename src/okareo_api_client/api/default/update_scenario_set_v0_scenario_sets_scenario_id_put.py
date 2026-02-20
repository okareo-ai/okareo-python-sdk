from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.scenario_set_response import ScenarioSetResponse
from ...models.scenario_set_update import ScenarioSetUpdate
from ...types import Response


def _get_kwargs(
    scenario_id: UUID,
    *,
    body: ScenarioSetUpdate,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v0/scenario_sets/{scenario_id}".format(
            scenario_id=quote(str(scenario_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | ScenarioSetResponse | None:
    if response.status_code == 201:
        response_201 = ScenarioSetResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | ScenarioSetResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    scenario_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ScenarioSetUpdate,
    api_key: str,
) -> Response[ErrorResponse | ScenarioSetResponse]:
    """Update Scenario Set

     Update a Scenario Set

    Returns:
        the updated Scenario Set

    Args:
        scenario_id (UUID): The ID of the scenario set to modify
        api_key (str):
        body (ScenarioSetUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ScenarioSetResponse]
    """

    kwargs = _get_kwargs(
        scenario_id=scenario_id,
        body=body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    scenario_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ScenarioSetUpdate,
    api_key: str,
) -> ErrorResponse | ScenarioSetResponse | None:
    """Update Scenario Set

     Update a Scenario Set

    Returns:
        the updated Scenario Set

    Args:
        scenario_id (UUID): The ID of the scenario set to modify
        api_key (str):
        body (ScenarioSetUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ScenarioSetResponse
    """

    return sync_detailed(
        scenario_id=scenario_id,
        client=client,
        body=body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    scenario_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ScenarioSetUpdate,
    api_key: str,
) -> Response[ErrorResponse | ScenarioSetResponse]:
    """Update Scenario Set

     Update a Scenario Set

    Returns:
        the updated Scenario Set

    Args:
        scenario_id (UUID): The ID of the scenario set to modify
        api_key (str):
        body (ScenarioSetUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ScenarioSetResponse]
    """

    kwargs = _get_kwargs(
        scenario_id=scenario_id,
        body=body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    scenario_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ScenarioSetUpdate,
    api_key: str,
) -> ErrorResponse | ScenarioSetResponse | None:
    """Update Scenario Set

     Update a Scenario Set

    Returns:
        the updated Scenario Set

    Args:
        scenario_id (UUID): The ID of the scenario set to modify
        api_key (str):
        body (ScenarioSetUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ScenarioSetResponse
    """

    return (
        await asyncio_detailed(
            scenario_id=scenario_id,
            client=client,
            body=body,
            api_key=api_key,
        )
    ).parsed
