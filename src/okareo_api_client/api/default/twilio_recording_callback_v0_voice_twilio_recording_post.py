from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.twilio_recording_callback_v0_voice_twilio_recording_post_response_twilio_recording_callback_v0_voice_twilio_recording_post import (
    TwilioRecordingCallbackV0VoiceTwilioRecordingPostResponseTwilioRecordingCallbackV0VoiceTwilioRecordingPost,
)
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    return {
        "method": "post",
        "url": "/v0/voice/twilio/recording",
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    TwilioRecordingCallbackV0VoiceTwilioRecordingPostResponseTwilioRecordingCallbackV0VoiceTwilioRecordingPost
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TwilioRecordingCallbackV0VoiceTwilioRecordingPostResponseTwilioRecordingCallbackV0VoiceTwilioRecordingPost.from_dict(
            response.json()
        )

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    TwilioRecordingCallbackV0VoiceTwilioRecordingPostResponseTwilioRecordingCallbackV0VoiceTwilioRecordingPost
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
) -> Response[
    TwilioRecordingCallbackV0VoiceTwilioRecordingPostResponseTwilioRecordingCallbackV0VoiceTwilioRecordingPost
]:
    """Twilio Recording Callback

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TwilioRecordingCallbackV0VoiceTwilioRecordingPostResponseTwilioRecordingCallbackV0VoiceTwilioRecordingPost]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    TwilioRecordingCallbackV0VoiceTwilioRecordingPostResponseTwilioRecordingCallbackV0VoiceTwilioRecordingPost
]:
    """Twilio Recording Callback

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TwilioRecordingCallbackV0VoiceTwilioRecordingPostResponseTwilioRecordingCallbackV0VoiceTwilioRecordingPost
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    TwilioRecordingCallbackV0VoiceTwilioRecordingPostResponseTwilioRecordingCallbackV0VoiceTwilioRecordingPost
]:
    """Twilio Recording Callback

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TwilioRecordingCallbackV0VoiceTwilioRecordingPostResponseTwilioRecordingCallbackV0VoiceTwilioRecordingPost]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    TwilioRecordingCallbackV0VoiceTwilioRecordingPostResponseTwilioRecordingCallbackV0VoiceTwilioRecordingPost
]:
    """Twilio Recording Callback

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TwilioRecordingCallbackV0VoiceTwilioRecordingPostResponseTwilioRecordingCallbackV0VoiceTwilioRecordingPost
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
