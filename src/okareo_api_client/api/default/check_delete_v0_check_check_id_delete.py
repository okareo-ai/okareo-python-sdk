from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_check_delete_v0_check_check_id_delete import BodyCheckDeleteV0CheckCheckIdDelete
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    check_id: str,
    *,
    form_data: BodyCheckDeleteV0CheckCheckIdDelete,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    return {
        "method": "delete",
        "url": "/v0/check/{check_id}".format(
            check_id=check_id,
        ),
        "data": form_data.to_dict(),
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ErrorResponse]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
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
) -> Response[Union[Any, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    check_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    form_data: BodyCheckDeleteV0CheckCheckIdDelete,
    api_key: str,
) -> Response[Union[Any, ErrorResponse]]:
    """Check Delete

     Deletes a check

    Raises:
        HTTPException: 404 if check_id is not found

    Returns: 204 status code on successful deletion

    Args:
        check_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        check_id=check_id,
        form_data=form_data,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    check_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    form_data: BodyCheckDeleteV0CheckCheckIdDelete,
    api_key: str,
) -> Optional[Union[Any, ErrorResponse]]:
    """Check Delete

     Deletes a check

    Raises:
        HTTPException: 404 if check_id is not found

    Returns: 204 status code on successful deletion

    Args:
        check_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return sync_detailed(
        check_id=check_id,
        client=client,
        form_data=form_data,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    check_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    form_data: BodyCheckDeleteV0CheckCheckIdDelete,
    api_key: str,
) -> Response[Union[Any, ErrorResponse]]:
    """Check Delete

     Deletes a check

    Raises:
        HTTPException: 404 if check_id is not found

    Returns: 204 status code on successful deletion

    Args:
        check_id (str):
        api_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        check_id=check_id,
        form_data=form_data,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    check_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    form_data: BodyCheckDeleteV0CheckCheckIdDelete,
    api_key: str,
) -> Optional[Union[Any, ErrorResponse]]:
    """Check Delete

     Deletes a check

    Raises:
        HTTPException: 404 if check_id is not found

    Returns: 204 status code on successful deletion

    Args:
        check_id (str):
        api_key (str):

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
            form_data=form_data,
            api_key=api_key,
        )
    ).parsed