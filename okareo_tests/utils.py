from typing import List, Union

from litellm import token_counter

from okareo import Okareo
from okareo.model_under_test import ModelUnderTest
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
        assert isinstance(tdp, FullDataPointItem)
        for check in checks:
            assert isinstance(tdp.checks_metadata, FullDataPointItemChecksMetadata)
            meta = tdp.checks_metadata[check]  # type: ignore[attr-defined]
            meta_metrics["latency"].append(meta[latency_key_meta])
            meta_metrics["input_tokens"].append(meta[input_tokens_key])
            meta_metrics["output_tokens"].append(meta[output_tokens_key])
            if cost:
                meta_metrics["cost"].append(meta[cost_key])

        assert isinstance(tdp.baseline_metrics, FullDataPointItemBaselineMetrics)
        baseline = tdp.baseline_metrics  # type: ignore[attr-defined]
        baseline_metrics["latency"].append(baseline[latency_key_baseline])
        baseline_metrics["input_tokens"].append(baseline[input_tokens_key])
        baseline_metrics["output_tokens"].append(baseline[output_tokens_key])
        if turns == 1:
            assert isinstance(tdp, FullDataPointItem) and isinstance(
                tdp.model_result, str
            )
            assert token_counter(text=tdp.model_result) == baseline[output_tokens_key]  # type: ignore
        if cost:
            baseline_metrics["cost"].append(baseline[cost_key])

    test_run = model.get_test_run(evaluation.id)
    run_check_meta = test_run.model_metrics.additional_properties[  # type: ignore
        "aggregate_check_metadata"
    ]
    run_baseline_meta = test_run.model_metrics.additional_properties[  # type: ignore
        "aggregate_baseline_metrics"
    ]

    if checks:
        assert round(run_check_meta["average_latency"], 2) == round(
            sum(meta_metrics["latency"]) / len(meta_metrics["latency"]), 2
        )
        assert round(run_check_meta["total_input_tokens"], 2) == round(
            sum(meta_metrics["input_tokens"]), 2
        )
        assert round(run_check_meta["total_output_tokens"], 2) == round(
            sum(meta_metrics["output_tokens"]), 2
        )

    assert round(run_baseline_meta[latency_key_run], 2) == round(
        sum(baseline_metrics["latency"]) / len(baseline_metrics["latency"]), 2
    )
    assert round(run_baseline_meta["total_input_tokens"], 2) == round(
        sum(baseline_metrics["input_tokens"]), 2
    )
    assert round(run_baseline_meta["total_output_tokens"], 2) == round(
        sum(baseline_metrics["output_tokens"]), 2
    )

    if cost:
        if checks:
            assert round(run_check_meta["total_cost"], 5) == round(
                sum(meta_metrics["cost"]), 5
            )
        assert round(run_baseline_meta["total_cost"], 5) == round(
            sum(baseline_metrics["cost"]), 5
        )
