import json
import os
import warnings
from typing import Any, Dict, List, TypedDict, Union

import httpx

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
    find_test_data_points_v0_find_test_data_points_post,
    generate_scenario_set_v0_scenario_sets_generate_post,
    get_all_checks_v0_checks_get,
    get_all_projects_v0_projects_get,
    get_check_v0_check_check_id_get,
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
from okareo_api_client.models.datapoint_list_item import DatapointListItem
from okareo_api_client.models.datapoint_search import DatapointSearch
from okareo_api_client.models.error_response import ErrorResponse
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
from okareo_api_client.models.seed_data_input_type_0 import SeedDataInputType0
from okareo_api_client.models.seed_data_result_type_0 import SeedDataResultType0
from okareo_api_client.models.test_data_point_item import TestDataPointItem
from okareo_api_client.types import UNSET, File, Unset

from .common import BASE_URL, HTTPX_TIME_OUT
from .model_under_test import BaseModel, ModelUnderTest

CHECK_DEPRECATION_WARNING = (
    "The `evaluator` naming convention is deprecated and will not be supported in a future release. "
    "Please use `check` in place of `evaluator` when invoking this method."
)

CUSTOM_MODEL_STRS = ["custom", "custom_batch"]


def check_deprecation_warning() -> None:
    warnings.warn(CHECK_DEPRECATION_WARNING, DeprecationWarning, stacklevel=2)


class SeedDataRow(TypedDict):
    input: Union[dict, list, str]
    result: Union[dict, list, str]


class Okareo:
    """A class for interacting with Okareo API"""

    def __init__(
        self, api_key: str, base_path: str = BASE_URL, timeout: float = HTTPX_TIME_OUT
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
        Create a list of SeedData objects from a list of dictionaries with specifically 'input' and 'result' keys.
        """
        seed_data_list = []
        for data in data_list:
            seed_input: Union[SeedDataInputType0, list, str] = (
                SeedDataInputType0.from_dict(data["input"])
                if isinstance(data["input"], dict)
                else data["input"]
            )
            seed_result: Union[SeedDataResultType0, list, str] = (
                SeedDataResultType0.from_dict(data["result"])
                if isinstance(data["result"], dict)
                else data["result"]
            )
            seed_data = SeedData(input_=seed_input, result=seed_result)
            seed_data_list.append(seed_data)

        return seed_data_list

    def get_projects(self) -> List[ProjectResponse]:
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
    ) -> ModelUnderTest:
        if tags is None:
            tags = []
        data: Dict[str, Any] = {"name": name, "tags": tags, "update": update}
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

    def find_test_data_points(
        self, test_data_point_payload: FindTestDataPointPayload
    ) -> Union[List[Union[TestDataPointItem, FullDataPointItem]], ErrorResponse]:
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

    def find_datapoints(
        self, datapoint_search: DatapointSearch
    ) -> Union[List[DatapointListItem], ErrorResponse]:
        data = get_datapoints_v0_find_datapoints_post.sync(
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
