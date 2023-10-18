from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.model_under_test_response import ModelUnderTestResponse
from ...models.model_under_test_schema import ModelUnderTestSchema
from ...types import Response


def _get_kwargs(
    *,
    json_body: ModelUnderTestSchema,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v0/register_model",
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ModelUnderTestResponse]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = ModelUnderTestResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ModelUnderTestResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ModelUnderTestSchema,
    api_key: str,
) -> Response[Union[HTTPValidationError, ModelUnderTestResponse]]:
    """Register Model

     Register the model under test

    Returns:
        the id of the registered model

    Args:
        api_key (str):
        json_body (ModelUnderTestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ModelUnderTestResponse]]
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
    json_body: ModelUnderTestSchema,
    api_key: str,
) -> Optional[Union[HTTPValidationError, ModelUnderTestResponse]]:
    """Register Model

     Register the model under test

    Returns:
        the id of the registered model

    Args:
        api_key (str):
        json_body (ModelUnderTestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ModelUnderTestResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ModelUnderTestSchema,
    api_key: str,
) -> Response[Union[HTTPValidationError, ModelUnderTestResponse]]:
    """Register Model

     Register the model under test

    Returns:
        the id of the registered model

    Args:
        api_key (str):
        json_body (ModelUnderTestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ModelUnderTestResponse]]
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
    json_body: ModelUnderTestSchema,
    api_key: str,
) -> Optional[Union[HTTPValidationError, ModelUnderTestResponse]]:
    """Register Model

     Register the model under test

    Returns:
        the id of the registered model

    Args:
        api_key (str):
        json_body (ModelUnderTestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ModelUnderTestResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
