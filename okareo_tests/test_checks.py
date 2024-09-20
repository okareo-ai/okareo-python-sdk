import pytest
from okareo_tests.common import API_KEY, random_string
from okareo_tests.sample_check import Check

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
    okareo_client.delete_check(uploaded_check.id, uploaded_check.name)
