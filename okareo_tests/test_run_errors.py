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
    Driver,
    ModelInvocation,
    OpenAIModel,
    SessionConfig,
    Target,
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
    """Tests for error paths in the run_simulation implementation."""

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
        target_config: Any,
        expected_error: str,
        driver_config: Any = None,
        run_config: Any = None,
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
            target_config: Configuration for Target
            expected_error: Expected error message pattern
            driver_config: Configuration for Driver
            run_config: Configuration for test run
            run_test: Whether to run a test after registration
            basic_scenario: Scenario for test run
            api_keys: API keys for test run
            checks: Checks for test run
            sensitive_fields: Sensitive fields to redact in responses/error messages
        """

        if run_test:
            target = Target(**target_config)
            driver = Driver(**driver_config) if driver_config else None
            # Register target and driver
            target_mut = okareo.create_or_update_target(target)
            driver_mut = okareo.create_or_update_driver(driver) if driver else None

            extra_run_config = {
                "target": target_mut,
                "driver": driver_mut,
                "scenario": basic_scenario,
                "api_keys": api_keys or self._create_basic_api_keys(),
                "name": "Test Run",
                "checks": checks or ["model_refusal"],
                "sensitive_fields": sensitive_fields,
            }

            all_config = {**extra_run_config, **(run_config or {})}

            with pytest.raises(Exception, match=expected_error):
                okareo.run_simulation(**all_config)
        else:
            # Expect error during registration
            with pytest.raises(Exception, match=expected_error):
                target = Target(**target_config)
                driver = Driver(**driver_config) if driver_config else None
                # Register target and driver
                target_mut = okareo.create_or_update_target(target)
                driver_mut = okareo.create_or_update_driver(driver) if driver else None

    def test_missing_target(self, rnd: str, okareo: Any) -> None:
        """Test failure when target is missing"""
        target_config = {
            "name": f"Missing Target {rnd}"
            # target is missing
        }

        self._register_and_expect_error(
            okareo=okareo,
            target_config=target_config,
            expected_error=re.escape(
                "Target.__init__() missing 1 required positional argument: 'target'"
            ),
        )

    def test_invalid_first_turn(
        self, rnd: str, basic_scenario: Any, okareo: Any
    ) -> None:
        """Test failure when first_turn is invalid"""
        run_config = {
            "max_turns": 2,
            "repeats": 1,
            "first_turn": "invalid",  # Should be 'driver' or 'target'
            "stop_check": self._create_basic_stop_check(),
        }
        target_config = {
            "target": self._create_basic_openai_target(),
            "name": f"Invalid First Turn {rnd}",
        }

        self._register_and_expect_error(
            okareo,
            target_config=target_config,
            run_config=run_config,
            expected_error="Invalid 'first_turn' value: 'invalid'. Must be either 'target' or 'driver'",
            run_test=True,
            basic_scenario=basic_scenario,
        )

    def test_missing_driver_api_key(
        self, rnd: str, okareo: Any, basic_scenario: Any
    ) -> None:
        """Test failure when driver API key is missing"""
        run_config = {
            "max_turns": 2,
            "repeats": 1,
            "stop_check": self._create_basic_stop_check(),
        }

        target_config = {
            "target": self._create_basic_openai_target(),
            "name": f"Missing Driver API Key {rnd}",
        }

        driver_config = {
            "model_id": "gpt-4o",  # Specifying driver model but will miss API key
            "name": f"Missing Driver API Key {rnd}",
        }

        self._register_and_expect_error(
            okareo=okareo,
            target_config=target_config,
            driver_config=driver_config,
            run_config=run_config,
            expected_error="Missing 'driver' API key",
            run_test=True,
            basic_scenario=basic_scenario,
            api_keys={"openai": "test-key"},  # Missing driver key
        )

    def test_empty_stop_check(self, rnd: str, okareo: Any, basic_scenario: Any) -> None:
        """Test failure when no checks are provided"""
        run_config = {
            "max_turns": 2,
            "repeats": 1,
            "stop_check": {"check_name": "", "stop_on": False},
        }

        target_config = {
            "target": self._create_basic_openai_target(),
            "name": f"Missing Checks {rnd}",
        }

        self._register_and_expect_error(
            okareo=okareo,
            target_config=target_config,
            run_config=run_config,
            expected_error="Invalid 'stop_check' configuration",
            run_test=True,
            basic_scenario=basic_scenario,
            checks=[],  # Empty list of checks
        )

    def test_invalid_stop_check(self, rnd: str, okareo: Any) -> None:
        """Test failure when stop_check is invalid"""
        run_config = {
            "max_turns": 2,
            "repeats": 1,
            "stop_check": {"invalid_field": "model_refusal"},  # Missing check_name
        }

        target_config = {
            "target": self._create_basic_openai_target(),
            "name": f"Invalid Stop Check {rnd}",
        }

        self._register_and_expect_error(
            okareo=okareo,
            target_config=target_config,
            run_config=run_config,
            expected_error="got an unexpected keyword argument 'invalid_field'",
            run_test=True,
        )

    def test_invalid_temperature_values(
        self, rnd: str, basic_scenario: Any, okareo: Any
    ) -> None:
        """Test failure when temperature values are invalid"""
        temperature_test_cases: Any = [
            {
                "target_config": {
                    "target": self._create_basic_openai_target(),
                    "name": f"Invalid Driver Temp {rnd}",
                },
                "driver_config": {
                    "temperature": 5.0,
                    "name": f"Invalid Driver Temp {rnd}",
                },  # Outside valid range
                "error": "Driver temperature must be between 0 and 2",
                "run_test": True,
            },
            {
                "target_config": {
                    "name": f"Invalid Target Temp {rnd}",
                    "target": self._create_basic_openai_target(
                        temperature=3.0
                    ),  # Outside valid range
                },
                "error": "Target temperature must be between 0 and 2",
                "run_test": True,
            },
            {
                "target_config": {
                    "name": f"Non-Numeric Temp {rnd}",
                    "target": self._create_basic_openai_target(),
                },
                "driver_config": {
                    "temperature": "hot",
                    "name": f"Non-Numeric Temp {rnd}",
                },  # Not a number
                "error": "Invalid driver_temperature value: hot. Must be a number.",
                "run_test": False,  # This case is for driver config only, no run test
            },
        ]

        for test_case in temperature_test_cases:
            run_config = {
                "max_turns": 2,
                "repeats": 1,
                "stop_check": self._create_basic_stop_check(),
            }

            self._register_and_expect_error(
                okareo=okareo,
                target_config=test_case["target_config"],
                run_config=run_config,
                driver_config=test_case.get("driver_config"),
                expected_error=test_case["error"],  # type: ignore
                run_test=test_case["run_test"],
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

            target_config = {
                "name": test_case["name"],
                "target": self._create_basic_openai_target(),
            }

            run_config = {
                "max_turns": test_case["max_turns"],
                "repeats": 1,
                "stop_check": self._create_basic_stop_check(),
            }

            self._register_and_expect_error(
                okareo=okareo,
                target_config=target_config,
                run_config=run_config,
                expected_error=test_case["error"],
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

        target_config = {
            "target": CustomEndpointTarget(start_config, next_config, end_config),
            "name": f"Status Code Mismatch {rnd}",
        }

        run_config = {
            "max_turns": 2,
            "repeats": 1,
            "stop_check": self._create_basic_stop_check(),
        }

        self._register_and_expect_error(
            okareo=okareo,
            target_config=target_config,
            run_config=run_config,
            expected_error="did not match expected status code",
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

        run_config = {
            "max_turns": 2,
            "repeats": 1,
            "stop_check": self._create_basic_stop_check(),
        }

        target_config = {
            "name": "Sensitive Fields Test " + rnd,
            "target": CustomEndpointTarget(start_config, next_config, end_config),
        }
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
            okareo=okareo,
            target_config=target_config,
            run_config=run_config,
            expected_error=exception_str_match,
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

        run_config = {
            "max_turns": 2,
            "repeats": 1,
            "stop_check": self._create_basic_stop_check(),
        }

        target_config = {
            "target": CustomEndpointTarget(start_config, next_config, end_config),
            "name": "Sensitive Fields Test " + rnd,
        }

        exception_str_match = exception_str_template.replace("{status_code}", "201")
        # Register the model with a custom endpoint that will fail.
        # Anticipate a redacted api-key
        self._register_and_expect_error(
            okareo=okareo,
            target_config=target_config,
            run_config=run_config,
            expected_error=exception_str_match,
            run_test=True,
            basic_scenario=basic_scenario,
            api_keys={"openai": OPENAI_API_KEY},
            sensitive_fields=["api-key"],
        )

        # Register the model using redacted api-key field with api-key rm from sensitive fields.
        # Anticipate an auth error failure due to bad api-key
        exception_str_match = exception_str_template.replace("{status_code}", "401")
        self._register_and_expect_error(
            okareo=okareo,
            target_config=target_config,
            run_config=run_config,
            expected_error=exception_str_match,
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

        target = Target(
            name=f"Error Model Test {rnd}",
            target=custom_model,
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
            okareo.run_simulation(
                target=target,
                name=f"Error Model Test - {rnd}",
                api_key=OPENAI_API_KEY,
                scenario=scenario,
                max_turns=3,
                repeats=1,
                stop_check={"check_name": "model_refusal", "stop_on": False},
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

        target = Target(
            name=f"Error Model Test {rnd}",
            target=custom_model,
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
            okareo.run_simulation(
                target=target,
                name=f"Error Model Test - {rnd}",
                api_key=OPENAI_API_KEY,
                scenario=scenario,
                max_turns=3,
                repeats=1,
                stop_check={"check_name": "model_refusal", "stop_on": False},
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

        target = Target(
            name=f"Error Check MT {rnd}",
            target=OpenAIModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="test prompt",
            ),
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
            okareo.run_simulation(
                target=target,
                scenario=scenario,
                name="Test Run",
                max_turns=3,
                repeats=1,
                stop_check={"check_name": "model_refusal", "stop_on": False},
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
