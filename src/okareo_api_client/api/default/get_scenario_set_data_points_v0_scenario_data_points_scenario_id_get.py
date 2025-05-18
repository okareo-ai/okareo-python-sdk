from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.scenario_data_poin_response import ScenarioDataPoinResponse
from ...types import Response


def _get_kwargs(
    scenario_id: UUID,
    *,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v0/scenario_data_points/{scenario_id}",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, list["ScenarioDataPoinResponse"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ScenarioDataPoinResponse.from_dict(response_200_item_data)

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
) -> Response[Union[ErrorResponse, list["ScenarioDataPoinResponse"]]]:
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
    api_key: str,
) -> Response[Union[ErrorResponse, list["ScenarioDataPoinResponse"]]]:
    """Get Scenario Set Data Points

     Get all scenarios datapoints

    Returns:
        a list of scenario datapoints

    Args:
        scenario_id (UUID): The ID of the scenario set to download
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, list['ScenarioDataPoinResponse']]]
    """

    kwargs = _get_kwargs(
        scenario_id=scenario_id,
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
    api_key: str,
) -> Optional[Union[ErrorResponse, list["ScenarioDataPoinResponse"]]]:
    """Get Scenario Set Data Points

     Get all scenarios datapoints

    Returns:
        a list of scenario datapoints

    Args:
        scenario_id (UUID): The ID of the scenario set to download
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, list['ScenarioDataPoinResponse']]
    """

    return sync_detailed(
        scenario_id=scenario_id,
        client=client,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    scenario_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Response[Union[ErrorResponse, list["ScenarioDataPoinResponse"]]]:
    """Get Scenario Set Data Points

     Get all scenarios datapoints

    Returns:
        a list of scenario datapoints

    Args:
        scenario_id (UUID): The ID of the scenario set to download
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, list['ScenarioDataPoinResponse']]]
    """

    kwargs = _get_kwargs(
        scenario_id=scenario_id,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    scenario_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Optional[Union[ErrorResponse, list["ScenarioDataPoinResponse"]]]:
    """Get Scenario Set Data Points

     Get all scenarios datapoints

    Returns:
        a list of scenario datapoints

    Args:
        scenario_id (UUID): The ID of the scenario set to download
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, list['ScenarioDataPoinResponse']]
    """

    return (
        await asyncio_detailed(
            scenario_id=scenario_id,
            client=client,
            api_key=api_key,
        )
    ).parsed
