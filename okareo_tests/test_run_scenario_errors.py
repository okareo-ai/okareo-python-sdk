import tempfile
from datetime import datetime
from typing import Any

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo_api_client.models import ScenarioType
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData

# Create unique identifiers for test resources
today_with_time = datetime.now().strftime("%m-%d %H:%M:%S")
rnd_str = random_string(5)
unique_key = f"{rnd_str} {today_with_time}"


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


class TestScenarioExceptions:
    """Tests for error paths related to scenario creation and manipulation."""

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

    def test_name_validation_error(self, okareo_client: Okareo) -> None:
        """Test failure when scenario name is invalid"""
        scenario_set_create = ScenarioSetCreate(
            name="",  # Empty name should cause a validation error
            seed_data=[SeedData(input_="Test input", result="Test result")],
        )

        with pytest.raises(Exception, match="Scenario set name is invalid"):
            okareo_client.create_scenario_set(scenario_set_create)

    def test_duplicate_name(self, okareo_client: Okareo) -> None:
        """Test duplicate name handling"""
        unique_name = f"Test Duplicate Name {unique_key}"

        # First creation should succeed
        scenario_set_create = ScenarioSetCreate(
            name=unique_name,
            seed_data=[SeedData(input_="Test input", result="Test result")],
        )
        okareo_client.create_scenario_set(scenario_set_create)

        # Second creation with same name should return a warning
        # In this case, it shouldn't throw an exception but return the existing set
        response = okareo_client.create_scenario_set(scenario_set_create)
        assert (
            response.warning is not None
            and isinstance(response.warning, str)
            and "is already in use" in response.warning
        )

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

    def test_file_validation_error_empty(self, okareo_client: Okareo) -> None:
        """Test error when uploading an empty file"""
        with tempfile.NamedTemporaryFile(suffix=".jsonl") as empty_file:
            # File is empty by default
            with pytest.raises(Exception, match="is empty"):
                okareo_client.upload_scenario_set(
                    file_path=empty_file.name,
                    scenario_name=f"Test Empty File {unique_key}",
                )

    def test_file_validation_error_invalid_json(self, okareo_client: Okareo) -> None:
        """Test error when uploading a file with invalid JSON"""
        with tempfile.NamedTemporaryFile(suffix=".jsonl", mode="w") as invalid_file:
            invalid_file.write('{"input": "test", "result": "test"}\n')  # Valid line
            invalid_file.write('{"input": "test", result: invalid}\n')  # Invalid JSON
            invalid_file.flush()

            with pytest.raises(Exception, match="Invalid JSON"):
                okareo_client.upload_scenario_set(
                    file_path=invalid_file.name,
                    scenario_name=f"Test Invalid JSON {unique_key}",
                )

    def test_file_validation_error_missing_fields(self, okareo_client: Okareo) -> None:
        """Test error when uploading a file with missing required fields"""
        with tempfile.NamedTemporaryFile(
            suffix=".jsonl", mode="w"
        ) as missing_fields_file:
            missing_fields_file.write(
                '{"only_input": "test"}\n'
            )  # Missing result field
            missing_fields_file.write(
                '{"only_result": "test"}\n'
            )  # Missing input field
            missing_fields_file.flush()

            with pytest.raises(Exception, match="must have 'input' and 'result'"):
                okareo_client.upload_scenario_set(
                    file_path=missing_fields_file.name,
                    scenario_name=f"Test Missing Fields {unique_key}",
                )

    def test_generation_with_invalid_source(self, okareo_client: Okareo) -> None:
        """Test scenario generation with invalid source scenario ID"""
        with pytest.raises(Exception, match="not found"):
            okareo_client.generate_scenarios(
                source_scenario="00000000-0000-0000-0000-000000000000",  # Non-existent scenario ID
                name=f"Test Invalid Source {unique_key}",
                number_examples=2,
                generation_type=ScenarioType.REPHRASE_INVARIANT,
            )
