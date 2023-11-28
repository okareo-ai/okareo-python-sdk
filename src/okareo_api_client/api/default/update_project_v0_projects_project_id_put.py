from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.project_response import ProjectResponse
from ...models.project_schema import ProjectSchema
from ...types import Response


def _get_kwargs(
    project_id: str,
    *,
    json_body: ProjectSchema,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/v0/projects/{project_id}".format(
            project_id=project_id,
        ),
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, ProjectResponse]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = ProjectResponse.from_dict(response.json())

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
) -> Response[Union[ErrorResponse, ProjectResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ProjectSchema,
    api_key: str,
) -> Response[Union[ErrorResponse, ProjectResponse]]:
    """Update Project

     Update a project

    Returns:
        the requested project

    Args:
        project_id (str): The ID of the project to get
        api_key (str):
        json_body (ProjectSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, ProjectResponse]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        json_body=json_body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ProjectSchema,
    api_key: str,
) -> Optional[Union[ErrorResponse, ProjectResponse]]:
    """Update Project

     Update a project

    Returns:
        the requested project

    Args:
        project_id (str): The ID of the project to get
        api_key (str):
        json_body (ProjectSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, ProjectResponse]
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ProjectSchema,
    api_key: str,
) -> Response[Union[ErrorResponse, ProjectResponse]]:
    """Update Project

     Update a project

    Returns:
        the requested project

    Args:
        project_id (str): The ID of the project to get
        api_key (str):
        json_body (ProjectSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, ProjectResponse]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        json_body=json_body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ProjectSchema,
    api_key: str,
) -> Optional[Union[ErrorResponse, ProjectResponse]]:
    """Update Project

     Update a project

    Returns:
        the requested project

    Args:
        project_id (str): The ID of the project to get
        api_key (str):
        json_body (ProjectSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, ProjectResponse]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
