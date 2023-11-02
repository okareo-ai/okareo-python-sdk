import json
from datetime import datetime
from typing import Any, Callable, List, Tuple, Union

from okareo_api_client.api.default import (
    add_datapoint_v0_datapoints_post,
    add_test_data_point_v0_test_data_point_post,
    add_test_run_v0_test_runs_post,
    get_scenario_set_data_points_v0_scenario_data_points_scenario_id_get,
    get_test_run_v0_test_runs_test_run_id_get,
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
from okareo_api_client.models.http_validation_error import HTTPValidationError


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
            "project_id": self.project_id,
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
                        result_datetime=str(datetime.now()),  # end of model invocation
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
        self, response: Union[HTTPValidationError, TestRunItem, None]
    ) -> TestRunItem:
        if isinstance(response, HTTPValidationError):
            error_message = f"error: {response}, {response.detail}"
            print(error_message)
            raise TypeError(error_message)
        if not response:
            raise TypeError("Empty response from Okareo API")
        return response
