import json
from typing import Any, Union

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import CustomModel, ModelInvocation
from okareo_api_client.api.default import delete_test_run_v0_test_runs_delete
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_type import TestRunType


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


SEED_DATA = [
    SeedData(
        input_="The quick brown fox jumps over the lazy dog",
        result="A fox jumps over a dog",
    ),
    SeedData(
        input_="Machine learning models require training data", result="ML needs data"
    ),
    SeedData(
        input_="The weather forecast predicts rain tomorrow",
        result="Rain expected tomorrow",
    ),
    SeedData(
        input_="Python is a popular programming language", result="Python is popular"
    ),
    SeedData(
        input_="Statistical testing validates hypotheses",
        result="Stats validates hypotheses",
    ),
]


class ControlModel(CustomModel):
    """Returns JSON output — is_json will pass, levenshtein and compression_ratio will differ from variant."""

    def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
        return ModelInvocation(
            model_prediction=json.dumps({"summary": str(input_value)[:20]}),
            model_input=input_value,
        )


class VariantModel(CustomModel):
    """Returns plain text — is_json will fail, different numeric check values than control."""

    def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
        return ModelInvocation(
            model_prediction=f"Summary: {str(input_value)[:50]}",
            model_input=input_value,
        )


@pytest.fixture(scope="module")
def scenario_set(rnd: str, okareo: Okareo) -> Any:
    return okareo.create_scenario_set(
        ScenarioSetCreate(
            name=f"compare-e2e-scenario-{rnd}",
            seed_data=SEED_DATA,
        )
    )


@pytest.fixture(scope="module")
def control_run(rnd: str, okareo: Okareo, scenario_set: Any) -> Any:
    mut = okareo.register_model(
        name=f"compare-e2e-control-{rnd}",
        model=ControlModel(name=f"compare-e2e-control-{rnd}"),
    )
    return mut.run_test(
        name=f"compare-e2e-control-run-{rnd}",
        scenario=scenario_set,
        test_run_type=TestRunType.NL_GENERATION,
        checks=["is_json", "levenshtein_distance", "compression_ratio"],
    )


@pytest.fixture(scope="module")
def variant_run(rnd: str, okareo: Okareo, scenario_set: Any) -> Any:
    mut = okareo.register_model(
        name=f"compare-e2e-variant-{rnd}",
        model=VariantModel(name=f"compare-e2e-variant-{rnd}"),
    )
    return mut.run_test(
        name=f"compare-e2e-variant-run-{rnd}",
        scenario=scenario_set,
        test_run_type=TestRunType.NL_GENERATION,
        checks=["is_json", "levenshtein_distance", "compression_ratio"],
    )


def _compare_test_runs(
    okareo: Okareo, control_id: str, variant_id: str, alpha: float = 0.05
) -> dict[str, Any]:
    """Call POST /v0/test_runs/compare directly via the client's httpx instance."""
    response = okareo.client.get_httpx_client().request(
        method="post",
        url="/v0/test_runs/compare",
        json={
            "control_test_run_id": str(control_id),
            "variant_test_run_id": str(variant_id),
            "alpha": alpha,
        },
        headers={"api-key": okareo.api_key, "Content-Type": "application/json"},
    )
    assert (
        response.status_code == 200
    ), f"Compare endpoint returned {response.status_code}: {response.text}"
    data: dict[str, Any] = response.json()
    return data


def test_compare_returns_correct_structure(
    okareo: Okareo, control_run: Any, variant_run: Any
) -> None:
    result = _compare_test_runs(okareo, control_run.id, variant_run.id)

    assert result["control_test_run_id"] == str(control_run.id)
    assert result["variant_test_run_id"] == str(variant_run.id)

    assert "scenarios" in result
    assert "statistical_tests" in result


def test_compare_scenarios_match_seed_count(
    okareo: Okareo, control_run: Any, variant_run: Any
) -> None:
    result = _compare_test_runs(okareo, control_run.id, variant_run.id)

    scenarios = result["scenarios"]
    assert len(scenarios) == len(SEED_DATA)

    for scenario in scenarios:
        assert "scenario_data_point_id" in scenario
        assert "control_checks" in scenario
        assert "variant_checks" in scenario
        assert scenario["control_repeat_count"] >= 1
        assert scenario["variant_repeat_count"] >= 1


def test_compare_binary_checks(
    okareo: Okareo, control_run: Any, variant_run: Any
) -> None:
    result = _compare_test_runs(okareo, control_run.id, variant_run.id)
    stats = result["statistical_tests"]

    assert stats["matched_scenario_count"] == len(SEED_DATA)
    assert stats["correction_method"] == "benjamini-hochberg"
    assert stats["alpha"] == 0.05

    binary_checks = stats["binary_checks"]
    is_json_check = next((c for c in binary_checks if c["name"] == "is_json"), None)
    assert (
        is_json_check is not None
    ), f"is_json not found in binary_checks: {binary_checks}"

    assert is_json_check["check_type"] == "binary"
    assert 0.0 <= is_json_check["control_pass_rate"] <= 1.0
    assert 0.0 <= is_json_check["variant_pass_rate"] <= 1.0
    assert is_json_check["control_pass_rate"] > is_json_check["variant_pass_rate"]
    assert isinstance(is_json_check["improvements"], int)
    assert isinstance(is_json_check["regressions"], int)
    assert isinstance(is_json_check["concordant_pass"], int)
    assert isinstance(is_json_check["concordant_fail"], int)
    assert 0.0 <= is_json_check["p_value"] <= 1.0
    assert 0.0 <= is_json_check["p_value_adjusted"] <= 1.0
    assert isinstance(is_json_check["significant"], bool)


def test_compare_numeric_checks(
    okareo: Okareo, control_run: Any, variant_run: Any
) -> None:
    result = _compare_test_runs(okareo, control_run.id, variant_run.id)
    stats = result["statistical_tests"]

    numeric_checks = stats["numeric_checks"]
    check_names = {c["name"] for c in numeric_checks}
    assert (
        "levenshtein_distance" in check_names
    ), f"levenshtein_distance not in {check_names}"
    assert "compression_ratio" in check_names, f"compression_ratio not in {check_names}"

    for check in numeric_checks:
        assert check["check_type"] == "numeric"
        assert isinstance(check["control_summary"], (int, float))
        assert isinstance(check["variant_summary"], (int, float))
        assert isinstance(check["mean_diff"], (int, float))
        assert 0.0 <= check["p_value"] <= 1.0
        assert 0.0 <= check["p_value_adjusted"] <= 1.0
        assert isinstance(check["significant"], bool)


def test_compare_bh_correction_applied(
    okareo: Okareo, control_run: Any, variant_run: Any
) -> None:
    """BH correction adjusts p-values upward; adjusted should be >= raw for at least one check."""
    result = _compare_test_runs(okareo, control_run.id, variant_run.id)
    stats = result["statistical_tests"]

    all_checks = stats["binary_checks"] + stats["numeric_checks"]
    assert len(all_checks) >= 3

    for check in all_checks:
        assert check["p_value_adjusted"] >= check["p_value"] - 1e-10


def test_compare_cleanup(okareo: Okareo, control_run: Any, variant_run: Any) -> None:
    """Cleanup test runs after all comparison tests complete."""
    for run in [control_run, variant_run]:
        delete_test_run_v0_test_runs_delete.sync(
            client=okareo.client,
            test_run_ids=[run.id],
            api_key=API_KEY,
        )
