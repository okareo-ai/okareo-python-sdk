from typing import List, Union

from okareo_api_client import Client
from okareo_api_client.api.default import (
    create_scenario_set_v0_scenario_sets_post,
    get_generations_v0_generations_get,
    register_model_v0_register_model_post,
)
from okareo_api_client.models.generation_list import GenerationList
from okareo_api_client.models.http_validation_error import HTTPValidationError
from okareo_api_client.models.model_under_test_schema import ModelUnderTestSchema
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.scenario_set_response import ScenarioSetResponse

from .common import BASE_URL, HTTPX_TIME_OUT
from .model_under_test import ModelUnderTest


class Okareo:
    """A class for interacting with Okareo API"""

    def __init__(
        self, api_key: str, base_path: str = BASE_URL, timeout: float = HTTPX_TIME_OUT
    ):
        self.api_key = api_key
        self.client = Client(base_url=base_path)

    def get_generations(self) -> Union[List[GenerationList], None]:
        """Get a list of generations"""
        data = get_generations_v0_generations_get.sync(
            client=self.client, api_key=self.api_key
        )
        if isinstance(data, HTTPValidationError):
            print(f"Unexpected {data=}, {type(data)=}")
            raise
        return data

    def register_model(
        self,
        name: str,
        tags: Union[List[str], None] = None,
        project_id: Union[str, None] = None,
    ) -> ModelUnderTest:
        if tags is None:
            tags = []
        data = {"name": name, "tags": tags}
        if project_id is not None:
            data["project_id"] = project_id
        json_body = ModelUnderTestSchema.from_dict(data)
        response = register_model_v0_register_model_post.sync(
            client=self.client, api_key=self.api_key, json_body=json_body
        )
        if isinstance(response, HTTPValidationError):
            print(f"Unexpected {response=}, {type(response)=}")
            raise
        if not response:
            print("Empty response from API")
        assert response is not None

        return ModelUnderTest(client=self.client, api_key=self.api_key, mut=response)

    def create_scenario_set(self, json_body: ScenarioSetCreate) -> ScenarioSetResponse:
        response = create_scenario_set_v0_scenario_sets_post.sync(
            client=self.client, api_key=self.api_key, json_body=json_body
        )
        if isinstance(response, HTTPValidationError):
            print(f"Unexpected {response=}, {type(response)=}")
            raise
        if not response:
            print("Empty response from API")
        assert response is not None
        return response
