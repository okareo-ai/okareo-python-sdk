import json
import os
from typing import Any

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
    def invoke(self, messages: Any) -> Any:
        return ModelInvocation(
            "Invalid response", messages, {"result": "dict response"}
        )


class TestMultiturnErrors:
    """Tests for error paths in the MultiTurnDriver implementation."""

    def _create_basic_openai_target(self, temperature: float = 0) -> Any:
        """Helper method to create a basic OpenAI target model"""
        return OpenAIModel(
            model_id="gpt-4o-mini",
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
        """
        if run_test:
            # Register model first, then run test and expect error
            mut = okareo.register_model(
                name=name,
                model=MultiTurnDriver(**model_config),
                update=True,
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
        self, start_status_code: int = 201, next_status_code: int = 200
    ) -> Any:
        """Helper method to create custom endpoint configurations"""
        api_headers = json.dumps(
            {"api-key": OKAREO_API_KEY, "Content-Type": "application/json"}
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

        return start_config, next_config

    def test_invalid_custom_endpoint_response_path(
        self, rnd: str, basic_scenario: Any, okareo: Any
    ) -> None:
        """Test failure when response_session_id_path is invalid in CustomEndpointTarget"""
        # Create configs with invalid response path
        start_config, next_config = self._create_custom_endpoint_configs()
        start_config.response_session_id_path = "response"  # Invalid path

        model_config = {
            "max_turns": 2,
            "repeats": 1,
            "target": CustomEndpointTarget(start_config, next_config),
            "stop_check": self._create_basic_stop_check(),
        }

        self._register_and_expect_error(
            okareo,
            f"Invalid Response Path {rnd}",
            model_config,
            "Failed to parse response from custom endpoint",
            run_test=True,
            basic_scenario=basic_scenario,
            api_keys={"openai": OPENAI_API_KEY},
        )

    def test_custom_endpoint_status_code_mismatch(
        self, rnd: str, basic_scenario: Any, okareo: Any
    ) -> None:
        """Test failure when expected status code doesn't match actual response status code"""
        # Create configs with mismatched status code
        start_config, next_config = self._create_custom_endpoint_configs(
            next_status_code=2000
        )  # Invalid status code

        model_config = {
            "max_turns": 2,
            "repeats": 1,
            "target": CustomEndpointTarget(start_config, next_config),
            "stop_check": self._create_basic_stop_check(),
        }

        self._register_and_expect_error(
            okareo,
            f"Status Code Mismatch {rnd}",
            model_config,
            "Custom endpoint returned status_code .* which does not match expected status code",
            run_test=True,
            basic_scenario=basic_scenario,
            api_keys={"openai": OPENAI_API_KEY},
        )
