import json
import os
import re
from typing import Any, Optional

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import (
    CustomEndpointTarget,
    CustomMultiturnTarget,
    ModelInvocation,
    MultiTurnDriver,
    OpenAIModel,
    SessionConfig,
    TurnConfig,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_type import TestRunType

from .check_error_raise import Check

OKAREO_API_KEY = os.environ.get("OKAREO_API_KEY", "NOT SET")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "NOT SET")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "NOT SET")
base_url = os.environ.get("BASE_URL", "https://api.okareo.com")


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


@pytest.fixture
def basic_scenario(rnd: str, okareo: Okareo) -> Any:
    scenario_set_create = ScenarioSetCreate(
        name=f"Test Scenario - {rnd}",
        seed_data=[SeedData(input_="Test input", result="Test result")],
    )
    return okareo.create_scenario_set(scenario_set_create)


class CustomModelWithDict(CustomMultiturnTarget):
    def invoke(self, messages: Any) -> Any:  # type: ignore
        return ModelInvocation(
            "Invalid response", messages, {"result": "dict response"}
        )


class TestMultiturnErrors:
    """Tests for error paths in the MultiTurnDriver implementation."""

    def _create_basic_openai_target(self, temperature: float = 0) -> Any:
        """Helper method to create a basic OpenAI target model"""
        return OpenAIModel(
            model_id="gpt-4o-2024-11-20",
            temperature=temperature,
            system_prompt_template="test prompt",
        )

    def _create_basic_stop_check(self) -> Any:
        """Helper method to create a basic stop check configuration"""
        return {"check_name": "model_refusal", "stop_on": False}

    def _create_basic_api_keys(self) -> Any:
        """Helper method to create basic API keys configuration"""
        return {"openai": OPENAI_API_KEY, "driver": OPENAI_API_KEY}

    def _register_and_expect_error(
        self,
        okareo: Any,
        name: str,
        model_config: Any,
        expected_error: str,
        run_test: bool = False,
        basic_scenario: Any = None,
        api_keys: Any = None,
        checks: Any = None,
        sensitive_fields: Optional[list[str]] = None,
    ) -> None:
        """
        Helper method to register a model and optionally run a test, expecting an error.

        Args:
            okareo: Okareo instance
            name: Model name
            model_config: Configuration for MultiTurnDriver
            expected_error: Expected error message pattern
            run_test: Whether to run a test after registration
            basic_scenario: Scenario for test run
            api_keys: API keys for test run
            checks: Checks for test run
            sensitive_fields: Sensitive fields to redact in responses/error messages
        """
        if run_test:
            # Register model first, then run test and expect error
            mut = okareo.register_model(
                name=name,
                model=MultiTurnDriver(**model_config),
                update=True,
                sensitive_fields=sensitive_fields,
            )

            with pytest.raises(Exception, match=expected_error):
                mut.run_test(
                    scenario=basic_scenario,
                    api_keys=api_keys or self._create_basic_api_keys(),
                    name="Test Run",
                    test_run_type=TestRunType.MULTI_TURN,
                    checks=checks or ["model_refusal"],
                )
        else:
            # Expect error during registration
            with pytest.raises(Exception, match=expected_error):
                okareo.register_model(
                    name=name,
                    model=MultiTurnDriver(**model_config),
                    update=True,
                    sensitive_fields=sensitive_fields,
                )

    def test_missing_target(self, rnd: str, okareo: Any) -> None:
        """Test failure when target is missing"""
        model_config = {
            "max_turns": 2,
            "repeats": 1,
            "stop_check": self._create_basic_stop_check(),
            # target is missing
        }

        self._register_and_expect_error(
            okareo,
            f"Missing Target {rnd}",
            model_config,
            "missing 1 required positional argument: 'target'",
        )

    def test_invalid_first_turn(
        self, rnd: str, basic_scenario: Any, okareo: Any
    ) -> None:
        """Test failure when first_turn is invalid"""
        model_config = {
            "max_turns": 2,
            "repeats": 1,
            "target": self._create_basic_openai_target(),
            "first_turn": "invalid",  # Should be 'driver' or 'target'
            "stop_check": self._create_basic_stop_check(),
        }

        self._register_and_expect_error(
            okareo,
            f"Invalid First Turn {rnd}",
            model_config,
            "Invalid 'first_turn' value: 'invalid'. Must be either 'target' or 'driver'",
            run_test=True,
            basic_scenario=basic_scenario,
        )

    def test_missing_driver_api_key(
        self, rnd: str, okareo: Any, basic_scenario: Any
    ) -> None:
        """Test failure when driver API key is missing"""
        model_config = {
            "max_turns": 2,
            "repeats": 1,
            "driver_model_id": "gpt-4o",  # Specifying driver model but will miss API key
            "target": self._create_basic_openai_target(),
            "stop_check": self._create_basic_stop_check(),
        }

        self._register_and_expect_error(
            okareo,
            f"Missing Driver API Key {rnd}",
            model_config,
            "Missing 'driver' API key",
            run_test=True,
            basic_scenario=basic_scenario,
            api_keys={"openai": "test-key"},  # Missing driver key
        )

    def test_empty_stop_check(self, rnd: str, okareo: Any, basic_scenario: Any) -> None:
        """Test failure when no checks are provided"""
        model_config = {
            "max_turns": 2,
            "repeats": 1,
            "target": self._create_basic_openai_target(),
            "stop_check": {"check_name": "", "stop_on": False},
        }

        self._register_and_expect_error(
            okareo,
            f"Missing Checks {rnd}",
            model_config,
            "Invalid 'stop_check' configuration",
            run_test=True,
            basic_scenario=basic_scenario,
            checks=[],  # Empty list of checks
        )

    def test_invalid_stop_check(self, rnd: str, okareo: Any) -> None:
        """Test failure when stop_check is invalid"""
        model_config = {
            "max_turns": 2,
            "repeats": 1,
            "target": self._create_basic_openai_target(),
            "stop_check": {"invalid_field": "model_refusal"},  # Missing check_name
        }

        self._register_and_expect_error(
            okareo,
            f"Invalid Stop Check {rnd}",
            model_config,
            "got an unexpected keyword argument 'invalid_field'",
        )

    def test_invalid_temperature_values(
        self, rnd: str, basic_scenario: Any, okareo: Any
    ) -> None:
        """Test failure when temperature values are invalid"""
        temperature_test_cases: Any = [
            {
                "name": f"Invalid Driver Temp {rnd}",
                "config": {"driver_temperature": 5.0},  # Outside valid range
                "error": "Driver temperature must be between 0 and 2",
            },
            {
                "name": f"Invalid Target Temp {rnd}",
                "config": {
                    "target": self._create_basic_openai_target(temperature=3.0)
                },  # Outside valid range
                "error": "Target temperature must be between 0 and 2",
            },
            {
                "name": f"Non-Numeric Temp {rnd}",
                "config": {"driver_temperature": "hot"},  # Not a number
                "error": "Invalid driver_temperature value",
            },
        ]

        for test_case in temperature_test_cases:
            base_config = {
                "max_turns": 2,
                "repeats": 1,
                "target": self._create_basic_openai_target(),
                "stop_check": self._create_basic_stop_check(),
            }
            # Manually update the config to avoid type issues
            if "driver_temperature" in test_case["config"]:
                base_config["driver_temperature"] = test_case["config"][
                    "driver_temperature"
                ]
            if "target" in test_case["config"]:
                base_config["target"] = test_case["config"]["target"]

            self._register_and_expect_error(
                okareo,
                test_case["name"],  # type: ignore
                base_config,
                test_case["error"],  # type: ignore
                run_test=True,
                basic_scenario=basic_scenario,
            )

    def test_invalid_max_turns(
        self, rnd: str, basic_scenario: Any, okareo: Any
    ) -> None:
        """Test failure when max_turns is invalid"""
        max_turns_test_cases: Any = [
            {
                "name": f"Negative Max Turns {rnd}",
                "max_turns": 0,  # Zero value
                "error": "max_turns must be greater than 0",
            },
            {
                "name": f"Too High Max Turns {rnd}",
                "max_turns": 1000,  # Too high
                "error": "max_turns must be greater than 0 and less than 999",
            },
            {
                "name": f"Non-Integer Max Turns {rnd}",
                "max_turns": "many",  # Not an integer
                "error": "Invalid max_turns value",
            },
        ]

        for test_case in max_turns_test_cases:
            model_config = {
                "max_turns": test_case["max_turns"],
                "repeats": 1,
                "target": self._create_basic_openai_target(),
                "stop_check": self._create_basic_stop_check(),
            }

            self._register_and_expect_error(
                okareo,
                test_case["name"],
                model_config,
                test_case["error"],
                run_test=True,
                basic_scenario=basic_scenario,
            )

    def _create_custom_endpoint_configs(
        self,
        start_status_code: int = 201,
        next_status_code: int = 200,
        api_key: str = OKAREO_API_KEY,
    ) -> Any:
        """Helper method to create custom endpoint configurations"""
        api_headers = json.dumps(
            {"api-key": api_key, "Content-Type": "application/json"}
        )

        start_config = SessionConfig(
            url=f"{base_url}/v0/custom_endpoint_stub/create",
            method="POST",
            headers=api_headers,
            status_code=start_status_code,
            response_session_id_path="response.thread_id",
        )

        next_config = TurnConfig(
            url=f"{base_url}/v0/custom_endpoint_stub/message",
            method="POST",
            headers=api_headers,
            body=json.dumps(
                {"thread_id": "{session_id}", "message": "{latest_message}"}
            ),
            status_code=next_status_code,
            response_message_path="response.assistant_response",
        )

        end_config = SessionConfig(
            url=f"{base_url}/v0/custom_endpoint_stub/end",
            method="POST",
            headers=api_headers,
            body=json.dumps({"thread_id": "{session_id}"}),
            status_code=start_status_code,
        )

        return start_config, next_config, end_config

    def test_custom_endpoint_status_code_mismatch(
        self, rnd: str, basic_scenario: Any, okareo: Any
    ) -> None:
        """Test failure when expected status code doesn't match actual response status code"""
        # Create configs with mismatched status code
        start_config, next_config, end_config = self._create_custom_endpoint_configs(
            next_status_code=2000
        )  # Invalid status code

        model_config = {
            "max_turns": 2,
            "repeats": 1,
            "target": CustomEndpointTarget(start_config, next_config, end_config),
            "stop_check": self._create_basic_stop_check(),
        }

        self._register_and_expect_error(
            okareo,
            f"Status Code Mismatch {rnd}",
            model_config,
            "did not match expected status code",
            run_test=True,
            basic_scenario=basic_scenario,
            api_keys={"openai": OPENAI_API_KEY},
        )

    def test_custom_endpoint_sensitive_fields(
        self, rnd: str, basic_scenario: Any, okareo: Any
    ) -> None:
        """Test failure ensuring that sensitive fields are not leaked in error messages"""
        # Create configs with mismatched status code
        # Status code mismatch will be used to trigger an error, but assertions will target
        # the sensitive fields redaction in the error message.
        start_config, next_config, end_config = self._create_custom_endpoint_configs(
            start_status_code=2000
        )

        model_config = {
            "max_turns": 2,
            "repeats": 1,
            "target": CustomEndpointTarget(start_config, next_config, end_config),
            "stop_check": self._create_basic_stop_check(),
        }

        model_name = "Sensitive Fields Test " + rnd
        redacted_str = re.escape("*" * 16)
        exception_str_template = (
            "Response status code {status_code} did not match expected status code 2000. Response: .*. Request: [A-Z]+ https?://.*?, Headers: {'api-key': '"
            + redacted_str
            + "', 'Content-Type': 'application/json'}, Body: {}."
        )
        exception_str_match = exception_str_template.replace("{status_code}", "201")

        # Register the model with a custom endpoint that will fail.
        # Anticipate a redacted api-key
        self._register_and_expect_error(
            okareo,
            model_name,
            model_config,
            exception_str_match,
            run_test=True,
            basic_scenario=basic_scenario,
            api_keys={"openai": OPENAI_API_KEY},
            sensitive_fields=["api-key"],
        )

        # Register the model using redacted api-key field with same sensitive fields.
        # Anticipate same failure as above
        start_config, next_config, end_config = self._create_custom_endpoint_configs(
            start_status_code=2000, api_key="****************"
        )

        model_config = {
            "max_turns": 2,
            "repeats": 1,
            "target": CustomEndpointTarget(start_config, next_config, end_config),
            "stop_check": self._create_basic_stop_check(),
        }

        # Register the model with a custom endpoint that will fail.
        # Anticipate a redacted api-key
        self._register_and_expect_error(
            okareo,
            model_name,
            model_config,
            exception_str_match,
            run_test=True,
            basic_scenario=basic_scenario,
            api_keys={"openai": OPENAI_API_KEY},
            sensitive_fields=["api-key"],
        )

        # Register the model using redacted api-key field with api-key rm from sensitive fields.
        # Anticipate an auth error failure due to bad api-key
        exception_str_match = exception_str_template.replace("{status_code}", "401")
        self._register_and_expect_error(
            okareo,
            model_name,
            model_config,
            exception_str_match,
            run_test=True,
            basic_scenario=basic_scenario,
            api_keys={"openai": OPENAI_API_KEY},
            sensitive_fields=[],  # api-key should be overwritten with redacted string, causing 401
        )

    def test_nl_generation_missing_api_key(
        self, rnd: str, basic_scenario: Any, okareo: Any
    ) -> None:
        """Test failure when API keys are missing for NL_GENERATION test run"""
        target = self._create_basic_openai_target()
        model_name = f"Missing API Key NL Gen {rnd}"

        # Register the model
        mut = okareo.register_model(name=model_name, model=target, update=True)

        # Run test without providing api_keys
        with pytest.raises(Exception, match="Missing API"):
            mut.run_test(
                scenario=basic_scenario,
                name="Test Run",
                test_run_type=TestRunType.NL_GENERATION,
                checks=["coherence_summary"],
            )

    def test_nl_generation_no_checks(
        self, rnd: str, basic_scenario: Any, okareo: Any
    ) -> None:
        """Test failure when no checks are provided for NL_GENERATION test run"""
        target = self._create_basic_openai_target()
        model_name = f"No Checks NL Gen {rnd}"

        # Register the model
        mut = okareo.register_model(name=model_name, model=target, update=True)

        # Run test with empty checks list
        with pytest.raises(Exception, match="No checks were provided"):
            mut.run_test(
                scenario=basic_scenario,
                name="Test Run",
                test_run_type=TestRunType.NL_GENERATION,
                api_keys={"openai": OPENAI_API_KEY},
                checks=[],
            )

    def test_nl_generation_invalid_checks(
        self, rnd: str, basic_scenario: Any, okareo: Any
    ) -> None:
        """Test failure when no checks are provided for NL_GENERATION test run"""
        target = self._create_basic_openai_target()
        model_name = f"No Checks NL Gen {rnd}"

        # Register the model
        mut = okareo.register_model(name=model_name, model=target, update=True)

        # Run test with empty checks list
        with pytest.raises(
            Exception, match="One of more of the checks entered was invalid"
        ):
            mut.run_test(
                scenario=basic_scenario,
                name="Test Run",
                test_run_type=TestRunType.NL_GENERATION,
                api_keys={"openai": OPENAI_API_KEY},
                checks=["asdf"],
            )

    def test_custom_model_raises_value_error(self, rnd: str, okareo: Okareo) -> None:
        """Test failure when custom model raises a ValueError during invocation."""

        # Define a custom model that raises a ValueError
        class ErrorRaisingModel(CustomMultiturnTarget):
            def invoke(self, messages: list[dict[str, str]]) -> ModelInvocation:  # type: ignore
                # Always raise a ValueError with a specific message
                raise ValueError("This is a deliberate error from the custom model")

        # Create the model instance
        custom_model = ErrorRaisingModel(name=f"error_model_{rnd}")

        # Register the model with MultiTurnDriver
        model_under_test = okareo.register_model(
            name=f"Error Model Test {rnd}",
            model=MultiTurnDriver(
                driver_temperature=0.5,
                max_turns=3,
                repeats=1,
                target=custom_model,
                stop_check={"check_name": "model_refusal", "stop_on": False},
            ),
            update=True,
        )

        # Create a basic scenario
        seeds = [
            SeedData(
                input_="Hello, how are you today?",
                result="appropriate greeting response",
            ),
        ]

        scenario_set_create = ScenarioSetCreate(
            name=f"Error Model Test Scenario - {rnd}", seed_data=seeds
        )
        scenario = okareo.create_scenario_set(scenario_set_create)

        # Run the test and expect an error
        with pytest.raises(
            Exception, match="This is a deliberate error from the custom model"
        ):
            model_under_test.run_test(
                name=f"Error Model Test - {rnd}",
                api_key=OPENAI_API_KEY,
                scenario=scenario,
                test_run_type=TestRunType.MULTI_TURN,
                checks=["task_completed"],
            )

    def test_custom_model_parsing_error_from_return(
        self, rnd: str, okareo: Okareo
    ) -> None:
        """Test failure when custom model raises a ValueError during invocation."""

        # Define a custom model that raises a ValueError
        class ErrorRaisingModel(CustomMultiturnTarget):
            def invoke(self, messages: list[dict[str, str]]) -> Any:  # type: ignore
                # Always raise a ValueError with a specific message
                return "Not a modelinvocation object"

        # Create the model instance
        custom_model = ErrorRaisingModel(name=f"error_model_{rnd}")

        # Register the model with MultiTurnDriver
        model_under_test = okareo.register_model(
            name=f"Error Model Test {rnd}",
            model=MultiTurnDriver(
                driver_temperature=0.5,
                max_turns=3,
                repeats=1,
                target=custom_model,
                stop_check={"check_name": "model_refusal", "stop_on": False},
            ),
            update=True,
        )

        # Create a basic scenario
        seeds = [
            SeedData(
                input_="Hello, how are you today?",
                result="appropriate greeting response",
            ),
        ]

        scenario_set_create = ScenarioSetCreate(
            name=f"Error Model Test Scenario - {rnd}", seed_data=seeds
        )
        scenario = okareo.create_scenario_set(scenario_set_create)

        # Run the test and expect an error
        with pytest.raises(
            Exception,
            match="CustomModel did not return a response, or we were unable to parse it.",
        ):
            model_under_test.run_test(
                name=f"Error Model Test - {rnd}",
                api_key=OPENAI_API_KEY,
                scenario=scenario,
                test_run_type=TestRunType.MULTI_TURN,
                checks=[
                    "contains_all_imports",
                    "compression_ratio",
                    "are_all_params_expected",
                    "reverse_qa_quality",
                ],
            )

    def test_multiturn_error_checks(self, rnd: str, okareo: Okareo) -> None:
        """Test failure when invalid checks are provided for MULTI_TURN test run"""
        # Create a custom check that raises an error
        okareo.create_or_update_check(
            name="error_check",
            description="error_check",
            check=Check(),
        )

        # Create a basic multiturn model
        model_under_test = okareo.register_model(
            name=f"Error Check MT {rnd}",
            model=MultiTurnDriver(
                driver_temperature=0.5,
                max_turns=3,
                repeats=1,
                target=OpenAIModel(
                    model_id="gpt-4o-mini",
                    temperature=0,
                    system_prompt_template="test prompt",
                ),
                stop_check={"check_name": "model_refusal", "stop_on": False},
            ),
            update=True,
        )

        # Create a basic scenario
        seeds = [
            SeedData(
                input_="Test input",
                result="Test result",
            ),
        ]

        scenario_set_create = ScenarioSetCreate(
            name=f"Error Check Test Scenario - {rnd}", seed_data=seeds
        )
        scenario = okareo.create_scenario_set(scenario_set_create)

        # Run test with invalid check and expect error
        with pytest.raises(Exception, match="An error occurred while running checks"):
            model_under_test.run_test(
                scenario=scenario,
                name="Test Run",
                test_run_type=TestRunType.MULTI_TURN,
                api_keys={"openai": OPENAI_API_KEY},
                checks=["error_check"],
            )

    def test_openai_authentication_error(
        self, rnd: str, basic_scenario: Any, okareo: Any
    ) -> None:
        """Test failure when an invalid OpenAI API key is provided"""
        target = self._create_basic_openai_target()
        model_name = f"Invalid API Key Test {rnd}"

        # Register the model
        mut = okareo.register_model(name=model_name, model=target, update=True)

        # Run test with invalid API key and expect authentication error
        with pytest.raises(Exception, match="authentication"):
            mut.run_test(
                scenario=basic_scenario,
                name="Test Run",
                test_run_type=TestRunType.NL_GENERATION,
                api_keys={"openai": "test"},  # Invalid API key
                checks=["coherence_summary"],
            )
