from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.slack_oauth_callback_v0_slack_get_response_slack_oauth_callback_v0_slack_get import (
    SlackOauthCallbackV0SlackGetResponseSlackOauthCallbackV0SlackGet,
)
from ...types import UNSET, Response


def _get_kwargs(
    *,
    code: str,
    state: str,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    params: dict[str, Any] = {}

    params["code"] = code

    params["state"] = state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v0/slack",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, SlackOauthCallbackV0SlackGetResponseSlackOauthCallbackV0SlackGet]]:
    if response.status_code == 200:
        response_200 = SlackOauthCallbackV0SlackGetResponseSlackOauthCallbackV0SlackGet.from_dict(response.json())

        return response_200
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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponse, SlackOauthCallbackV0SlackGetResponseSlackOauthCallbackV0SlackGet]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    code: str,
    state: str,
    api_key: str,
) -> Response[Union[ErrorResponse, SlackOauthCallbackV0SlackGetResponseSlackOauthCallbackV0SlackGet]]:
    """Slack Oauth Callback

    Args:
        code (str):
        state (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SlackOauthCallbackV0SlackGetResponseSlackOauthCallbackV0SlackGet]]
    """

    kwargs = _get_kwargs(
        code=code,
        state=state,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    code: str,
    state: str,
    api_key: str,
) -> Optional[Union[ErrorResponse, SlackOauthCallbackV0SlackGetResponseSlackOauthCallbackV0SlackGet]]:
    """Slack Oauth Callback

    Args:
        code (str):
        state (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SlackOauthCallbackV0SlackGetResponseSlackOauthCallbackV0SlackGet]
    """

    return sync_detailed(
        client=client,
        code=code,
        state=state,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    code: str,
    state: str,
    api_key: str,
) -> Response[Union[ErrorResponse, SlackOauthCallbackV0SlackGetResponseSlackOauthCallbackV0SlackGet]]:
    """Slack Oauth Callback

    Args:
        code (str):
        state (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SlackOauthCallbackV0SlackGetResponseSlackOauthCallbackV0SlackGet]]
    """

    kwargs = _get_kwargs(
        code=code,
        state=state,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    code: str,
    state: str,
    api_key: str,
) -> Optional[Union[ErrorResponse, SlackOauthCallbackV0SlackGetResponseSlackOauthCallbackV0SlackGet]]:
    """Slack Oauth Callback

    Args:
        code (str):
        state (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SlackOauthCallbackV0SlackGetResponseSlackOauthCallbackV0SlackGet]
    """

    return (
        await asyncio_detailed(
            client=client,
            code=code,
            state=state,
            api_key=api_key,
        )
    ).parsed
