from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.scenario_set_response import ScenarioSetResponse
from ...models.scenario_set_update import ScenarioSetUpdate
from ...types import Response


def _get_kwargs(
    scenario_id: str,
    *,
    json_body: ScenarioSetUpdate,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/v0/scenario_sets/{scenario_id}".format(
            scenario_id=scenario_id,
        ),
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ScenarioSetResponse]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = ScenarioSetResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ScenarioSetResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    scenario_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ScenarioSetUpdate,
    api_key: str,
) -> Response[Union[HTTPValidationError, ScenarioSetResponse]]:
    """Update Scenario Set

     Update a Scenario Set

    Returns:
        the updated Scenario Set

    Args:
        scenario_id (str):
        api_key (str):
        json_body (ScenarioSetUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ScenarioSetResponse]]
    """

    kwargs = _get_kwargs(
        scenario_id=scenario_id,
        json_body=json_body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    scenario_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ScenarioSetUpdate,
    api_key: str,
) -> Optional[Union[HTTPValidationError, ScenarioSetResponse]]:
    """Update Scenario Set

     Update a Scenario Set

    Returns:
        the updated Scenario Set

    Args:
        scenario_id (str):
        api_key (str):
        json_body (ScenarioSetUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ScenarioSetResponse]
    """

    return sync_detailed(
        scenario_id=scenario_id,
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    scenario_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ScenarioSetUpdate,
    api_key: str,
) -> Response[Union[HTTPValidationError, ScenarioSetResponse]]:
    """Update Scenario Set

     Update a Scenario Set

    Returns:
        the updated Scenario Set

    Args:
        scenario_id (str):
        api_key (str):
        json_body (ScenarioSetUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ScenarioSetResponse]]
    """

    kwargs = _get_kwargs(
        scenario_id=scenario_id,
        json_body=json_body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    scenario_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ScenarioSetUpdate,
    api_key: str,
) -> Optional[Union[HTTPValidationError, ScenarioSetResponse]]:
    """Update Scenario Set

     Update a Scenario Set

    Returns:
        the updated Scenario Set

    Args:
        scenario_id (str):
        api_key (str):
        json_body (ScenarioSetUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ScenarioSetResponse]
    """

    return (
        await asyncio_detailed(
            scenario_id=scenario_id,
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
