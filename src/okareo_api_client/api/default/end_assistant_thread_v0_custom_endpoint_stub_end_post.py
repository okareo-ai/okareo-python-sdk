from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.assistant_end_thread_request import AssistantEndThreadRequest
from ...models.assistant_end_thread_response import AssistantEndThreadResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    json_body: AssistantEndThreadRequest,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v0/custom_endpoint_stub/end",
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AssistantEndThreadResponse, ErrorResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AssistantEndThreadResponse.from_dict(response.json())

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
) -> Response[Union[AssistantEndThreadResponse, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: AssistantEndThreadRequest,
    api_key: str,
) -> Response[Union[AssistantEndThreadResponse, ErrorResponse]]:
    """End Assistant Thread

     Ends an OpenAI Assistant thread and returns a thread summary.

    Args:
        thread_id: The ID of the thread to end

    Returns:
        A confirmation message

    Args:
        api_key (str):
        json_body (AssistantEndThreadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AssistantEndThreadResponse, ErrorResponse]]
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
    json_body: AssistantEndThreadRequest,
    api_key: str,
) -> Optional[Union[AssistantEndThreadResponse, ErrorResponse]]:
    """End Assistant Thread

     Ends an OpenAI Assistant thread and returns a thread summary.

    Args:
        thread_id: The ID of the thread to end

    Returns:
        A confirmation message

    Args:
        api_key (str):
        json_body (AssistantEndThreadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AssistantEndThreadResponse, ErrorResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: AssistantEndThreadRequest,
    api_key: str,
) -> Response[Union[AssistantEndThreadResponse, ErrorResponse]]:
    """End Assistant Thread

     Ends an OpenAI Assistant thread and returns a thread summary.

    Args:
        thread_id: The ID of the thread to end

    Returns:
        A confirmation message

    Args:
        api_key (str):
        json_body (AssistantEndThreadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AssistantEndThreadResponse, ErrorResponse]]
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
    json_body: AssistantEndThreadRequest,
    api_key: str,
) -> Optional[Union[AssistantEndThreadResponse, ErrorResponse]]:
    """End Assistant Thread

     Ends an OpenAI Assistant thread and returns a thread summary.

    Args:
        thread_id: The ID of the thread to end

    Returns:
        A confirmation message

    Args:
        api_key (str):
        json_body (AssistantEndThreadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AssistantEndThreadResponse, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
