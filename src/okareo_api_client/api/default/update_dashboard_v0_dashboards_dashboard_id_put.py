from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dashboard_update import DashboardUpdate
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    dashboard_id: UUID,
    *,
    body: DashboardUpdate,
    project_id: UUID,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    params: dict[str, Any] = {}

    json_project_id = str(project_id)
    params["project_id"] = json_project_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v0/dashboards/{dashboard_id}".format(
            dashboard_id=quote(str(dashboard_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> HTTPValidationError | None:
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dashboard_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: DashboardUpdate,
    project_id: UUID,
    api_key: str,
) -> Response[HTTPValidationError]:
    """Update Dashboard

    Args:
        dashboard_id (UUID):
        project_id (UUID):
        api_key (str):
        body (DashboardUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dashboard_id=dashboard_id,
        body=body,
        project_id=project_id,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dashboard_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: DashboardUpdate,
    project_id: UUID,
    api_key: str,
) -> HTTPValidationError | None:
    """Update Dashboard

    Args:
        dashboard_id (UUID):
        project_id (UUID):
        api_key (str):
        body (DashboardUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
    """

    return sync_detailed(
        dashboard_id=dashboard_id,
        client=client,
        body=body,
        project_id=project_id,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    dashboard_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: DashboardUpdate,
    project_id: UUID,
    api_key: str,
) -> Response[HTTPValidationError]:
    """Update Dashboard

    Args:
        dashboard_id (UUID):
        project_id (UUID):
        api_key (str):
        body (DashboardUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dashboard_id=dashboard_id,
        body=body,
        project_id=project_id,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dashboard_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: DashboardUpdate,
    project_id: UUID,
    api_key: str,
) -> HTTPValidationError | None:
    """Update Dashboard

    Args:
        dashboard_id (UUID):
        project_id (UUID):
        api_key (str):
        body (DashboardUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
    """

    return (
        await asyncio_detailed(
            dashboard_id=dashboard_id,
            client=client,
            body=body,
            project_id=project_id,
            api_key=api_key,
        )
    ).parsed
