from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.model_under_test_response import ModelUnderTestResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    project_id: Union[Unset, None, str] = UNSET,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    params: Dict[str, Any] = {}
    params["project_id"] = project_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/v0/models_under_test",
        "params": params,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, List["ModelUnderTestResponse"]]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = ModelUnderTestResponse.from_dict(response_201_item_data)

            response_201.append(response_201_item)

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
) -> Response[Union[ErrorResponse, List["ModelUnderTestResponse"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    project_id: Union[Unset, None, str] = UNSET,
    api_key: str,
) -> Response[Union[ErrorResponse, List["ModelUnderTestResponse"]]]:
    """Get All Models Under Test

     Get a list of models under test for this organization

    Returns:
        a list of requested models under test

    Args:
        project_id (Union[Unset, None, str]): The ID of the project
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['ModelUnderTestResponse']]]
    """

    kwargs = _get_kwargs(
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
    project_id: Union[Unset, None, str] = UNSET,
    api_key: str,
) -> Optional[Union[ErrorResponse, List["ModelUnderTestResponse"]]]:
    """Get All Models Under Test

     Get a list of models under test for this organization

    Returns:
        a list of requested models under test

    Args:
        project_id (Union[Unset, None, str]): The ID of the project
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['ModelUnderTestResponse']]
    """

    return sync_detailed(
        client=client,
        project_id=project_id,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    project_id: Union[Unset, None, str] = UNSET,
    api_key: str,
) -> Response[Union[ErrorResponse, List["ModelUnderTestResponse"]]]:
    """Get All Models Under Test

     Get a list of models under test for this organization

    Returns:
        a list of requested models under test

    Args:
        project_id (Union[Unset, None, str]): The ID of the project
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['ModelUnderTestResponse']]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    project_id: Union[Unset, None, str] = UNSET,
    api_key: str,
) -> Optional[Union[ErrorResponse, List["ModelUnderTestResponse"]]]:
    """Get All Models Under Test

     Get a list of models under test for this organization

    Returns:
        a list of requested models under test

    Args:
        project_id (Union[Unset, None, str]): The ID of the project
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['ModelUnderTestResponse']]
    """

    return (
        await asyncio_detailed(
            client=client,
            project_id=project_id,
            api_key=api_key,
        )
    ).parsed
