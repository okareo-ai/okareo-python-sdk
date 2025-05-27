from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.scenario_set_response import ScenarioSetResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    scenario_id: Union[Unset, UUID] = UNSET,
    project_id: Union[Unset, UUID] = UNSET,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    params: dict[str, Any] = {}

    json_scenario_id: Union[Unset, str] = UNSET
    if not isinstance(scenario_id, Unset):
        json_scenario_id = str(scenario_id)
    params["scenario_id"] = json_scenario_id

    json_project_id: Union[Unset, str] = UNSET
    if not isinstance(project_id, Unset):
        json_project_id = str(project_id)
    params["project_id"] = json_project_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v0/scenario_sets",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, list["ScenarioSetResponse"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ScenarioSetResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
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
) -> Response[Union[ErrorResponse, list["ScenarioSetResponse"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    scenario_id: Union[Unset, UUID] = UNSET,
    project_id: Union[Unset, UUID] = UNSET,
    api_key: str,
) -> Response[Union[ErrorResponse, list["ScenarioSetResponse"]]]:
    """Get Scenario Sets

     Find all scenario sets based on either the project id or the scenario id

    Returns:
        a list of scenario sets (project id) or a list of scenarios (scenario id)

    Args:
        scenario_id (Union[Unset, UUID]): The ID of the scenario set
        project_id (Union[Unset, UUID]): The ID of the project
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, list['ScenarioSetResponse']]]
    """

    kwargs = _get_kwargs(
        scenario_id=scenario_id,
        project_id=project_id,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    scenario_id: Union[Unset, UUID] = UNSET,
    project_id: Union[Unset, UUID] = UNSET,
    api_key: str,
) -> Optional[Union[ErrorResponse, list["ScenarioSetResponse"]]]:
    """Get Scenario Sets

     Find all scenario sets based on either the project id or the scenario id

    Returns:
        a list of scenario sets (project id) or a list of scenarios (scenario id)

    Args:
        scenario_id (Union[Unset, UUID]): The ID of the scenario set
        project_id (Union[Unset, UUID]): The ID of the project
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, list['ScenarioSetResponse']]
    """

    return sync_detailed(
        client=client,
        scenario_id=scenario_id,
        project_id=project_id,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    scenario_id: Union[Unset, UUID] = UNSET,
    project_id: Union[Unset, UUID] = UNSET,
    api_key: str,
) -> Response[Union[ErrorResponse, list["ScenarioSetResponse"]]]:
    """Get Scenario Sets

     Find all scenario sets based on either the project id or the scenario id

    Returns:
        a list of scenario sets (project id) or a list of scenarios (scenario id)

    Args:
        scenario_id (Union[Unset, UUID]): The ID of the scenario set
        project_id (Union[Unset, UUID]): The ID of the project
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, list['ScenarioSetResponse']]]
    """

    kwargs = _get_kwargs(
        scenario_id=scenario_id,
        project_id=project_id,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    scenario_id: Union[Unset, UUID] = UNSET,
    project_id: Union[Unset, UUID] = UNSET,
    api_key: str,
) -> Optional[Union[ErrorResponse, list["ScenarioSetResponse"]]]:
    """Get Scenario Sets

     Find all scenario sets based on either the project id or the scenario id

    Returns:
        a list of scenario sets (project id) or a list of scenarios (scenario id)

    Args:
        scenario_id (Union[Unset, UUID]): The ID of the scenario set
        project_id (Union[Unset, UUID]): The ID of the project
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, list['ScenarioSetResponse']]
    """

    return (
        await asyncio_detailed(
            client=client,
            scenario_id=scenario_id,
            project_id=project_id,
            api_key=api_key,
        )
    ).parsed
