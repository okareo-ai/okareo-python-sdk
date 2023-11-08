import json
from abc import abstractmethod
from datetime import datetime
from typing import List, Union

from attrs import define as _attrs_define

from okareo_api_client.api.default import (
    add_datapoint_v0_datapoints_post,
    get_test_run_v0_test_runs_test_run_id_get,
    run_test_v0_test_runs_post,
)
from okareo_api_client.client import Client
from okareo_api_client.errors import UnexpectedStatus
from okareo_api_client.models import (
    DatapointResponse,
    DatapointSchema,
    ModelUnderTestResponse,
    TestRunItem,
    TestRunPayload,
    TestRunType,
)
from okareo_api_client.models.http_validation_error import HTTPValidationError
from okareo_api_client.models.scenario_set_response import ScenarioSetResponse


class BaseModel:
    name: str
    type: str

    @abstractmethod
    def params(self) -> dict:
        pass


@_attrs_define
class OpenAIModel(BaseModel):
    name: str
    type = "openai"
    model_id: str
    temperature: float

    def params(self) -> dict:
        return {
            "model_id": self.model_id,
            "temperature": self.temperature,
        }


@_attrs_define
class CohereModel(BaseModel):
    temperature: float


@_attrs_define
class PineconeModel(BaseModel):
    temperature: float


@_attrs_define
class CustomModel(BaseModel):
    url: str


class ModelUnderTest:
    def __init__(self, client: Client, api_key: str, mut: ModelUnderTestResponse):
        self.client = client
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
        project_id: Union[str, None] = None,
        tags: Union[List[str], None] = None,
        test_run_id: Union[None, str] = None,
    ) -> DatapointResponse:
        body = {
            "tags": tags or [],
            "input": json.dumps(input_obj, default=str),
            "result": json.dumps(result_obj, default=str),
            "context_token": context_token,
            "feedback": feedback,
            "error_message": error_message,
            "error_code": error_code,
            "input_datetime": input_datetime or datetime.now().isoformat(),
            "result_datetime": result_datetime or datetime.now().isoformat(),
            "project_id": project_id or self.project_id,
            "mut_id": self.mut_id,
            "test_run_id": test_run_id,
        }
        response = add_datapoint_v0_datapoints_post.sync(
            client=self.client,
            api_key=self.api_key,
            json_body=DatapointSchema.from_dict(body),
        )
        if isinstance(response, HTTPValidationError):
            print(f"Unexpected {response=}, {type(response)=}")
            raise
        if not response:
            print("Empty response from API")
        assert response is not None

        return response

    def run_test(
        self,
        scenario: ScenarioSetResponse,
        name: str,
        api_key: str,
        test_run_type: TestRunType = TestRunType.MULTI_CLASS_CLASSIFICATION,
    ) -> TestRunItem:
        try:
            response = run_test_v0_test_runs_post.sync(
                client=self.client,
                api_key=self.api_key,
                json_body=TestRunPayload(
                    mut_id=self.mut_id,
                    api_key=api_key,
                    scenario_id=scenario.scenario_id,
                    name=name,
                    type=test_run_type,
                    project_id=self.project_id,
                ),
            )
        except UnexpectedStatus as e:
            print(f"Unexpected status {e=}, {e.content=}")
            raise

        if isinstance(response, HTTPValidationError):
            print(f"Unexpected {response=}, {type(response)=}")
            raise
        if not response:
            print("Empty response from API")
        assert response is not None
        return response

    def get_test_run(self, test_run_id: str) -> TestRunItem:
        try:
            response = get_test_run_v0_test_runs_test_run_id_get.sync(
                client=self.client, api_key=self.api_key, test_run_id=test_run_id
            )

            return self.validate_return_type(response)
        except UnexpectedStatus as e:
            print(e.content)
            raise

    def validate_return_type(
        self, response: Union[HTTPValidationError, TestRunItem, None]
    ) -> TestRunItem:
        if isinstance(response, HTTPValidationError):
            error_message = f"error: {response}, {response.detail}"
            print(error_message)
            raise TypeError(error_message)
        if not response:
            raise TypeError("Empty response from Okareo API")
        return response
