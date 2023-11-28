from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.model_under_test_response import ModelUnderTestResponse
from ...models.model_under_test_schema import ModelUnderTestSchema
from ...types import Response


def _get_kwargs(
    mut_id: str,
    *,
    json_body: ModelUnderTestSchema,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/v0/models_under_test/{mut_id}".format(
            mut_id=mut_id,
        ),
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, ModelUnderTestResponse]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = ModelUnderTestResponse.from_dict(response.json())

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
) -> Response[Union[ErrorResponse, ModelUnderTestResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    mut_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ModelUnderTestSchema,
    api_key: str,
) -> Response[Union[ErrorResponse, ModelUnderTestResponse]]:
    """Update Model Under Test

     Update a model under test

    Returns:
        the updated model under test

    Args:
        mut_id (str): The ID of the model under test to get
        api_key (str):
        json_body (ModelUnderTestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, ModelUnderTestResponse]]
    """

    kwargs = _get_kwargs(
        mut_id=mut_id,
        json_body=json_body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    mut_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ModelUnderTestSchema,
    api_key: str,
) -> Optional[Union[ErrorResponse, ModelUnderTestResponse]]:
    """Update Model Under Test

     Update a model under test

    Returns:
        the updated model under test

    Args:
        mut_id (str): The ID of the model under test to get
        api_key (str):
        json_body (ModelUnderTestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, ModelUnderTestResponse]
    """

    return sync_detailed(
        mut_id=mut_id,
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    mut_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ModelUnderTestSchema,
    api_key: str,
) -> Response[Union[ErrorResponse, ModelUnderTestResponse]]:
    """Update Model Under Test

     Update a model under test

    Returns:
        the updated model under test

    Args:
        mut_id (str): The ID of the model under test to get
        api_key (str):
        json_body (ModelUnderTestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, ModelUnderTestResponse]]
    """

    kwargs = _get_kwargs(
        mut_id=mut_id,
        json_body=json_body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    mut_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ModelUnderTestSchema,
    api_key: str,
) -> Optional[Union[ErrorResponse, ModelUnderTestResponse]]:
    """Update Model Under Test

     Update a model under test

    Returns:
        the updated model under test

    Args:
        mut_id (str): The ID of the model under test to get
        api_key (str):
        json_body (ModelUnderTestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, ModelUnderTestResponse]
    """

    return (
        await asyncio_detailed(
            mut_id=mut_id,
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
