import asyncio
import json
import ssl
import threading
from abc import abstractmethod
from base64 import b64encode
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import nats  # type: ignore
from attrs import define as _attrs_define
from nkeys import from_seed  # type: ignore

from okareo.error import MissingApiKeyError, MissingVectorDbError
from okareo_api_client.api.default import (
    add_datapoint_v0_datapoints_post,
    get_scenario_set_data_points_v0_scenario_data_points_scenario_id_get,
    get_test_run_v0_test_runs_test_run_id_get,
    internal_custom_model_listener_v0_internal_custom_model_listener_get,
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
from okareo_api_client.models.scenario_data_poin_response_input_type_0 import (
    ScenarioDataPoinResponseInputType0,
)
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
class ModelInvocation:
    """Model invocation response object returned from a CustomModel.invoke method"""

    """or as an element of a list returned from a CustomBatchModel.invoke_batch method"""

    model_prediction: Union[dict, list, str, None] = None
    """Prediction from the model to be used when running the evaluation,
    e.g. predicted class from classification model or generated text completion from
    a generative model. This would typically be parsed out of the overall model_output_metadata."""

    model_input: Union[dict, list, str, None] = None
    """All the input sent to the model"""

    model_output_metadata: Union[dict, list, str, None] = None
    """Full model response, including any metadata returned with model's output"""

    tool_calls: Optional[List] = None
    """List of tool calls made during the model invocation, if any"""

    def params(self) -> dict:
        return {
            "actual": self.model_prediction,
            "model_input": self.model_input,
            "model_result": self.model_output_metadata,
            "tool_calls": self.tool_calls,
        }


@_attrs_define
class OpenAIModel(BaseModel):
    type = "openai"
    model_id: str
    temperature: float
    system_prompt_template: Optional[str] = None
    user_prompt_template: Optional[str] = None
    dialog_template: Optional[str] = None
    tools: Optional[List] = None

    def params(self) -> dict:
        return {
            "model_id": self.model_id,
            "temperature": self.temperature,
            "system_prompt_template": self.system_prompt_template,
            "user_prompt_template": self.user_prompt_template,
            "dialog_template": self.dialog_template,
            "type": self.type,
            "tools": self.tools,
        }


@_attrs_define
class GenerationModel(BaseModel):
    type = "generation"
    model_id: str
    temperature: float
    system_prompt_template: Optional[str] = None
    user_prompt_template: Optional[str] = None
    dialog_template: Optional[str] = None
    tools: Optional[List] = None

    def params(self) -> dict:
        return {
            "model_id": self.model_id,
            "temperature": self.temperature,
            "system_prompt_template": self.system_prompt_template,
            "user_prompt_template": self.user_prompt_template,
            "dialog_template": self.dialog_template,
            "type": self.type,
            "tools": self.tools,
        }


@_attrs_define
class OpenAIAssistantModel(BaseModel):
    type = "openai_assistant"
    model_id: str
    assistant_prompt_template: Optional[str] = None
    user_prompt_template: Optional[str] = None
    dialog_template: Optional[str] = None

    def params(self) -> dict:
        return {
            "model_id": self.model_id,
            "assistant_prompt_template": self.assistant_prompt_template,
            "user_prompt_template": self.user_prompt_template,
            "dialog_template": self.dialog_template,
            "type": self.type,
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
    def invoke(
        self, input_value: Union[dict, list, str]
    ) -> Union[ModelInvocation, Any]:
        """method for taking a single scenario input and returning a single model output
        input_value: Union[dict, list, str] - input to the model.
        """

    def params(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "model_invoker": self.invoke,
        }


@_attrs_define
class CustomMultiturnTarget(BaseModel):
    type = "custom_target"
    name: str

    @abstractmethod
    def invoke(self, messages: List[dict[str, str]]) -> Union[ModelInvocation, Any]:
        """method for continueing a multiturn conversation with a custom model
        messages: list - list of messages in the conversation
        """

    def params(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "model_invoker": self.invoke,
        }


@_attrs_define
class StopConfig:
    check_name: str
    stop_on: bool

    def params(self) -> dict:
        return {"check_name": self.check_name, "stop_on": self.stop_on}


@_attrs_define
class MultiTurnDriver(BaseModel):
    type = "driver"
    target: Union[OpenAIModel, CustomMultiturnTarget, GenerationModel]
    stop_check: Union[StopConfig, dict]
    driver_temperature: Optional[float] = 0.8
    repeats: Optional[int] = 1
    max_turns: Optional[int] = 5
    first_turn: Optional[str] = "target"

    def __attrs_post_init__(self) -> None:
        if isinstance(self.stop_check, dict):
            self.stop_check = StopConfig(**self.stop_check)

    def params(self) -> dict:
        return {
            "type": self.type,
            "target": self.target.params(),
            "driver_temperature": self.driver_temperature,
            "repeats": self.repeats,
            "max_turns": self.max_turns,
            "first_turn": self.first_turn,
            "stop_check": (
                self.stop_check.params()
                if isinstance(self.stop_check, StopConfig)
                else self.stop_check
            ),
        }


@_attrs_define
class CustomBatchModel(BaseModel):
    type = "custom_batch"
    name: str
    batch_size: int = 1

    @abstractmethod
    def invoke_batch(
        self, input_batch: list[dict[str, Union[dict, list, str]]]
    ) -> list[dict[str, Union[ModelInvocation, Any]]]:
        """method for taking a batch of scenario inputs and returning a corresponding batch of model outputs

        arguments:
        -> input_batch: list[dict[str, Union[dict, list, str]]] - batch of inputs to the model. Expects a list of
        dicts of the format { 'id': str, 'input_value': Union[dict, list, str] }.

        returns:
        -> list of dicts of format { 'id': str, 'model_invocation': Union[ModelInvocation, Any] }. 'id' must match
        the corresponding input_batch element's 'id'.
        """

    def params(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "batch_size": self.batch_size,
            "model_invoker": self.invoke_batch,
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
        group_id: Union[None, str] = None,
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
            "group_id": group_id,
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
        group_id: Union[None, str] = None,
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
            "group_id": group_id,
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

        if ("custom" not in model_names) and len(model_names) != len(run_api_keys):
            raise MissingApiKeyError("Number of models and API keys does not match")

        if test_run_type == TestRunType.INFORMATION_RETRIEVAL:
            if {"pinecone", "qdrant", "custom"}.isdisjoint(model_names):
                raise MissingVectorDbError("No vector database specified")

        return run_api_keys

    def _has_custom_model(self) -> bool:
        assert isinstance(self.models, dict)
        if (
            "driver" in self.models
            and self.models["driver"]["target"]["type"] == "custom_target"
        ):
            return True
        custom_model_strs = ["custom", "custom_batch"]
        assert isinstance(self.models, dict)
        return any(
            model_str in list(self.models.keys()) for model_str in custom_model_strs
        )

    def _has_custom_batch_model(self) -> bool:
        assert isinstance(self.models, dict)
        return "custom_batch" in list(self.models.keys())

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

    def _add_model_invocation_for_scenario(
        self,
        custom_model_return_value: Any,
        model_data: dict,
        scenario_data_point_id: str,
    ) -> None:
        if isinstance(custom_model_return_value, ModelInvocation):
            model_prediction = custom_model_return_value.model_prediction
            model_output_metadata = custom_model_return_value.model_output_metadata
            model_input = custom_model_return_value.model_input
        else:  # assume the preexisting behavior of returning a tuple
            model_prediction, model_output_metadata = custom_model_return_value
            model_input = None

        model_data["model_data"][scenario_data_point_id] = {
            "actual": model_prediction,
            "model_response": model_output_metadata,
            "model_input": model_input,
        }

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
        checks: Optional[List[str]],
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
            calculate_metrics=calculate_metrics,
            metrics_kwargs=TestRunPayloadV2MetricsKwargs.from_dict(
                metrics_kwargs or {}
            ),
            model_results=(
                TestRunPayloadV2ModelResults.from_dict(model_data)
                if self._has_custom_model()
                else UNSET
            ),
            checks=checks if checks else UNSET,
        )

    def _extract_input_from_scenario_data_point(
        self, scenario_data_point: ScenarioDataPoinResponse
    ) -> Union[dict, list, str]:
        """helper method to handle different scenario data point formats"""
        scenario_input: Union[dict, list, str] = (
            scenario_data_point.input_.to_dict()
            if isinstance(
                scenario_data_point.input_,
                ScenarioDataPoinResponseInputType0,
            )
            else scenario_data_point.input_
        )
        return scenario_input

    async def connect_nats(self, user_jwt: str, seed: str) -> Any:
        nkey = from_seed(seed.encode())

        def user_jwt_cb() -> Any:
            return user_jwt.encode()

        def user_sign_cb(nonce: str) -> Any:
            sig = nkey.sign(nonce.encode())
            return b64encode(sig)

        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = True
        ssl_ctx.verify_mode = ssl.CERT_REQUIRED
        ngs_url = "wss://connect.ngs.global:443"
        nc = await nats.connect(
            servers=[ngs_url],
            user_jwt_cb=user_jwt_cb,
            signature_cb=user_sign_cb,
            tls=ssl_ctx,
            connect_timeout=30,
            allow_reconnect=True,
            max_reconnect_attempts=5,
            reconnect_time_wait=1,
        )
        return nc

    def call_custom_invoker(self, args: Any) -> Any:
        assert isinstance(self.models, dict)
        if self.models.get("custom"):
            return self.models["custom"]["model_invoker"](args)
        elif self.models.get("custom_batch"):
            return self.models["custom_batch"]["model_invoker"](args)
        else:
            return self.models["driver"]["target"]["model_invoker"](args)

    def get_params_from_custom_result(self, result: Any) -> Any:
        if isinstance(result, ModelInvocation):
            result = result.params()
        if (
            isinstance(result, list)
            and len(result) > 0
            and result[0].get("model_invocation")
        ):
            result = [r["model_invocation"].params() for r in result]
        return result

    async def _internal_run_custom_model_listener(
        self, stop_event: Any, nats_jwt: str, seed: str
    ) -> None:
        nats_connection = await self.connect_nats(nats_jwt, seed)
        try:

            async def message_handler_custom_model(msg: Any) -> None:
                try:
                    data = json.loads(msg.data.decode())
                    if data.get("close"):
                        await nats_connection.publish(
                            msg.reply, json.dumps({"status": "disconnected"}).encode()
                        )
                        stop_event.set()
                        return
                    args = data.get("args", [])
                    result = self.call_custom_invoker(args)
                    json_encodable_result = self.get_params_from_custom_result(result)
                    await nats_connection.publish(
                        msg.reply, json.dumps(json_encodable_result).encode()
                    )
                except Exception as e:
                    error_msg = f"An error occurred in the custom model invocation. {type(e).__name__}: {str(e)}"
                    print(error_msg)
                    await nats_connection.publish(
                        msg.reply, json.dumps({"error": error_msg}).encode()
                    )

            await nats_connection.subscribe(
                f"invoke.{self.mut_id}", cb=message_handler_custom_model
            )
            while not stop_event.is_set():
                await asyncio.sleep(0.1)
        except Exception as e:
            print(f"An error occurred in the custom model invocation: {str(e)}")
        finally:
            await nats_connection.close()

    def _internal_run_custom_model_thread(self, coro: Any) -> Any:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

    def _internal_start_custom_model_thread(self, nats_jwt: str, seed: str) -> tuple:
        custom_model_thread_stop_event = threading.Event()
        custom_model_thread = threading.Thread(
            target=self._internal_run_custom_model_thread,
            args=(
                self._internal_run_custom_model_listener(
                    custom_model_thread_stop_event, nats_jwt, seed
                ),
            ),
        )
        return custom_model_thread, custom_model_thread_stop_event

    def _internal_cleanup_custom_model(
        self,
        custom_model_thread_stop_event: threading.Event,
        custom_model_thread: threading.Thread,
    ) -> None:
        if custom_model_thread_stop_event:
            custom_model_thread_stop_event.set()  # Signal the thread to stop

        if custom_model_thread:
            custom_model_thread.join(timeout=5)

    def run_test(
        self,
        scenario: Union[ScenarioSetResponse, str],
        name: str,
        api_key: Optional[str] = None,
        api_keys: Optional[dict] = None,
        metrics_kwargs: Optional[dict] = None,
        test_run_type: TestRunType = TestRunType.MULTI_CLASS_CLASSIFICATION,
        calculate_metrics: bool = True,
        checks: Optional[List[str]] = None,
    ) -> TestRunItem:
        """Server-based version of test-run execution"""
        self.custom_model_thread: Any = None
        self.custom_model_thread_stop_event: Any = None

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
                creds = internal_custom_model_listener_v0_internal_custom_model_listener_get.sync(
                    client=self.client, api_key=self.api_key, mut_id=self.mut_id
                )
                assert isinstance(creds, dict)
                nats_jwt = creds["jwt"]
                seed = creds["seed"]
                self.custom_model_thread, self.custom_model_thread_stop_event = (
                    self._internal_start_custom_model_thread(nats_jwt, seed)
                )
                self.custom_model_thread.start()

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
                    checks,
                ),
            )
            if isinstance(response, ErrorResponse):
                error_message = f"error: {response}, {response.detail}"
                print(error_message)
                raise
            if not response:
                print("Empty response from API")
            assert response is not None
            return response
        except UnexpectedStatus as e:
            print(f"Unexpected status {e=}, {e.content=}")
            raise
        finally:
            self._internal_cleanup_custom_model(
                self.custom_model_thread_stop_event, self.custom_model_thread
            )

    def get_test_run(self, test_run_id: str) -> TestRunItem:
        try:
            response = get_test_run_v0_test_runs_test_run_id_get.sync(
                client=self.client, api_key=self.api_key, test_run_id=test_run_id
            )
            self.validate_response(response)
            assert isinstance(response, TestRunItem)

            return response
        except UnexpectedStatus as e:
            print(e.content)
            raise

    def validate_response(self, response: Any) -> None:
        if isinstance(response, ErrorResponse):
            error_message = f"error: {response}, {response.detail}"
            print(error_message)
            raise TypeError(error_message)
        if response is None:
            print("Received no response (None) from the API")
            raise ValueError("No response received")
