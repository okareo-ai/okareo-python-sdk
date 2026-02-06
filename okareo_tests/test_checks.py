import pytest
from okareo_tests.checks.sample_check import Check
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo_api_client.models import EvaluatorSpecRequest


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


def test_get_all_checks(okareo_client: Okareo) -> None:
    checks = okareo_client.get_all_checks()
    # iterate through all the checks and ensure they have required fields
    for check in checks:
        assert check.id
        assert check.name
        assert type(check.description) is str
        assert type(check.output_data_type) is str
        assert check.time_created
        assert isinstance(check.is_predefined, bool)
        # concurrency issues with this test when ran in parallel


def test_generate_and_create_check(okareo_client: Okareo) -> None:
    generate_request = EvaluatorSpecRequest(
        description="""
        Return True if the model_output is at least 20 characters long, otherwise return False.""",
        requires_scenario_input=False,
        requires_scenario_result=False,
        output_data_type="bool",
    )
    check = okareo_client.generate_check(generate_request)
    assert check.generated_code
    uploaded_check = okareo_client.create_or_update_check(
        name=f"test_create_check {random_string(5)}",
        description="Test check",
        check=Check(),
    )
    assert uploaded_check.id
    assert uploaded_check.name
    assert uploaded_check.is_predefined is False
    okareo_client.delete_check(uploaded_check.id, uploaded_check.name)


def test_upload_code_based_check_all_args(okareo_client: Okareo) -> None:
    check_arg_names = [
        "scenario_input",
        "model_input",
        "model_output",
        "metadata",
    ]
    for arg_name in check_arg_names:
        # dynamically import the Check class from the arg_name file
        module_name = f"okareo_tests.checks.{arg_name}_check"
        module = __import__(module_name, fromlist=["Check"])

        # upload the check
        check = okareo_client.create_or_update_check(
            name=f"test_upload_check_{arg_name} {random_string(5)}",
            description=f"Test check for {arg_name}",
            check=module.Check(),
        )

        # assert the check was created successfully
        assert check.id
        assert check.name
        assert check.is_predefined is False
        okareo_client.delete_check(check.id, check.name)


def test_check_update_blocks_malicious_code(okareo_client: Okareo) -> None:
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
