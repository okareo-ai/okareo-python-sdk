from datetime import datetime
from typing import List, TypedDict, Union

from okareo.okareo_api_client.models.generation_list import GenerationList
from okareo.okareo_api_client.models.http_validation_error import HTTPValidationError

from .common import BASE_URL
from .okareo_api_client import Client
from .okareo_api_client.api.default import get_generations_v0_generations_get


class Generation(TypedDict):
    id: str
    data: datetime


class Okareo:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = Client(base_url=BASE_URL)

    def get_generations(self) -> Union[List[GenerationList], None]:
        data = get_generations_v0_generations_get.sync(
            client=self.client, api_key=self.api_key
        )
        if isinstance(data, HTTPValidationError):
            print(f"Unexpected {data=}, {type(data)=}")
            raise
        return data
