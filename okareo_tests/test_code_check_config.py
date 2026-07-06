"""Unit tests for CodeBasedCheck.check_config().

These run without a live server. The SDK no longer declares an output type for
code-based checks: check_config() emits only `code_contents`, and the server
infers pass/fail vs. score from the check's runtime return value at persist time.
"""

from okareo_tests.checks import (
    code_check_pass_fail,
    code_check_score,
    sample_check,
)


def test_check_config_emits_code_contents_and_no_type() -> None:
    config = code_check_pass_fail.Check().check_config()
    assert "code_contents" in config
    assert "type" not in config


def test_check_response_check_without_type_does_not_raise() -> None:
    # A CheckResponse-returning check with no type declaration is valid now;
    # the server infers the output type from the runtime value.
    config = code_check_score.Check().check_config()
    assert "code_contents" in config
    assert "type" not in config


def test_primitive_annotation_check_emits_no_type() -> None:
    # A `-> bool` check no longer sends a derived "type" either.
    config = sample_check.Check().check_config()
    assert "code_contents" in config
    assert "type" not in config
