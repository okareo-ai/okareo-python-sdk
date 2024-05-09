import os
import tempfile

import pytest
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
        # test that we can get the detailed response for the check
        check_detailed = okareo_client.get_check(check.id)
        assert check_detailed.id
        assert check_detailed.name
        assert type(check_detailed.description) is str
        assert type(check_detailed.output_data_type) is str
        assert check_detailed.requires_scenario_input is not None
        assert check_detailed.requires_scenario_result is not None
        assert check_detailed.time_created


def test_generate_and_upload_check(okareo_client: Okareo) -> None:
    generate_request = EvaluatorSpecRequest(
        description="""
        Return True if the model_output is at least 20 characters long, otherwise return False.""",
        requires_scenario_input=False,
        requires_scenario_result=False,
        output_data_type="bool",
    )
    check = okareo_client.generate_check(generate_request)
    assert check.generated_code
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "sample_check.py")
    with open(file_path, "w+") as file:
        file.write(check.generated_code)
    uploaded_check = okareo_client.upload_check(
        name=f"test_upload_check {random_string(5)}",
        file_path=file_path,
        requires_scenario_input=False,
        requires_scenario_result=False,
        output_data_type="bool",
    )
    os.remove(file_path)
    assert uploaded_check.id
    assert uploaded_check.name
    okareo_client.delete_check(uploaded_check.id, uploaded_check.name)
