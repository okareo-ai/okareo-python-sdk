from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.scenario_set_generate import ScenarioSetGenerate
from ...models.scenario_set_response import ScenarioSetResponse
from ...types import Response


def _get_kwargs(
    *,
    json_body: ScenarioSetGenerate,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v0/scenario_sets_generate",
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
    json_body: ScenarioSetGenerate,
    api_key: str,
) -> Response[Union[ErrorResponse, ScenarioSetResponse]]:
    """Generate Scenario Set

     Triggers a generation of a scenario set based on either a source scenario ID or a list of source
    scenario rows.
    Generation can run long depending on number of source rows, number of examples, and generation
    type/prompt.
    Optionally save the generated scenario, allowing a registered model to use the generated scenario
    set for testing.

    Returns:
        Object: generation result with '201 Created' status code on success.

    Args:
        api_key (str):
        json_body (ScenarioSetGenerate):

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
    json_body: ScenarioSetGenerate,
    api_key: str,
) -> Optional[Union[ErrorResponse, ScenarioSetResponse]]:
    """Generate Scenario Set

     Triggers a generation of a scenario set based on either a source scenario ID or a list of source
    scenario rows.
    Generation can run long depending on number of source rows, number of examples, and generation
    type/prompt.
    Optionally save the generated scenario, allowing a registered model to use the generated scenario
    set for testing.

    Returns:
        Object: generation result with '201 Created' status code on success.

    Args:
        api_key (str):
        json_body (ScenarioSetGenerate):

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
    json_body: ScenarioSetGenerate,
    api_key: str,
) -> Response[Union[ErrorResponse, ScenarioSetResponse]]:
    """Generate Scenario Set

     Triggers a generation of a scenario set based on either a source scenario ID or a list of source
    scenario rows.
    Generation can run long depending on number of source rows, number of examples, and generation
    type/prompt.
    Optionally save the generated scenario, allowing a registered model to use the generated scenario
    set for testing.

    Returns:
        Object: generation result with '201 Created' status code on success.

    Args:
        api_key (str):
        json_body (ScenarioSetGenerate):

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
    json_body: ScenarioSetGenerate,
    api_key: str,
) -> Optional[Union[ErrorResponse, ScenarioSetResponse]]:
    """Generate Scenario Set

     Triggers a generation of a scenario set based on either a source scenario ID or a list of source
    scenario rows.
    Generation can run long depending on number of source rows, number of examples, and generation
    type/prompt.
    Optionally save the generated scenario, allowing a registered model to use the generated scenario
    set for testing.

    Returns:
        Object: generation result with '201 Created' status code on success.

    Args:
        api_key (str):
        json_body (ScenarioSetGenerate):

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
