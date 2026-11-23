import os
import re
from typing import Any, Optional

import httpx
import pytest
from okareo_tests.common import random_string
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo.model_under_test import Driver, OpenAIModel, Target

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "NOT SET")

MOCK_UUID = "0156f5d7-4ac4-4568-9d44-24750aa08d1a"


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


MOCK_ANSWERS = {
    ("GET", "/v0/projects"): [
        {
            "id": MOCK_UUID,
            "name": "Global",
            "onboarding_status": "onboarding_status",
            "tags": [],
            "additional_properties": {},
        }
    ],
    ("POST", "/v0/register_model"): {
        "id": MOCK_UUID,
        "project_id": MOCK_UUID,
        "version": 1,
        "name": "mocked target",
        "tags": [],
        "time_created": "2026-11-23T00:00:00",
    },
}


@pytest.fixture
def okareo(httpx_mock: HTTPXMock) -> Okareo:
    """A client on a mocked host that answers the Project list and a Target registration.

    One callback answers both, so a test that fails before registering a Target leaves nothing unrequested.
    """

    def answer(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            201, json=MOCK_ANSWERS[(request.method, request.url.path)]
        )

    httpx_mock.add_callback(answer)
    return Okareo("api-key", "http://mocked.com")


class TestMultiturnErrors:
    """Tests for the errors the SDK raises itself, before a Simulation reaches the server."""

    def _create_basic_openai_target(self, temperature: float = 0) -> Any:
        """Helper method to create a basic OpenAI target model"""
        return OpenAIModel(
            model_id="gpt-4o-2024-11-20",
            temperature=temperature,
            system_prompt_template="test prompt",
        )

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

    def test_invalid_temperature_values(self, rnd: str, okareo: Any) -> None:
        """Test failure when the Driver temperature is not a number"""
        self._register_and_expect_error(
            okareo=okareo,
            target_config={
                "name": f"Non-Numeric Temp {rnd}",
                "target": self._create_basic_openai_target(),
            },
            driver_config={
                "temperature": "hot",
                "name": f"Non-Numeric Temp {rnd}",
            },  # Not a number
            expected_error="Invalid driver_temperature value: hot. Must be a number.",
        )
