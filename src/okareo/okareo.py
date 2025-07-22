import datetime
import json
import os
import warnings
from typing import Any, Dict, List, TypedDict, Union

import httpx
from pydantic import BaseModel as PydanticBaseModel

from okareo.checks import BaseCheck
from okareo_api_client import Client
from okareo_api_client.api.default import (
    add_model_to_group_v0_groups_group_id_models_post,
    check_create_or_update_v0_check_create_or_update_post,
    check_delete_v0_check_check_id_delete,
    check_generate_v0_check_generate_post,
    create_group_v0_groups_post,
    create_project_v0_projects_post,
    create_scenario_set_v0_scenario_sets_post,
    create_trace_eval_v0_groups_group_id_trace_eval_post,
    evaluate_v0_evaluate_post,
    find_test_data_points_v0_find_test_data_points_post,
    generate_scenario_set_v0_scenario_sets_generate_post,
    get_all_checks_v0_checks_get,
    get_all_projects_v0_projects_get,
    get_check_v0_check_check_id_get,
    get_datapoints_filter_v0_find_datapoints_filter_post,
    get_datapoints_v0_find_datapoints_post,
    get_scenario_set_data_points_v0_scenario_data_points_scenario_id_get,
    register_model_v0_register_model_post,
    scenario_sets_upload_v0_scenario_sets_upload_post,
)
from okareo_api_client.errors import UnexpectedStatus
from okareo_api_client.models.body_check_delete_v0_check_check_id_delete import (
    BodyCheckDeleteV0CheckCheckIdDelete,
)
from okareo_api_client.models.body_scenario_sets_upload_v0_scenario_sets_upload_post import (
    BodyScenarioSetsUploadV0ScenarioSetsUploadPost,
)
from okareo_api_client.models.check_create_update_schema import CheckCreateUpdateSchema
from okareo_api_client.models.check_create_update_schema_check_config import (
    CheckCreateUpdateSchemaCheckConfig,
)
from okareo_api_client.models.create_group_v0_groups_post_source import (
    CreateGroupV0GroupsPostSource,
)
from okareo_api_client.models.datapoint_filter_search import DatapointFilterSearch
from okareo_api_client.models.datapoint_list_item import DatapointListItem
from okareo_api_client.models.datapoint_search import DatapointSearch
from okareo_api_client.models.error_response import ErrorResponse
from okareo_api_client.models.evaluation_payload import EvaluationPayload
from okareo_api_client.models.evaluation_payload_metrics_kwargs import (
    EvaluationPayloadMetricsKwargs,
)
from okareo_api_client.models.evaluator_brief_response import EvaluatorBriefResponse
from okareo_api_client.models.evaluator_detailed_response import (
    EvaluatorDetailedResponse,
)
from okareo_api_client.models.evaluator_generate_response import (
    EvaluatorGenerateResponse,
)
from okareo_api_client.models.evaluator_spec_request import EvaluatorSpecRequest
from okareo_api_client.models.find_test_data_point_payload import (
    FindTestDataPointPayload,
)
from okareo_api_client.models.full_data_point_item import FullDataPointItem
from okareo_api_client.models.model_under_test_response import ModelUnderTestResponse
from okareo_api_client.models.model_under_test_schema import ModelUnderTestSchema
from okareo_api_client.models.project_response import ProjectResponse
from okareo_api_client.models.project_schema import ProjectSchema
from okareo_api_client.models.scenario_data_poin_response import (
    ScenarioDataPoinResponse,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.scenario_set_generate import ScenarioSetGenerate
from okareo_api_client.models.scenario_set_response import ScenarioSetResponse
from okareo_api_client.models.scenario_type import ScenarioType
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_data_point_item import TestDataPointItem
from okareo_api_client.models.test_run_item import TestRunItem
from okareo_api_client.models.test_run_type import TestRunType
from okareo_api_client.types import UNSET, File, Unset

from .common import BASE_URL, HTTPX_TIME_OUT
from .model_under_test import BaseModel, ModelUnderTest

CHECK_DEPRECATION_WARNING = (
    "The `evaluator` naming convention is deprecated and will not be supported in a future release. "
    "Please use `check` in place of `evaluator` when invoking this method."
)

# Error message for empty generation
# TODO: Determine warning criteria by status_code = 422
_EMPTY_GENERATION_MESSAGE = "No scenario rows generated for scenario_id"

CUSTOM_MODEL_STRS = ["custom", "custom_batch"]


def check_deprecation_warning() -> None:
    warnings.warn(CHECK_DEPRECATION_WARNING, DeprecationWarning, stacklevel=2)


class SeedDataRow(TypedDict):
    input: Union[dict, list, str]
    result: Union[dict, list, str]


class BaseGenerationSchema(PydanticBaseModel):
    """A base schema class for specifying structured outputs to synthetic data generators."""

    @classmethod
    def to_dict(cls) -> dict:
        return cls.model_json_schema()


class Okareo:
    """A class for interacting with Okareo API and for formatting request data."""

    def __init__(
        self, api_key: str, base_path: str = BASE_URL, timeout: float = HTTPX_TIME_OUT  # type: ignore
    ):
        self.api_key = api_key
        self.client = Client(
            base_url=base_path, raise_on_unexpected_status=True
        )  # otherwise everything except 201 and 422 is swallowed
        response = get_all_projects_v0_projects_get.sync(
            client=self.client,
            api_key=self.api_key,
        )
        self.validate_response(response)

    @staticmethod
    def seed_data_from_list(data_list: List[SeedDataRow]) -> List[SeedData]:
        """
        Create a list of SeedData objects from a list of dictionaries.

        Each dictionary in the input list must have 'input' and 'result' keys.

        Args:
            data_list (List[SeedDataRow]): A list of dictionaries, where each dictionary
                                        contains 'input' and 'result' keys.

        Returns:
            List[SeedData]: A list of SeedData objects created from the input dictionaries.
        """
        seed_data_list = []
        for data in data_list:
            seed_input: Union[dict, list, str] = data["input"]
            seed_result: Union[dict, list, str] = data["result"]
            seed_data = SeedData(input_=seed_input, result=seed_result)
            seed_data_list.append(seed_data)

        return seed_data_list

    def get_projects(self) -> List[ProjectResponse]:
        """
        Get a list of all Okareo projects available to the user.

        Returns:
            List[ProjectResponse]: A list of ProjectResponse objects accessible to the user.

        Raises:
            TypeError: If the API response is an error.
            ValueError: If no response is received from the API.
        """
        response = get_all_projects_v0_projects_get.sync(
            client=self.client,
            api_key=self.api_key,
        )
        self.validate_response(response)
        assert isinstance(response, List)

        return response

    def create_project(
        self, name: str, tags: Union[Unset, List[str]] = UNSET
    ) -> ProjectResponse:
        """
        Create a new Okareo project.

        Args:
            name (str): The name of the new project.
            tags (Union[Unset, List[str]], optional): Optional list of tags to associate with the project.

        Returns:
            ProjectResponse: The created ProjectResponse object.

        Raises:
            TypeError: If the API response is an error.
            ValueError: If no response is received from the API.
        """
        response = create_project_v0_projects_post.sync(
            client=self.client,
            api_key=self.api_key,
            json_body=ProjectSchema(name=name, tags=tags),
        )
        self.validate_response(response)
        assert isinstance(response, ProjectResponse)

        return response

    def _get_custom_model_invoker(
        self, data: Dict[str, Any]
    ) -> tuple[dict[str, Any], Any]:
        for custom_model_str in CUSTOM_MODEL_STRS:
            if custom_model_str in data["models"].keys():
                model_invoker = data["models"][custom_model_str]["model_invoker"]
                del data["models"][custom_model_str]["model_invoker"]
                return data, model_invoker
        if (
            "driver" in data["models"].keys()
            and data["models"]["driver"]["target"]["type"] == "custom_target"
        ):
            model_invoker = data["models"]["driver"]["target"]["model_invoker"]
            del data["models"]["driver"]["target"]["model_invoker"]
            return data, model_invoker
        return data, None

    def _set_custom_model_invoker(
        self, data: Dict[str, Any], model_invoker: Any
    ) -> Any:
        for custom_model_str in CUSTOM_MODEL_STRS:
            if custom_model_str in data.keys():
                data[custom_model_str]["model_invoker"] = model_invoker
        if "driver" in data.keys():
            data["driver"]["target"]["model_invoker"] = model_invoker
        return data

    def register_model(
        self,
        name: str,
        tags: Union[List[str], None] = None,
        project_id: Union[str, None] = None,
        model: Union[None, BaseModel, List[BaseModel]] = None,
        update: bool = False,
        sensitive_fields: Union[List[str], None] = None,
    ) -> ModelUnderTest:
        """
        Register a new Model Under Test (MUT) to use in an Okareo evaluation.

        Args:
            name (str): The name of the model. Model names must be unique within a project. Using the same name will return or update the existing model.
            tags (Union[List[str], None], optional): Optional list of tags to associate with the model.
            project_id (Union[str, None], optional): The project ID to associate the model with.
            model (Union[None, BaseModel, List[BaseModel]], optional): The model or list of models to register.
            update (bool, optional): Whether to update an existing model with the same name. Defaults to False.
            sensitive_fields (List[str], optional): A list of sensitive fields to mask in the model parameters. Defaults to None.

        Returns:
            ModelUnderTest: The registered ModelUnderTest object.

        Raises:
            TypeError: If the API response is an error.
            ValueError: If no response is received from the API.
        """
        if tags is None:
            tags = []
        data: Dict[str, Any] = {
            "name": name,
            "tags": tags,
            "update": update,
            "sensitive_fields": sensitive_fields,
        }
        # will rename name to model in the future api-breaking release
        model_invoker = None
        if isinstance(model, BaseModel) or (
            isinstance(model, list) and all(isinstance(x, BaseModel) for x in model)
        ):
            models = model if isinstance(model, list) else [model]
            data["models"] = {}
            for model in models:
                data["models"][model.type] = model.params()
            data, model_invoker = self._get_custom_model_invoker(data)
        if project_id is not None:
            data["project_id"] = project_id
        json_body = ModelUnderTestSchema.from_dict(data)
        response = register_model_v0_register_model_post.sync(
            client=self.client, api_key=self.api_key, json_body=json_body
        )

        self.validate_response(response)
        assert isinstance(response, ModelUnderTestResponse)
        model_data = data.get("models")
        if model_invoker and isinstance(model_data, dict):
            model_data = self._set_custom_model_invoker(model_data, model_invoker)
        if response.warning:
            print(response.warning)
        return ModelUnderTest(
            client=self.client,
            api_key=self.api_key,
            mut=response,
            models=model_data,
        )

    def create_scenario_set(
        self, create_request: ScenarioSetCreate
    ) -> ScenarioSetResponse:
        """
        Create a new scenario set to use in an Okareo evaluation or as a seed for synthetic data generation.

        Args:
            create_request (ScenarioSetCreate): The request object containing scenario set details and seed data. The ScenarioSetCreate object should include:

        Returns:
            ScenarioSetResponse: The created ScenarioSetResponse object.

        Raises:
            ValueError: If the seed data is empty or if no response is received from the API.
            TypeError: If the API response is an error.

        Example:
        ```python
        seed_data = okareo_client.seed_data_from_list([
            {"input": {"animal": "fish", "color": "red"}, "result": "red"},
            {"input": {"animal": "dog", "color": "blue"}, "result": "blue"},
            {"input": {"animal": "cat", "color": "green"}, "result": "green"}
        ])
        create_request = ScenarioSetCreate(name="My Scenario Set", seed_data=seed_data)
        okareo_client.create_scenario_set(create_request)
        ```
        """
        if create_request.seed_data == [] or create_request.seed_data is None:
            raise ValueError("Non-empty seed data is required to create a scenario set")

        response = create_scenario_set_v0_scenario_sets_post.sync(
            client=self.client, api_key=self.api_key, json_body=create_request
        )

        self.validate_response(response)
        assert isinstance(response, ScenarioSetResponse)
        if response.warning:
            print(response.warning)
        return response

    def upload_scenario_set(
        self, scenario_name: str, file_path: str, project_id: Union[Unset, str] = UNSET
    ) -> ScenarioSetResponse:
        """
        Upload a file as a scenario set to use in an Okareo evaluation or as a seed for synthetic data generation.

        Args:
            scenario_name (str): The name to assign to the uploaded scenario set.
            file_path (str): The path to the file to upload.
            project_id (Union[Unset, str], optional): The project ID to associate with the scenario set.

        Returns:
            ScenarioSetResponse: The created ScenarioSetResponse object.

        Raises:
            UnexpectedStatus: If the API returns an unexpected status.
            TypeError: If the API response is an error.
            ValueError: If no response is received from the API.

        Example:
        ```python
        project_id = "your_project_id"  # Optional, can be None
        okareo_client.upload_scenario_set(
            scenario_name="My Uploaded Scenario Set",
            file_path="/path/to/scenario_set_file.json",
            project_id=project_id or None,
        )
        ```
        """
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
            if response.warning:
                print(response.warning)
            return response
        except UnexpectedStatus as e:
            print(e.content)
            raise

    def download_scenario_set(
        self,
        scenario: Union[ScenarioSetResponse, str],
        file_path: str = "",
    ) -> Any:
        """
        Download a scenario set from Okareo to the client's local filesystem.

        Args:
            scenario_set (ScenarioSetResponse): The scenario set to download.
            file_path (str, optional): The path where the file will be saved. If not provided, uses scenario set name.

        Returns:
            File: The downloaded file object.

        Example:
        ```python
        response_file = okareo_client.download_scenario_set(create_scenario_set)
        with open(response_file.name) as scenario_file:
            for line in scenario_file:
                print(line)
        ```
        """
        try:
            scenario_id = (
                scenario if isinstance(scenario, str) else scenario.scenario_id
            )
            url = f"{BASE_URL}/v0/scenario_sets_download/{scenario_id}"
            headers = {
                "accept": "application/json",
                "api-key": self.api_key,
            }
            response = httpx.get(
                url,
                headers=headers,
            )
            filename = response.headers["content-disposition"].split('"')[1]
            if file_path != "":
                filename = file_path
            binary_file = open(filename, "wb")
            binary_file.write(response.content)
            binary_file.close()
            return binary_file
        except Exception as e:
            print(e)
            raise

    def generate_scenarios(
        self,
        source_scenario: Union[str, ScenarioSetResponse],
        name: str,
        number_examples: int,
        project_id: Union[Unset, str] = UNSET,
        generation_type: Union[Unset, ScenarioType] = ScenarioType.REPHRASE_INVARIANT,
    ) -> ScenarioSetResponse:
        """
        Generate a synthetic scenario set based on an existing seed scenario.

        Args:
            source_scenario (Union[str, ScenarioSetResponse]): The source scenario set or its ID to generate from.
            name (str): The name for the new generated scenario set.
            number_examples (int): The number of synthetic examples to generate per seed scenario row.
            project_id (Union[Unset, str], optional): The project ID to associate with the generated scenario set.
            generation_type (Union[Unset, ScenarioType], optional): The type of scenario generation to use.

        Returns:
            ScenarioSetResponse: The generated synthetic scenario set.

        Raises:
            TypeError: If the API response is an error.
            ValueError: If no response is received from the API.

        Example:
        ```python
        source_scenario = "source_scenario_id"  # or ScenarioSetResponse object
        generated_set = okareo_client.generate_scenarios(
            source_scenario=source_scenario,
            name="Generated Scenario Set",
            number_examples=100,
            project_id="your_project_id",
            generation_type=ScenarioType.REPHRASE_INVARIANT
        )
        print(generated_set.app_link) # Prints the link to the generated scenario set
        ```
        """
        scenario_id = (
            source_scenario.scenario_id
            if isinstance(source_scenario, ScenarioSetResponse)
            else source_scenario
        )
        return self.generate_scenario_set(
            ScenarioSetGenerate(
                source_scenario_id=scenario_id,
                name=name,
                number_examples=number_examples,
                project_id=project_id,
                generation_type=generation_type,
            )
        )

    def generate_scenario_set(
        self, create_request: ScenarioSetGenerate
    ) -> ScenarioSetResponse:
        """
        Generate a synthetic scenario set based on an existing seed scenario and a ScenarioSetGenerate object. Offers more controls than the comparable `generate_scenarios` method.

        Args:
            create_request (ScenarioSetGenerate): The request object specifying scenario generation parameters.

        Returns:
            ScenarioSetResponse: The generated synthetic scenario set.

        Example:
        ```python
        generate_request = ScenarioSetGenerate(
            source_scenario_id="seed_scenario_id",
            name="My Synthetic Scenario Set",
            number_examples=50,
            project_id="your_project_id",
            generation_type=ScenarioType.REPHRASE_INVARIANT,
        )
        generated_set = okareo_client.generate_scenario_set(generate_request)
        print(generated_set.app_link)  # Prints the link to the generated scenario set
        ```
        """
        response = generate_scenario_set_v0_scenario_sets_generate_post.sync(
            client=self.client, api_key=self.api_key, json_body=create_request
        )

        if self.validate_generate_scenario_response(response):
            self.validate_response(response)
            assert isinstance(response, ScenarioSetResponse)
        else:
            # return empty response
            return ScenarioSetResponse(
                project_id=(
                    create_request.project_id if create_request.project_id else ""
                ),
                scenario_id="",
                time_created=datetime.datetime.now(),
                type=(
                    create_request.generation_type.value
                    if create_request.generation_type
                    else ""
                ),
            )

        return response

    def get_scenario_data_points(
        self, scenario_id: str
    ) -> List[ScenarioDataPoinResponse]:
        """
        Fetch the scenario data points associated with a scenario set with scenario_id.

        Args:
            scenario_id (str): The ID of the scenario set to fetch data points for.

        Returns:
            List[ScenarioDataPoinResponse]: A list of scenario data point responses associated with the scenario set.

        Example:
        ```python
        okareo_client = Okareo(api_key="your_api_key")
        scenario_id = "your_scenario_id"
        data_points = okareo_client.get_scenario_data_points(scenario_id)
        for dp in data_points:
            print(dp.input_, dp.result)
        ```
        """
        response = (
            get_scenario_set_data_points_v0_scenario_data_points_scenario_id_get.sync(
                client=self.client, api_key=self.api_key, scenario_id=scenario_id
            )
        )

        self.validate_response(response)
        assert isinstance(response, List)

        return response

    def find_test_data_points(
        self, test_data_point_payload: FindTestDataPointPayload
    ) -> Union[List[Union[TestDataPointItem, FullDataPointItem]], ErrorResponse]:
        """
        Fetch the test run data points associated as specified in the payload.

        Args:
            test_data_point_payload (FindTestDataPointPayload): The payload specifying the test data point search criteria.

        Returns:
            Union[List[Union[TestDataPointItem, FullDataPointItem]], ErrorResponse]:
                A list of test or full data point items, or an error response.

        Example:
        ```python
        from okareo_api_client.models.find_test_data_point_payload import (
            FindTestDataPointPayload,
        )

        test_run_id = "your_test_run_id"  # Replace with your actual test run ID
        payload = FindTestDataPointPayload(
            test_run_id=test_run_id,
        )
        data_points = okareo_client.find_test_data_points(payload)
        for dp in data_points:
            print(dp)
        ```
        """
        data = find_test_data_points_v0_find_test_data_points_post.sync(
            client=self.client, api_key=self.api_key, json_body=test_data_point_payload
        )
        if not data:
            return []
        return data

    def validate_response(self, response: Any) -> None:
        if isinstance(response, ErrorResponse):
            error_message = f"error: {response.detail}"
            print(error_message)
            raise TypeError(error_message)
        if response is None:
            print("Received no response (None) from the API")
            raise ValueError("No response received")

    def validate_generate_scenario_response(self, response: Any) -> bool:
        if (
            isinstance(response, ErrorResponse)
            and _EMPTY_GENERATION_MESSAGE in response.detail[0]
        ):
            # TODO: parse 422 status code rather than string matching
            # Generated scenario is empty. Raise warning rather than error.
            warning_message = f"warning: {response.detail}"
            print(warning_message)
            warnings.warn(
                warning_message,
                category=UserWarning,
                stacklevel=2,
            )
            return False
        return True

    def find_datapoints(
        self, datapoint_search: DatapointSearch
    ) -> Union[List[DatapointListItem], ErrorResponse]:
        """
        Fetch the datapoints specified by a Datapoint Search.

        Args:
            datapoint_search (DatapointSearch): The search criteria for fetching datapoints.

        Returns:
            Union[List[DatapointListItem], ErrorResponse]: A list of datapoint items matching the search, or an error response.

        Example:
        ```python
        from okareo_api_client.models.datapoint_search import DatapointSearch

        ### Search based on a test run ID
        test_run__id = "your_test_run_id"  # Replace with your actual test run ID
        search = DatapointSearch(
            test_run_id=test_run__id,
        )
        datapoints = okareo_client.find_datapoints(search)
        for dp in datapoints:
            print(dp)

        ### Search based on a context token from a logger
        logger_config = {
            "api_key": "<API_KEY>",
            "tags": ["logger-test"],
            "context_token": random_string(10),
        }
        # Use the logger config to log completions from CrewAI or Autogen
        ...

        # Search for the logged datapoints by the context token
        search = DatapointSearch(
            context_token=context_token,
        )
        datapoints = okareo_client.find_datapoints(search)
        for dp in datapoints:
            print(dp)
        ```
        """
        data = get_datapoints_v0_find_datapoints_post.sync(
            client=self.client,
            api_key=self.api_key,
            json_body=datapoint_search,
        )
        if not data:
            return []
        return data

    def find_datapoints_filter(
        self, datapoint_search: DatapointFilterSearch
    ) -> Union[List[DatapointListItem], ErrorResponse]:
        """
        Fetch the datapoints specified by a Datapoint Search.

        Args:
            datapoint_search (DatapointSearch): The search criteria for fetching datapoints.

        Returns:
            Union[List[DatapointListItem], ErrorResponse]: A list of datapoint items matching the search, or an error response.

        Example:
        ```python
        from okareo_api_client.models.datapoint_search import DatapointFilterSearch

        ### Search based on a test run ID
        test_run__id = "your_test_run_id"  # Replace with your actual test run ID
        search = DatapointFilterSearch(
            test_run_id=test_run__id,
        )
        datapoints = okareo_client.find_datapoints(search)
        for dp in datapoints:
            print(dp)

        ### Find datapoints based on filters on datapoints fields
        from okareo_api_client.models.datapoint_filter_search import DatapointFilterSearch
        from okareo_api_client.models.filter_condition import FilterCondition
        from okareo_api_client.models.comparison_operator import ComparisonOperator

        search = DatapointFilterSearch(
            filters=[FilterCondition(
                field=DatapointField.TEST_RUN_ID,
                operator=ComparisonOperator.EQUAL,
                value="France"
            )]
        )
        datapoints = okareo_client.find_datapoints_filter(search)
        for dp in datapoints:
            print(dp)
        ```
        """
        data = get_datapoints_filter_v0_find_datapoints_filter_post.sync(
            client=self.client,
            api_key=self.api_key,
            json_body=datapoint_search,
        )
        if not data:
            return []
        return data

    def generate_evaluator(
        self, create_evaluator: EvaluatorSpecRequest
    ) -> EvaluatorGenerateResponse:
        check_deprecation_warning()
        return self.generate_check(create_evaluator)

    def generate_check(
        self, create_check: EvaluatorSpecRequest
    ) -> EvaluatorGenerateResponse:
        """
        Generate the contents of a Check based on an EvaluatorSpecRequest. Can be used to generate a behavioral (model-based) or a deterministic (code-based) check. Check names must be unique within a project.

        Args:
            create_check (EvaluatorSpecRequest): The specification for the check to generate.

        Returns:
            EvaluatorGenerateResponse: The generated check response.

        Example:
        ```python
        from okareo_api_client.models.evaluator_spec_request import EvaluatorSpecRequest
        from okareo.okareo import OkareoClient, BaseCheck

        # Generate a behavioral model-based check
        spec = EvaluatorSpecRequest(
            description="Checks if the output contains toxic language.",
            requires_scenario_input=False,
            requires_scenario_result=False,
            output_data_type="bool", # bool, int, float
        )
        okareo_client = Okareo(api_key="your_api_key")
        generated_check = okareo_client.generate_check(spec)

        # Inspect the generated check to ensure it meets your requirements
        print(generated_check)

        # Upload the generated check to Okareo to use in evaluations
        toxicity_check = okareo.create_or_update_check(
            name="toxicity_check",
            description=generated_check.description,
            check=ModelBasedCheck(  # type: ignore
                prompt_template=check.generated_prompt,
                check_type=CheckOutputType.PASS_FAIL,
            ),
        )
        # Inspect the uploaded check
        print(toxicity_check)
        ```
        """
        response = check_generate_v0_check_generate_post.sync(
            client=self.client, api_key=self.api_key, json_body=create_check
        )
        self.validate_response(response)
        assert isinstance(response, EvaluatorGenerateResponse)

        return response

    def get_all_evaluators(self) -> List[EvaluatorBriefResponse]:
        check_deprecation_warning()
        return self.get_all_checks()

    def get_all_checks(self) -> List[EvaluatorBriefResponse]:
        """
        Fetch all available checks.

        Args:
            None

        Returns:
            List[EvaluatorBriefResponse]: A list of EvaluatorBriefResponse objects representing all available checks.

        Example:
        ```python
        checks = okareo_client.get_all_checks()
        for check in checks:
            print(check.name, check.id)
        ```
        """
        response = get_all_checks_v0_checks_get.sync(
            client=self.client,
            api_key=self.api_key,
        )
        self.validate_response(response)
        assert isinstance(response, List)

        return response

    def get_evaluator(self, evaluator_id: str) -> EvaluatorDetailedResponse:
        check_deprecation_warning()
        return self.get_check(evaluator_id)

    def get_check(self, check_id: str) -> EvaluatorDetailedResponse:
        """
        Fetch details for a specific check.

        Args:
            check_id (str): The ID of the check to fetch.

        Returns:
            EvaluatorDetailedResponse: The detailed response for the specified check.

        Example:
        ```python
        check_id = "your_check_id"
        check_details = okareo_client.get_check(check_id)
        print(check_details)
        ```
        """
        response = get_check_v0_check_check_id_get.sync(
            client=self.client, api_key=self.api_key, check_id=check_id
        )
        self.validate_response(response)
        assert isinstance(response, EvaluatorDetailedResponse)

        return response

    def delete_evaluator(self, evaluator_id: str, evaluator_name: str) -> str:
        check_deprecation_warning()
        return self.delete_check(evaluator_id, evaluator_name)

    def delete_check(self, check_id: str, check_name: str) -> str:
        """
        Deletes a check identified by its ID and name.

        Args:
            check_id (str): The unique identifier of the check to delete.
            check_name (str): The name of the check to delete.

        Returns:
            str: A message indicating the result of the deletion.

        Example:
        ```python
        result = okareo_client.delete_check(check_id="abc123", check_name="MyCheck")
        print(result)  # Output: Check deletion was successful
        ```
        """
        check_delete_v0_check_check_id_delete.sync(
            client=self.client,
            api_key=self.api_key,
            check_id=check_id,
            form_data=BodyCheckDeleteV0CheckCheckIdDelete.from_dict(
                {"name": check_name}
            ),
        )
        return "Check deletion was successful"

    def create_or_update_check(
        self, name: str, description: str, check: BaseCheck
    ) -> EvaluatorDetailedResponse:
        """
        Create or update an existing check. If the check with 'name' already exists, then this method will update the existing check. Otherwise, this method will create a new check.

        Args:
            name (str): The unique name of the check to create or update.
            description (str): A human-readable description of the check.
            check (BaseCheck): An instance of BaseCheck containing the check configuration.

        Returns:
            EvaluatorDetailedResponse: The detailed response from the evaluator after creating or updating the check.

        Raises:
            AssertionError: If the response is not an instance of EvaluatorDetailedResponse.
            ValueError: If the response validation fails.

        Example:
        ```python
        from okareo.checks import CheckOutputType, ModelBasedCheck

        # Define your custom check; here we use a ModelBasedCheck as an example.
        # Mustache template is used in the prompt to pipe scenario input and generated output
        my_check = ModelBasedCheck(
            prompt_template="Only output the number of words in the following text: {scenario_input} {generation}",
            check_type=CheckOutputType.PASS_FAIL,
        )

        # Create or update the check
        response = okareo_client.create_or_update_check(
            name="my_word_count_check",
            description="Custom check for counting combined total number of words in input and output.",
            check=my_check
        )

        print(response)
        ```
        """
        check_config = CheckCreateUpdateSchemaCheckConfig.from_dict(
            check.check_config()
        )
        response = check_create_or_update_v0_check_create_or_update_post.sync(
            client=self.client,
            api_key=self.api_key,
            json_body=CheckCreateUpdateSchema(
                name=name, description=description, check_config=check_config
            ),
        )
        self.validate_response(response)
        assert isinstance(response, EvaluatorDetailedResponse)

        return response

    def create_group(
        self,
        name: str,
        tags: Union[List[str], None] = None,
        source: Union[dict, None] = None,
    ) -> Any:
        json_body = CreateGroupV0GroupsPostSource()
        if source:
            json_body.additional_properties.update(source)
        response = create_group_v0_groups_post.sync_detailed(
            client=self.client,
            json_body=json_body,
            name=name,
            tags=tags,
            api_key=self.api_key,
        )
        self.validate_response(response)

        return json.loads(response.content)

    def add_model_to_group(self, group: Any, model: Any) -> Any:
        response = add_model_to_group_v0_groups_group_id_models_post.sync_detailed(
            client=self.client,
            group_id=group.get("id", ""),
            model_id=model.mut_id,
            api_key=self.api_key,
        )
        self.validate_response(response)
        return response.parsed.additional_properties  # type: ignore

    def create_trace_eval(self, group: Any, context_token: str) -> Any:
        """
        Create a trace evaluation for a group.

        Args:
            group_id (str): The ID of the group.
            context_token (str): The context token for the trace.

        Returns:
            The created trace evaluation details.

        Raises:
            OkareoAPIException: If the API request fails.
        """
        response = create_trace_eval_v0_groups_group_id_trace_eval_post.sync_detailed(
            client=self.client,
            group_id=group.get("id", ""),
            context_token=context_token,
            api_key=self.api_key,
        )
        self.validate_response(response)
        return response.parsed

    def evaluate(
        self,
        name: str,
        test_run_type: TestRunType,
        scenario_id: Union[Unset, str] = UNSET,
        datapoint_ids: Union[Unset, list[str]] = UNSET,
        filter_group_id: Union[Unset, str] = UNSET,
        tags: Union[Unset, list[str]] = UNSET,
        metrics_kwargs: Union[Dict[str, Any], Unset] = UNSET,
        checks: Union[Unset, list[str]] = UNSET,
    ) -> TestRunItem:
        """
        Evaluate datapoints using the specified parameters.

        Args:
            scenario_id: ID of the scenario set
            metrics_kwargs: Dictionary of metrics to be measured
            name: Name of the test run
            test_run_type: Type of test run
            tags: Tags for filtering test runs
            checks: List of checks to include
            datapoint_ids: List of datapoint IDs to filter by
            filter_group_id: ID of the datapoint filter group to apply

        Returns:
            TestRunItem: The evaluation results as a TestRunItem object.

        Example:
        ```python
        checks = ["model_refusal"]  # one or more checks to apply in the evaluation
        test_run = okareo.evaluate(
            name="My Test Run",
            test_run_type=TestRunType.NL_GENERATION,
            checks=checks,
            datapoint_ids=["datapoint_id_1", "datapoint_id_2"],
        )
        print(test_run.app_link)  # View link to eval results in Okareo app
        ```
        """
        payload = EvaluationPayload(
            metrics_kwargs=EvaluationPayloadMetricsKwargs.from_dict(
                metrics_kwargs or {}
            ),
            name=name,
            type=test_run_type,
            tags=tags,
            checks=checks,
            scenario_id=scenario_id,
            datapoint_ids=datapoint_ids,
            filter_group_id=filter_group_id,
        )

        response = evaluate_v0_evaluate_post.sync(
            client=self.client,
            json_body=payload,
            api_key=self.api_key,
        )
        self.validate_response(response)
        if isinstance(response, ErrorResponse):
            error_message = f"error: {response}, {response.detail}"
            print(error_message)
            raise
        if not response:
            print("Empty response from API")
        assert response is not None
        return response
