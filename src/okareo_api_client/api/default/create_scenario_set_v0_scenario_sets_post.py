from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.scenario_set_create import ScenarioSetCreate
from ...models.scenario_set_response import ScenarioSetResponse
from ...types import Response


def _get_kwargs(
    *,
    json_body: ScenarioSetCreate,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v0/scenario_sets",
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, ScenarioSetResponse]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = ScenarioSetResponse.from_dict(response.json())

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
) -> Response[Union[ErrorResponse, ScenarioSetResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ScenarioSetCreate,
    api_key: str,
) -> Response[Union[ErrorResponse, ScenarioSetResponse]]:
    """Create Scenario Set

     Triggers a generation of a test scenario set, could be long running.
    This scenario set can now be used for testing on a model.

    Returns:
        Object: generation result with '201 Created' status code on success.

    Args:
        api_key (str):
        json_body (ScenarioSetCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, ScenarioSetResponse]]
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
    json_body: ScenarioSetCreate,
    api_key: str,
) -> Optional[Union[ErrorResponse, ScenarioSetResponse]]:
    """Create Scenario Set

     Triggers a generation of a test scenario set, could be long running.
    This scenario set can now be used for testing on a model.

    Returns:
        Object: generation result with '201 Created' status code on success.

    Args:
        api_key (str):
        json_body (ScenarioSetCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, ScenarioSetResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ScenarioSetCreate,
    api_key: str,
) -> Response[Union[ErrorResponse, ScenarioSetResponse]]:
    """Create Scenario Set

     Triggers a generation of a test scenario set, could be long running.
    This scenario set can now be used for testing on a model.

    Returns:
        Object: generation result with '201 Created' status code on success.

    Args:
        api_key (str):
        json_body (ScenarioSetCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, ScenarioSetResponse]]
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
    json_body: ScenarioSetCreate,
    api_key: str,
) -> Optional[Union[ErrorResponse, ScenarioSetResponse]]:
    """Create Scenario Set

     Triggers a generation of a test scenario set, could be long running.
    This scenario set can now be used for testing on a model.

    Returns:
        Object: generation result with '201 Created' status code on success.

    Args:
        api_key (str):
        json_body (ScenarioSetCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, ScenarioSetResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
