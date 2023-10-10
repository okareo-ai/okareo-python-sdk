import json
from typing import List, Union

from okareo_api_client.models import (
    DatapointResponse,
    DatapointSchema,
    ModelUnderTestResponse,
)
from okareo_api_client.services.None_service import add_datapoint_v0_datapoints_post


class ModelUnderTest:
    def __init__(self, api_key: str, mut: ModelUnderTestResponse):
        self.api_key = api_key
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
        project_id: Union[int, None] = None,
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
            "input_datetime": input_datetime,
            "result_datetime": result_datetime,
            "project_id": self.project_id,
            "mut_id": self.mut_id,
        }
        return add_datapoint_v0_datapoints_post(
            self.api_key,
            DatapointSchema.model_validate(body, strict=True),
        )
