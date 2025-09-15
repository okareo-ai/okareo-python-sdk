import datetime
from typing import List, Union

from litellm import token_counter

from okareo import Okareo
from okareo.model_under_test import ModelUnderTest, Target
from okareo_api_client.models.find_test_data_point_payload import (
    FindTestDataPointPayload,
)
from okareo_api_client.models.full_data_point_item import FullDataPointItem
from okareo_api_client.models.full_data_point_item_baseline_metrics import (
    FullDataPointItemBaselineMetrics,
)
from okareo_api_client.models.full_data_point_item_checks_metadata import (
    FullDataPointItemChecksMetadata,
)
from okareo_api_client.models.model_under_test_response import (
    ModelUnderTestResponse,
)
from okareo_api_client.models.test_data_point_item import TestDataPointItem
from okareo_api_client.models.test_run_item import TestRunItem
from okareo_api_client.types import Unset


def assert_scores_geval(scores: dict) -> None:
    dimension_keys = [
        "consistency_summary",
        "coherence_summary",
        "fluency_summary",
        "relevance_summary",
    ]
    for dimension in dimension_keys:
        assert dimension in scores
        assert isinstance(scores[dimension], float)
        # Due to the imprecision of logprob calculation and python floats, the value can sometimes be 5.0000000000001
        assert 1 <= scores[dimension] <= 5.001


def assert_scores(scores: dict, custom_dimensions: List[str]) -> None:
    # Assert non-explanation scores specified in 'custom_dimensions' are present in 'scores'
    dimension_keys = custom_dimensions
    skip_keys = ["scenario_index", "test_id"]
    assert len(dimension_keys) == len(
        [k for k in scores.keys() if k not in skip_keys and "__explanation" not in k]
    )
    for dimension in dimension_keys:
        assert dimension in scores


def assert_metrics(
    run_resp: TestRunItem,
    custom_dimensions: Union[List[str], None] = None,
    num_rows: int = 3,
) -> None:
    assert run_resp.model_metrics is not None and not isinstance(
        run_resp.model_metrics, Unset
    )
    metrics_dict = run_resp.model_metrics.to_dict()

    assert metrics_dict["mean_scores"] is not None
    if custom_dimensions is not None:
        assert_scores(metrics_dict["mean_scores"], custom_dimensions)
    else:
        assert_scores_geval(metrics_dict["mean_scores"])
    assert metrics_dict["scores_by_row"] is not None
    assert len(metrics_dict["scores_by_row"]) == num_rows
    for row in metrics_dict["scores_by_row"]:
        if custom_dimensions is not None:
            assert_scores(row, custom_dimensions)
        else:
            assert_scores_geval(row)


def _set_keys(multiturn: bool) -> tuple[str, str, str, str, str, str]:
    if multiturn:
        latency_key_baseline = "avg_turn_latency"
        latency_key_run = "avg_turn_latency"
        latency_key_meta = "average_latency"
        input_tokens_key = "total_input_tokens"
        output_tokens_key = "total_output_tokens"
        cost_key = "total_cost"
    else:
        latency_key_baseline = "latency"
        latency_key_run = "avg_latency"
        latency_key_meta = "latency"
        input_tokens_key = "input_tokens"
        output_tokens_key = "output_tokens"
        cost_key = "cost"
    return (
        latency_key_baseline,
        latency_key_run,
        latency_key_meta,
        input_tokens_key,
        output_tokens_key,
        cost_key,
    )


def _parse_check_metrics(
    tdp: Union[TestDataPointItem, FullDataPointItem],
    meta_metrics: dict,
    check: str,
    latency_key_meta: str,
    input_tokens_key: str,
    output_tokens_key: str,
    cost_key: str,
    cost: bool,
) -> dict:
    if isinstance(tdp, FullDataPointItem) and tdp.checks_metadata:
        meta = tdp.checks_metadata  # type: ignore[attr-defined]
        if (
            isinstance(meta, FullDataPointItemChecksMetadata)
            and meta.additional_properties.get(check) is not None
        ):
            check_meta = meta.additional_properties.get(check)
            if check_meta is not None:
                meta_metrics["latency"].append(check_meta[latency_key_meta])
                meta_metrics["input_tokens"].append(check_meta[input_tokens_key])
                meta_metrics["output_tokens"].append(check_meta[output_tokens_key])
                if cost:
                    meta_metrics["cost"].append(check_meta[cost_key])
    return meta_metrics


def _parse_baseline_metrics(
    tdp: Union[TestDataPointItem, FullDataPointItem],
    baseline_metrics: dict,
    latency_key_baseline: str,
    input_tokens_key: str,
    output_tokens_key: str,
    cost_key: str,
    turns: int | None = None,
    cost: bool = False,
) -> dict:
    baseline = None
    if isinstance(tdp, FullDataPointItem) and tdp.baseline_metrics:
        baseline = tdp.baseline_metrics  # type: ignore[attr-defined]
        if isinstance(baseline, FullDataPointItemBaselineMetrics):
            tdp_baseline_metrics = baseline.additional_properties
            baseline_metrics["latency"].append(
                tdp_baseline_metrics[latency_key_baseline]
            )
            baseline_metrics["input_tokens"].append(
                tdp_baseline_metrics[input_tokens_key]
            )
            baseline_metrics["output_tokens"].append(
                tdp_baseline_metrics[output_tokens_key]
            )

    elif isinstance(tdp, TestDataPointItem) and tdp.additional_properties.get(
        "baseline_metrics"
    ):
        baseline = tdp.additional_properties["baseline_metrics"]
        baseline_metrics["latency"].append(baseline[latency_key_baseline])
        baseline_metrics["input_tokens"].append(baseline[input_tokens_key])
        baseline_metrics["output_tokens"].append(baseline[output_tokens_key])

    if turns == 1:
        if isinstance(tdp, FullDataPointItem):
            assert token_counter(text=tdp.model_result) == baseline[output_tokens_key]  # type: ignore
        elif isinstance(tdp, TestDataPointItem) and isinstance(
            tdp.additional_properties["model_result"], str
        ):
            assert token_counter(text=tdp.additional_properties["model_result"]) == baseline[output_tokens_key]  # type: ignore
    if cost:
        if isinstance(baseline, dict) and cost_key in baseline:
            baseline_metrics["cost"].append(baseline[cost_key])
        elif isinstance(baseline, FullDataPointItemBaselineMetrics):
            baseline_metrics["cost"].append(baseline.additional_properties[cost_key])
    return baseline_metrics


def _parse_checks_and_baseline_metrics(
    tdps: List[TestDataPointItem | FullDataPointItem],
    checks: List[str],
    cost: bool,
    turns: int | None,
    multiturn: bool,
) -> tuple[dict, dict, str]:

    (
        latency_key_baseline,
        latency_key_run,
        latency_key_meta,
        input_tokens_key,
        output_tokens_key,
        cost_key,
    ) = _set_keys(multiturn)

    meta_metrics: dict[str, list[float]] = {
        "latency": [],
        "cost": [],
        "input_tokens": [],
        "output_tokens": [],
    }
    baseline_metrics: dict[str, list[float]] = {
        "latency": [],
        "cost": [],
        "input_tokens": [],
        "output_tokens": [],
    }

    for tdp in tdps:
        assert isinstance(tdp, FullDataPointItem) or isinstance(tdp, TestDataPointItem)
        for check in checks:
            meta_metrics = _parse_check_metrics(
                tdp,
                meta_metrics,
                check,
                latency_key_meta,
                input_tokens_key,
                output_tokens_key,
                cost_key,
                cost,
            )

        baseline_metrics = _parse_baseline_metrics(
            tdp,
            baseline_metrics,
            latency_key_baseline,
            input_tokens_key,
            output_tokens_key,
            cost_key,
            turns=turns,
            cost=cost,
        )

    return baseline_metrics, meta_metrics, latency_key_run


def _internal_assert_baseline_metrics(
    checks: List[str],
    cost: bool,
    latency_key_run: str,
    baseline_metrics: dict[str, List[float]],
    run_check_meta: dict,
    run_baseline_meta: dict,
    meta_metrics: dict[str, List[float]],
) -> None:
    if checks:
        if len(meta_metrics["latency"]) > 0:
            assert round(run_check_meta["average_latency"], 2) == round(
                sum(meta_metrics["latency"]) / len(meta_metrics["latency"]), 2
            )
        assert round(run_check_meta["total_input_tokens"], 2) == round(
            sum(meta_metrics["input_tokens"]), 2
        )
        assert round(run_check_meta["total_output_tokens"], 2) == round(
            sum(meta_metrics["output_tokens"]), 2
        )

    if len(baseline_metrics["latency"]) > 0:
        assert round(run_baseline_meta[latency_key_run], 2) == round(
            sum(baseline_metrics["latency"]) / len(baseline_metrics["latency"]), 2
        )
    if "total_input_tokens" in run_baseline_meta:
        assert round(run_baseline_meta["total_input_tokens"], 2) == round(
            sum(baseline_metrics["input_tokens"]), 2
        )
    if "total_output_tokens" in run_baseline_meta:
        assert round(run_baseline_meta["total_output_tokens"], 2) == round(
            sum(baseline_metrics["output_tokens"]), 2
        )

    if cost:
        if checks:
            assert round(run_check_meta["total_cost"], 5) == round(
                sum(meta_metrics["cost"]), 5
            )
        if "total_cost" in run_baseline_meta:
            assert round(run_baseline_meta["total_cost"], 5) == round(
                sum(baseline_metrics["cost"]), 5
            )


def assert_baseline_metrics(
    okareo: Okareo,
    evaluation: TestRunItem,
    model: ModelUnderTest,
    checks: list,
    cost: bool = False,
    multiturn: bool = True,
    turns: int | None = None,
) -> None:

    tdps = okareo.find_test_data_points(
        FindTestDataPointPayload(test_run_id=evaluation.id, full_data_point=True)
    )
    assert isinstance(tdps, list)

    test_run = model.get_test_run(evaluation.id)
    run_check_meta = test_run.model_metrics.additional_properties[  # type: ignore
        "aggregate_check_metadata"
    ]
    run_baseline_meta = test_run.model_metrics.additional_properties[  # type: ignore
        "aggregate_baseline_metrics"
    ]
    print(tdps)
    (
        baseline_metrics,
        meta_metrics,
        latency_key_run,
    ) = _parse_checks_and_baseline_metrics(tdps, checks, cost, turns, multiturn)

    _internal_assert_baseline_metrics(
        checks,
        cost,
        latency_key_run,
        baseline_metrics,
        run_check_meta,
        run_baseline_meta,
        meta_metrics,
    )


def create_dummy_mut(
    target: Target, evaluation: TestRunItem, okareo: Okareo
) -> ModelUnderTest:
    """Create a dummy ModelUnderTest for testing purposes."""
    assert isinstance(target, Target)
    t_get = okareo.get_target_by_name(target.name)
    assert isinstance(t_get, Target) and t_get.id is not None
    dummy_response = ModelUnderTestResponse(
        id=t_get.id,
        project_id=evaluation.project_id,
        name=t_get.name,
        tags=[],
        time_created=datetime.datetime.now().isoformat(),
    )
    target_type = (
        target.target["type"] if isinstance(target.target, dict) else target.target.type
    )
    mut = ModelUnderTest(
        client=okareo.client,
        api_key=okareo.api_key,
        mut=dummy_response,
        models={target_type: target.target},
    )
    return mut
