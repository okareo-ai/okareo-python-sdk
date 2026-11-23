from datetime import datetime
from typing import Any

import pytest
from okareo_tests.common import random_string
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData

# Create unique identifiers for test resources
today_with_time = datetime.now().strftime("%m-%d %H:%M:%S")
rnd_str = random_string(5)
unique_key = f"{rnd_str} {today_with_time}"


@pytest.fixture
def okareo_client(httpx_mock: HTTPXMock) -> Okareo:
    httpx_mock.add_response(
        json=[
            {
                "id": "0156f5d7-4ac4-4568-9d44-24750aa08d1a",
                "name": "Global",
                "onboarding_status": "onboarding_status",
                "tags": [],
                "additional_properties": {},
            }
        ],
        status_code=201,
    )
    return Okareo("api-key", "http://mocked.com")


class TestScenarioExceptions:
    """Tests for the errors the SDK raises itself when creating a scenario."""

    def test_seed_data_missing(self, okareo_client: Okareo) -> None:
        """Test failure when seed data is missing"""
        scenario_set_create = ScenarioSetCreate(
            name=f"Test Missing Seed Data {unique_key}",
            seed_data=[],  # Empty seed data should cause an error
        )

        with pytest.raises(
            Exception, match="Non-empty seed data is required to create a scenario set"
        ):
            okareo_client.create_scenario_set(scenario_set_create)

    def test_seed_data_processing_error(self, okareo_client: Okareo) -> None:
        """Test failure when there's an error processing seed data"""
        # Create problematic seed data structure
        # Using a nested structure that's too complex or has circular references
        complex_input: Any = {"data": {"nested": {"more_nested": {"circular": {}}}}}
        complex_input["data"]["nested"]["more_nested"][
            "circular"
        ] = complex_input  # Create circular reference

        try:
            # This should fail during JSON serialization
            scenario_set_create = ScenarioSetCreate(
                name=f"Test Processing Error {unique_key}",
                seed_data=[SeedData(input_=complex_input, result="Test result")],
            )
            okareo_client.create_scenario_set(scenario_set_create)
            pytest.fail("Expected exception was not raised")
        except Exception:
            # Either a client-side serialization error or server-side processing error
            assert True
