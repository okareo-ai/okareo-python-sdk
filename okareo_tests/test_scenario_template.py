from datetime import datetime
from typing import Union

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import CustomModel, ModelInvocation
from okareo_api_client.models import ScenarioSetResponse, ScenarioType, TestRunType
from okareo_api_client.models.generation_tone import GenerationTone
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.scenario_set_generate import ScenarioSetGenerate

today_with_time = datetime.now().strftime("%m-%d %H:%M:%S")
rnd_str = random_string(5)
unique_key = f"{rnd_str} {today_with_time}"
create_scenario_name = f"ci_scenario_template_create {unique_key}"
generate_scenario_name = f"ci_scenario_template_generate {unique_key}"


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


JSON_SCENARIO = [
    {
        "input": {
            "document": "WebBizz is dedicated to providing our customers with a seamless online shopping experience. Our platform is designed with user-friendly interfaces to help you browse and select the best products suitable for your needs. We offer a wide range of products from top brands and new entrants, ensuring diversity and quality in our offerings. Our 24/7 customer support is ready to assist you with any queries, from product details, shipping timelines, to payment methods. We also have a dedicated FAQ section addressing common concerns. Always ensure you are logged in to enjoy personalized product recommendations and faster checkout processes.",
            "metadata": {"version": "1", "last update": "2024-05-16T14:15:30Z"},
        },
        "result": "75eaa363-dfcc-499f-b2af-1407b43cb133",
    },
    {
        "input": {
            "document": "Safety and security of your data is our top priority at WebBizz. Our platform employs state-of-the-art encryption methods ensuring your personal and financial information remains confidential. Our two-factor authentication at checkout provides an added layer of security. We understand the importance of timely deliveries, hence we've partnered with reliable logistics partners ensuring your products reach you in pristine condition. In case of any delays or issues, our tracking tool can provide real-time updates on your product's location. We believe in transparency and guarantee no hidden fees or charges during your purchase journey.",
            "metadata": {"version": "2", "last update": "2024-05-16T14:15:30Z"},
        },
        "result": "ac0d464c-f673-44b8-8195-60c965e47525",
    },
    {
        "input": {
            "document": "At WebBizz, we value our customer's feedback and are always striving to improve. Our product review section allows customers to share their experiences and helps others make informed decisions. If unsatisfied with a purchase, our easy return and refund policy ensures hassle-free returns within 30 days of purchase. We also offer a loyalty program, WebBizz Rewards, where customers can earn points with each purchase and avail exclusive discounts. For any further assistance, our 'Live Chat' feature connects you instantly with a customer support representative. We thank you for choosing WebBizz and look forward to serving you again!",
            "metadata": {"version": "3", "last update": "2024-05-16T14:15:30Z"},
        },
        "result": "35a4fd5b-453e-4ca6-9536-f20db7303344",
    },
]

JSON_SEED = Okareo.seed_data_from_list(JSON_SCENARIO)  # type: ignore


@pytest.fixture(scope="module")
def create_scenario_set(okareo_client: Okareo) -> ScenarioSetResponse:
    scenario_set_create = ScenarioSetCreate(
        name=create_scenario_name,
        seed_data=JSON_SEED,
    )
    scenario = okareo_client.create_scenario_set(scenario_set_create)
    return scenario


@pytest.fixture(scope="module")
def generate_scenarios(
    okareo_client: Okareo, create_scenario_set: ScenarioSetResponse
) -> ScenarioSetResponse:
    questions: ScenarioSetResponse = okareo_client.generate_scenario_set(
        ScenarioSetGenerate(
            name=generate_scenario_name,
            source_scenario_id=create_scenario_set.scenario_id,
            number_examples=2,
            generation_type=ScenarioType.TEXT_REVERSE_QUESTION,
            generation_tone=GenerationTone.INFORMAL,
            pre_template="""{input.document}""",
            post_template="""{"question": "{generation.input}", "metadata": {input.metadata}}""",
        )
    )

    return questions


def test_generate_scenarios(
    okareo_client: Okareo, generate_scenarios: ScenarioSetResponse
) -> None:
    assert generate_scenarios is not None
    assert generate_scenarios.name == generate_scenario_name
    assert generate_scenarios.scenario_id
    assert generate_scenarios.project_id
    assert generate_scenarios.time_created

    scenario_dps = okareo_client.get_scenario_data_points(
        generate_scenarios.scenario_id
    )
    assert scenario_dps
    assert len(scenario_dps) == 6  # 3 documents * 2 questions each
    for dp in scenario_dps:
        input_ = dp.to_dict()["input"]
        result = dp.to_dict()["result"]

        assert input_
        assert result
        assert input_["question"]
        assert input_["metadata"]

        result_to_version = {
            entry["result"]: entry["input"]["metadata"]["version"]  # type: ignore
            for entry in JSON_SCENARIO
        }

        assert input_["metadata"]["version"] == result_to_version[result[0]]


def test_custom_retrieval(
    okareo_client: Okareo, generate_scenarios: ScenarioSetResponse
) -> None:
    test_run_name = f"ci_scenario_template_custom {unique_key}"

    class RetrievalModel(CustomModel):
        def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
            assert isinstance(input_value, dict)
            assert input_value["question"]
            assert input_value["metadata"]

            return ModelInvocation(
                model_prediction=[
                    {
                        "id": "red",
                        "score": 1,
                        "label": "red",
                        "metadata": input_value["metadata"],
                    }
                ],
                model_input=input_value["question"],
                model_output_metadata=input_value["metadata"],
            )

    model_under_test = okareo_client.register_model(
        name=test_run_name,
        model=RetrievalModel(name=test_run_name),
    )

    retrieval_test_run = model_under_test.run_test(
        scenario=generate_scenarios,
        name=test_run_name,
        test_run_type=TestRunType.INFORMATION_RETRIEVAL,
        calculate_metrics=True,
    )

    assert retrieval_test_run.id
    assert retrieval_test_run.model_metrics
    metrics_dict = retrieval_test_run.model_metrics.to_dict()
    assert metrics_dict["Accuracy@k"]
