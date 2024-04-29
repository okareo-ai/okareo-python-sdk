import os
import warnings
from typing import Any, Dict, List, Union

import httpx

from okareo_api_client import Client
from okareo_api_client.api.default import (
    check_delete_v0_check_check_id_delete,
    check_generate_v0_check_generate_post,
    check_upload_v0_check_upload_post,
    create_project_v0_projects_post,
    create_scenario_set_v0_scenario_sets_post,
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
from okareo_api_client.models.body_check_upload_v0_check_upload_post import (
    BodyCheckUploadV0CheckUploadPost,
)
from okareo_api_client.models.body_scenario_sets_upload_v0_scenario_sets_upload_post import (
    BodyScenarioSetsUploadV0ScenarioSetsUploadPost,
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
from okareo_api_client.types import UNSET, File, Unset

from .common import BASE_URL, HTTPX_TIME_OUT
from .model_under_test import BaseModel, ModelUnderTest

CHECK_DEPRECATION_WARNING = (
    "The `evaluator` naming convention is deprecated and will not be supported in a future release. "
    "Please use `check` in place of `evaluator` when invoking this method."
)


def check_deprecation_warning() -> None:
    warnings.warn(CHECK_DEPRECATION_WARNING, DeprecationWarning, stacklevel=2)


class Okareo:
    """A class for interacting with Okareo API"""

    def __init__(
        self, api_key: str, base_path: str = BASE_URL, timeout: float = HTTPX_TIME_OUT
    ):
        self.api_key = api_key
        self.client = Client(
            base_url=base_path, raise_on_unexpected_status=True
        )  # otherwise everything except 201 and 422 is swallowed

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
            if "custom" in data["models"].keys():
                model_invoker = data["models"]["custom"]["model_invoker"]
                del data["models"]["custom"]["model_invoker"]
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
            model_data["custom"]["model_invoker"] = model_invoker
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

    def validate_response(self, response: Any) -> None:
        if isinstance(response, ErrorResponse):
            error_message = f"error: {response}, {response.detail}"
            print(error_message)
            raise TypeError(error_message)
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

    def upload_evaluator(
        self,
        name: str,
        file_path: str,
        requires_scenario_input: bool,
        requires_scenario_result: bool,
        description: str = "",
        output_data_type: str = "",
        project_id: Union[Unset, str] = UNSET,
        update: bool = False,
    ) -> EvaluatorDetailedResponse:
        check_deprecation_warning()
        return self.upload_check(
            name,
            file_path,
            requires_scenario_input,
            requires_scenario_result,
            description,
            output_data_type,
            project_id,
            update,
        )

    def upload_check(
        self,
        name: str,
        file_path: str,
        requires_scenario_input: bool,
        requires_scenario_result: bool,
        description: str = "",
        output_data_type: str = "",
        project_id: Union[Unset, str] = UNSET,
        update: bool = False,
    ) -> EvaluatorDetailedResponse:
        try:
            file_name = os.path.basename(file_path)

            with open(file_path, "rb") as binary_io:
                multipart_body = BodyCheckUploadV0CheckUploadPost(
                    name=name,
                    requires_scenario_input=requires_scenario_input,
                    requires_scenario_result=requires_scenario_result,
                    description=description,
                    output_data_type=output_data_type,
                    project_id=project_id,
                    file=File(file_name=file_name, payload=binary_io),
                    update=update,
                )
                response = check_upload_v0_check_upload_post.sync(
                    client=self.client,
                    multipart_data=multipart_body,
                    api_key=self.api_key,
                )

            self.validate_response(response)
            assert isinstance(response, EvaluatorDetailedResponse)
            if response.warning:
                print(response.warning)
            return response
        except UnexpectedStatus as e:
            print(e.content)
            raise

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
