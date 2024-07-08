from typing import List, Union

from okareo_api_client.models.test_run_item import TestRunItem
from okareo_api_client.types import Unset


def assert_scores_geval(scores: dict) -> None:
    dimension_keys = ["consistency", "coherence", "fluency", "relevance"]
    for dimension in dimension_keys:
        assert dimension in scores
        assert isinstance(scores[dimension], float)
        assert 1 <= scores[dimension] <= 5


def assert_scores(scores: dict, custom_dimensions: List[str]) -> None:
    dimension_keys = custom_dimensions
    skip_keys = ["scenario_index", "test_id"]
    assert len(dimension_keys) == len([k for k in scores.keys() if k not in skip_keys])
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
