import asyncio
import inspect
import json
import logging
import ssl
import threading
import urllib
from abc import abstractmethod
from base64 import b64encode
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import aiohttp
from attrs import define
from attrs import define as _attrs_define
from attrs import field
from nkeys import from_seed  # type: ignore
from tqdm import tqdm  # type: ignore

from okareo.error import MissingApiKeyError, MissingVectorDbError, TestRunError
from okareo_api_client.api.default import (
    add_datapoint_v0_datapoints_post,
    get_scenario_set_data_points_v0_scenario_data_points_scenario_id_get,
    get_test_run_v0_test_runs_test_run_id_get,
    internal_custom_model_listener_v0_internal_custom_model_listener_get,
    run_test_v0_test_run_post,
    submit_test_v0_test_run_submit_post,
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

## BEGIN Monkey Patch for nats to use proxy env vars (via aiohttp)
#  Apply monkey patch at module level to allow aiohttp client session to pull proxy env vars
_original_client_session = aiohttp.ClientSession


# Create a wrapper class that inherits from the original ClientSession
class PatchedClientSession(_original_client_session):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        logging.debug("Applying proxy patch to aiohttp")
        logging.debug("Proxy env vars: %s", urllib.request.getproxies())
        kwargs["trust_env"] = True
        super().__init__(*args, **kwargs)


# Replace the original ClientSession with our patched version
aiohttp.ClientSession = PatchedClientSession  # type: ignore
# We import nats only after patching aiohttp to respect the proxy env vars
import nats  # type: ignore # noqa: E402

## END Monkey Patch for nats to use proxy env vars (via aiohttp)


class BaseModel:
    type: str
    api_key: Optional[str]

    @abstractmethod
    def params(self) -> dict:
        pass


class ModelUnderTest(AsyncProcessorMixin):
    """A class for managing a Model Under Test (MUT) in Okareo.
    Returned by [okareo.register_model()](/docs/reference/python-sdk/okareo#register_model)
    """

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

        if (
            "custom" not in model_names  # custom is a model without a key
            and "driver"
            not in model_names  # driver can have 2 keys for driver and target
            and len(model_names) != len(run_api_keys)
        ):
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
            tool_calls = custom_model_return_value.tool_calls
        else:  # assume the preexisting behavior of returning a tuple
            model_prediction, model_output_metadata = custom_model_return_value
            model_input = None
            tool_calls = None

        model_data["model_data"][scenario_data_point_id] = {
            "actual": model_prediction,
            "model_response": model_output_metadata,
            "model_input": model_input,
            "tool_calls": tool_calls,
        }

    def _get_test_run_payload(
        self,
        scenario_id: Any,
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

    async def connect_nats(self, user_jwt: str, seed: str, local_nats: str) -> Any:
        nc = None
        if local_nats != "":
            nc = await nats.connect(
                # Use the hostname 'nats' which is the service name in docker-compose
                servers=[local_nats],
                connect_timeout=120,
                allow_reconnect=True,
                max_reconnect_attempts=10,
                reconnect_time_wait=10,
            )
        else:
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

    def call_custom_invoker(
        self,
        args: Any,
        message_history: Optional[list[dict[str, str]]] = None,
        scenario_input: Optional[Union[str, dict, list]] = None,
    ) -> Any:
        assert isinstance(self.models, dict)
        if self.models.get("custom"):
            return self.models["custom"]["model_invoker"](args)
        elif self.models.get("custom_batch"):
            return self.models["custom_batch"]["model_invoker"](args)
        else:
            messages = message_history if message_history is not None else args
            invoker = self.models["driver"]["target"]["model_invoker"]
            sig = inspect.signature(invoker)
            num_positional = sum(
                1
                for param in sig.parameters.values()
                if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD)
            )
            if num_positional > 1 and scenario_input is not None:
                # new impl; first pos arg is message_history, second is scenario_input
                return invoker(messages, scenario_input)
            else:
                # legacy impl; first pos arg is message_history (named args)
                return invoker(args)

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
        self, stop_event: Any, nats_jwt: str, seed: str, local_nats: str
    ) -> None:
        nats_connection = await self.connect_nats(nats_jwt, seed, local_nats)
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
                    message_history = data.get("message_history", [])
                    scenario_input = data.get("scenario_input", None)
                    result = self.call_custom_invoker(
                        args, message_history, scenario_input
                    )
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

    def _internal_start_custom_model_thread(
        self, nats_jwt: str, seed: str, local_nats: str
    ) -> tuple:
        custom_model_thread_stop_event = threading.Event()
        custom_model_thread = threading.Thread(
            target=self._internal_run_custom_model_thread,
            args=(
                self._internal_run_custom_model_listener(
                    custom_model_thread_stop_event, nats_jwt, seed, local_nats
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

    def _run_test_internal(
        self,
        scenario: Union[ScenarioSetResponse, str],
        name: str,
        api_key: Optional[str] = None,
        api_keys: Optional[dict] = None,
        metrics_kwargs: Optional[dict] = None,
        test_run_type: TestRunType = TestRunType.MULTI_CLASS_CLASSIFICATION,
        calculate_metrics: bool = True,
        checks: Optional[List[str]] = None,
        run_test_method: Any = None,
    ) -> TestRunItem:
        """Internal method to run a test. This method is used by both run_test and submit_test."""
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
            if self._has_custom_model() and "driver" in self.models:
                creds = internal_custom_model_listener_v0_internal_custom_model_listener_get.sync(
                    client=self.client, api_key=self.api_key, mut_id=self.mut_id
                )
                assert isinstance(creds, dict)
                nats_jwt = creds["jwt"]
                seed = creds["seed"]
                local_nats = creds["local_nats"]
                (
                    self.custom_model_thread,
                    self.custom_model_thread_stop_event,
                ) = self._internal_start_custom_model_thread(nats_jwt, seed, local_nats)
                self.custom_model_thread.start()
            elif self._has_custom_model():
                self._custom_exec(scenario_id, model_data)

            response: TestRunItem = run_test_method(
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
                raise TestRunError(str(response.detail))
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

    def _check_multiturn_submit_safe(self, test_run_type: TestRunType) -> bool:
        """Check if the test_run_type is MULTI_TURN and if the model is a CustomMultiturnTarget.
        If so, return False to indicate that submit_test should not be used."""
        if (
            test_run_type == TestRunType.MULTI_TURN
            and self.models is not None
            and isinstance(self.models, dict)
            and "driver" in self.models
            and "target" in self.models["driver"]
            and "type" in self.models["driver"]["target"]
            and self.models["driver"]["target"]["type"] == "custom_target"
        ):
            return False
        return True

    def submit_test(
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
        """Asynchronous server-based version of test-run execution. For CustomModels, model
        invocations are handled client-side then evaluated server-side asynchronously. For other models,
        model invocations and evaluations handled server-side asynchronously.

        Arguments:
            scenario (Union[ScenarioSetResponse, str]): The scenario set or identifier to use for the test run.
            name (str): The name to assign to the test run.
            api_key (Optional[str]): Optional API key for authentication.
            api_keys (Optional[dict]): Optional dictionary of API keys for different services.
            metrics_kwargs (Optional[dict]): Optional dictionary of keyword arguments for metrics calculation.
            test_run_type (TestRunType): The type of test run to execute. Defaults to MULTI_CLASS_CLASSIFICATION.
            calculate_metrics (bool): Whether to calculate metrics after the test run. Defaults to True.
            checks (Optional[List[str]]): Optional list of checks to perform during the test run.

        Returns:
            TestRunItem: The resulting test run item for the submitted test run. The `id` field can be used to retrieve the test run.
        """
        endpoint = submit_test_v0_test_run_submit_post.sync
        if not self._check_multiturn_submit_safe(test_run_type):
            print(
                "WARNING: CustomMultiturnTarget models are not supported in submit_test. "
                + "Falling back to run_test instead."
            )
            endpoint = run_test_v0_test_run_post.sync
        return self._run_test_internal(
            scenario,
            name,
            api_key,
            api_keys,
            metrics_kwargs,
            test_run_type,
            calculate_metrics,
            checks,
            endpoint,
        )

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
        """Server-based version of test-run execution. For CustomModels, model
        invocations are handled client-side then evaluated server-side. For other models,
        model invocations and evaluations handled server-side.

        Arguments:
            scenario (Union[ScenarioSetResponse, str]): The scenario set or identifier to use for the test run.
            name (str): The name to assign to the test run.
            api_key (Optional[str]): Optional API key for authentication.
            api_keys (Optional[dict]): Optional dictionary of API keys for different services.
            metrics_kwargs (Optional[dict]): Optional dictionary of keyword arguments for metrics calculation.
            test_run_type (TestRunType): The type of test run to execute. Defaults to MULTI_CLASS_CLASSIFICATION.
            calculate_metrics (bool): Whether to calculate metrics after the test run. Defaults to True.
            checks (Optional[List[str]]): Optional list of checks to perform during the test run.

        Returns:
            TestRunItem: The resulting test run item for the completed test run.
        """
        try:
            return self._run_test_internal(
                scenario,
                name,
                api_key,
                api_keys,
                metrics_kwargs,
                test_run_type,
                calculate_metrics,
                checks,
                run_test_v0_test_run_post.sync,
            )
        except Exception as e:
            raise TestRunError(str(e)) from e

    def get_test_run(self, test_run_id: str) -> TestRunItem:
        """Retrieve a test run by its ID.

        Arguments:
            test_run_id (str): The ID of the test run to retrieve.

        Returns:
            TestRunItem: The test run item corresponding to the provided ID.
        """
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

    def _extract_input_from_scenario_data_point(
        self, scenario_data_point: ScenarioDataPoinResponse
    ) -> Any:
        """helper method to handle different scenario data point formats"""
        scenario_input = scenario_data_point.input_
        return scenario_input

    def _custom_exec(self, scenario_id: Any, model_data: Any) -> Any:
        assert isinstance(self.models, dict)

        assert scenario_id
        scenario_data_points = self._get_scenario_data_points(scenario_id)
        datapoint_len = len(scenario_data_points)

        if not self._has_custom_batch_model():
            custom_model_invoker = self.models["custom"]["model_invoker"]
            for scenario_data_point in tqdm(
                scenario_data_points, desc="Invoking CustomModel", unit="datapoint"
            ):
                scenario_input = self._extract_input_from_scenario_data_point(
                    scenario_data_point
                )

                custom_model_return_value = custom_model_invoker(scenario_input)
                self._add_model_invocation_for_scenario(
                    custom_model_return_value,
                    model_data,
                    scenario_data_point.id,
                )
        else:
            # batch inputs to the custom model
            custom_model_invoker = self.models["custom_batch"]["model_invoker"]
            batch_size = self.models["custom_batch"]["batch_size"]
            for index in tqdm(
                range(0, datapoint_len, batch_size),
                desc="Invoking CustomModel",
                unit="batch",
            ):
                end_index = min(index + batch_size, datapoint_len)
                scenario_data_points_batch = scenario_data_points[index:end_index]
                scenario_inputs = [
                    {
                        "id": sdp.id,
                        "input_value": self._extract_input_from_scenario_data_point(
                            sdp
                        ),
                    }
                    for sdp in scenario_data_points_batch
                ]
                custom_model_return_batch = custom_model_invoker(scenario_inputs)

                for return_dict in custom_model_return_batch:
                    self._add_model_invocation_for_scenario(
                        return_dict["model_invocation"],
                        model_data,
                        return_dict["id"],
                    )


@_attrs_define
class ModelInvocation:
    """
    Model invocation response object returned from a CustomModel.invoke method
    or as an element of a list returned from a CustomBatchModel.invoke_batch method.

    Arguments:
        model_prediction: Prediction from the model to be used when running the evaluation,
            e.g. predicted class from classification model or generated text completion from
            a generative model. This would typically be parsed out of the overall model_output_metadata.
        model_input: All the input sent to the model.
        model_output_metadata: Full model response, including any metadata returned with model's output.
        tool_calls: List of tool calls made during the model invocation, if any.
    """

    model_prediction: Union[dict, list, str, None] = None
    model_input: Union[dict, list, str, None] = None
    model_output_metadata: Union[dict, list, str, None] = None
    tool_calls: Optional[List] = None

    def params(self) -> dict:
        return {
            "actual": self.model_prediction,
            "model_input": self.model_input,
            "model_result": self.model_output_metadata,
            "tool_calls": self.tool_calls,
        }


@define
class OpenAIModel(BaseModel):
    """
    An OpenAI model definition with prompt template and relevant parameters for an Okareo evaluation.

    Arguments:
        model_id: Model ID to request from OpenAI completion.
            For list of available models, see https://platform.openai.com/docs/models
        temperature: Parameter for controlling the randomness of the model's output.
        system_prompt_template: `System` role prompt template to pass to the model. Uses mustache syntax for variable substitution, e.g. `{scenario_input}`.
        user_prompt_template: `User` role prompt template to pass to the model. Uses mustache syntax for variable substitution, e.g. `{scenario_input}`
        dialog_template: Dialog template in OpenAI message format to pass to the model. Uses mustache syntax for variable substitution.
        tools: List of tools to pass to the model.
    """

    type = "openai"
    model_id: str = field(default="gpt-4o-mini")
    temperature: float = field(default=0)
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


@define
class GenerationModel(BaseModel):
    """An LLM definition with prompt template and relevant parameters for an Okareo evaluation.

    Arguments:
        model_id: Model ID to request for LLM completion.
        temperature: Parameter for controlling the randomness of the model's output.
        system_prompt_template: `System` role prompt template to pass to the model. Uses mustache syntax for variable substitution, e.g. `{scenario_input}`.
        user_prompt_template: `User` role prompt template to pass to the model. Uses mustache syntax for variable substitution, e.g. `{scenario_input}`
        dialog_template: Dialog template in OpenAI message format to pass to the model. Uses mustache syntax for variable substitution.
        tools: List of tools to pass to the model.
    """

    type = "generation"
    model_id: str = field(default="gpt-4o-mini")
    temperature: float = field(default=0)
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
    """An OpenAI Assistant definition with prompt template and relevant parameters for an Okareo evaluation.

    Arguments:
        model_id: Assistant ID to request to run a thread against.
        assistant_prompt_template: `System` role prompt template to pass to the model. Uses mustache syntax for variable substitution, e.g. `{scenario_input}`.
        user_prompt_template: `User` role prompt template to pass to the model. Uses mustache syntax for variable substitution, e.g. `{scenario_input}`
        dialog_template: Dialog template in OpenAI message format to pass to the model. Uses mustache syntax for variable substitution.
    """

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
    """
    A Cohere model definition with prompt template and relevant parameters for an Okareo evaluation.

    Arguments:
        model_id: Model ID to request for the Cohere completion.
            For a full list of available models, see https://docs.cohere.com/v2/docs/models
        model_type: Type of application for the Cohere model. Currently, we support 'classify' and 'embed'.
        input_type: Input type for the Cohere embedding model.
            For more details, see https://docs.cohere.com/v2/docs/embeddings#the-input_type-parameter
    """

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
    """
    A Pinecone vector database configuration for use in an Okareo retrieval evaluation.

    Arguments:
        index_name: The name of the Pinecone index to connect to.
        region: The region where the Pinecone index is hosted.
        project_id: The project identifier associated with the Pinecone index.
        top_k: The number of top results to retrieve for queries. Defaults to 5.
    """

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
    """
    A Qdrant vector database configuration for use in an Okareo retrieval evaluation.

    Arguments:
        collection_name: The name of the Qdrant collection to connect to.
        url: The URL of the Qdrant instance.
        top_k: The number of top results to retrieve for queries. Defaults to 5.
        sparse: Whether to use sparse vectors for the Qdrant collection. Defaults to False.
    """

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
    """A custom model definition for an Okareo evaluation.
    Requires a valid `invoke` definition that operates on a single input.

    Arguments:
        name: A name for the custom model.
    """

    type = "custom"
    name: str

    @abstractmethod
    def invoke(
        self, input_value: Union[dict, list, str]
    ) -> Union[ModelInvocation, Any]:
        """Method for taking a single scenario input and returning a single model output

        Arguments:
            input_value: Union[dict, list, str] - input to the model.

        Returns:
            Union[ModelInvocation, Any] - model output.
            If the model returns a ModelInvocation, it should contain the model's prediction, input, and metadata.
            If the model returns a tuple, the first element should be the model's prediction and the second element should be the metadata.
        """

    def params(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "model_invoker": self.invoke,
        }


@_attrs_define
class CustomMultiturnTarget(BaseModel):
    """A custom model definition for an Okareo multiturn evaluation.
    Requires a valid `invoke` definition that operates on a single turn of a converstation.
    """

    type = "custom_target"
    name: str

    @abstractmethod
    def invoke(
        self,
        messages: List[dict[str, str]],
        scenario_input: Optional[Union[dict, list, str]] = None,
    ) -> Union[ModelInvocation, Any]:
        """Method for continuing a multiturn conversation with a custom model

        Arguments:
            messages: list - list of messages in the conversation
            scenario_input: Optional[dict | list | str] - scenario input for the conversation

        Returns:
            Union[ModelInvocation, Any] - model output.
            If the model returns a ModelInvocation, it should contain the model's prediction, input, and metadata.
            If the model returns a tuple, the first element should be the model's prediction and the second element should be the metadata.
        """

    def params(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "model_invoker": self.invoke,
        }


@define
class StopConfig:
    """
    Configuration for stopping a multiturn conversation based on a specific check.

    Arguments:
        check_name: Name of the check to use for stopping the conversation.
        stop_on: The check condition to stop the conversation.
            Defaults to `True` (i.e., conversation stops when check evaluates to `True`).
    """

    check_name: str
    stop_on: bool = field(default=True)

    def params(self) -> dict:
        return {"check_name": self.check_name, "stop_on": self.stop_on}


class SessionConfig:
    """Configuration for a custom API endpoint that starts a session.

    Arguments:
        url: URL of the endpoint to start the session.
        method: HTTP method to use for the request. Defaults to `POST`.
        headers: Headers to include in the request. Defaults to an empty JSON object.
        body: Body to include in the request. Defaults to an empty JSON object.
        status_code: Expected HTTP status code of the response.
        response_session_id_path: Path to extract the session ID from the response.
            E.g., `response.id` will use the `id` field of the response JSON object to set the `session_id`.
    """

    def __init__(
        self,
        url: str,
        method: str = "POST",
        headers: Optional[Union[str, dict]] = None,
        body: Union[str, dict] = "{}",
        status_code: Optional[int] = None,
        response_session_id_path: str = "",
        response_message_path: str = "",
    ) -> None:
        self.url = url
        self.method = method
        self.headers = headers or json.dumps({})
        self.body = body
        self.status_code = status_code
        self.response_session_id_path = response_session_id_path
        self.response_message_path = response_message_path

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "method": self.method,
            "headers": self.headers,
            "body": self.body,
            "status_code": self.status_code,
            "response_session_id_path": self.response_session_id_path,
            "response_message_path": self.response_message_path,
        }


class TurnConfig:
    """
    Configuration for a custom API endpoint that continues a session/conversation by one turn.

    Arguments:
        url: URL of the endpoint to start the session.
        method: HTTP method to use for the request. Defaults to `POST`.
        headers: Headers to include in the request.
            Supports mustache syntax for variable substitution for `{latest_message}`, `{message_history}`, `{session_id}`.
            Defaults to an empty JSON object.
        body: Body to include in the request.
            Supports mustache syntax for variable substitution for `{latest_message}`, `{message_history}`, `{session_id}`.
            Defaults to an empty JSON object.
        status_code: Expected HTTP status code of the response.
        response_message_path: Path to extract the model's generated message from the response.
            E.g., `response.completion.message.content` will parse out the corresponding field of
            the response JSON object as the model's generated response.
        response_tool_calls_path: Path to extract tool calls from the response.
    """

    def __init__(
        self,
        url: str,
        method: str = "POST",
        headers: Optional[Union[str, dict]] = None,
        body: Union[str, dict] = "{}",
        status_code: Optional[int] = None,
        response_message_path: str = "",
        response_tool_calls_path: str = "",
    ) -> None:
        self.url = url
        self.method = method
        self.headers = headers or json.dumps({})
        self.body = body
        self.status_code = status_code
        self.response_message_path = response_message_path
        self.response_tool_calls_path = (
            response_tool_calls_path  # TODO: populate this once we support on BE
        )

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "method": self.method,
            "headers": self.headers,
            "body": self.body,
            "status_code": self.status_code,
            "response_message_path": self.response_message_path,
            "response_tool_calls_path": self.response_tool_calls_path,
        }


class EndSessionConfig:
    """Configuration for a custom API endpoint that ends a session.

    Arguments:
        url: URL of the endpoint to start the session.
        method: HTTP method to use for the request. Defaults to `POST`.
        headers: Headers to include in the request. Defaults to an empty JSON object.
        body: Body to include in the request. Defaults to an empty JSON object.
        status_code: Expected HTTP status code of the response.
        response_session_id_path: Path to extract the session ID from the response.
    """

    def __init__(
        self,
        url: str,
        method: str = "POST",
        headers: Optional[Union[str, dict]] = None,
        body: Union[str, dict] = "{}",
        status_code: Optional[int] = None,
        response_session_id_path: str = "",
    ) -> None:
        self.url = url
        self.method = method
        self.headers = headers or json.dumps({})
        self.body = body
        self.status_code = status_code
        self.response_session_id_path = response_session_id_path

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "method": self.method,
            "headers": self.headers,
            "body": self.body,
            "status_code": self.status_code,
        }


class CustomEndpointTarget:
    """
    A pair of custom API endpoints for starting a session and continuing a conversation to use in
    Okareo multiturn evaluation.

    Arguments:
        start_session: A valid SessionConfig for starting a session.
        next_turn: A valid TurnConfig for requesting and parsing the next turn of a conversation.
        end_session: A valid EndSessionConfig for ending a session.
        max_parallel_requests: Maximum number of parallel requests to allow when running the evaluation.
    """

    type = "custom_endpoint"

    def __init__(
        self,
        start_session: SessionConfig,
        next_turn: TurnConfig,
        end_session: Optional[EndSessionConfig] = None,
        max_parallel_requests: Optional[int] = None,
    ) -> None:
        self.start_session = start_session
        self.next_turn = next_turn
        self.end_session = end_session
        self.max_parallel_requests = max_parallel_requests

    def params(self) -> dict:
        return {
            "type": self.type,
            "start_session_params": self.start_session.to_dict(),
            "next_message_params": self.next_turn.to_dict(),
            "end_session_params": (
                self.end_session.to_dict() if self.end_session is not None else {}
            ),
            "max_parallel_requests": self.max_parallel_requests,
        }


@_attrs_define
class MultiTurnDriver(BaseModel):
    """
    A driver model for Okareo multiturn evaluation.

    Arguments:
        target: Target model under test to use in the multiturn evaluation.
        stop_check: A valid StopConfig or a dict that can be converted to StopConfig.
        driver_model_id: Model ID to use for the driver model (e.g., "gpt-4.1").
        driver_temperature: Parameter for controlling the randomness of the driver model's output.
        repeats: Number of times to run a conversation per scenario row. Defaults to 1.
        max_turns: Maximum number of turns to run in a conversation. Defaults to 5.
        first_turn: Name of model (i.e., "target" or "driver") that should initiate each conversation. Defaults to "target".
        driver_prompt_template: Optional system prompt template to pass to the driver model.
            Uses mustache syntax for variable substitution, e.g. `{input}`.
    """

    type = "driver"
    target: Union[
        OpenAIModel, CustomMultiturnTarget, GenerationModel, CustomEndpointTarget
    ]
    stop_check: Union[StopConfig, dict, None] = None
    driver_model_id: Optional[str] = None
    driver_temperature: Optional[float] = 0.8
    repeats: Optional[int] = 1
    max_turns: Optional[int] = 5
    first_turn: Optional[str] = "target"
    driver_prompt_template: Optional[str] = None
    checks_at_every_turn: Optional[bool] = False

    def __attrs_post_init__(self) -> None:
        if isinstance(self.stop_check, dict):
            self.stop_check = StopConfig(**self.stop_check)

    def params(self) -> dict:
        return {
            "type": self.type,
            "target": self.target.params(),
            "driver_model_id": self.driver_model_id,
            "driver_temperature": self.driver_temperature,
            "driver_prompt_template": self.driver_prompt_template,
            "repeats": self.repeats,
            "max_turns": self.max_turns,
            "first_turn": self.first_turn,
            "stop_check": (
                self.stop_check.params()
                if isinstance(self.stop_check, StopConfig)
                else self.stop_check
            ),
            "checks_at_every_turn": self.checks_at_every_turn,
        }


@_attrs_define
class CustomBatchModel(BaseModel):
    """A custom batch model definition for an Okareo evaluation.
    Requires a valid `invoke_batch` definition that operates on a single input.
    """

    type = "custom_batch"
    name: str
    batch_size: int = 1

    @abstractmethod
    def invoke_batch(
        self, input_batch: list[dict[str, Union[dict, list, str]]]
    ) -> list[dict[str, Union[ModelInvocation, Any]]]:
        """Method for taking a batch of scenario inputs and returning a corresponding batch of model outputs

        Arguments:
            input_batch: list[dict[str, Union[dict, list, str]]] - batch of inputs to the model. Expects a list of
            dicts of the format `{ 'id': str, 'input_value': Union[dict, list, str] }`.

        Returns:
            List of dicts of format `{ 'id': str, 'model_invocation': Union[ModelInvocation, Any] }`. 'id' must match
            the corresponding input_batch element's 'id'.
        """

    def params(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "batch_size": self.batch_size,
            "model_invoker": self.invoke_batch,
        }
