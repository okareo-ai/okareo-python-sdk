import inspect
import json
from abc import abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from attrs import define as _attrs_define

from okareo.error import MissingApiKeyError, MissingVectorDbError
from okareo_api_client.api.default import (
    add_datapoint_v0_datapoints_post,
    get_scenario_set_data_points_v0_scenario_data_points_scenario_id_get,
    get_test_run_v0_test_runs_test_run_id_get,
    run_test_v0_test_run_post,
)
from okareo_api_client.client import Client
from okareo_api_client.errors import UnexpectedStatus
from okareo_api_client.models import (
    DatapointResponse,
    DatapointSchema,
    ModelUnderTestResponse,
    ScenarioDataPoinResponse,
    TestRunItem,
    TestRunType,
)
from okareo_api_client.models.error_response import ErrorResponse
from okareo_api_client.models.scenario_set_response import ScenarioSetResponse
from okareo_api_client.models.test_run_payload_v2 import TestRunPayloadV2
from okareo_api_client.models.test_run_payload_v2_api_keys import (
    TestRunPayloadV2ApiKeys,
)
from okareo_api_client.models.test_run_payload_v2_metrics_kwargs import (
    TestRunPayloadV2MetricsKwargs,
)
from okareo_api_client.models.test_run_payload_v2_model_results import (
    TestRunPayloadV2ModelResults,
)
from okareo_api_client.types import UNSET, Unset

from .async_utils import AsyncProcessorMixin


class BaseModel:
    type: str
    api_key: Optional[str]

    @abstractmethod
    def params(self) -> dict:
        pass


@_attrs_define
class OpenAIModel(BaseModel):
    type = "openai"
    model_id: str
    temperature: float
    system_prompt_template: str
    user_prompt_template: Optional[str] = None

    def params(self) -> dict:
        return {
            "model_id": self.model_id,
            "temperature": self.temperature,
            "system_prompt_template": self.system_prompt_template,
            "user_prompt_template": self.user_prompt_template,
        }


@_attrs_define
class CohereModel(BaseModel):
    type = "cohere"
    model_id: str
    model_type: str
    input_type: Optional[str] = None

    def params(self) -> dict:
        return {
            "model_id": self.model_id,
            "model_type": self.model_type,
            "input_type": self.input_type,
        }


@_attrs_define
class PineconeDb(BaseModel):
    type = "pinecone"
    index_name: str
    region: str
    project_id: str
    top_k: int = 5

    def params(self) -> dict:
        return {
            "index_name": self.index_name,
            "region": self.region,
            "project_id": self.project_id,
            "top_k": self.top_k,
        }


@_attrs_define
class QdrantDB(BaseModel):
    type = "qdrant"
    collection_name: str
    url: str
    top_k: int = 5
    sparse: bool = False

    def params(self) -> dict:
        return {
            "collection_name": self.collection_name,
            "url": self.url,
            "top_k": self.top_k,
            "sparse": self.sparse,
        }


@_attrs_define
class CustomModel(BaseModel):
    type = "custom"
    name: str

    @abstractmethod
    def invoke(self, input_value: str) -> Any:
        pass

    def params(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "model_invoker": self.invoke,
        }


class ModelUnderTest(AsyncProcessorMixin):
    def __init__(
        self,
        client: Client,
        api_key: str,
        mut: ModelUnderTestResponse,
        models: Optional[Dict[str, Any]] = None,
    ):
        self.client = client
        self.api_key = api_key

        self.mut_id = mut.id
        self.project_id = mut.project_id
        self.name = mut.name
        self.tags = mut.tags
        self.models = models
        self.app_link = mut.app_link
        super().__init__(name="OkareoDatapointsProcessor")

    def get_client(self) -> Client:
        return self.client

    def get_api_key(self) -> str:
        return self.api_key

    def add_data_point(
        self,
        input_obj: Union[dict, str, None] = None,
        result_obj: Union[dict, str, None] = None,
        feedback: Union[float, None] = None,
        context_token: Union[str, None] = None,
        error_message: Union[str, None] = None,
        error_code: Union[str, None] = None,
        input_datetime: Union[str, Unset] = UNSET,
        result_datetime: Union[str, Unset] = UNSET,
        project_id: Union[str, None] = None,
        tags: Union[List[str], None] = None,
        test_run_id: Union[None, str] = None,
    ) -> Union[DatapointResponse, ErrorResponse]:
        body = {
            "tags": tags or [],
            "input": json.dumps(input_obj, default=str),
            "result": json.dumps(result_obj, default=str),
            "context_token": context_token,
            "feedback": feedback,
            "error_message": error_message,
            "error_code": error_code,
            "input_datetime": (
                datetime.now().isoformat()
                if input_datetime == UNSET and input_obj is not None
                else input_datetime
            ),
            "result_datetime": (
                datetime.now().isoformat()
                if result_datetime == UNSET and result_obj is not None
                else result_datetime
            ),
            "project_id": self.project_id,
            "mut_id": self.mut_id,
            "test_run_id": test_run_id,
        }
        response = add_datapoint_v0_datapoints_post.sync(
            client=self.client,
            api_key=self.api_key,
            json_body=DatapointSchema.from_dict(body),
        )
        if not response:
            print("Empty response from API")
        assert response is not None

        return response

    def add_data_point_async(
        self,
        input_obj: Union[dict, str, None] = None,
        result_obj: Union[dict, str, None] = None,
        feedback: Union[float, None] = None,
        context_token: Union[str, None] = None,
        error_message: Union[str, None] = None,
        error_code: Union[str, None] = None,
        input_datetime: Union[str, Unset] = UNSET,
        result_datetime: Union[str, Unset] = UNSET,
        project_id: Union[str, None] = None,
        tags: Union[List[str], None] = None,
        test_run_id: Union[None, str] = None,
    ) -> bool:
        body = {
            "tags": tags or [],
            "input": json.dumps(input_obj, default=str),
            "result": json.dumps(result_obj, default=str),
            "context_token": context_token,
            "feedback": feedback,
            "error_message": error_message,
            "error_code": error_code,
            "input_datetime": (
                datetime.now().isoformat()
                if input_datetime == UNSET and input_obj is not None
                else input_datetime
            ),
            "result_datetime": (
                datetime.now().isoformat()
                if result_datetime == UNSET and result_obj is not None
                else result_datetime
            ),
            "project_id": self.project_id,
            "mut_id": self.mut_id,
            "test_run_id": test_run_id,
        }

        return self.async_call(
            add_datapoint_v0_datapoints_post.sync, DatapointSchema.from_dict(body)
        )

    def _validate_run_test_params(
        self,
        api_key: Optional[str],
        api_keys: Optional[dict],
        test_run_type: TestRunType,
    ) -> dict:
        assert isinstance(self.models, dict)
        model_names = list(self.models.keys())
        run_api_keys = api_keys if api_keys else {model_names[0]: api_key}

        if "custom" not in model_names and len(model_names) != len(run_api_keys):
            raise MissingApiKeyError("Number of models and API keys does not match")

        if test_run_type == TestRunType.INFORMATION_RETRIEVAL:
            if {"pinecone", "qdrant", "custom"}.isdisjoint(model_names):
                raise MissingVectorDbError("No vector database specified")

        return run_api_keys

    def _has_custom_model(self) -> bool:
        assert isinstance(self.models, dict)
        return "custom" in list(self.models.keys())

    def _get_scenario_data_points(
        self, scenario_id: str
    ) -> List[ScenarioDataPoinResponse]:
        scenario_data_points = (
            get_scenario_set_data_points_v0_scenario_data_points_scenario_id_get.sync(
                client=self.client,
                api_key=self.api_key,
                scenario_id=scenario_id,
            )
        )
        scenario_data_points = (
            scenario_data_points if isinstance(scenario_data_points, List) else []
        )
        return scenario_data_points

    def _get_test_run_payload(
        self,
        scenario_id: str,
        name: str,
        api_key: Optional[str],
        api_keys: Optional[dict],
        run_api_keys: dict,
        metrics_kwargs: Optional[dict],
        test_run_type: TestRunType,
        calculate_metrics: bool,
        model_data: dict,
    ) -> TestRunPayloadV2:
        return TestRunPayloadV2(
            mut_id=self.mut_id,
            api_keys=(
                TestRunPayloadV2ApiKeys.from_dict(run_api_keys)
                if api_keys or api_key
                else UNSET
            ),
            scenario_id=scenario_id,
            name=name,
            type=test_run_type,
            project_id=self.project_id,
            calculate_metrics=calculate_metrics,
            metrics_kwargs=TestRunPayloadV2MetricsKwargs.from_dict(
                metrics_kwargs or {}
            ),
            model_results=(
                TestRunPayloadV2ModelResults.from_dict(model_data)
                if self._has_custom_model()
                else UNSET
            ),
        )

    def run_test(
        self,
        scenario: Union[ScenarioSetResponse, str],
        name: str,
        api_key: Optional[str] = None,
        api_keys: Optional[dict] = None,
        metrics_kwargs: Optional[dict] = None,
        test_run_type: TestRunType = TestRunType.MULTI_CLASS_CLASSIFICATION,
        calculate_metrics: bool = False,
    ) -> TestRunItem:
        """Server-based version of test-run execution"""
        try:
            assert isinstance(self.models, dict)
            scenario_id = (
                scenario.scenario_id
                if isinstance(scenario, ScenarioSetResponse)
                else scenario
            )
            run_api_keys = self._validate_run_test_params(
                api_key, api_keys, test_run_type
            )

            model_data: dict = {"model_data": {}}
            if self._has_custom_model():
                scenario_data_points = self._get_scenario_data_points(scenario_id)

                custom_model_invoker = self.models["custom"]["model_invoker"]
                for scenario_data_point in scenario_data_points:
                    assert isinstance(scenario_data_point.input_, str)
                    actual, model_response = custom_model_invoker(
                        scenario_data_point.input_
                    )
                    model_data["model_data"][scenario_data_point.id] = {
                        "actual": actual,
                        "model_response": model_response,
                    }

            response = run_test_v0_test_run_post.sync(
                client=self.client,
                api_key=self.api_key,
                json_body=self._get_test_run_payload(
                    scenario_id,
                    name,
                    api_key,
                    api_keys,
                    run_api_keys,
                    metrics_kwargs,
                    test_run_type,
                    calculate_metrics,
                    model_data,
                ),
            )
        except UnexpectedStatus as e:
            print(f"Unexpected status {e=}, {e.content=}")
            raise

        if isinstance(response, ErrorResponse):
            error_message = f"error: {response}, {response.detail}"
            print(error_message)
            raise
        if not response:
            print("Empty response from API")
        assert response is not None
        return response

    async def run_test_async(
        self,
        scenario: Union[ScenarioSetResponse, str],
        name: str,
        api_key: Optional[str] = None,
        api_keys: Optional[dict] = None,
        metrics_kwargs: Optional[dict] = None,
        test_run_type: TestRunType = TestRunType.MULTI_CLASS_CLASSIFICATION,
        calculate_metrics: bool = False,
    ) -> TestRunItem:
        """Server-based version of test-run execution"""
        try:
            assert isinstance(self.models, dict)
            scenario_id = (
                scenario.scenario_id
                if isinstance(scenario, ScenarioSetResponse)
                else scenario
            )
            run_api_keys = self._validate_run_test_params(
                api_key, api_keys, test_run_type
            )

            model_data: dict = {"model_data": {}}
            if self._has_custom_model():
                scenario_data_points = self._get_scenario_data_points(scenario_id)

                custom_model_invoker = self.models["custom"]["model_invoker"]
                async_custom_model = inspect.iscoroutinefunction(custom_model_invoker)
                for scenario_data_point in scenario_data_points:
                    assert isinstance(scenario_data_point.input_, str)
                    if async_custom_model:
                        # If the method is async, await it
                        actual, model_response = await custom_model_invoker(
                            scenario_data_point.input_
                        )
                    else:
                        # If the method is not async, call it directly
                        actual, model_response = custom_model_invoker(
                            scenario_data_point.input_
                        )
                    model_data["model_data"][scenario_data_point.id] = {
                        "actual": actual,
                        "model_response": model_response,
                    }

            response = run_test_v0_test_run_post.sync(
                client=self.client,
                api_key=self.api_key,
                json_body=self._get_test_run_payload(
                    scenario_id,
                    name,
                    api_key,
                    api_keys,
                    run_api_keys,
                    metrics_kwargs,
                    test_run_type,
                    calculate_metrics,
                    model_data,
                ),
            )
        except UnexpectedStatus as e:
            print(f"Unexpected status {e=}, {e.content=}")
            raise

        if isinstance(response, ErrorResponse):
            error_message = f"error: {response}, {response.detail}"
            print(error_message)
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
            if not isinstance(response, TestRunItem):
                raise
            return response
        except UnexpectedStatus as e:
            print(e.content)
            raise
