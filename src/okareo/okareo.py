import json
from datetime import datetime
from typing import List, TypedDict, Union

from okareo_api_client import Client
from okareo_api_client.api.default import (
    add_datapoint_v0_datapoints_post,
    get_generations_v0_generations_get,
)
from okareo_api_client.models.datapoint_schema import DatapointSchema
from okareo_api_client.models.generation_list import GenerationList
from okareo_api_client.models.http_validation_error import HTTPValidationError

from .common import BASE_URL


class Generation(TypedDict):
    id: str
    data: datetime


class Okareo:
    """A class for interacting with Okareo API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = Client(base_url=BASE_URL)

    def get_generations(self) -> Union[List[GenerationList], None]:
        """Get a list of generations"""
        data = get_generations_v0_generations_get.sync(
            client=self.client, api_key=self.api_key
        )
        if isinstance(data, HTTPValidationError):
            print(f"Unexpected {data=}, {type(data)=}")
            raise
        return data

    def add_data_point(
        self,
        input_: dict | str,
        result: dict | str,
        feedback: int,
        context_token: str,
        error_message: str | None = None,
        error_code: str | None = None,
        input_datetime: datetime | None = None,
        result_datetime: datetime | None = None,
        project_id: int | None = None,
        tags: List[str] | None = None,
    ) -> None:
        body = {
            "tags": tags or [],
            "input": json.dumps(input_),
            "result": json.dumps(result),
            "context_token": context_token,
            "feedback": feedback,
            "error_message": error_message,
            "error_code": error_code,
            "input_datetime": input_datetime,
            "result_datetime": result_datetime,
            "project_id": project_id,
        }
        add_datapoint_v0_datapoints_post.sync(
            client=self.client,
            api_key=self.api_key,
            json_body=DatapointSchema.from_dict(body),
        )
