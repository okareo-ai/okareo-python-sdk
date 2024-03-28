from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_evaluator_upload_v0_evaluator_upload_post import BodyEvaluatorUploadV0EvaluatorUploadPost
from ...models.error_response import ErrorResponse
from ...models.evaluator_response import EvaluatorResponse
from ...types import UNSET, Response


def _get_kwargs(
    *,
    multipart_data: BodyEvaluatorUploadV0EvaluatorUploadPost,
    requires_scenario_input: bool,
    requires_scenario_result: bool,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    params: Dict[str, Any] = {}
    params["requires_scenario_input"] = requires_scenario_input

    params["requires_scenario_result"] = requires_scenario_result

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": "/v0/evaluator_upload",
        "files": multipart_multipart_data,
        "params": params,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, EvaluatorResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = EvaluatorResponse.from_dict(response.json())

        return response_200
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
) -> Response[Union[ErrorResponse, EvaluatorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: BodyEvaluatorUploadV0EvaluatorUploadPost,
    requires_scenario_input: bool,
    requires_scenario_result: bool,
    api_key: str,
) -> Response[Union[ErrorResponse, EvaluatorResponse]]:
    """Evaluator Upload

     Upload a new evaluator

    Returns:
        the evaluator object with its ID

    Args:
        requires_scenario_input (bool):
        requires_scenario_result (bool):
        api_key (str):
        multipart_data (BodyEvaluatorUploadV0EvaluatorUploadPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, EvaluatorResponse]]
    """

    kwargs = _get_kwargs(
        multipart_data=multipart_data,
        requires_scenario_input=requires_scenario_input,
        requires_scenario_result=requires_scenario_result,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: BodyEvaluatorUploadV0EvaluatorUploadPost,
    requires_scenario_input: bool,
    requires_scenario_result: bool,
    api_key: str,
) -> Optional[Union[ErrorResponse, EvaluatorResponse]]:
    """Evaluator Upload

     Upload a new evaluator

    Returns:
        the evaluator object with its ID

    Args:
        requires_scenario_input (bool):
        requires_scenario_result (bool):
        api_key (str):
        multipart_data (BodyEvaluatorUploadV0EvaluatorUploadPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, EvaluatorResponse]
    """

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
        requires_scenario_input=requires_scenario_input,
        requires_scenario_result=requires_scenario_result,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: BodyEvaluatorUploadV0EvaluatorUploadPost,
    requires_scenario_input: bool,
    requires_scenario_result: bool,
    api_key: str,
) -> Response[Union[ErrorResponse, EvaluatorResponse]]:
    """Evaluator Upload

     Upload a new evaluator

    Returns:
        the evaluator object with its ID

    Args:
        requires_scenario_input (bool):
        requires_scenario_result (bool):
        api_key (str):
        multipart_data (BodyEvaluatorUploadV0EvaluatorUploadPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, EvaluatorResponse]]
    """

    kwargs = _get_kwargs(
        multipart_data=multipart_data,
        requires_scenario_input=requires_scenario_input,
        requires_scenario_result=requires_scenario_result,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: BodyEvaluatorUploadV0EvaluatorUploadPost,
    requires_scenario_input: bool,
    requires_scenario_result: bool,
    api_key: str,
) -> Optional[Union[ErrorResponse, EvaluatorResponse]]:
    """Evaluator Upload

     Upload a new evaluator

    Returns:
        the evaluator object with its ID

    Args:
        requires_scenario_input (bool):
        requires_scenario_result (bool):
        api_key (str):
        multipart_data (BodyEvaluatorUploadV0EvaluatorUploadPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, EvaluatorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
            requires_scenario_input=requires_scenario_input,
            requires_scenario_result=requires_scenario_result,
            api_key=api_key,
        )
    ).parsed
