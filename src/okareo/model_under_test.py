import json
from contextlib import contextmanager
from datetime import datetime
from typing import Iterator, List, Union

from okareo_api_client.models import (
    DatapointResponse,
    DatapointSchema,
    ModelUnderTestResponse,
)
from okareo_api_client.services.None_service import add_datapoint_v0_datapoints_post

from .common import API_CONFIG


class DataPoint:
    def __init__(self) -> None:
        self.result_obj: dict | None = None

    def set_result_obj(self, result_obj: dict) -> None:
        self.result_obj = result_obj


class ModelUnderTest:
    def __init__(self, api_key: str, mut: ModelUnderTestResponse):
        self.api_key = api_key
        self.mut_id = mut.id
        self.project_id = mut.project_id
        self.name = mut.name
        self.tags = mut.tags

    @contextmanager
    def instrument(
        self,
        input_obj: Union[dict, str],
        feedback: Union[int, None] = None,
        context_token: Union[str, None] = None,
        tags: Union[List[str], None] = None,
    ) -> Iterator[DataPoint]:
        data_point = DataPoint()
        yield data_point
        if not data_point.result_obj:
            print(f"result_obj not set, {type(data_point.result_obj)=}")
            raise
        self.add_data_point(
            input_obj, data_point.result_obj, feedback, context_token, tags=tags
        )

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
            "input_datetime": input_datetime or datetime.now().isoformat(),
            "result_datetime": result_datetime or datetime.now().isoformat(),
            "project_id": self.project_id,
            "mut_id": self.mut_id,
        }
        return add_datapoint_v0_datapoints_post(
            self.api_key,
            DatapointSchema.model_validate(body, strict=True),
            api_config_override=API_CONFIG,
        )
