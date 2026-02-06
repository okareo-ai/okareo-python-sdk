"""Extended tests for Okareo checks functionality."""

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo_api_client.models import EvaluatorSpecRequest


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


class TestCheckGeneration:
    """Tests for AI-generated check creation."""

    def test_generate_check_bool_output(self, okareo_client: Okareo) -> None:
        """Test generating a check with boolean output."""
        generate_request = EvaluatorSpecRequest(
            description="Return True if the model_output contains the word 'hello', otherwise return False.",
            requires_scenario_input=False,
            requires_scenario_result=False,
            output_data_type="bool",
        )

        check = okareo_client.generate_check(generate_request)

        assert check.generated_code is not None
        assert isinstance(check.generated_code, str)
        assert len(check.generated_code) > 0
        assert "def evaluate" in check.generated_code
        assert "bool" in check.generated_code

    def test_generate_check_with_scenario_input(self, okareo_client: Okareo) -> None:
        """Test generating a check that requires scenario_input."""
        generate_request = EvaluatorSpecRequest(
            description="Return True if the model_output is longer than the scenario_input.",
            requires_scenario_input=True,
            requires_scenario_result=False,
            output_data_type="bool",
        )

        check = okareo_client.generate_check(generate_request)

        assert check.generated_code is not None
        assert isinstance(check.generated_code, str)
        assert "scenario_input" in check.generated_code

    def test_generate_check_with_scenario_result(self, okareo_client: Okareo) -> None:
        """Test generating a check that requires scenario_result."""
        generate_request = EvaluatorSpecRequest(
            description="Return True if the model_output matches the scenario_result.",
            requires_scenario_input=False,
            requires_scenario_result=True,
            output_data_type="bool",
        )

        check = okareo_client.generate_check(generate_request)

        assert check.generated_code is not None
        assert isinstance(check.generated_code, str)
        assert "scenario_result" in check.generated_code

    def test_generate_check_with_all_inputs(self, okareo_client: Okareo) -> None:
        """Test generating a check that uses all available inputs."""
        generate_request = EvaluatorSpecRequest(
            description="Return a score from 0-100 based on how well the model_output addresses the scenario_input compared to the scenario_result.",
            requires_scenario_input=True,
            requires_scenario_result=True,
            output_data_type="int",
        )

        check = okareo_client.generate_check(generate_request)

        assert check.generated_code is not None
        assert isinstance(check.generated_code, str)
        assert "scenario_input" in check.generated_code
        assert "scenario_result" in check.generated_code
        assert "int" in check.generated_code or "float" in check.generated_code


class TestCheckSecurity:
    """Tests for check security validation."""

    def test_check_update_blocks_malicious_code(self, okareo_client: Okareo) -> None:
        """Test that updating a check with malicious code is properly rejected."""
        from okareo_tests.checks.malicious_check import Check as MaliciousCheck
        from okareo_tests.checks.sample_check import Check as SampleCheck

        check_name = f"test_check_security_{random_string(5)}"

        # Create a legitimate check
        legitimate_check = okareo_client.create_or_update_check(
            name=check_name,
            description="Legitimate check for testing security",
            check=SampleCheck(),
        )

        assert legitimate_check.id
        assert legitimate_check.name == check_name

        # Try to update it with malicious code - should fail
        with pytest.raises(Exception) as exc_info:
            okareo_client.create_or_update_check(
                name=check_name,
                description="Attempting to update with malicious code",
                check=MaliciousCheck(),
            )

        # Verify the error indicates the security violation
        error_message = str(exc_info.value).lower()
        assert any(
            keyword in error_message
            for keyword in [
                "forbidden",
                "blocked",
                "not allowed",
                "security",
                "validation",
                "disallowed",
            ]
        ), f"Expected security-related error, got: {exc_info.value}"

        # Cleanup
        if legitimate_check.name:
            okareo_client.delete_check(legitimate_check.id, legitimate_check.name)
