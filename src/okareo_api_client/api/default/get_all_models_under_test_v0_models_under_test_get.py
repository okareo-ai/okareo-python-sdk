from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.model_under_test_response import ModelUnderTestResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    project_id: None | Unset | UUID = UNSET,
    version: str | Unset = "all",
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    params: dict[str, Any] = {}

    json_project_id: None | str | Unset
    if isinstance(project_id, Unset):
        json_project_id = UNSET
    elif isinstance(project_id, UUID):
        json_project_id = str(project_id)
    else:
        json_project_id = project_id
    params["project_id"] = json_project_id

    params["version"] = version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v0/models_under_test",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[ModelUnderTestResponse] | None:
    if response.status_code == 201:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = ModelUnderTestResponse.from_dict(response_201_item_data)

            response_201.append(response_201_item)

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
) -> Response[ErrorResponse | list[ModelUnderTestResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    project_id: None | Unset | UUID = UNSET,
    version: str | Unset = "all",
    api_key: str,
) -> Response[ErrorResponse | list[ModelUnderTestResponse]]:
    """Get All Models Under Test

     Get a list of models under test for this organization

    Returns:
        a list of requested models under test

    Args:
        project_id (None | Unset | UUID): The ID of the project
        version (str | Unset): The version(s) of the mut to retrieve. 'latest' will retrieve only
            the latest version for each mut name. 'all' will retrieve all versions for all mut names.
            Default: 'all'.
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[ModelUnderTestResponse]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        version=version,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    project_id: None | Unset | UUID = UNSET,
    version: str | Unset = "all",
    api_key: str,
) -> ErrorResponse | list[ModelUnderTestResponse] | None:
    """Get All Models Under Test

     Get a list of models under test for this organization

    Returns:
        a list of requested models under test

    Args:
        project_id (None | Unset | UUID): The ID of the project
        version (str | Unset): The version(s) of the mut to retrieve. 'latest' will retrieve only
            the latest version for each mut name. 'all' will retrieve all versions for all mut names.
            Default: 'all'.
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[ModelUnderTestResponse]
    """

    return sync_detailed(
        client=client,
        project_id=project_id,
        version=version,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    project_id: None | Unset | UUID = UNSET,
    version: str | Unset = "all",
    api_key: str,
) -> Response[ErrorResponse | list[ModelUnderTestResponse]]:
    """Get All Models Under Test

     Get a list of models under test for this organization

    Returns:
        a list of requested models under test

    Args:
        project_id (None | Unset | UUID): The ID of the project
        version (str | Unset): The version(s) of the mut to retrieve. 'latest' will retrieve only
            the latest version for each mut name. 'all' will retrieve all versions for all mut names.
            Default: 'all'.
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[ModelUnderTestResponse]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        version=version,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    project_id: None | Unset | UUID = UNSET,
    version: str | Unset = "all",
    api_key: str,
) -> ErrorResponse | list[ModelUnderTestResponse] | None:
    """Get All Models Under Test

     Get a list of models under test for this organization

    Returns:
        a list of requested models under test

    Args:
        project_id (None | Unset | UUID): The ID of the project
        version (str | Unset): The version(s) of the mut to retrieve. 'latest' will retrieve only
            the latest version for each mut name. 'all' will retrieve all versions for all mut names.
            Default: 'all'.
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[ModelUnderTestResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            project_id=project_id,
            version=version,
            api_key=api_key,
        )
    ).parsed
