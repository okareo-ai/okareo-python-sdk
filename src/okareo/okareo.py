from typing import List, Union

from okareo_api_client.api_config import HTTPException
from okareo_api_client.models import GenerationList, ModelUnderTestSchema
from okareo_api_client.services.None_service import (
    get_generations_v0_generations_get,
    register_model_v0_register_model_post,
)

from .model_under_test import ModelUnderTest


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
    ) -> ModelUnderTest:
        if tags is None:
            tags = []
        data = {
            "name": name,
            "tags": tags,
            "project_id": project_id,
        }
        registered_model = register_model_v0_register_model_post(
            self.api_key, ModelUnderTestSchema.model_validate(data, strict=True)
        )
        return ModelUnderTest(self.api_key, registered_model)
