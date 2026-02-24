from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    call_sid: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v0/voice/call_sid/{call_sid}".format(
            call_sid=quote(str(call_sid), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    call_sid: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError]:
    r"""Download File By Call Sid

     Download a voice recording by call_sid.

    This endpoint allows the UI to fetch recordings using just the call_sid
    from the datapoint metadata, without needing to know the file_id.

    Args:
        call_sid: Twilio CallSid (e.g., \"CA1234567890abcdef\")

    Returns:
        StreamingResponse with the audio file (WAV format)

    Raises:
        HTTPException 404: If no recording found for the call_sid

    Args:
        call_sid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        call_sid=call_sid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    call_sid: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | HTTPValidationError | None:
    r"""Download File By Call Sid

     Download a voice recording by call_sid.

    This endpoint allows the UI to fetch recordings using just the call_sid
    from the datapoint metadata, without needing to know the file_id.

    Args:
        call_sid: Twilio CallSid (e.g., \"CA1234567890abcdef\")

    Returns:
        StreamingResponse with the audio file (WAV format)

    Raises:
        HTTPException 404: If no recording found for the call_sid

    Args:
        call_sid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        call_sid=call_sid,
        client=client,
    ).parsed


async def asyncio_detailed(
    call_sid: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError]:
    r"""Download File By Call Sid

     Download a voice recording by call_sid.

    This endpoint allows the UI to fetch recordings using just the call_sid
    from the datapoint metadata, without needing to know the file_id.

    Args:
        call_sid: Twilio CallSid (e.g., \"CA1234567890abcdef\")

    Returns:
        StreamingResponse with the audio file (WAV format)

    Raises:
        HTTPException 404: If no recording found for the call_sid

    Args:
        call_sid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        call_sid=call_sid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    call_sid: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | HTTPValidationError | None:
    r"""Download File By Call Sid

     Download a voice recording by call_sid.

    This endpoint allows the UI to fetch recordings using just the call_sid
    from the datapoint metadata, without needing to know the file_id.

    Args:
        call_sid: Twilio CallSid (e.g., \"CA1234567890abcdef\")

    Returns:
        StreamingResponse with the audio file (WAV format)

    Raises:
        HTTPException 404: If no recording found for the call_sid

    Args:
        call_sid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            call_sid=call_sid,
            client=client,
        )
    ).parsed
