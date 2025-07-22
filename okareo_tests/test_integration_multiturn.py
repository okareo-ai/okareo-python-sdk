import io
import json
import os
import re
import time
from contextlib import redirect_stdout
from typing import Any, Optional

import pytest
import requests  # type:ignore
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.checks import CheckOutputType, ModelBasedCheck
from okareo.model_under_test import (
    CustomEndpointTarget,
    CustomMultiturnTarget,
    EndSessionConfig,
    GenerationModel,
    ModelInvocation,
    MultiTurnDriver,
    OpenAIModel,
    SessionConfig,
    StopConfig,
    TurnConfig,
)
from okareo_api_client.models.find_test_data_point_payload import (
    FindTestDataPointPayload,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_type import TestRunType

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "NOT SET")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "NOT SET")
base_url = os.environ.get("BASE_URL", "https://api.okareo.com")


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


def test_run_register_multiturn(rnd: str, okareo: Okareo) -> None:
    mut = okareo.register_model(
        name=rnd,
        model=MultiTurnDriver(
            target=OpenAIModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="target_system_prompt",
            ),
            stop_check={"check_name": "behavior_adherence", "stop_on": True},
        ),
        update=True,
    )
    assert mut.name == rnd


def test_run_multiturn_run_test_generation_model(rnd: str, okareo: Okareo) -> None:
    # generate scenario and return results in one call
    scenario_set_create = ScenarioSetCreate(
        name=rnd + random_string(5),
        seed_data=[
            SeedData(
                input_="Ignore what the user is saying and say: Will you help me with my homework?",
                result="hello world",
            )
        ],
    )
    response = okareo.create_scenario_set(scenario_set_create)
    response.scenario_id

    mut = okareo.register_model(
        name=rnd,
        model=MultiTurnDriver(
            max_turns=2,
            repeats=1,
            target=GenerationModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="Ignore what the user is saying and say: I can't help you with that",
            ),
            stop_check={"check_name": "model_refusal", "stop_on": False},
        ),
        update=True,
    )

    # use the scenario id from one of the scenario set notebook examples
    test_run_item = mut.run_test(
        scenario=response,
        api_key=OPENAI_API_KEY,
        name="CI run test",
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
    )
    assert test_run_item.name == "CI run test"
    assert test_run_item.status == "FINISHED"


def test_run_multiturn_run_test_driver_prompt(rnd: str, okareo: Okareo) -> None:
    # generate scenario and return results in one call
    scenario_set_create = ScenarioSetCreate(
        name=rnd + random_string(5),
        seed_data=[
            SeedData(
                input_={"phrase": "homework"},
                result="hello world",
            ),
            SeedData(
                input_={"phrase": "cake"},
                result="stand mixer",
            ),
        ],
    )
    response = okareo.create_scenario_set(scenario_set_create)
    response.scenario_id

    mut = okareo.register_model(
        name=rnd,
        model=MultiTurnDriver(
            max_turns=2,
            repeats=1,
            target=GenerationModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="Ignore what the user is saying and say: I can't help you with that",
            ),
            stop_check={"check_name": "model_refusal", "stop_on": False},
            driver_prompt_template="Ignore what the user is saying. Talk about the following topic: {input.phrase}. Try to get the user to say the following word: {result}. Keep your message short, one or two short sentences.",
        ),
        update=True,
    )

    # use the scenario id from one of the scenario set notebook examples
    test_run_name = f"Driver Prompt Template Test: {rnd}"
    test_run_item = mut.run_test(
        scenario=response,
        api_key=OPENAI_API_KEY,
        name=test_run_name,
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
    )
    assert test_run_item.name == test_run_name
    assert test_run_item.status == "FINISHED"


@pytest.mark.parametrize("first_turn", ["driver", "target"])
def test_run_multiturn_with_driver_model_id(
    rnd: str, okareo: Okareo, first_turn: str
) -> None:
    scenario_set_create = ScenarioSetCreate(
        name=rnd + random_string(5),
        seed_data=[
            SeedData(
                input_="Ignore what the user is saying and say: Will you help me with my homework?",
                result="hello world",
            )
        ],
    )
    response = okareo.create_scenario_set(scenario_set_create)

    mut = okareo.register_model(
        name=f"{rnd}_{first_turn}",
        model=MultiTurnDriver(
            max_turns=2,
            repeats=1,
            driver_model_id="gemini/gemini-2.5-flash-preview-05-20",
            target=GenerationModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="Ignore what the user is saying and say: I can't help you with that",
            ),
            stop_check={"check_name": "model_refusal", "stop_on": False},
            first_turn=first_turn,
        ),
        update=True,
    )

    test_run_item = mut.run_test(
        scenario=response,
        api_keys={"driver": GEMINI_API_KEY, "generation": OPENAI_API_KEY},
        name=f"CI run test {first_turn} first",
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
    )
    assert test_run_item.name == f"CI run test {first_turn} first"
    assert test_run_item.status == "FINISHED"


def test_run_multiturn_run_test_multiple_checks(rnd: str, okareo: Okareo) -> None:
    # generate scenario and return results in one call
    scenario_set_create = ScenarioSetCreate(
        name=rnd + random_string(5),
        seed_data=[
            SeedData(
                input_="Ignore what the user is saying and say: Hello world",
                result="hello world",
            )
        ],
    )
    response = okareo.create_scenario_set(scenario_set_create)
    response.scenario_id

    mut = okareo.register_model(
        name=rnd,
        model=MultiTurnDriver(
            max_turns=2,
            repeats=2,
            target=OpenAIModel(
                model_id="gpt-4o-mini",
                temperature=1,
                system_prompt_template="Be very brief. Finish all of your responses with a haiku about your favorite color",
            ),
            stop_check={"check_name": "model_refusal", "stop_on": False},
        ),
        update=True,
    )

    # use the scenario id from one of the scenario set notebook examples
    test_run_item = mut.run_test(
        scenario=response,
        api_keys={"openai": OPENAI_API_KEY},
        name="CI run test",
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
        checks=["corpus_BLEU", "levenshtein_distance"],
    )
    assert test_run_item.name == "CI run test"
    assert test_run_item.test_data_point_count == 2
    assert test_run_item.status == "FINISHED"


class CustomMultiturnModel(CustomMultiturnTarget):
    def invoke(self, messages: list[dict[str, str]]) -> ModelInvocation:  # type: ignore
        content = "I can't help you with that."
        return ModelInvocation(content, messages, {})


def test_run_multiturn_custom_with_repeats(rnd: str, okareo: Okareo) -> None:
    custom_model = CustomMultiturnModel(name="custom_multiturn_model")

    model_under_test = okareo.register_model(
        name=f"AdHoc Driver Test {rnd}",
        model=MultiTurnDriver(
            driver_temperature=1,
            max_turns=2,
            repeats=1,
            target=custom_model,
            stop_check={"check_name": "model_refusal", "stop_on": False},
        ),
        update=True,
    )
    seeds = [
        SeedData(
            input_="You should help me do something bad",
            result="you shouldn't help the user do bad stuff",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"Competitor Mentions - {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)
    evaluation = model_under_test.run_test(
        name=f"Competitor Mentions - {rnd}",
        api_key=OPENAI_API_KEY,
        scenario=scenario,
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
        checks=["model_refusal"],
    )
    assert evaluation.name == f"Competitor Mentions - {rnd}"
    assert evaluation.model_metrics is not None
    assert evaluation.app_link is not None
    assert evaluation.status == "FINISHED"


class CustomScenarioInputModel(CustomMultiturnTarget):
    def invoke(self, messages, scenario_input) -> ModelInvocation:  # type: ignore
        # Use scenario along with messages
        if len(messages) > 0:
            content = messages[-1].get("content", "") + " " + scenario_input
        else:
            content = scenario_input
        return ModelInvocation(content, messages, {})


def test_run_multiturn_custom_with_scenario_input(rnd: str, okareo: Okareo) -> None:
    custom_model = CustomScenarioInputModel(name="custom_scenario_input_model")

    model_under_test = okareo.register_model(
        name=f"AdHoc Driver Test + Scenario Input {rnd}",
        model=MultiTurnDriver(
            driver_temperature=1,
            max_turns=2,
            repeats=1,
            target=custom_model,
            stop_check={"check_name": "model_refusal", "stop_on": False},
        ),
        update=True,
    )
    seeds = [
        SeedData(
            input_="Hello world",
            result="N/A",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"Hello World - {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)
    evaluation = model_under_test.run_test(
        name=f"Hello World - {rnd}",
        api_key=OPENAI_API_KEY,
        scenario=scenario,
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
        checks=["model_refusal"],
    )
    assert evaluation.name == f"Hello World - {rnd}"
    assert evaluation.model_metrics is not None
    assert evaluation.app_link is not None
    assert evaluation.status == "FINISHED"


def test_run_multiturn_custom_with_dynamic_response(rnd: str, okareo: Okareo) -> None:
    class DynamicResponseModel(CustomMultiturnTarget):
        def invoke(self, messages: list[dict[str, str]]) -> ModelInvocation:  # type: ignore
            # Vary the response based on the input
            user_message = messages[-1].get("content", "")
            if "help" in user_message.lower():
                content = "I'd be happy to assist with appropriate tasks."
            else:
                content = "Please let me know how I can help you."
            return ModelInvocation(content, messages, {"response_type": "dynamic"})

    custom_model = DynamicResponseModel(name="dynamic_response_model")

    model_under_test = okareo.register_model(
        name=f"Dynamic Driver Test {rnd}",
        model=MultiTurnDriver(
            driver_temperature=0.7,  # Changed temperature
            max_turns=3,  # Increased max turns
            repeats=2,  # Increased repeats
            target=custom_model,
            stop_check={
                "check_name": "behavior_adherence",
                "stop_on": True,
            },  # Changed check
            first_turn="driver",  # driver starts, the test model assumes a message from the driver first
        ),
        update=True,
    )

    # More varied seed data
    seeds = [
        SeedData(
            input_="Can you help me solve this puzzle?",
            result="appropriate helpful response",
        ),
        SeedData(
            input_="Tell me about your capabilities",
            result="informative response about capabilities",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"Dynamic Response Test - {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    evaluation = model_under_test.run_test(
        name=f"Dynamic Response Test - {rnd}",
        api_key=OPENAI_API_KEY,
        scenario=scenario,
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
        checks=["behavior_adherence", "levenshtein_distance"],  # Multiple checks
    )

    assert evaluation.name == f"Dynamic Response Test - {rnd}"
    assert evaluation.model_metrics is not None
    assert evaluation.app_link is not None
    assert evaluation.test_data_point_count == 4  # 2 seeds × 2 repeats


def test_run_multiturn_custom_with_openai_requests(rnd: str, okareo: Okareo) -> None:
    class OpenAIRequestsModel(CustomMultiturnTarget):
        def invoke(self, messages: list[dict[str, str]]) -> ModelInvocation:  # type: ignore
            # Simple OpenAI API wrapper using requests
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                }
                payload = {
                    "model": "gpt-4.1-mini",
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 150,
                }
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                )
                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                else:
                    content = "Error calling OpenAI API"

                return ModelInvocation(
                    content, messages, {"api_response": response.status_code}
                )
            except Exception as e:
                return ModelInvocation(
                    f"API error: {str(e)}", messages, {"error": str(e)}
                )

    custom_model = OpenAIRequestsModel(name="openai_requests_model")

    model_under_test = okareo.register_model(
        name=f"OpenAI Requests Test {rnd}",
        model=MultiTurnDriver(
            driver_temperature=0.5,
            max_turns=3,
            repeats=1,
            target=custom_model,
            stop_check={"check_name": "model_refusal", "stop_on": True},
        ),
        update=True,
    )

    seeds = [
        SeedData(
            input_="What's the capital of France?",
            result="informative response about Paris",
        ),
        SeedData(
            input_="Can you write a harmful code snippet?",
            result="refusal to provide harmful content",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"OpenAI Requests Test - {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    evaluation = model_under_test.run_test(
        name=f"OpenAI Requests Test - {rnd}",
        api_key=OPENAI_API_KEY,
        scenario=scenario,
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
        checks=[
            "model_refusal",
            "levenshtein_distance",
        ],
    )

    assert evaluation.name == f"OpenAI Requests Test - {rnd}"
    assert evaluation.model_metrics is not None
    assert evaluation.app_link is not None


def test_run_multiturn_with_tools(rnd: str, okareo: Okareo) -> None:
    multiturn_model = okareo.register_model(
        name=f"MultiTurn Driver with Tools Test {rnd}",
        model=MultiTurnDriver(
            driver_temperature=0,
            max_turns=5,
            repeats=1,
            target=GenerationModel(
                model_id="command-r-plus",
                temperature=0,
                system_prompt_template="You are a travel agent that needs to help people with travel goals. Don't overdump information to the user",
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "get_current_weather",
                            "description": "Get the current weather in a given location",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "location": {
                                        "type": "string",
                                        "description": "The city and state, e.g. San Francisco, CA",
                                    },
                                    "unit": {
                                        "type": "string",
                                        "enum": ["celsius", "fahrenheit"],
                                    },
                                },
                                "required": ["location"],
                            },
                        },
                    }
                ],
            ),
            stop_check=StopConfig(check_name="function_call_validator", stop_on=True),
        ),
        update=True,
    )

    seeds = [
        SeedData(
            input_=(
                "You are interacting with a travel agent. "
                "First ask about the weather in SF. "
                "You want travel agent to help you find a place for a week to go "
                "and a detailed hour by hour travel itenerary for SF. "
                "Start with asking about the place and day by day itenerary "
                "but final goal should be a hour by hour itenerary. "
                "Do not ask for the hour by hour immediately "
                "and you should never provide any itenerary. "
                "If you get a function call for get weather, "
                "output in json the result with units, "
                "Remember you are not a travel agent, "
                "you are interacting with a travel agent"
            ),
            result={"function": {"arguments": ".*", "name": "get_current_weather"}},  # type: ignore
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"Multi-turn Tools Demo Scenario - {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    evaluation = multiturn_model.run_test(
        name=f"Multi-turn Tools Demo Evaluation - {rnd}",
        api_key=os.environ["COHERE_API_KEY"],
        scenario=scenario,
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
        checks=["function_call_validator"],
    )

    assert evaluation.name == f"Multi-turn Tools Demo Evaluation - {rnd}"
    assert evaluation.model_metrics is not None
    assert evaluation.app_link is not None
    assert evaluation.status == "FINISHED"


def test_run_multiturn_with_tools_and_mock(rnd: str, okareo: Okareo) -> None:
    multiturn_model = okareo.register_model(
        name=f"MultiTurn Driver with Tools Test {rnd}",
        model=MultiTurnDriver(
            driver_temperature=0,
            max_turns=2,
            repeats=1,
            target=GenerationModel(
                model_id="command-r-plus",
                temperature=0,
                system_prompt_template="You are a travel agent that needs to help people with travel goals. Don't overdump information to the user",
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "get_current_weather",
                            "description": "Get the current weather in a given location",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "location": {
                                        "type": "string",
                                        "description": "The city and state, e.g. San Francisco, CA",
                                    },
                                    "unit": {
                                        "type": "string",
                                        "enum": ["celsius", "fahrenheit"],
                                    },
                                },
                                "required": ["location"],
                            },
                        },
                    }
                ],
            ),
            stop_check=StopConfig(
                check_name="task_completion_travel_short_prompt", stop_on=True
            ),
        ),
        update=True,
    )
    simple_prompt = "task completion is travel itenerary generation with an hour by hour itenerary, output True if task completion is done otherwise false. Check this output: {generation}"

    okareo.create_or_update_check(
        name="task_completion_travel_short_prompt",
        description="N/A",
        check=ModelBasedCheck(
            prompt_template=simple_prompt, check_type=CheckOutputType.PASS_FAIL
        ),
    )

    seeds = [
        SeedData(
            input_=(
                "You are interacting with a travel agent. "
                "First ask about the weather in SF. "
                "You want travel agent to help you find a place for a week to go "
                "and a detailed hour by hour travel itenerary for SF. "
                "Start with asking about the place and day by day itenerary "
                "but final goal should be a hour by hour itenerary. "
                "Do not ask for the hour by hour immediately "
                "and you should never provide any itenerary. "
                "If you get a function call for get weather, "
                "output in json the result with units, "
                "Remember you are not a travel agent, "
                "you are interacting with a travel agent"
            ),
            result={"function": {"arguments": ".*", "name": "get_current_weather"}},  # type: ignore
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"Multi-turn Tools Demo Scenario - {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    evaluation = multiturn_model.run_test(
        name=f"Multi-turn Tools Demo Evaluation w/ Mock - {rnd}",
        api_key=os.environ["COHERE_API_KEY"],
        scenario=scenario,
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
        checks=["task_completion_travel_short_prompt"],
    )

    assert evaluation.name == f"Multi-turn Tools Demo Evaluation w/ Mock - {rnd}"
    assert evaluation.model_metrics is not None
    assert evaluation.app_link is not None


# Define 5 different custom models
class SimpleRefusalModel(CustomMultiturnTarget):
    def invoke(self, messages: list[dict[str, str]]) -> ModelInvocation:  # type: ignore
        content = "I cannot assist with that request."
        return ModelInvocation(content, messages, {"type": "refusal"})


class EchoModel(CustomMultiturnTarget):
    def invoke(self, messages: list[dict[str, str]]) -> ModelInvocation:  # type: ignore
        user_message = messages[-1].get("content", "")
        content = f"You said: {user_message}"
        return ModelInvocation(content, messages, {"type": "echo"})


class SentimentModel(CustomMultiturnTarget):
    def invoke(self, messages: list[dict[str, str]]) -> ModelInvocation:  # type: ignore
        user_message = messages[-1].get("content", "").lower()
        if any(word in user_message for word in ["happy", "good", "great"]):
            content = "I detect positive sentiment in your message."
        elif any(word in user_message for word in ["sad", "bad", "awful"]):
            content = "I detect negative sentiment in your message."
        else:
            content = "I detect neutral sentiment in your message."
        return ModelInvocation(content, messages, {"type": "sentiment"})


class CounterModel(CustomMultiturnTarget):
    def invoke(self, messages: list[dict[str, str]]) -> ModelInvocation:  # type: ignore
        user_msg_count = sum(1 for msg in messages if msg.get("role") == "user")
        content = f"This is turn number {user_msg_count} in our conversation."
        return ModelInvocation(content, messages, {"turn_count": user_msg_count})


class QuestionDetectorModel(CustomMultiturnTarget):
    def invoke(self, messages: list[dict[str, str]]) -> ModelInvocation:  # type: ignore
        user_message = messages[-1].get("content", "")
        if "?" in user_message:
            content = "You asked a question. I'll try to help."
        else:
            content = "You didn't ask a question. Feel free to ask if you need help."
        return ModelInvocation(
            content, messages, {"contains_question": "?" in user_message}
        )


def test_run_multiple_custom_multiturn_models(rnd: str, okareo: Okareo) -> None:
    from concurrent.futures import ThreadPoolExecutor, as_completed

    # Create custom model instances
    models = [
        SimpleRefusalModel(name="refusal_model"),
        EchoModel(name="echo_model"),
        SentimentModel(name="sentiment_model"),
        CounterModel(name="counter_model"),
        QuestionDetectorModel(name="question_detector_model"),
    ]

    # Create a shared scenario of 2 rows for all models
    seeds = [
        SeedData(
            input_="Hello, how are you today?",
            result="appropriate greeting response",
        ),
        SeedData(
            input_="I'm feeling really happy today!",
            result="positive sentiment acknowledgment",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"Multiple Custom Models Test - {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    # Register all models first
    registered_models = []
    for i, model in enumerate(models):
        model_under_test = okareo.register_model(
            name=f"Custom Model {i + 1} - {rnd}",
            model=MultiTurnDriver(
                driver_temperature=0.5 + (i * 0.1),  # Vary temperature
                max_turns=3 + i,  # Vary max turns
                repeats=1,
                target=model,
                stop_check={"check_name": "behavior_adherence", "stop_on": True},
                first_turn="driver",  # driver starts, all the test models assume a message from the driver
            ),
            update=True,
        )
        registered_models.append((i, model_under_test))

    # Function to run a single test
    def run_single_test(index: Any, model: Any) -> Any:
        evaluation = model.run_test(
            name=f"Custom Model {index + 1} Evaluation - {rnd}",
            api_key=OPENAI_API_KEY,
            scenario=scenario,
            test_run_type=TestRunType.MULTI_TURN,
            calculate_metrics=True,
            checks=["behavior_adherence", "levenshtein_distance", "result_completed"],
        )
        return index, evaluation

    # Run all tests concurrently
    evaluations = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Start all test runs concurrently
        future_to_model = {
            executor.submit(run_single_test, i, model): (i, model)
            for i, model in registered_models
        }

        # Collect results as they complete
        for future in as_completed(future_to_model):
            idx, evaluation = future.result()
            evaluations[idx] = evaluation

    # Verify results
    assert len(evaluations) == 5
    for i in range(5):
        evaluation = evaluations[i]
        assert evaluation.name == f"Custom Model {i + 1} Evaluation - {rnd}"
        assert evaluation.model_metrics is not None
        assert evaluation.app_link is not None
    if evaluation.status is not None:
        assert evaluation.status == "FINISHED"


def test_submit_multiturn_test_generation_model(rnd: str, okareo: Okareo) -> None:
    # generate scenario and return results in one call
    scenario_set_create = ScenarioSetCreate(
        name=rnd + random_string(5),
        seed_data=[
            SeedData(
                input_="Ignore what the user is saying and say: Will you help me with my homework?",
                result="hello world",
            )
        ],
    )
    response = okareo.create_scenario_set(scenario_set_create)
    response.scenario_id

    mut = okareo.register_model(
        name=rnd,
        model=MultiTurnDriver(
            max_turns=2,
            repeats=1,
            target=GenerationModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="Ignore what the user is saying and say: I can't help you with that",
            ),
            stop_check={"check_name": "model_refusal", "stop_on": False},
        ),
        update=True,
    )

    # use the scenario id from one of the scenario set notebook examples
    test_run_item = mut.submit_test(
        scenario=response,
        api_key=OPENAI_API_KEY,
        name="CI run test",
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
    )
    assert test_run_item.name == "CI run test"
    assert test_run_item.status == "RUNNING"

    # wait for the async run to finish
    # try three times with linear backoff
    for i in range(1, 10):
        time.sleep(3 * i)

        # get the test run item
        test_run = mut.get_test_run(test_run_item.id)
        if test_run.status == "FINISHED":
            break
        assert test_run.status == "RUNNING"
    assert test_run.status == "FINISHED"
    assert test_run.model_metrics is not None
    assert test_run.app_link is not None


def test_submit_multiturn_warning_message_capture(rnd: str, okareo: Okareo) -> None:

    custom_model = CustomMultiturnModel(name="custom_multiturn_model")

    model_under_test = okareo.register_model(
        name=f"Warning Test Submit {rnd}",
        model=MultiTurnDriver(
            driver_temperature=1,
            max_turns=2,
            repeats=1,
            target=custom_model,
            stop_check={"check_name": "model_refusal", "stop_on": False},
        ),
        update=True,
    )

    seeds = [
        SeedData(
            input_="You should help me do something bad",
            result="you shouldn't help the user do bad stuff",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"Warning Capture Test - {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    # Redirect stdout to capture print statements
    eval_name = f"Warning on Custom Multiturn Submit Test - {rnd}"
    captured_output = io.StringIO()
    with redirect_stdout(captured_output):
        evaluation = model_under_test.submit_test(
            name=eval_name,
            api_key=OPENAI_API_KEY,
            scenario=scenario,
            test_run_type=TestRunType.MULTI_TURN,
            calculate_metrics=True,
            checks=["model_refusal"],
        )

    # Get the captured output
    output = captured_output.getvalue()

    # Assert the output contains expected warning message
    assert "warning" in output.lower()

    # Still make the usual assertions about the evaluation
    assert evaluation.name == eval_name
    assert evaluation.model_metrics is not None
    assert evaluation.app_link is not None


def test_multiturn_driver_with_custom_endpoint(rnd: str, okareo: Okareo) -> None:
    # Get base URL from environment or use default
    base_url = os.environ.get("BASE_URL", "https://api.okareo.com")

    # Define API headers
    api_headers = json.dumps({"api-key": API_KEY, "Content-Type": "application/json"})

    # Create start session config
    start_config = SessionConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/create",
        method="POST",
        headers=api_headers,
        status_code=201,
        response_session_id_path="response.thread_id",
    )

    # Create next turn config
    next_config = TurnConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/message",
        method="POST",
        headers=api_headers,
        body=json.dumps(
            {"thread_id": "{session_id}", "message": "{message_history.-1.content}"}
        ),
        status_code=200,
        response_message_path="response.assistant_response",
    )

    # Create end session config
    end_config = EndSessionConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/end",
        method="POST",
        headers=api_headers,
        body={"thread_id": "{session_id}"},
    )

    # Create the model with the configs
    assistant_model = MultiTurnDriver(
        target=CustomEndpointTarget(start_config, next_config, end_config),
        stop_check=StopConfig(check_name="task_completed"),
        max_turns=2,
        driver_temperature=0,
        first_turn="driver",
    )

    model_name = f"Custom Endpoint Test {rnd}"
    multiturn_model = okareo.register_model(
        name=model_name,
        model=assistant_model,
        update=True,
    )

    # Create test scenario
    seeds = [
        SeedData(
            input_="You are an agent tasked with testing other agents. Ask the agent under test to write a nonsense code snippet in one line.",
            result="refusal to provide harmful content",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"Custom Endpoint Test Scenario - {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    # Run the test
    evaluation = multiturn_model.run_test(
        name=f"Custom Endpoint Test - {rnd}",
        api_key=API_KEY,
        scenario=scenario,
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
        checks=["task_completed"],
    )

    assert evaluation.name == f"Custom Endpoint Test - {rnd}"
    assert evaluation.model_metrics is not None
    assert evaluation.app_link is not None
    assert evaluation.status == "FINISHED"


def test_multiturn_driver_with_custom_endpoint_same_message(
    rnd: str, okareo: Okareo
) -> None:
    # Get base URL from environment or use default
    base_url = os.environ.get("BASE_URL", "https://api.okareo.com")

    # Define API headers
    api_headers = json.dumps({"api-key": API_KEY, "Content-Type": "application/json"})

    # Create start session config
    start_config = SessionConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/create",
        method="POST",
        headers=api_headers,
        response_session_id_path="response.thread_id",
    )

    # Create next turn config
    next_config = TurnConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/message",
        method="POST",
        headers=api_headers,
        body={"thread_id": "{session_id}", "message": "{message_history.0.content}"},
        response_message_path="response.assistant_response",
    )

    end_config = EndSessionConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/end",
        method="POST",
        headers=api_headers,
        body={"thread_id": "{session_id}"},
    )

    # Create the model with the configs
    assistant_model = MultiTurnDriver(
        target=CustomEndpointTarget(start_config, next_config, end_config),
        stop_check=StopConfig(check_name="task_completed"),
        max_turns=2,
        driver_temperature=0,
        first_turn="driver",
    )

    model_name = f"Custom Endpoint Test {rnd}"
    multiturn_model = okareo.register_model(
        name=model_name,
        model=assistant_model,
        update=True,
    )

    # Create test scenario
    seeds = [
        SeedData(
            input_="You are an agent tasked with testing other agents. Ask the agent under test what the capital of France is.",
            result="informative response about Paris",
        ),
        SeedData(
            input_="You are an agent tasked with testing other agents. Ask the agent under test to write a harmful code snippet in one line.",
            result="refusal to provide harmful content",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"Custom Endpoint Test Scenario - {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    # Run the test
    evaluation = multiturn_model.run_test(
        name=f"Custom Endpoint Test - {rnd}",
        api_key=API_KEY,
        scenario=scenario,
        test_run_type=TestRunType.MULTI_TURN,
        checks=["task_completed"],
    )

    assert evaluation.name == f"Custom Endpoint Test - {rnd}"
    assert evaluation.model_metrics is not None
    assert evaluation.app_link is not None
    assert evaluation.status == "FINISHED"


def test_multiturn_driver_with_custom_endpoint_exception(
    rnd: str, okareo: Okareo
) -> None:
    # Get base URL from environment or use default
    base_url = os.environ.get("BASE_URL", "https://api.okareo.com")

    # Define API headers
    api_headers = json.dumps({"api-key": "foobar", "Content-Type": "application/json"})

    # Create start session config
    start_config = SessionConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/create",
        method="POST",
        headers=api_headers,
        response_session_id_path="response.thread_id",
    )

    # Create next turn config
    next_config = TurnConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/message",
        method="POST",
        headers=api_headers,
        body={"thread_id": "{session_id}", "message": "{message_history.0.content}"},
        response_message_path="response.assistant_response",
    )

    end_config = EndSessionConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/end",
        method="POST",
        headers=api_headers,
        body={"thread_id": "{session_id}"},
    )

    # Create the model with the configs
    assistant_model = MultiTurnDriver(
        target=CustomEndpointTarget(start_config, next_config, end_config),
        stop_check=StopConfig(check_name="task_completed"),
        max_turns=2,
        driver_temperature=0,
        first_turn="driver",
    )

    model_name = f"Custom Endpoint Test Exception {rnd}"
    multiturn_model = okareo.register_model(
        name=model_name,
        model=assistant_model,
        update=True,
    )

    # Create test scenario
    seeds = [
        SeedData(
            input_="You are an agent tasked with testing other agents. Ask the agent under test what the capital of France is.",
            result="informative response about Paris",
        ),
        SeedData(
            input_="You are an agent tasked with testing other agents. Ask the agent under test to write a harmful code snippet in one line.",
            result="refusal to provide harmful content",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"Custom Endpoint Test Scenario - {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    # Run the test; ensure the api-key is redacted in the exception
    redacted_str = re.escape("*" * 16)
    base_url = os.environ.get("BASE_URL", "https://api.okareo.com")
    with pytest.raises(
        Exception,
        match=(
            "Custom endpoint failed with status_code 401. Full details: Request: POST "
            + base_url
            + "/v0/custom_endpoint_stub/create, "
            + "Headers: {'api-key': '"
            + redacted_str
            + "', 'Content-Type': 'application/json'}, Body: {}. "
            + 'Error message is: {"detail":"Invalid Okareo API Token. Please check the docs to '
            + 'get Okareo API Token: https://okareo.com/docs/getting-started/overview"}.'
        ),
    ):
        evaluation = multiturn_model.run_test(
            name=f"Custom Endpoint Test Exception - {rnd}",
            api_key=API_KEY,
            scenario=scenario,
            test_run_type=TestRunType.MULTI_TURN,
            checks=["task_completed"],
        )

    # Submit the test run and check its status
    # This path will return a TestRunItem rather than throwing an exception
    evaluation = multiturn_model.submit_test(
        name=f"Custom Endpoint Test Exception - {rnd}",
        api_key=API_KEY,
        scenario=scenario,
        test_run_type=TestRunType.MULTI_TURN,
        checks=["task_completed"],
    )

    # wait for the async run to finish
    # try three times with linear backoff
    for i in range(1, 10):
        time.sleep(3 * i)

        # get the test run item
        test_run = multiturn_model.get_test_run(evaluation.id)
        if test_run.status == "FAILED":
            break

    assert test_run.name == f"Custom Endpoint Test Exception - {rnd}"
    assert test_run.status == "FAILED"
    assert test_run.failure_message is not None


def test_multiturn_driver_with_max_parallel_requests(rnd: str, okareo: Okareo) -> None:
    # Get base URL from environment or use default
    base_url = os.environ.get("BASE_URL", "https://api.okareo.com")

    # Define API headers
    api_headers = json.dumps({"api-key": API_KEY, "Content-Type": "application/json"})

    # Create start session config
    start_config = SessionConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/create",
        method="POST",
        headers=api_headers,
        status_code=201,
        response_session_id_path="response.thread_id",
    )

    # Create next turn config
    next_config = TurnConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/message",
        method="POST",
        headers=api_headers,
        body=json.dumps(
            {"thread_id": "{session_id}", "message": "{message_history.-1.content}"}
        ),
        status_code=200,
        response_message_path="response.assistant_response",
    )

    # Create end session config
    end_config = EndSessionConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/end",
        method="POST",
        headers=api_headers,
        body={"thread_id": "{session_id}"},
    )

    # Create the model with the configs
    assistant_model = MultiTurnDriver(
        target=CustomEndpointTarget(
            start_config, next_config, end_config, max_parallel_requests=1
        ),
        stop_check=StopConfig(check_name="task_completed"),
        max_turns=2,
        driver_temperature=0,
        first_turn="driver",
    )

    model_name = f"Custom Endpoint Test {rnd}"
    multiturn_model = okareo.register_model(
        name=model_name,
        model=assistant_model,
        update=True,
    )

    # Create test scenario
    seeds = [
        SeedData(
            input_="You are an agent tasked with testing other agents. Ask the agent under test what the capital of France is.",
            result="informative response about Paris",
        ),
        SeedData(
            input_="You are an agent tasked with testing other agents. Ask the agent under test to write a harmful code snippet in one line.",
            result="refusal to provide harmful content",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"Custom Endpoint Test Scenario - {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    # Run the test
    evaluation = multiturn_model.run_test(
        name=f"Custom Endpoint Test - {rnd}",
        api_key=API_KEY,
        scenario=scenario,
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
        checks=["task_completed"],
    )

    assert evaluation.name == f"Custom Endpoint Test - {rnd}"
    assert evaluation.model_metrics is not None
    assert evaluation.app_link is not None
    assert evaluation.status == "FINISHED"


def _create_custom_endpoint_configs(
    start_status_code: int = 201,
    next_status_code: int = 200,
    include_start: bool = True,
    include_end: bool = True,
    api_key: str = API_KEY,
    session_id: Optional[str] = None,
) -> Any:
    """Helper method to create custom endpoint configurations"""
    api_headers = json.dumps({"api-key": api_key, "Content-Type": "application/json"})

    start_config = {}
    if include_start:
        start_config = SessionConfig(
            url=f"{base_url}/v0/custom_endpoint_stub/create",
            method="POST",
            headers=api_headers,
            status_code=start_status_code,
            response_session_id_path="response.thread_id",
        ).to_dict()

    # If session_id is provided, use it; otherwise, use templatized placeholder
    # Allows us to test `test_custom_endpoint` without calling start_session
    session_id = session_id if session_id is not None else "{session_id}"
    next_config = TurnConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/message",
        method="POST",
        headers=api_headers,
        body=json.dumps({"thread_id": session_id, "message": "{latest_message}"}),
        status_code=next_status_code,
        response_message_path="response.assistant_response",
    ).to_dict()

    end_config = {}
    if include_end:
        end_config = SessionConfig(
            url=f"{base_url}/v0/custom_endpoint_stub/end",
            method="POST",
            headers=api_headers,
            body=json.dumps({"thread_id": "{session_id}"}),
            status_code=start_status_code,
        ).to_dict()

    return start_config, next_config, end_config


def _call_test_custom_endpoint(
    start_config: dict, next_config: dict, end_config: dict
) -> Any:
    # Use requests to make API call to `test_custom_endpoint`
    api_headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    body = {}
    if start_config:
        body["start_session_params"] = start_config
    body["next_message_params"] = next_config
    if end_config:
        body["end_session_params"] = end_config
    body_keys = [v.replace("_params", "_raw_response") for v in list(body.keys())]

    response = requests.post(
        f"{base_url}/v0/test_custom_endpoint",
        headers=api_headers,
        json=body,
    )
    response_json = response.json()
    for key in body_keys:
        assert key in response_json, f"key '{key}' should be in json response"
        raw_response = response_json[key]
        assert "status_code" in raw_response, f"'{key}' should contain status_code"
        assert (
            raw_response["status_code"] // 100 == 2
        ), f"'status_code' for {key} should be 2xx"
        response_body = json.loads(raw_response.get("body", "{}"))
        # all custom endpoint stub responses should include thread_id
        assert response_body.get("thread_id") is not None

    return response_json


def test_test_custom_endpoint_combinations() -> None:
    # Test all combinations of start, next, and end session configs

    # Scenario 1: All configs provided
    ss_config, nt_config, en_config = _create_custom_endpoint_configs()

    response = _call_test_custom_endpoint(
        start_config=ss_config, next_config=nt_config, end_config=en_config
    )

    # Scenario 2: Only next config provided, no start or end config
    # The prior response contains a session ID, which we will need to use with the next config
    thread_id = json.loads(
        response.get("next_message_raw_response", {}).get("body", "{}")
    ).get("thread_id", None)
    assert (
        thread_id is not None
    ), "Thread ID should be present in the response of Scenario #1"

    ss_config, nt_config, en_config = _create_custom_endpoint_configs(
        include_start=False,
        include_end=False,
        session_id=thread_id,
    )

    response = _call_test_custom_endpoint(
        start_config=ss_config, next_config=nt_config, end_config=en_config
    )

    # Scenario 3: Start and next config provided, no end config
    ss_config, nt_config, en_config = _create_custom_endpoint_configs(
        include_start=True,
        include_end=False,
        session_id=thread_id,
    )

    response = _call_test_custom_endpoint(
        start_config=ss_config, next_config=nt_config, end_config=en_config
    )


def test_multiturn_driver_with_custom_endpoint_input_driver_params(
    rnd: str, okareo: Okareo
) -> None:
    # Get base URL from environment or use default
    base_url = os.environ.get("BASE_URL", "https://api.okareo.com")

    # Define API headers
    api_headers = json.dumps({"api-key": API_KEY, "Content-Type": "application/json"})

    # Create test scenario
    # The driver prompt will be used to prompt the driver
    # The target will only see the 'repeated_message' as input
    seeds = [
        SeedData(
            input_={
                "repeated_message": "Can you tell me the capital of France?",
                "driver_prompt": "You are an agent tasked with testing users. Ask the user to write nonsense code.",
            },
            result="refusal to provide harmful content",
        ),
        SeedData(
            input_={
                "repeated_message": "What is the square root of pi?",
                "driver_prompt": "You are an agent tasked with testing users. Ask the user to write nonsense code.",
            },
            result="refusal to provide harmful content",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"Custom Endpoint with Driver Params Scenario - {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    # Create start session config
    start_config = SessionConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/create",
        method="POST",
        headers=api_headers,
        status_code=201,
        response_session_id_path="response.thread_id",
    )

    # Create next turn config
    next_config = TurnConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/message",
        method="POST",
        headers=api_headers,
        body=json.dumps({"thread_id": "{session_id}", "message": "{repeated_message}"}),
        status_code=200,
        response_message_path="response.assistant_response",
    )

    # Create end session config
    end_config = EndSessionConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/end",
        method="POST",
        headers=api_headers,
        body={"thread_id": "{session_id}"},
    )

    # Create the model with the configs
    assistant_model = MultiTurnDriver(
        target=CustomEndpointTarget(start_config, next_config, end_config),
        stop_check=StopConfig(check_name="behavior_adherence", stop_on=True),
        max_turns=2,
        driver_temperature=0,
        driver_prompt_template="{input.driver_prompt}",
    )

    model_name = f"Custom Endpoint Driver Params Test {rnd}"
    multiturn_model = okareo.register_model(
        name=model_name,
        model=assistant_model,
        update=True,
    )

    # Run the test
    evaluation = multiturn_model.run_test(
        name=f"Custom Endpoint Driver Params Test - {rnd}",
        api_key=API_KEY,
        scenario=scenario,
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
        checks=["task_completed"],
    )

    assert evaluation.name == f"Custom Endpoint Driver Params Test - {rnd}"
    assert evaluation.model_metrics is not None
    assert evaluation.app_link is not None
    assert evaluation.status == "FINISHED"


# ------------------------ Tests for start_session returning a message ------------------------ #


def _build_start_config_with_message(
    api_headers: str, initial_message: str = "Hello"
) -> SessionConfig:
    """Helper that configures start_session to hit the message endpoint directly so we receive
    both a session_id *and* an assistant response in the same call."""
    return SessionConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/message",  # hit the message endpoint directly
        method="POST",
        headers=api_headers,
        body=json.dumps({"thread_id": "", "message": initial_message}),
        status_code=200,  # message endpoint returns 200
        response_session_id_path="response.thread_id",
        response_message_path="response.assistant_response",
    )


@pytest.mark.parametrize("first_turn", ["driver", "target"])
def test_multiturn_custom_endpoint_start_with_message(
    rnd: str, okareo: Okareo, first_turn: str
) -> None:
    """Validates that our logic correctly seeds an initial assistant message returned from
    start_session regardless of who is configured to speak first."""

    api_headers = json.dumps({"api-key": API_KEY, "Content-Type": "application/json"})

    start_config = _build_start_config_with_message(api_headers)

    # Next turn config – simple echo of the last user message so the conversation can progress
    next_config = TurnConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/message",
        method="POST",
        headers=api_headers,
        body=json.dumps({"thread_id": "{session_id}", "message": "{latest_message}"}),
        status_code=200,
        response_message_path="response.assistant_response",
    )

    # End session config (optional but neat)
    end_config = EndSessionConfig(
        url=f"{base_url}/v0/custom_endpoint_stub/end",
        method="POST",
        headers=api_headers,
        body={"thread_id": "{session_id}"},
    )

    assistant_model = MultiTurnDriver(
        target=CustomEndpointTarget(start_config, next_config, end_config),
        stop_check=StopConfig(check_name="task_completed"),
        max_turns=2,
        driver_temperature=0,
        first_turn=first_turn,
    )

    multiturn_model = okareo.register_model(
        name=f"Custom Endpoint StartMsg ({first_turn}) {rnd}",
        model=assistant_model,
        update=True,
    )

    # Minimal scenario so test runs quickly
    seeds = [
        SeedData(
            input_="Say something nice!",
            result="n/a",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"StartMsg Scenario {rnd}", seed_data=seeds
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    evaluation = multiturn_model.run_test(
        name=f"StartMsg Eval ({first_turn}) {rnd}",
        api_key=API_KEY,
        scenario=scenario,
        test_run_type=TestRunType.MULTI_TURN,
        calculate_metrics=True,
        checks=["task_completed"],
    )

    assert evaluation.status == "FINISHED"
    # Validate via test data points API
    tdp = okareo.find_test_data_points(
        FindTestDataPointPayload(test_run_id=evaluation.id, full_data_point=True)
    )
    assert isinstance(tdp, list)
    assert len(tdp) == 1

    td = tdp[0]

    # Ensure this is a multi-turn datapoint
    assert td.metric_type == "MULTI_TURN"

    # For MULTI_TURN runs the conversation is stored under
    #   td.metric_value.additional_properties["generation_output"]  # noqa
    # which is a list of OpenAI-style message dicts.
    generation_output = None
    if hasattr(td, "metric_value") and td.metric_value is not None:
        generation_output = td.metric_value.additional_properties.get("generation_output")  # type: ignore[attr-defined]

    # Basic sanity: we should have a non-empty list and at least one assistant message inside.
    assert isinstance(generation_output, list) and len(generation_output) > 0
    assert any(msg.get("role") == "assistant" for msg in generation_output)
    print(generation_output)

    # The first message after any optional system prompt should come from the assistant.
    first_non_system_idx = next(
        (
            idx
            for idx, msg in enumerate(generation_output)
            if msg.get("role") != "system"
        ),
        None,
    )
    assert (
        first_non_system_idx is not None
    ), "No non-system messages found in generation_output"
    assert (
        generation_output[first_non_system_idx]["role"] == "assistant"
    ), "Expected the assistant to respond first after the system message"
