from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.check_validate_request import CheckValidateRequest
from ...models.check_validate_response import CheckValidateResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    body: CheckValidateRequest,
    api_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key"] = api_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v0/check_validate",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CheckValidateResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = CheckValidateResponse.from_dict(response.json())

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
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CheckValidateResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CheckValidateRequest,
    api_key: str,
) -> Response[CheckValidateResponse | ErrorResponse]:
    """Check Validate

     Validate a check without persisting.
    For code-based checks validates code_contents; for model-based checks validates prompt_template.
    Returns valid=True/False and an optional message.

    Args:
        api_key (str):
        body (CheckValidateRequest): Request body for POST /check_validate. Validates check code
            or prompt without persisting.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CheckValidateResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: CheckValidateRequest,
    api_key: str,
) -> CheckValidateResponse | ErrorResponse | None:
    """Check Validate

     Validate a check without persisting.
    For code-based checks validates code_contents; for model-based checks validates prompt_template.
    Returns valid=True/False and an optional message.

    Args:
        api_key (str):
        body (CheckValidateRequest): Request body for POST /check_validate. Validates check code
            or prompt without persisting.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CheckValidateResponse | ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CheckValidateRequest,
    api_key: str,
) -> Response[CheckValidateResponse | ErrorResponse]:
    """Check Validate

     Validate a check without persisting.
    For code-based checks validates code_contents; for model-based checks validates prompt_template.
    Returns valid=True/False and an optional message.

    Args:
        api_key (str):
        body (CheckValidateRequest): Request body for POST /check_validate. Validates check code
            or prompt without persisting.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CheckValidateResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: CheckValidateRequest,
    api_key: str,
) -> CheckValidateResponse | ErrorResponse | None:
    """Check Validate

     Validate a check without persisting.
    For code-based checks validates code_contents; for model-based checks validates prompt_template.
    Returns valid=True/False and an optional message.

    Args:
        api_key (str):
        body (CheckValidateRequest): Request body for POST /check_validate. Validates check code
            or prompt without persisting.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CheckValidateResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key=api_key,
        )
    ).parsed
