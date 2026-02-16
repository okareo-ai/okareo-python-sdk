import pytest
from okareo_tests.checks.sample_check import Check
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.checks import CheckOutputType
from okareo_api_client.api.default import (
    check_create_or_update_v0_check_create_or_update_post,
    check_delete_v0_check_check_id_delete,
    get_check_v0_check_check_id_get,
)
from okareo_api_client.models import EvaluatorSpecRequest
from okareo_api_client.models.body_check_delete_v0_check_check_id_delete import (
    BodyCheckDeleteV0CheckCheckIdDelete,
)
from okareo_api_client.models.check_create_update_schema import CheckCreateUpdateSchema
from okareo_api_client.models.check_create_update_schema_check_config import (
    CheckCreateUpdateSchemaCheckConfig,
)
from okareo_api_client.models.error_response import ErrorResponse
from okareo_api_client.models.evaluator_detailed_response import (
    EvaluatorDetailedResponse,
)
from okareo_api_client.types import Unset

BOOL_CODE = """\
from okareo.checks import CodeBasedCheck

class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str) -> bool:
        return True
"""

INT_CODE = """\
from okareo.checks import CodeBasedCheck

class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str) -> int:
        return 3
"""

FLOAT_CODE = """\
from okareo.checks import CodeBasedCheck

class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str) -> float:
        return 0.75
"""

CHECK_RESPONSE_BOOL_CODE = """\
from okareo.checks import CodeBasedCheck, CheckResponse

class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str) -> CheckResponse:
        return CheckResponse(score=True, explanation="ok")
"""

CHECK_RESPONSE_FLOAT_CODE = """\
from okareo.checks import CodeBasedCheck, CheckResponse

class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str) -> CheckResponse:
        return CheckResponse(score=0.75, explanation="test")
"""


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


def _parse_return_type(code: str) -> str:
    """Extract the return type annotation name from the evaluate method in code."""
    import ast

    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "evaluate":
            if node.returns is not None:
                if isinstance(node.returns, ast.Name):
                    return node.returns.id
                if isinstance(node.returns, ast.Attribute):
                    return node.returns.attr
    return "bool"


def _create_or_update_check(
    okareo_client: Okareo,
    name: str,
    code: str,
    check_id: str | None = None,
) -> EvaluatorDetailedResponse:
    """Helper to call POST /v0/check_create_or_update with raw code_contents."""
    annotation_type = _parse_return_type(code)
    check_config = CheckCreateUpdateSchemaCheckConfig.from_dict(
        {"code_contents": code, "type": annotation_type}
    )
    json_body = CheckCreateUpdateSchema(
        name=name,
        description="type inference test",
        check_config=check_config,
    )
    if check_id is not None:
        json_body["check_id"] = check_id

    response = check_create_or_update_v0_check_create_or_update_post.sync(
        client=okareo_client.client,
        api_key=okareo_client.api_key,
        json_body=json_body,
    )
    assert not isinstance(response, ErrorResponse), f"API error: {response}"
    assert isinstance(response, EvaluatorDetailedResponse)
    return response


def _get_check(okareo_client: Okareo, check_id: str) -> EvaluatorDetailedResponse:
    """Helper to call GET /v0/check/{check_id}."""
    response = get_check_v0_check_check_id_get.sync(
        client=okareo_client.client,
        api_key=okareo_client.api_key,
        check_id=check_id,
    )
    assert not isinstance(response, ErrorResponse), f"API error: {response}"
    assert isinstance(response, EvaluatorDetailedResponse)
    return response


def _delete_check(okareo_client: Okareo, check_id: str, name: str) -> None:
    """Helper to call DELETE /v0/check/{check_id}."""
    check_delete_v0_check_check_id_delete.sync(
        client=okareo_client.client,
        api_key=okareo_client.api_key,
        check_id=check_id,
        form_data=BodyCheckDeleteV0CheckCheckIdDelete.from_dict({"name": name}),
    )


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

    check_name = f"test_check_security_{random_string(5)}"

    # Create a legitimate check
    legitimate_check = okareo_client.create_or_update_check(
        name=check_name,
        description="Legitimate check for testing security",
        check=Check(),
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


def _assert_check_type(
    response: EvaluatorDetailedResponse, expected_type: CheckOutputType
) -> None:
    """Assert that both check_config['type'] and output_data_type match expected enum value."""
    assert not isinstance(response.check_config, Unset)
    assert response.check_config["type"] == expected_type.value, (
        f"Expected check_config['type'] == {expected_type.value!r}, "
        f"got {response.check_config['type']!r}"
    )
    assert response.output_data_type == expected_type.value, (
        f"Expected output_data_type == {expected_type.value!r}, "
        f"got {response.output_data_type!r}"
    )


def test_create_update_by_id_update_by_name_type_inference(
    okareo_client: Okareo,
) -> None:
    """Test: Create → Update by ID → Update by name with static normalization.

    Covers static normalization of raw Python types sent by the SDK:
    "bool" → "pass_fail", "int" → "score", "float" → "score".
    Tests create path, update-by-id path, and update-by-name path.
    """
    check_name = f"infer_type_test_{random_string(5)}"
    check_id = None

    try:
        # --- Step 1: Create with "bool" annotation → server normalizes to "pass_fail" ---
        create_resp = _create_or_update_check(okareo_client, check_name, BOOL_CODE)
        assert isinstance(create_resp.id, str)
        check_id = create_resp.id
        _assert_check_type(create_resp, CheckOutputType.PASS_FAIL)

        # --- Step 2: GET and verify pass_fail persisted ---
        get_resp = _get_check(okareo_client, check_id)
        _assert_check_type(get_resp, CheckOutputType.PASS_FAIL)

        # --- Step 3: Update by check_id with "int" annotation → server normalizes to "score" ---
        update_by_id_resp = _create_or_update_check(
            okareo_client, check_name, INT_CODE, check_id=check_id
        )
        _assert_check_type(update_by_id_resp, CheckOutputType.SCORE)

        # --- Step 4: GET and verify score persisted ---
        get_resp = _get_check(okareo_client, check_id)
        _assert_check_type(get_resp, CheckOutputType.SCORE)

        # --- Step 5: Update by name with "float" annotation → server normalizes to "score" ---
        update_by_name_resp = _create_or_update_check(
            okareo_client, check_name, FLOAT_CODE
        )
        _assert_check_type(update_by_name_resp, CheckOutputType.SCORE)

        # --- Step 6: GET and verify score persisted ---
        get_resp = _get_check(okareo_client, check_id)
        _assert_check_type(get_resp, CheckOutputType.SCORE)

    finally:
        if check_id is not None:
            _delete_check(okareo_client, check_id, check_name)


def test_check_response_runtime_type_inference(
    okareo_client: Okareo,
) -> None:
    """Test runtime type inference when SDK sends "CheckResponse".

    When the SDK sends type="CheckResponse" (not in the static map),
    the server falls back to runtime inference from the actual score value:
    CheckResponse(score=True) → "pass_fail", CheckResponse(score=0.75) → "score".
    """
    check_name = f"infer_cr_test_{random_string(5)}"
    check_id = None

    try:
        # --- Step 1: Create with CheckResponse(score=True) → runtime infers "pass_fail" ---
        create_resp = _create_or_update_check(
            okareo_client, check_name, CHECK_RESPONSE_BOOL_CODE
        )
        assert isinstance(create_resp.id, str)
        check_id = create_resp.id
        _assert_check_type(create_resp, CheckOutputType.PASS_FAIL)

        # --- Step 2: Update with CheckResponse(score=0.75) → runtime infers "score" ---
        update_resp = _create_or_update_check(
            okareo_client, check_name, CHECK_RESPONSE_FLOAT_CODE, check_id=check_id
        )
        _assert_check_type(update_resp, CheckOutputType.SCORE)

        # --- Step 3: GET and verify score persisted ---
        get_resp = _get_check(okareo_client, check_id)
        _assert_check_type(get_resp, CheckOutputType.SCORE)

    finally:
        if check_id is not None:
            _delete_check(okareo_client, check_id, check_name)
