import json
from abc import abstractmethod
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from attrs import define as _attrs_define

from okareo.error import MissingApiKeyError, MissingVectorDbError
from okareo_api_client.api.default import (
    add_datapoint_v0_datapoints_post,
    add_test_data_point_v0_test_data_point_post,
    add_test_run_v0_test_runs_post,
    get_scenario_set_data_points_v0_scenario_data_points_scenario_id_get,
    get_test_run_v0_test_runs_test_run_id_get,
    run_test_v0_test_run_post,
    update_test_run_v0_test_runs_test_run_id_put,
)
from okareo_api_client.client import Client
from okareo_api_client.errors import UnexpectedStatus
from okareo_api_client.models import (
    DatapointResponse,
    DatapointSchema,
    ModelUnderTestResponse,
    TestDataPointPayload,
    TestRunItem,
    TestRunPayload,
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

    def params(self) -> dict:
        return {
            "model_id": self.model_id,
            "temperature": self.temperature,
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
class CustomModel(BaseModel):
    url: str


class ModelUnderTest:
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

    def add_data_point(
        self,
        input_obj: Union[dict, str, None] = None,
        result_obj: Union[dict, str, None] = None,
        feedback: Union[int, None] = None,
        context_token: Union[str, None] = None,
        error_message: Union[str, None] = None,
        error_code: Union[str, None] = None,
        input_datetime: Union[str, None] = None,
        result_datetime: Union[str, None] = None,
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
            "input_datetime": input_datetime or datetime.now().isoformat(),
            "result_datetime": result_datetime or datetime.now().isoformat(),
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

    # TODO this is moving to the server
    def run_test(
        self,
        scenario_id: str,
        model_invoker: Callable[[str], Tuple[Any, Any]],
        test_run_name: str = "",
        test_run_type: TestRunType = TestRunType.MULTI_CLASS_CLASSIFICATION,
    ) -> TestRunItem:
        try:
            scenario_data_points = get_scenario_set_data_points_v0_scenario_data_points_scenario_id_get.sync(
                client=self.client, api_key=self.api_key, scenario_id=scenario_id
            )

            test_run_payload = TestRunPayload(
                mut_id=self.mut_id,
                scenario_set_id=scenario_id,
                name=test_run_name,
                type=test_run_type,
                start_time=datetime.now(),
                end_time=datetime.now(),  # TODO getting around server error, it's updated later
            )

            test_run_item = add_test_run_v0_test_runs_post.sync(
                client=self.client, api_key=self.api_key, json_body=test_run_payload
            )
            test_run_item = self.validate_return_type(test_run_item)

            if isinstance(scenario_data_points, list):
                for scenario_data_point in scenario_data_points:
                    input_datetime = str(datetime.now())

                    actual, model_response = model_invoker(scenario_data_point.input_)

                    self.add_data_point(
                        input_obj=scenario_data_point.input_,  # todo get full request from inovker
                        input_datetime=input_datetime,  # start of model invocation
                        result_obj=model_response,  # json.dumps() the result objects from the model
                        # end of model invocation
                        result_datetime=str(datetime.now()),
                        test_run_id=test_run_item.id,
                    )  # todo need to store test_run_id in datapoint

                    test_data_point_payload = TestDataPointPayload(
                        test_run_id=test_run_item.id,
                        scenario_data_point_id=scenario_data_point.id,
                        metric_type=test_run_type.value,  # same as test_run_item.type for now
                        metric_value=self.get_metric_value_by_run_type(
                            test_run_type, scenario_data_point.result, actual
                        ),
                    )

                    add_test_data_point_v0_test_data_point_post.sync(
                        client=self.client,
                        api_key=self.api_key,
                        json_body=test_data_point_payload,
                    )

            # update completed test run with end time and test data point count

            test_run_payload.end_time = datetime.now()
            test_run_payload.calculate_model_metrics = (
                True  # trigger server side calculation
            )
            # test_run_payload.test_data_point_count = len(response) #todo
            test_run_item = update_test_run_v0_test_runs_test_run_id_put.sync(
                client=self.client,
                api_key=self.api_key,
                test_run_id=test_run_item.id,
                json_body=test_run_payload,
            )
            return self.validate_return_type(test_run_item)

        except UnexpectedStatus as e:
            print(e.content)
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    def run_test_v2(
        self,
        scenario: ScenarioSetResponse,
        name: str,
        api_key: Optional[str] = None,
        api_keys: Optional[dict] = None,
        metrics_kwargs: Optional[dict] = None,
        test_run_type: TestRunType = TestRunType.MULTI_CLASS_CLASSIFICATION,
        calculate_metrics: bool = False,
    ) -> TestRunItem:
        """Server-based version of test-run execution"""
        assert isinstance(self.models, dict)
        model_names = list(self.models.keys())
        run_api_keys = api_keys if api_keys else {model_names[0]: api_key}

        if len(model_names) != len(run_api_keys):
            raise MissingApiKeyError("Number of models and API keys does not match")

        if test_run_type == TestRunType.INFORMATION_RETRIEVAL:
            if "pinecone" not in model_names:
                raise MissingVectorDbError("No vector database specified")

        try:
            response = run_test_v0_test_run_post.sync(
                client=self.client,
                api_key=self.api_key,
                json_body=TestRunPayloadV2(
                    mut_id=self.mut_id,
                    api_keys=TestRunPayloadV2ApiKeys.from_dict(run_api_keys),
                    scenario_id=scenario.scenario_id,
                    name=name,
                    type=test_run_type,
                    project_id=self.project_id,
                    calculate_metrics=calculate_metrics,
                    metrics_kwargs=TestRunPayloadV2MetricsKwargs.from_dict(
                        metrics_kwargs or {}
                    ),
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

    def get_metric_value_by_run_type(
        self, test_run_type: TestRunType, result: Any, actual: str
    ) -> str:
        if test_run_type == TestRunType.MULTI_CLASS_CLASSIFICATION:
            if not isinstance(result, str):
                raise TypeError(
                    f"Expected result to be a string, but got {type(result)}"
                )
            metric_value = json.dumps({"expected": result, "actual": actual})
        elif test_run_type == TestRunType.INFORMATION_RETRIEVAL:
            metric_value = json.dumps({"retrieved_ids_with_scores": actual})
        else:
            raise ValueError(f"Unsupported test run type: {test_run_type}")

        return metric_value

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
        self, response: Union[ErrorResponse, TestRunItem, None]
    ) -> TestRunItem:
        if isinstance(response, ErrorResponse):
            error_message = f"error: {response}, {response.detail}"
            print(error_message)
            raise TypeError(error_message)
        if not response:
            raise TypeError("Empty response from Okareo API")
        return response
