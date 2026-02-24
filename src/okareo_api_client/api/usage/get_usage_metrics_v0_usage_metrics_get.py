from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.usage_metrics_response import UsageMetricsResponse
from ...models.usage_precision import UsagePrecision
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    start_date: None | str | Unset = UNSET,
    end_date: None | str | Unset = UNSET,
    project_id: None | Unset | UUID = UNSET,
    precision: UsagePrecision | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_start_date: None | str | Unset
    if isinstance(start_date, Unset):
        json_start_date = UNSET
    else:
        json_start_date = start_date
    params["start_date"] = json_start_date

    json_end_date: None | str | Unset
    if isinstance(end_date, Unset):
        json_end_date = UNSET
    else:
        json_end_date = end_date
    params["end_date"] = json_end_date

    json_project_id: None | str | Unset
    if isinstance(project_id, Unset):
        json_project_id = UNSET
    elif isinstance(project_id, UUID):
        json_project_id = str(project_id)
    else:
        json_project_id = project_id
    params["project_id"] = json_project_id

    json_precision: str | Unset = UNSET
    if not isinstance(precision, Unset):
        json_precision = precision.value

    params["precision"] = json_precision

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v0/usage/metrics",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | UsageMetricsResponse | None:
    if response.status_code == 200:
        response_200 = UsageMetricsResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | UsageMetricsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    start_date: None | str | Unset = UNSET,
    end_date: None | str | Unset = UNSET,
    project_id: None | Unset | UUID = UNSET,
    precision: UsagePrecision | Unset = UNSET,
) -> Response[HTTPValidationError | UsageMetricsResponse]:
    """Get usage metrics

     Get usage metrics for the authenticated organization.

        **Authentication:** Requires valid API key in 'api-key' header.
        The organization is automatically deduced from the API key via VerifyTokenMiddleware.

        **Date Range Defaults:**
        - If `start_date` is not provided, defaults to 30 days ago
        - If `end_date` is not provided, defaults to current time (with buffer applied)

        **Data Completeness:** Metrics include only completed sessions, test runs,
        and datapoints. A configurable time buffer may be applied to ensure data completeness.

        **Metrics Included:**
        - **voice_minutes**: Sum of audio/voice minutes from completed sessions
        - **simulations**: Count of completed test runs (all types: voice and non-voice)
        - **datapoints**: Count of non-error datapoints
        - **checks**: Total check executions from test runs and monitors

        **Example Usage:**
        ```
        # Last 30 days (default)
        GET /v0/usage/metrics

        # Specific date range
        GET /v0/usage/metrics?start_date=2026-01-01T00:00:00Z&end_date=2026-01-31T23:59:59Z

        # Custom start, default end
        GET /v0/usage/metrics?start_date=2026-01-01T00:00:00Z
        ```

    Args:
        start_date (None | str | Unset): Start date for metrics period (ISO 8601 or YYYY-MM-DD).
            Defaults to 30 days ago if not provided.
        end_date (None | str | Unset): End date for metrics period (will be capped based on
            buffer). Defaults to current time with buffer applied.
        project_id (None | Unset | UUID): Optional project filter - only include metrics for this
            project
        precision (UsagePrecision | Unset): Time period precision for usage metrics.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UsageMetricsResponse]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
        project_id=project_id,
        precision=precision,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    start_date: None | str | Unset = UNSET,
    end_date: None | str | Unset = UNSET,
    project_id: None | Unset | UUID = UNSET,
    precision: UsagePrecision | Unset = UNSET,
) -> HTTPValidationError | UsageMetricsResponse | None:
    """Get usage metrics

     Get usage metrics for the authenticated organization.

        **Authentication:** Requires valid API key in 'api-key' header.
        The organization is automatically deduced from the API key via VerifyTokenMiddleware.

        **Date Range Defaults:**
        - If `start_date` is not provided, defaults to 30 days ago
        - If `end_date` is not provided, defaults to current time (with buffer applied)

        **Data Completeness:** Metrics include only completed sessions, test runs,
        and datapoints. A configurable time buffer may be applied to ensure data completeness.

        **Metrics Included:**
        - **voice_minutes**: Sum of audio/voice minutes from completed sessions
        - **simulations**: Count of completed test runs (all types: voice and non-voice)
        - **datapoints**: Count of non-error datapoints
        - **checks**: Total check executions from test runs and monitors

        **Example Usage:**
        ```
        # Last 30 days (default)
        GET /v0/usage/metrics

        # Specific date range
        GET /v0/usage/metrics?start_date=2026-01-01T00:00:00Z&end_date=2026-01-31T23:59:59Z

        # Custom start, default end
        GET /v0/usage/metrics?start_date=2026-01-01T00:00:00Z
        ```

    Args:
        start_date (None | str | Unset): Start date for metrics period (ISO 8601 or YYYY-MM-DD).
            Defaults to 30 days ago if not provided.
        end_date (None | str | Unset): End date for metrics period (will be capped based on
            buffer). Defaults to current time with buffer applied.
        project_id (None | Unset | UUID): Optional project filter - only include metrics for this
            project
        precision (UsagePrecision | Unset): Time period precision for usage metrics.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UsageMetricsResponse
    """

    return sync_detailed(
        client=client,
        start_date=start_date,
        end_date=end_date,
        project_id=project_id,
        precision=precision,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    start_date: None | str | Unset = UNSET,
    end_date: None | str | Unset = UNSET,
    project_id: None | Unset | UUID = UNSET,
    precision: UsagePrecision | Unset = UNSET,
) -> Response[HTTPValidationError | UsageMetricsResponse]:
    """Get usage metrics

     Get usage metrics for the authenticated organization.

        **Authentication:** Requires valid API key in 'api-key' header.
        The organization is automatically deduced from the API key via VerifyTokenMiddleware.

        **Date Range Defaults:**
        - If `start_date` is not provided, defaults to 30 days ago
        - If `end_date` is not provided, defaults to current time (with buffer applied)

        **Data Completeness:** Metrics include only completed sessions, test runs,
        and datapoints. A configurable time buffer may be applied to ensure data completeness.

        **Metrics Included:**
        - **voice_minutes**: Sum of audio/voice minutes from completed sessions
        - **simulations**: Count of completed test runs (all types: voice and non-voice)
        - **datapoints**: Count of non-error datapoints
        - **checks**: Total check executions from test runs and monitors

        **Example Usage:**
        ```
        # Last 30 days (default)
        GET /v0/usage/metrics

        # Specific date range
        GET /v0/usage/metrics?start_date=2026-01-01T00:00:00Z&end_date=2026-01-31T23:59:59Z

        # Custom start, default end
        GET /v0/usage/metrics?start_date=2026-01-01T00:00:00Z
        ```

    Args:
        start_date (None | str | Unset): Start date for metrics period (ISO 8601 or YYYY-MM-DD).
            Defaults to 30 days ago if not provided.
        end_date (None | str | Unset): End date for metrics period (will be capped based on
            buffer). Defaults to current time with buffer applied.
        project_id (None | Unset | UUID): Optional project filter - only include metrics for this
            project
        precision (UsagePrecision | Unset): Time period precision for usage metrics.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UsageMetricsResponse]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
        project_id=project_id,
        precision=precision,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    start_date: None | str | Unset = UNSET,
    end_date: None | str | Unset = UNSET,
    project_id: None | Unset | UUID = UNSET,
    precision: UsagePrecision | Unset = UNSET,
) -> HTTPValidationError | UsageMetricsResponse | None:
    """Get usage metrics

     Get usage metrics for the authenticated organization.

        **Authentication:** Requires valid API key in 'api-key' header.
        The organization is automatically deduced from the API key via VerifyTokenMiddleware.

        **Date Range Defaults:**
        - If `start_date` is not provided, defaults to 30 days ago
        - If `end_date` is not provided, defaults to current time (with buffer applied)

        **Data Completeness:** Metrics include only completed sessions, test runs,
        and datapoints. A configurable time buffer may be applied to ensure data completeness.

        **Metrics Included:**
        - **voice_minutes**: Sum of audio/voice minutes from completed sessions
        - **simulations**: Count of completed test runs (all types: voice and non-voice)
        - **datapoints**: Count of non-error datapoints
        - **checks**: Total check executions from test runs and monitors

        **Example Usage:**
        ```
        # Last 30 days (default)
        GET /v0/usage/metrics

        # Specific date range
        GET /v0/usage/metrics?start_date=2026-01-01T00:00:00Z&end_date=2026-01-31T23:59:59Z

        # Custom start, default end
        GET /v0/usage/metrics?start_date=2026-01-01T00:00:00Z
        ```

    Args:
        start_date (None | str | Unset): Start date for metrics period (ISO 8601 or YYYY-MM-DD).
            Defaults to 30 days ago if not provided.
        end_date (None | str | Unset): End date for metrics period (will be capped based on
            buffer). Defaults to current time with buffer applied.
        project_id (None | Unset | UUID): Optional project filter - only include metrics for this
            project
        precision (UsagePrecision | Unset): Time period precision for usage metrics.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UsageMetricsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            start_date=start_date,
            end_date=end_date,
            project_id=project_id,
            precision=precision,
        )
    ).parsed
