import json
from datetime import datetime
from typing import List, Union, cast

from okareo_api_client.models import (
    DatapointResponse,
    DatapointSchema,
    ModelUnderTestResponse,
)

from .client import HTTPXHandler


class ModelUnderTest:
    def __init__(self, httpx_handler: HTTPXHandler, mut: ModelUnderTestResponse):
        self.httpx_handler = httpx_handler
        self.mut_id = mut.id
        self.project_id = mut.project_id
        self.name = mut.name
        self.tags = mut.tags

    def add_data_point(
        self,
        input_obj: Union[dict, str],
        result_obj: Union[dict, str],
        feedback: Union[int, None] = None,
        context_token: Union[str, None] = None,
        error_message: Union[str, None] = None,
        error_code: Union[str, None] = None,
        input_datetime: Union[str, None] = None,
        result_datetime: Union[str, None] = None,
        project_id: Union[str, None] = None,
        tags: Union[List[str], None] = None,
    ) -> DatapointResponse:
        body = {
            "tags": tags or [],
            "input": json.dumps(input_obj),
            "result": json.dumps(result_obj),
            "context_token": context_token,
            "feedback": feedback,
            "error_message": error_message,
            "error_code": error_code,
            "input_datetime": input_datetime or datetime.now().isoformat(),
            "result_datetime": result_datetime or datetime.now().isoformat(),
            "project_id": self.project_id,
            "mut_id": self.mut_id,
        }
        request = DatapointSchema.model_validate(body)
        response = self.httpx_handler.request(
            method=HTTPXHandler.POST,
            endpoint="/v0/datapoints",
            request_data=request,
            response_model=DatapointResponse,
        )

        return cast(DatapointResponse, response)
