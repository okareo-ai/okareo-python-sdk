"""Extended tests for Okareo checks functionality."""

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.checks import CheckOutputType, ModelBasedCheck
from okareo_api_client.models import EvaluatorSpecRequest


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


class TestCheckRetrieval:
    """Tests for retrieving checks."""

    def test_get_all_checks_returns_list(self, okareo_client: Okareo) -> None:
        """Test that get_all_checks returns a non-empty list."""
        checks = okareo_client.get_all_checks()
        assert isinstance(checks, list)
        assert len(checks) > 0

    def test_get_all_checks_structure(self, okareo_client: Okareo) -> None:
        """Test that each check has the expected fields."""
        checks = okareo_client.get_all_checks()
        for check in checks:
            assert hasattr(check, "id")
            assert hasattr(check, "name")
            assert hasattr(check, "description")
            assert hasattr(check, "output_data_type")
            assert hasattr(check, "time_created")
            assert hasattr(check, "is_predefined")
            # Verify types
            assert isinstance(check.id, str)
            assert isinstance(check.name, str)
            assert isinstance(check.description, str)
            assert isinstance(check.output_data_type, str)
            assert isinstance(check.is_predefined, bool)

    def test_predefined_checks_exist(self, okareo_client: Okareo) -> None:
        """Test that predefined checks are available."""
        checks = okareo_client.get_all_checks()
        predefined_checks = [c for c in checks if c.is_predefined]
        assert len(predefined_checks) > 0

        # Verify some common predefined checks exist
        check_names = [c.name for c in predefined_checks]
        expected_checks = ["levenshtein_distance", "is_json", "latency"]
        for expected in expected_checks:
            assert (
                expected in check_names
            ), f"Expected predefined check '{expected}' not found"


# Note: Code-based check tests are in test_checks.py, which uses separate check files
# to avoid module source contamination issues with inline check definitions.


class TestModelBasedChecks:
    """Tests for model-based check creation."""

    def test_create_model_based_pass_fail_check(self, okareo_client: Okareo) -> None:
        """Test creating a model-based pass/fail check."""
        check_name = f"test_model_pass_fail_{random_string(8)}"

        check = okareo_client.create_or_update_check(
            name=check_name,
            description="Model-based pass/fail check",
            check=ModelBasedCheck(
                prompt_template="Is the following text grammatically correct? Answer only True or False: {generation}",
                check_type=CheckOutputType.PASS_FAIL,
            ),
        )

        assert isinstance(check.id, str)
        assert check.name == check_name
        assert isinstance(check.name, str)
        assert check.is_predefined is False

        # Cleanup
        okareo_client.delete_check(check.id, check.name)

    def test_create_model_based_score_check(self, okareo_client: Okareo) -> None:
        """Test creating a model-based score check."""
        check_name = f"test_model_score_{random_string(8)}"

        check = okareo_client.create_or_update_check(
            name=check_name,
            description="Model-based score check",
            check=ModelBasedCheck(
                prompt_template="Rate the quality of this response from 1-10: {generation}",
                check_type=CheckOutputType.SCORE,
            ),
        )

        assert isinstance(check.id, str)
        assert check.name == check_name
        assert isinstance(check.name, str)
        assert check.is_predefined is False

        # Cleanup
        okareo_client.delete_check(check.id, check.name)

    def test_model_based_check_with_multiple_placeholders(
        self, okareo_client: Okareo
    ) -> None:
        """Test creating a check that uses multiple template placeholders."""
        check_name = f"test_model_multi_{random_string(8)}"

        check = okareo_client.create_or_update_check(
            name=check_name,
            description="Check with multiple placeholders",
            check=ModelBasedCheck(
                prompt_template="Does the {generation} accurately address the question: {scenario_input}? Answer True or False.",
                check_type=CheckOutputType.PASS_FAIL,
            ),
        )

        assert isinstance(check.id, str)
        assert check.name == check_name
        assert isinstance(check.name, str)

        # Cleanup
        okareo_client.delete_check(check.id, check.name)


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
        # Check should contain the evaluate method
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
        # Generated code should reference scenario_input
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
        # Generated code should reference scenario_result
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


class TestCheckValidationFailures:
    """Tests for check validation failures."""

    def test_check_with_disallowed_import_fails(self, okareo_client: Okareo) -> None:
        """Test that uploading a check with disallowed import (os) fails validation."""
        from okareo_tests.checks.invalid_os_check import Check

        check_name = f"test_invalid_check_{random_string(8)}"

        with pytest.raises(Exception) as exc_info:
            okareo_client.create_or_update_check(
                name=check_name,
                description="Check with disallowed os import",
                check=Check(),
            )

        # Verify the error message mentions the import issue
        error_msg = str(exc_info.value).lower()
        assert "import" in error_msg or "not allowed" in error_msg or "os" in error_msg


class TestComplexCheckValidation:
    """Tests for complex checks passing validation."""

    def test_complex_ast_validator_check_passes(self, okareo_client: Okareo) -> None:
        """Test that a complex check (function call AST validator) passes validation."""
        from okareo_tests.checks.function_call_ast_validator import Check

        check_name = f"test_ast_validator_{random_string(8)}"

        check = okareo_client.create_or_update_check(
            name=check_name,
            description="Complex function call AST validator check",
            check=Check(),
        )

        assert isinstance(check.id, str)
        assert check.name == check_name
        assert isinstance(check.name, str)
        assert check.is_predefined is False

        # Cleanup
        okareo_client.delete_check(check.id, check.name)
