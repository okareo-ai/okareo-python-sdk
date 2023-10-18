from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_scenario_sets_upload_v0_scenario_sets_upload_post import (
    BodyScenarioSetsUploadV0ScenarioSetsUploadPost,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.scenario_set_response import ScenarioSetResponse
from ...types import Response


def _get_kwargs(
    *,
    multipart_data: BodyScenarioSetsUploadV0ScenarioSetsUploadPost,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": "/v0/scenario_sets_upload/",
        "files": multipart_multipart_data,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ScenarioSetResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ScenarioSetResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ScenarioSetResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: BodyScenarioSetsUploadV0ScenarioSetsUploadPost,
    api_key: str,
) -> Response[Union[HTTPValidationError, ScenarioSetResponse]]:
    """Scenario Sets Upload

    Args:
        api_key (str):
        multipart_data (BodyScenarioSetsUploadV0ScenarioSetsUploadPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ScenarioSetResponse]]
    """

    kwargs = _get_kwargs(
        multipart_data=multipart_data,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: BodyScenarioSetsUploadV0ScenarioSetsUploadPost,
    api_key: str,
) -> Optional[Union[HTTPValidationError, ScenarioSetResponse]]:
    """Scenario Sets Upload

    Args:
        api_key (str):
        multipart_data (BodyScenarioSetsUploadV0ScenarioSetsUploadPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ScenarioSetResponse]
    """

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: BodyScenarioSetsUploadV0ScenarioSetsUploadPost,
    api_key: str,
) -> Response[Union[HTTPValidationError, ScenarioSetResponse]]:
    """Scenario Sets Upload

    Args:
        api_key (str):
        multipart_data (BodyScenarioSetsUploadV0ScenarioSetsUploadPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ScenarioSetResponse]]
    """

    kwargs = _get_kwargs(
        multipart_data=multipart_data,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: BodyScenarioSetsUploadV0ScenarioSetsUploadPost,
    api_key: str,
) -> Optional[Union[HTTPValidationError, ScenarioSetResponse]]:
    """Scenario Sets Upload

    Args:
        api_key (str):
        multipart_data (BodyScenarioSetsUploadV0ScenarioSetsUploadPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ScenarioSetResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
            api_key=api_key,
        )
    ).parsed
