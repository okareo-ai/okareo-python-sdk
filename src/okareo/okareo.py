import os
from typing import Any, Dict, List, Union

from okareo_api_client import Client
from okareo_api_client.api.default import (
    create_scenario_set_v0_scenario_sets_post,
    generate_scenario_set_v0_scenario_sets_generate_post,
    get_datapoints_v0_find_datapoints_post,
    get_generations_v0_generations_get,
    get_scenario_set_data_points_v0_scenario_data_points_scenario_id_get,
    register_model_v0_register_model_post,
    scenario_sets_upload_v0_scenario_sets_upload_post,
)
from okareo_api_client.errors import UnexpectedStatus
from okareo_api_client.models.body_scenario_sets_upload_v0_scenario_sets_upload_post import (
    BodyScenarioSetsUploadV0ScenarioSetsUploadPost,
)
from okareo_api_client.models.datapoint_list_item import DatapointListItem
from okareo_api_client.models.datapoint_search import DatapointSearch
from okareo_api_client.models.error_response import ErrorResponse
from okareo_api_client.models.generation_list import GenerationList
from okareo_api_client.models.model_under_test_response import ModelUnderTestResponse
from okareo_api_client.models.model_under_test_schema import ModelUnderTestSchema
from okareo_api_client.models.scenario_data_poin_response import (
    ScenarioDataPoinResponse,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.scenario_set_generate import ScenarioSetGenerate
from okareo_api_client.models.scenario_set_response import ScenarioSetResponse
from okareo_api_client.models.scenario_type import ScenarioType
from okareo_api_client.types import UNSET, File, Unset

from .common import BASE_URL, HTTPX_TIME_OUT
from .model_under_test import BaseModel, ModelUnderTest


class Okareo:
    """A class for interacting with Okareo API"""

    def __init__(
        self, api_key: str, base_path: str = BASE_URL, timeout: float = HTTPX_TIME_OUT
    ):
        self.api_key = api_key
        self.client = Client(
            base_url=base_path, raise_on_unexpected_status=True
        )  # otherwise everything except 201 and 422 is swallowed

    def get_generations(self) -> Union[List[GenerationList], ErrorResponse, None]:
        """Get a list of generations"""
        data = get_generations_v0_generations_get.sync(
            client=self.client, api_key=self.api_key
        )
        return data

    def register_model(
        self,
        name: str,
        tags: Union[List[str], None] = None,
        project_id: Union[str, None] = None,
        model: Union[None, BaseModel, List[BaseModel]] = None,
    ) -> ModelUnderTest:
        if tags is None:
            tags = []
        data: Dict[str, Any] = {"name": name, "tags": tags}
        # will rename name to model in the future api-breaking release
        if isinstance(model, BaseModel) or (
            isinstance(model, list) and all(isinstance(x, BaseModel) for x in model)
        ):
            models = model if isinstance(model, list) else [model]
            data["models"] = {}
            for model in models:
                data["models"][model.type] = model.params()
        if project_id is not None:
            data["project_id"] = project_id
        json_body = ModelUnderTestSchema.from_dict(data)
        response = register_model_v0_register_model_post.sync(
            client=self.client, api_key=self.api_key, json_body=json_body
        )

        self.validate_response(response)
        assert isinstance(response, ModelUnderTestResponse)

        return ModelUnderTest(
            client=self.client,
            api_key=self.api_key,
            mut=response,
            models=data.get("models"),
        )

    def create_scenario_set(
        self, create_request: ScenarioSetCreate
    ) -> ScenarioSetResponse:
        response = create_scenario_set_v0_scenario_sets_post.sync(
            client=self.client, api_key=self.api_key, json_body=create_request
        )

        self.validate_response(response)
        assert isinstance(response, ScenarioSetResponse)

        return response

    def upload_scenario_set(
        self, scenario_name: str, file_path: str, project_id: Union[Unset, str] = UNSET
    ) -> ScenarioSetResponse:
        try:
            file_name = os.path.basename(file_path)

            with open(file_path, "rb") as binary_io:
                multipart_body = BodyScenarioSetsUploadV0ScenarioSetsUploadPost(
                    name=scenario_name,
                    project_id=project_id,
                    file=File(file_name=file_name, payload=binary_io),
                )
                response = scenario_sets_upload_v0_scenario_sets_upload_post.sync(
                    client=self.client,
                    api_key=self.api_key,
                    multipart_data=multipart_body,
                )

            self.validate_response(response)
            assert isinstance(response, ScenarioSetResponse)

            return response
        except UnexpectedStatus as e:
            print(e.content)
            raise

    def generate_scenarios(
        self,
        source_scenario_id: str,
        name: str,
        number_examples: int,
        project_id: Union[Unset, str] = UNSET,
        generation_type: Union[Unset, ScenarioType] = ScenarioType.REPHRASE_INVARIANT,
    ) -> ScenarioSetResponse:
        return self.generate_scenario_set(
            ScenarioSetGenerate(
                source_scenario_id=source_scenario_id,
                name=name,
                number_examples=number_examples,
                project_id=project_id,
                generation_type=generation_type,
            )
        )

    def generate_scenario_set(
        self, create_request: ScenarioSetGenerate
    ) -> ScenarioSetResponse:
        response = generate_scenario_set_v0_scenario_sets_generate_post.sync(
            client=self.client, api_key=self.api_key, json_body=create_request
        )

        self.validate_response(response)
        assert isinstance(response, ScenarioSetResponse)

        return response

    def get_scenario_data_points(
        self, scenario_id: str
    ) -> List[ScenarioDataPoinResponse]:
        response = (
            get_scenario_set_data_points_v0_scenario_data_points_scenario_id_get.sync(
                client=self.client, api_key=self.api_key, scenario_id=scenario_id
            )
        )

        self.validate_response(response)
        assert isinstance(response, List)

        return response

    def validate_response(self, response: Any) -> None:
        if response is None:
            print("Received no response (None) from the API")
            raise ValueError("No response received")

    def find_datapoints(
        self, context_token: str
    ) -> Union[List[DatapointListItem], ErrorResponse]:
        data = get_datapoints_v0_find_datapoints_post.sync(
            client=self.client,
            api_key=self.api_key,
            json_body=DatapointSearch(context_token=context_token),
        )
        if not data:
            return []
        return data
