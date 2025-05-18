from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_check_delete_v0_check_check_id_delete import BodyCheckDeleteV0CheckCheckIdDelete
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    check_id: UUID,
    *,
    body: BodyCheckDeleteV0CheckCheckIdDelete,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/v0/check/{check_id}",
    }

    _body = body.to_dict()

    _kwargs["data"] = _body
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ErrorResponse]]:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
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
) -> Response[Union[Any, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    check_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyCheckDeleteV0CheckCheckIdDelete,
    api_key: str,
) -> Response[Union[Any, ErrorResponse]]:
    """Check Delete

     Deletes a check

    Raises:
        HTTPException: 404 if check_id is not found

    Returns: 204 status code on successful deletion

    Args:
        check_id (UUID):
        api_key (str):
        body (BodyCheckDeleteV0CheckCheckIdDelete):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        check_id=check_id,
        body=body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    check_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyCheckDeleteV0CheckCheckIdDelete,
    api_key: str,
) -> Optional[Union[Any, ErrorResponse]]:
    """Check Delete

     Deletes a check

    Raises:
        HTTPException: 404 if check_id is not found

    Returns: 204 status code on successful deletion

    Args:
        check_id (UUID):
        api_key (str):
        body (BodyCheckDeleteV0CheckCheckIdDelete):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return sync_detailed(
        check_id=check_id,
        client=client,
        body=body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    check_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyCheckDeleteV0CheckCheckIdDelete,
    api_key: str,
) -> Response[Union[Any, ErrorResponse]]:
    """Check Delete

     Deletes a check

    Raises:
        HTTPException: 404 if check_id is not found

    Returns: 204 status code on successful deletion

    Args:
        check_id (UUID):
        api_key (str):
        body (BodyCheckDeleteV0CheckCheckIdDelete):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        check_id=check_id,
        body=body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    check_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyCheckDeleteV0CheckCheckIdDelete,
    api_key: str,
) -> Optional[Union[Any, ErrorResponse]]:
    """Check Delete

     Deletes a check

    Raises:
        HTTPException: 404 if check_id is not found

    Returns: 204 status code on successful deletion

    Args:
        check_id (UUID):
        api_key (str):
        body (BodyCheckDeleteV0CheckCheckIdDelete):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            check_id=check_id,
            client=client,
            body=body,
            api_key=api_key,
        )
    ).parsed
