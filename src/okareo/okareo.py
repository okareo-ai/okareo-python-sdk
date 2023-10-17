from typing import List, Union, cast

from okareo_api_client.models import (
    GenerationList,
    ModelUnderTestResponse,
    ModelUnderTestSchema,
    ScenarioSetCreate,
    ScenarioSetResponse,
)

from .client import HTTPXHandler
from .common import BASE_URL, HTTPX_TIME_OUT
from .model_under_test import ModelUnderTest


class Okareo:
    """A class for interacting with Okareo API"""

    def __init__(
        self, api_key: str, base_path: str = BASE_URL, timeout: float = HTTPX_TIME_OUT
    ):
        self.api_key = api_key
        self.httpx_handler = HTTPXHandler(
            api_key=self.api_key, base_path=base_path, timeout=timeout
        )

    def get_generations(self) -> Union[List[GenerationList], None]:
        """Get a list of generations"""
        response = self.httpx_handler.request(
            method=HTTPXHandler.GET,
            endpoint="/v0/generations",
            response_model=GenerationList,
        )

        return cast(List[GenerationList], response)

    def register_model(
        self,
        name: str,
        tags: Union[List[str], None] = None,
        project_id: Union[int, None] = None,
    ) -> ModelUnderTest:
        if tags is None:
            tags = []
        data = {"name": name, "tags": tags}
        if project_id is not None:
            data["project_id"] = project_id  # type: ignore
        request = ModelUnderTestSchema.model_validate(data)
        registered_model = self.httpx_handler.request(
            method=HTTPXHandler.POST,
            endpoint="/v0/register_model",
            request_data=request,
            response_model=ModelUnderTestResponse,
        )

        return ModelUnderTest(self.httpx_handler, registered_model)

    def create_scenario_set(self, request: ScenarioSetCreate) -> ScenarioSetResponse:
        response = self.httpx_handler.request(
            method=HTTPXHandler.POST,
            endpoint="/v0/scenario_sets",
            request_data=request,
            response_model=ScenarioSetResponse,
        )

        return cast(ScenarioSetResponse, response)
