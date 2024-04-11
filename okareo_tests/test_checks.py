import os
import random
import string
import tempfile
from datetime import datetime

import pytest
from okareo_tests.common import API_KEY

from okareo import Okareo
from okareo_api_client.models import EvaluatorSpecRequest

today_with_time = datetime.now().strftime("%m-%d %H:%M:%S")
PREDEFINED_CHECKS = [
    "levenshtein_distance",
    "levenshtein_distance_input",
    "compression_ratio",
    "does_code_compile",
    "contains_all_imports",
    "coherence_summary",
    "consistency_summary",
    "fluency_summary",
    "relevance_summary",
    "consistency",
    "coherence",
    "conciseness",
    "fluency",
    "uniqueness",
]


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


def test_get_all_checks(okareo_client: Okareo) -> None:
    checks = okareo_client.get_all_checks()
    check_names = [check.name for check in checks]
    # make sure all the predefined checks are present
    for predefined_check_name in PREDEFINED_CHECKS:
        assert predefined_check_name in check_names
    # iterate through all the checks and ensure they have required fields
    for check in checks:
        assert check.id
        assert check.name
        assert check.description
        assert check.time_created
        # test that we can get the detailed response for the check
        check_detailed = okareo_client.get_check(check.id)
        assert check_detailed.id
        assert check_detailed.name
        assert check_detailed.description
        assert check_detailed.requires_scenario_input is not None
        assert check_detailed.requires_scenario_result is not None
        assert check_detailed.time_created
        assert check_detailed.output_data_type
        if check_detailed.name not in PREDEFINED_CHECKS:
            assert check_detailed.code_contents


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
    random_string = "".join(random.choices(string.ascii_letters, k=5))
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "sample_check.py")
    with open(file_path, "w+") as file:
        file.write(check.generated_code)
    uploaded_check = okareo_client.upload_check(
        name=f"test_upload_check {random_string}",
        file_path=file_path,
        requires_scenario_input=False,
        requires_scenario_result=False,
        output_data_type="bool",
    )
    os.remove(file_path)
    assert uploaded_check.id
    assert uploaded_check.name
    okareo_client.delete_check(uploaded_check.id, uploaded_check.name)
