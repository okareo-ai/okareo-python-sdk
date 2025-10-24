from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.driver_model_response import DriverModelResponse
from ...models.driver_model_schema import DriverModelSchema
from ...models.error_response import ErrorResponse
from ...models.voice_driver_model_response import VoiceDriverModelResponse
from ...types import Response


def _get_kwargs(
    driver_id: str,
    *,
    json_body: DriverModelSchema,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/v0/driver/{driver_id}".format(
            driver_id=driver_id,
        ),
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, Union["DriverModelResponse", "VoiceDriverModelResponse"]]]:
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
) -> Response[Union[ErrorResponse, Union["DriverModelResponse", "VoiceDriverModelResponse"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    driver_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DriverModelSchema,
    api_key: str,
) -> Response[Union[ErrorResponse, Union["DriverModelResponse", "VoiceDriverModelResponse"]]]:
    """Update Driver Model

    Args:
        driver_id (str):
        api_key (str):
        json_body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, Union['DriverModelResponse', 'VoiceDriverModelResponse']]]
    """

    kwargs = _get_kwargs(
        driver_id=driver_id,
        json_body=json_body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    driver_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DriverModelSchema,
    api_key: str,
) -> Optional[Union[ErrorResponse, Union["DriverModelResponse", "VoiceDriverModelResponse"]]]:
    """Update Driver Model

    Args:
        driver_id (str):
        api_key (str):
        json_body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, Union['DriverModelResponse', 'VoiceDriverModelResponse']]
    """

    return sync_detailed(
        driver_id=driver_id,
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    driver_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DriverModelSchema,
    api_key: str,
) -> Response[Union[ErrorResponse, Union["DriverModelResponse", "VoiceDriverModelResponse"]]]:
    """Update Driver Model

    Args:
        driver_id (str):
        api_key (str):
        json_body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, Union['DriverModelResponse', 'VoiceDriverModelResponse']]]
    """

    kwargs = _get_kwargs(
        driver_id=driver_id,
        json_body=json_body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    driver_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DriverModelSchema,
    api_key: str,
) -> Optional[Union[ErrorResponse, Union["DriverModelResponse", "VoiceDriverModelResponse"]]]:
    """Update Driver Model

    Args:
        driver_id (str):
        api_key (str):
        json_body (DriverModelSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, Union['DriverModelResponse', 'VoiceDriverModelResponse']]
    """

    return (
        await asyncio_detailed(
            driver_id=driver_id,
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
