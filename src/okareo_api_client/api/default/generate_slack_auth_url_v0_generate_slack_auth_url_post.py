from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.generate_slack_auth_url_v0_generate_slack_auth_url_post_project_data import (
    GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostProjectData,
)
from ...models.generate_slack_auth_url_v0_generate_slack_auth_url_post_response_generate_slack_auth_url_v0_generate_slack_auth_url_post import (
    GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostResponseGenerateSlackAuthUrlV0GenerateSlackAuthUrlPost,
)
from ...types import Response


def _get_kwargs(
    *,
    json_body: GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostProjectData,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v0/generate_slack_auth_url",
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        ErrorResponse,
        GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostResponseGenerateSlackAuthUrlV0GenerateSlackAuthUrlPost,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostResponseGenerateSlackAuthUrlV0GenerateSlackAuthUrlPost.from_dict(
            response.json()
        )

        return response_200
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
) -> Response[
    Union[
        ErrorResponse,
        GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostResponseGenerateSlackAuthUrlV0GenerateSlackAuthUrlPost,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostProjectData,
    api_key: str,
) -> Response[
    Union[
        ErrorResponse,
        GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostResponseGenerateSlackAuthUrlV0GenerateSlackAuthUrlPost,
    ]
]:
    """Generate Slack Auth Url

     Generates a Slack authentication URL with a temporary authorization token.

    Args:
        request: The HTTP request containing project_id in the body
        db: Database session

    Returns:
        dict: Contains the Slack authentication URL

    Args:
        api_key (str):
        json_body (GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostProjectData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostResponseGenerateSlackAuthUrlV0GenerateSlackAuthUrlPost]]
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
    json_body: GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostProjectData,
    api_key: str,
) -> Optional[
    Union[
        ErrorResponse,
        GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostResponseGenerateSlackAuthUrlV0GenerateSlackAuthUrlPost,
    ]
]:
    """Generate Slack Auth Url

     Generates a Slack authentication URL with a temporary authorization token.

    Args:
        request: The HTTP request containing project_id in the body
        db: Database session

    Returns:
        dict: Contains the Slack authentication URL

    Args:
        api_key (str):
        json_body (GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostProjectData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostResponseGenerateSlackAuthUrlV0GenerateSlackAuthUrlPost]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostProjectData,
    api_key: str,
) -> Response[
    Union[
        ErrorResponse,
        GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostResponseGenerateSlackAuthUrlV0GenerateSlackAuthUrlPost,
    ]
]:
    """Generate Slack Auth Url

     Generates a Slack authentication URL with a temporary authorization token.

    Args:
        request: The HTTP request containing project_id in the body
        db: Database session

    Returns:
        dict: Contains the Slack authentication URL

    Args:
        api_key (str):
        json_body (GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostProjectData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostResponseGenerateSlackAuthUrlV0GenerateSlackAuthUrlPost]]
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
    json_body: GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostProjectData,
    api_key: str,
) -> Optional[
    Union[
        ErrorResponse,
        GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostResponseGenerateSlackAuthUrlV0GenerateSlackAuthUrlPost,
    ]
]:
    """Generate Slack Auth Url

     Generates a Slack authentication URL with a temporary authorization token.

    Args:
        request: The HTTP request containing project_id in the body
        db: Database session

    Returns:
        dict: Contains the Slack authentication URL

    Args:
        api_key (str):
        json_body (GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostProjectData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, GenerateSlackAuthUrlV0GenerateSlackAuthUrlPostResponseGenerateSlackAuthUrlV0GenerateSlackAuthUrlPost]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
