from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.setup_filter_group_notification_v0_setup_filter_group_notification_post_response_setup_filter_group_notification_v0_setup_filter_group_notification_post import (
    SetupFilterGroupNotificationV0SetupFilterGroupNotificationPostResponseSetupFilterGroupNotificationV0SetupFilterGroupNotificationPost,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    filter_group_id: str,
    notification_type: str,
    status: str,
    cooldown_seconds: Union[Unset, None, int] = 0,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    params: Dict[str, Any] = {}
    params["filter_group_id"] = filter_group_id

    params["notification_type"] = notification_type

    params["status"] = status

    params["cooldown_seconds"] = cooldown_seconds

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": "/v0/setup_filter_group_notification",
        "params": params,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        ErrorResponse,
        SetupFilterGroupNotificationV0SetupFilterGroupNotificationPostResponseSetupFilterGroupNotificationV0SetupFilterGroupNotificationPost,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SetupFilterGroupNotificationV0SetupFilterGroupNotificationPostResponseSetupFilterGroupNotificationV0SetupFilterGroupNotificationPost.from_dict(
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
        SetupFilterGroupNotificationV0SetupFilterGroupNotificationPostResponseSetupFilterGroupNotificationV0SetupFilterGroupNotificationPost,
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
    filter_group_id: str,
    notification_type: str,
    status: str,
    cooldown_seconds: Union[Unset, None, int] = 0,
    api_key: str,
) -> Response[
    Union[
        ErrorResponse,
        SetupFilterGroupNotificationV0SetupFilterGroupNotificationPostResponseSetupFilterGroupNotificationV0SetupFilterGroupNotificationPost,
    ]
]:
    r"""Setup Filter Group Notification

     Set up or manage a notification for a specific filter group.

    Args:
        request: The HTTP request
        filter_group_id: The ID of the filter group to set up notifications for
        notification_type: The type of notification channel (\"slack\" or \"email\" only for now)
        status: Whether to enable (\"on\") or disable (\"off\") notifications
        cooldown_seconds: The cooldown period in seconds for notifications (default of 0 will use
    default cooldowns of 24 hours (email) and 1 minute (slack)).

    Returns:
        dict: Details about the notification configuration

    Args:
        filter_group_id (str):
        notification_type (str):
        status (str):
        cooldown_seconds (Union[Unset, None, int]):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SetupFilterGroupNotificationV0SetupFilterGroupNotificationPostResponseSetupFilterGroupNotificationV0SetupFilterGroupNotificationPost]]
    """

    kwargs = _get_kwargs(
        filter_group_id=filter_group_id,
        notification_type=notification_type,
        status=status,
        cooldown_seconds=cooldown_seconds,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    filter_group_id: str,
    notification_type: str,
    status: str,
    cooldown_seconds: Union[Unset, None, int] = 0,
    api_key: str,
) -> Optional[
    Union[
        ErrorResponse,
        SetupFilterGroupNotificationV0SetupFilterGroupNotificationPostResponseSetupFilterGroupNotificationV0SetupFilterGroupNotificationPost,
    ]
]:
    r"""Setup Filter Group Notification

     Set up or manage a notification for a specific filter group.

    Args:
        request: The HTTP request
        filter_group_id: The ID of the filter group to set up notifications for
        notification_type: The type of notification channel (\"slack\" or \"email\" only for now)
        status: Whether to enable (\"on\") or disable (\"off\") notifications
        cooldown_seconds: The cooldown period in seconds for notifications (default of 0 will use
    default cooldowns of 24 hours (email) and 1 minute (slack)).

    Returns:
        dict: Details about the notification configuration

    Args:
        filter_group_id (str):
        notification_type (str):
        status (str):
        cooldown_seconds (Union[Unset, None, int]):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SetupFilterGroupNotificationV0SetupFilterGroupNotificationPostResponseSetupFilterGroupNotificationV0SetupFilterGroupNotificationPost]
    """

    return sync_detailed(
        client=client,
        filter_group_id=filter_group_id,
        notification_type=notification_type,
        status=status,
        cooldown_seconds=cooldown_seconds,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    filter_group_id: str,
    notification_type: str,
    status: str,
    cooldown_seconds: Union[Unset, None, int] = 0,
    api_key: str,
) -> Response[
    Union[
        ErrorResponse,
        SetupFilterGroupNotificationV0SetupFilterGroupNotificationPostResponseSetupFilterGroupNotificationV0SetupFilterGroupNotificationPost,
    ]
]:
    r"""Setup Filter Group Notification

     Set up or manage a notification for a specific filter group.

    Args:
        request: The HTTP request
        filter_group_id: The ID of the filter group to set up notifications for
        notification_type: The type of notification channel (\"slack\" or \"email\" only for now)
        status: Whether to enable (\"on\") or disable (\"off\") notifications
        cooldown_seconds: The cooldown period in seconds for notifications (default of 0 will use
    default cooldowns of 24 hours (email) and 1 minute (slack)).

    Returns:
        dict: Details about the notification configuration

    Args:
        filter_group_id (str):
        notification_type (str):
        status (str):
        cooldown_seconds (Union[Unset, None, int]):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SetupFilterGroupNotificationV0SetupFilterGroupNotificationPostResponseSetupFilterGroupNotificationV0SetupFilterGroupNotificationPost]]
    """

    kwargs = _get_kwargs(
        filter_group_id=filter_group_id,
        notification_type=notification_type,
        status=status,
        cooldown_seconds=cooldown_seconds,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    filter_group_id: str,
    notification_type: str,
    status: str,
    cooldown_seconds: Union[Unset, None, int] = 0,
    api_key: str,
) -> Optional[
    Union[
        ErrorResponse,
        SetupFilterGroupNotificationV0SetupFilterGroupNotificationPostResponseSetupFilterGroupNotificationV0SetupFilterGroupNotificationPost,
    ]
]:
    r"""Setup Filter Group Notification

     Set up or manage a notification for a specific filter group.

    Args:
        request: The HTTP request
        filter_group_id: The ID of the filter group to set up notifications for
        notification_type: The type of notification channel (\"slack\" or \"email\" only for now)
        status: Whether to enable (\"on\") or disable (\"off\") notifications
        cooldown_seconds: The cooldown period in seconds for notifications (default of 0 will use
    default cooldowns of 24 hours (email) and 1 minute (slack)).

    Returns:
        dict: Details about the notification configuration

    Args:
        filter_group_id (str):
        notification_type (str):
        status (str):
        cooldown_seconds (Union[Unset, None, int]):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SetupFilterGroupNotificationV0SetupFilterGroupNotificationPostResponseSetupFilterGroupNotificationV0SetupFilterGroupNotificationPost]
    """

    return (
        await asyncio_detailed(
            client=client,
            filter_group_id=filter_group_id,
            notification_type=notification_type,
            status=status,
            cooldown_seconds=cooldown_seconds,
            api_key=api_key,
        )
    ).parsed
