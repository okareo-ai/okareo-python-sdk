from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.driver_model_response import DriverModelResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.voice_driver_model_response import VoiceDriverModelResponse
from ...types import Response


def _get_kwargs(
    identifier: str,
    *,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    return {
        "method": "get",
        "url": "/v0/driver/{identifier}".format(
            identifier=identifier,
        ),
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, Union["DriverModelResponse", "VoiceDriverModelResponse"]]]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(data: object) -> Union["DriverModelResponse", "VoiceDriverModelResponse"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = VoiceDriverModelResponse.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = DriverModelResponse.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, Union["DriverModelResponse", "VoiceDriverModelResponse"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Response[Union[HTTPValidationError, Union["DriverModelResponse", "VoiceDriverModelResponse"]]]:
    """Get Driver

    Args:
        identifier (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['DriverModelResponse', 'VoiceDriverModelResponse']]]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Optional[Union[HTTPValidationError, Union["DriverModelResponse", "VoiceDriverModelResponse"]]]:
    """Get Driver

    Args:
        identifier (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['DriverModelResponse', 'VoiceDriverModelResponse']]
    """

    return sync_detailed(
        identifier=identifier,
        client=client,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Response[Union[HTTPValidationError, Union["DriverModelResponse", "VoiceDriverModelResponse"]]]:
    """Get Driver

    Args:
        identifier (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['DriverModelResponse', 'VoiceDriverModelResponse']]]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    api_key: str,
) -> Optional[Union[HTTPValidationError, Union["DriverModelResponse", "VoiceDriverModelResponse"]]]:
    """Get Driver

    Args:
        identifier (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['DriverModelResponse', 'VoiceDriverModelResponse']]
    """

    return (
        await asyncio_detailed(
            identifier=identifier,
            client=client,
            api_key=api_key,
        )
    ).parsed
