import json
from typing import Any, Dict, NoReturn, Optional, Type, TypeVar

import httpx
from httpx._models import Response
from pydantic import BaseModel

from .common import NotJSONError

T = TypeVar("T", bound=BaseModel)


class HTTPXHandler:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    def __init__(self, api_key: str, base_path: str, timeout: float = 5.0):
        self.api_key = api_key
        self.base_path = base_path

        self.timeout = timeout

    def request(
        self,
        method: str,
        endpoint: str,
        request_data: Optional[BaseModel] = None,
        path_params: Optional[Dict[str, str]] = None,
        response_model: Optional[Type[T]] = None,
    ) -> Any:
        path = endpoint.format(**path_params) if path_params else endpoint

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            # "Authorization": f"Bearer { self.access_token }",#we don't use this
            "api-key": self.api_key,
        }

        query_params: Dict[str, Any] = {}
        query_params = {
            key: value for key, value in query_params.items() if value is not None
        }

        with httpx.Client(base_url=self.base_path, timeout=self.timeout) as client:
            if method == self.GET:
                response = client.get(
                    httpx.URL(path), headers=headers, params=query_params
                )
            elif method == self.POST:
                response = client.post(
                    httpx.URL(path),
                    headers=headers,
                    params=query_params,
                    json=request_data.dict() if request_data else None,
                )
            elif method == self.PUT:
                response = client.put(
                    httpx.URL(path),
                    headers=headers,
                    params=query_params,
                    json=request_data.dict() if request_data else None,
                )
            elif method == self.DELETE:
                response = client.delete(
                    httpx.URL(path), headers=headers, params=query_params
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

        # Check if response has a JSON content-type
        content_type = response.headers.get("Content-Type", "")
        is_json_response = "application/json" in content_type

        if 200 <= response.status_code < 300:
            return self.get_return_type(response, response_model, is_json_response)
        else:
            self.handle_and_raise_error(response, is_json_response)

    def get_return_type(
        self,
        response: Response,
        response_model: Optional[Type[T]],
        is_json_response: bool,
    ) -> Any:
        if response_model:
            if not is_json_response:
                raise NotJSONError()

            try:
                json_content = response.json()
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Failed to decode response as JSON. Content: {response.text}"
                ) from exc

            if isinstance(json_content, list):
                return [response_model(**item) for item in json_content]
            else:
                return response_model(**json_content)
        else:
            return response.json() if is_json_response else response.text

    def handle_and_raise_error(
        self, response: Response, is_json_response: bool
    ) -> NoReturn:
        error_message = f"Request failed with status code: {response.status_code}. "
        if is_json_response:
            try:
                error_message += f"Message: {response.json()}"
            except json.JSONDecodeError:
                error_message += f"Content: {response.text}"
        else:
            error_message += f"Content: {response.text}"

        raise httpx.HTTPStatusError(
            error_message, request=response.request, response=response
        )
