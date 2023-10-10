import json
from typing import List, Union

from okareo_api_client.api_config import HTTPException
from okareo_api_client.models import (
    DatapointResponse,
    DatapointSchema,
    GenerationList,
    ModelUnderTestResponse,
    ModelUnderTestSchema,
)
from okareo_api_client.services.None_service import (
    add_datapoint_v0_datapoints_post,
    get_generations_v0_generations_get,
    register_model_v0_register_model_post,
)


class Okareo:
    """A class for interacting with Okareo API"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_generations(self) -> Union[List[GenerationList], None]:
        """Get a list of generations"""
        data = get_generations_v0_generations_get(self.api_key)
        if isinstance(data, HTTPException):
            print(f"Unexpected {data=}, {type(data)=}")
            raise
        return data

    def register_model(
        self,
        name: str,
        tags: Union[List[str], None] = None,
        project_id: Union[int, None] = None,
    ) -> ModelUnderTestResponse:
        if tags is None:
            tags = []
        data = {
            "name": name,
            "tags": tags,
            "project_id": project_id,
        }
        return register_model_v0_register_model_post(
            self.api_key, ModelUnderTestSchema.model_validate(data, strict=True)
        )

    def add_data_point(
        self,
        mut_id: int,
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
            "project_id": project_id,
            "mut_id": mut_id,
        }
        return add_datapoint_v0_datapoints_post(
            self.api_key,
            DatapointSchema.model_validate(body, strict=True),
        )
