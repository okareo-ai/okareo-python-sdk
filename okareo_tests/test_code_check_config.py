"""Unit tests for CodeBasedCheck output-type resolution in check_config().

These run without a live server: they call check.check_config() directly and
assert the `type` value the SDK would send to the backend.
"""

import pytest
from okareo_tests.checks import (
    code_check_no_type,
    code_check_pass_fail,
    code_check_score,
    sample_check,
)


def test_explicit_pass_fail_maps_to_pass_fail() -> None:
    config = code_check_pass_fail.Check().check_config()
    assert config["type"] == "pass_fail"


def test_explicit_score_maps_to_score() -> None:
    config = code_check_score.Check().check_config()
    assert config["type"] == "score"


def test_primitive_bool_annotation_is_backward_compatible() -> None:
    # No check_type declared; a `-> bool` return annotation still resolves to "bool".
    config = sample_check.Check().check_config()
    assert config["type"] == "bool"


def test_check_response_without_check_type_raises() -> None:
    with pytest.raises(ValueError):
        code_check_no_type.Check().check_config()
