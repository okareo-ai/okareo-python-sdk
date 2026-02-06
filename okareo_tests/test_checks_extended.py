"""Extended tests for Okareo checks functionality."""

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo_api_client.models import EvaluatorSpecRequest


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


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
