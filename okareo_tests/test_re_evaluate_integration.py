import json
import time
from typing import Any, Tuple, Union
from uuid import UUID, uuid4

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import CustomModel, ModelInvocation
from okareo_api_client.models.find_test_data_point_payload import (
    FindTestDataPointPayload,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_type import TestRunType


class _SimpleModel(CustomModel):
    def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
        return ModelInvocation(
            model_prediction=f"prediction::{str(input_value)}",
            model_input=input_value,
        )


class _SlowModel(CustomModel):
    delay_seconds: float = 0.5

    def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
        time.sleep(self.delay_seconds)
        return ModelInvocation(
            model_prediction=f"slow-prediction::{str(input_value)}",
            model_input=input_value,
        )


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(8)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


def _response_detail_text(response: Any) -> str:
    try:
        body = response.json()
    except Exception:
        return str(getattr(response, "text", ""))

    detail = body.get("detail") if isinstance(body, dict) else body
    if isinstance(detail, str):
        return detail
    return json.dumps(detail)


def _resolve_check_reference(okareo: Okareo) -> Tuple[str, str]:
    preferred_names = [
        "levenshtein_distance",
        "compression_ratio",
        "is_json",
    ]
    checks = okareo.get_all_checks()

    for preferred_name in preferred_names:
        for check in checks:
            if check.name == preferred_name and check.id is not None:
                return str(check.id), preferred_name

    raise AssertionError("Could not resolve a reusable check id for re-evaluate tests.")


def _make_scenario(okareo: Okareo, name: str, datapoint_count: int = 2) -> Any:
    return okareo.create_scenario_set(
        ScenarioSetCreate(
            name=name,
            seed_data=[
                SeedData(input_=f"input-{i}", result=f"result-{i}")
                for i in range(datapoint_count)
            ],
        )
    )


def _post_re_evaluate(
    okareo: Okareo,
    source_run_id: Union[str, UUID],
    check_ids: list[str],
    tags: list[str],
    name: str,
) -> Any:
    return okareo.client.get_httpx_client().request(
        method="post",
        url=f"/v0/test_runs/{source_run_id}/re_evaluate",
        json={
            "check_ids": check_ids,
            "tags": tags,
            "name": name,
        },
        headers={"api-key": okareo.api_key, "Content-Type": "application/json"},
    )


def _find_runs_by_tag(okareo: Okareo, tag: str) -> list[dict]:
    return okareo.find_test_runs(tags=[tag])


def _extract_check_value_records(tdp: Any) -> list[dict]:
    check_values = None
    if hasattr(tdp, "check_values") and tdp.check_values is not None:
        check_values = tdp.check_values
    elif hasattr(tdp, "additional_properties"):
        check_values = tdp.additional_properties.get("check_values")

    if not check_values:
        return []
    return [item if isinstance(item, dict) else item.to_dict() for item in check_values]


def test_re_evaluate_happy_path_executes_checks_and_keeps_source_immutable(
    okareo: Okareo, rnd: str
) -> None:
    check_id, check_name = _resolve_check_reference(okareo)
    scenario = _make_scenario(okareo, f"reeval-happy-scenario-{rnd}", datapoint_count=3)
    mut = okareo.register_model(
        name=f"reeval-happy-model-{rnd}",
        model=_SimpleModel(name=f"reeval-happy-model-{rnd}"),
    )
    source_run = mut.run_test(
        name=f"reeval-happy-source-{rnd}",
        scenario=scenario,
        test_run_type=TestRunType.NL_GENERATION,
        checks=[check_name],
    )
    assert source_run.id is not None

    source_before = mut.get_test_run(source_run.id)
    source_tdps_before = okareo.find_test_data_points(
        FindTestDataPointPayload(test_run_id=source_run.id, full_data_point=True)
    )
    assert isinstance(source_tdps_before, list)
    marker_tag = f"reeval-happy-{rnd}-{random_string(6)}"

    new_run = okareo.re_evaluate(
        test_run_id=str(source_run.id),
        checks=[check_id],
        tags=[marker_tag],
        name=f"reeval-happy-dest-{rnd}",
    )
    assert new_run.id is not None
    reeval_run_id = str(new_run.id)
    assert reeval_run_id != str(source_run.id)

    reeval_run = mut.get_test_run(reeval_run_id)
    assert str(reeval_run.id) == str(reeval_run_id)
    assert reeval_run.status == "FINISHED"
    assert marker_tag in (reeval_run.tags or [])

    # find_test_runs: tag filter is server-side, name filter is client-side.
    found = okareo.find_test_runs(tags=[marker_tag], name=f"reeval-happy-dest-{rnd}")
    assert len(found) == 1
    assert str(found[0]["id"]) == reeval_run_id

    reeval_tdps = okareo.find_test_data_points(
        FindTestDataPointPayload(test_run_id=UUID(reeval_run_id), full_data_point=True)
    )
    assert isinstance(reeval_tdps, list)
    assert len(reeval_tdps) > 0

    matched_check_values = 0
    for tdp in reeval_tdps:
        for check_value in _extract_check_value_records(tdp):
            if str(check_value.get("check_id")) == check_id:
                matched_check_values += 1
    assert (
        matched_check_values > 0
    ), "Expected at least one executed check value tied to requested check_id."

    source_after = mut.get_test_run(source_run.id)
    source_tdps_after = okareo.find_test_data_points(
        FindTestDataPointPayload(test_run_id=source_run.id, full_data_point=True)
    )
    assert isinstance(source_tdps_after, list)
    assert source_after.status == source_before.status
    assert source_after.start_time == source_before.start_time
    assert source_after.end_time == source_before.end_time
    assert len(source_tdps_after) == len(source_tdps_before)


def test_re_evaluate_rejects_non_terminal_source_without_side_effects(
    okareo: Okareo, rnd: str
) -> None:
    check_id, check_name = _resolve_check_reference(okareo)
    scenario = _make_scenario(
        okareo, f"reeval-running-scenario-{rnd}", datapoint_count=18
    )
    mut = okareo.register_model(
        name=f"reeval-running-model-{rnd}",
        model=_SlowModel(name=f"reeval-running-model-{rnd}"),
    )
    submitted_run = mut.submit_test(
        name=f"reeval-running-source-{rnd}",
        scenario=scenario,
        test_run_type=TestRunType.NL_GENERATION,
        checks=[check_name],
    )
    assert submitted_run.id is not None

    current = mut.get_test_run(submitted_run.id)
    assert (
        current.status == "RUNNING"
    ), f"Expected RUNNING source status, got {current.status}."

    marker_tag = f"reeval-running-{rnd}-{random_string(6)}"
    assert len(_find_runs_by_tag(okareo, marker_tag)) == 0

    response = _post_re_evaluate(
        okareo=okareo,
        source_run_id=submitted_run.id,
        check_ids=[check_id],
        tags=[marker_tag],
        name=f"reeval-running-dest-{rnd}",
    )
    assert response.status_code == 422, (
        f"Expected 422 for non-terminal source run, "
        f"got {response.status_code}: {response.text}"
    )
    assert "not re-evaluatable" in _response_detail_text(response)
    assert len(_find_runs_by_tag(okareo, marker_tag)) == 0


def test_re_evaluate_rejects_missing_source_without_side_effects(
    okareo: Okareo, rnd: str
) -> None:
    check_id, _ = _resolve_check_reference(okareo)
    marker_tag = f"reeval-missing-{rnd}-{random_string(6)}"
    assert len(_find_runs_by_tag(okareo, marker_tag)) == 0

    response = _post_re_evaluate(
        okareo=okareo,
        source_run_id=str(uuid4()),
        check_ids=[check_id],
        tags=[marker_tag],
        name=f"reeval-missing-dest-{rnd}",
    )
    assert response.status_code == 404
    assert "not found" in _response_detail_text(response)
    assert len(_find_runs_by_tag(okareo, marker_tag)) == 0


def test_re_evaluate_rejects_empty_checks_without_side_effects(
    okareo: Okareo, rnd: str
) -> None:
    check_id, check_name = _resolve_check_reference(okareo)
    scenario = _make_scenario(okareo, f"reeval-empty-checks-scenario-{rnd}", 2)
    mut = okareo.register_model(
        name=f"reeval-empty-checks-model-{rnd}",
        model=_SimpleModel(name=f"reeval-empty-checks-model-{rnd}"),
    )
    source_run = mut.run_test(
        name=f"reeval-empty-checks-source-{rnd}",
        scenario=scenario,
        test_run_type=TestRunType.NL_GENERATION,
        checks=[check_name],
    )
    assert source_run.id is not None
    marker_tag = f"reeval-empty-checks-{rnd}-{random_string(6)}"
    assert len(_find_runs_by_tag(okareo, marker_tag)) == 0

    response = _post_re_evaluate(
        okareo=okareo,
        source_run_id=source_run.id,
        check_ids=[],
        tags=[marker_tag],
        name=f"reeval-empty-checks-dest-{rnd}",
    )
    assert response.status_code == 422
    assert "at least 1 item" in _response_detail_text(response)
    assert len(_find_runs_by_tag(okareo, marker_tag)) == 0

    # Ensure helper references are both used in this test path.
    assert check_id


def test_re_evaluate_rejects_invalid_check_ids_without_side_effects(
    okareo: Okareo, rnd: str
) -> None:
    _, check_name = _resolve_check_reference(okareo)
    scenario = _make_scenario(okareo, f"reeval-invalid-checks-scenario-{rnd}", 2)
    mut = okareo.register_model(
        name=f"reeval-invalid-checks-model-{rnd}",
        model=_SimpleModel(name=f"reeval-invalid-checks-model-{rnd}"),
    )
    source_run = mut.run_test(
        name=f"reeval-invalid-checks-source-{rnd}",
        scenario=scenario,
        test_run_type=TestRunType.NL_GENERATION,
        checks=[check_name],
    )
    assert source_run.id is not None
    marker_tag = f"reeval-invalid-checks-{rnd}-{random_string(6)}"
    assert len(_find_runs_by_tag(okareo, marker_tag)) == 0

    response = _post_re_evaluate(
        okareo=okareo,
        source_run_id=source_run.id,
        check_ids=[str(uuid4())],
        tags=[marker_tag],
        name=f"reeval-invalid-checks-dest-{rnd}",
    )
    assert response.status_code in (400, 404, 422), (
        "Expected client error for invalid check ids, "
        f"got {response.status_code}: {response.text}"
    )
    assert len(_find_runs_by_tag(okareo, marker_tag)) == 0
