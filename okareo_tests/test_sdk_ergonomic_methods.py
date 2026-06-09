"""Integration tests for new Okareo SDK ergonomic methods.

Covers: generate_driver_prompt, find_test_runs, re_evaluate,
download_call_recording.

Requires OKAREO_API_KEY in environment.
"""

import os
from typing import Tuple, Union

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import CustomModel, Driver, ModelInvocation
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_type import TestRunType


class _SimpleModel(CustomModel):
    def invoke(self, input_value: Union[dict, list, str]) -> ModelInvocation:
        return ModelInvocation(
            model_prediction=f"echo::{str(input_value)}",
            model_input=input_value,
        )


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(6)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)


def _resolve_check_reference(okareo: Okareo) -> Tuple[str, str]:
    """Return (check_id, check_name) for a known built-in check."""
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
    raise AssertionError("Could not resolve a reusable check for tests.")


# ============================================================================
# generate_driver_prompt
# ============================================================================


class TestGenerateDriverPrompt:
    def test_returns_driver(self, okareo: Okareo) -> None:
        driver = okareo.generate_driver_prompt(
            "confused customer calling about a charge"
        )
        assert isinstance(driver, Driver)
        assert driver.name
        assert driver.prompt_template
        assert len(driver.prompt_template) > 50

    def test_with_voice_instructions(self, okareo: Okareo) -> None:
        driver = okareo.generate_driver_prompt(
            "angry customer demanding a refund",
            voice_instructions="Speak with frustration and urgency.",
        )
        assert isinstance(driver, Driver)
        assert driver.voice_instructions == "Speak with frustration and urgency."

    def test_with_language(self, okareo: Okareo) -> None:
        driver = okareo.generate_driver_prompt(
            "cliente confundido llamando sobre un cargo",
            language="es",
        )
        assert isinstance(driver, Driver)
        assert driver.name
        assert driver.prompt_template


# ============================================================================
# find_test_runs
# ============================================================================


class TestFindTestRuns:
    def test_returns_list(self, okareo: Okareo) -> None:
        runs = okareo.find_test_runs()
        assert isinstance(runs, list)

    def test_filters_by_name(self, okareo: Okareo, rnd: str) -> None:
        unique_name = f"find-test-runs-{rnd}"
        _, check_name = _resolve_check_reference(okareo)
        scenario = okareo.create_scenario_set(
            ScenarioSetCreate(
                name=f"find-runs-scenario-{rnd}",
                seed_data=[SeedData(input_="hello", result="world")],
            )
        )
        mut = okareo.register_model(
            name=f"find-runs-model-{rnd}",
            model=_SimpleModel(name=f"find-runs-model-{rnd}"),
        )
        mut.run_test(
            name=unique_name,
            scenario=scenario,
            test_run_type=TestRunType.NL_GENERATION,
            checks=[check_name],
        )

        runs = okareo.find_test_runs(name=unique_name)
        assert len(runs) >= 1
        assert all(r["name"] == unique_name for r in runs)


# ============================================================================
# re_evaluate
# ============================================================================


class TestReEvaluate:
    def test_creates_new_run(self, okareo: Okareo, rnd: str) -> None:
        check_id, check_name = _resolve_check_reference(okareo)
        scenario = okareo.create_scenario_set(
            ScenarioSetCreate(
                name=f"reeval-ergo-scenario-{rnd}",
                seed_data=[
                    SeedData(input_=f"input-{i}", result=f"result-{i}")
                    for i in range(2)
                ],
            )
        )
        mut = okareo.register_model(
            name=f"reeval-ergo-model-{rnd}",
            model=_SimpleModel(name=f"reeval-ergo-model-{rnd}"),
        )
        source_run = mut.run_test(
            name=f"reeval-ergo-source-{rnd}",
            scenario=scenario,
            test_run_type=TestRunType.NL_GENERATION,
            checks=[check_name],
        )
        assert source_run.id is not None

        new_run = okareo.re_evaluate(
            test_run_id=str(source_run.id),
            checks=[check_id],
            name=f"reeval-ergo-dest-{rnd}",
        )
        assert str(new_run.id) != str(source_run.id)
        assert new_run.status == "FINISHED"


# ============================================================================
# download_call_recording
# ============================================================================

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")


@pytest.mark.skipif(
    not TWILIO_ACCOUNT_SID,
    reason="Requires TWILIO credentials and a live voice call",
)
class TestDownloadCallRecording:
    """Requires a completed voice simulation to extract a call_sid.

    Only runs when TWILIO_ACCOUNT_SID is set (CI voice environment).
    """

    def test_downloads_bytes(self, okareo: Okareo, rnd: str) -> None:
        from okareo.model_under_test import PhoneTarget, Target
        from okareo_api_client.models.find_test_data_point_payload import (
            FindTestDataPointPayload,
        )

        target_phone = os.getenv("TWILIO_TO_PHONE", "+17623004777")
        scenario = okareo.create_scenario_set(
            ScenarioSetCreate(
                name=f"recording-scenario-{rnd}",
                seed_data=Okareo.seed_data_from_list(
                    [{"input": "What are your hours?", "result": "Hours provided"}]
                ),
            )
        )
        result = okareo.run_simulation(
            name=f"recording-sim-{rnd}",
            target=Target(
                name=f"recording-target-{rnd}",
                target=PhoneTarget(phone_number=target_phone),
            ),
            scenario=scenario,
            max_turns=1,
            checks=["avg_turn_taking_latency"],
        )
        assert result.id is not None

        tdps = okareo.find_test_data_points(
            FindTestDataPointPayload(test_run_id=result.id, full_data_point=True)
        )
        assert isinstance(tdps, list) and len(tdps) > 0
        dp = tdps[0]
        assert hasattr(dp, "model_metadata") and dp.model_metadata is not None
        metadata = dp.model_metadata.additional_properties  # type: ignore[union-attr]
        call_sid = metadata.get("call_sid")
        assert call_sid, "No call_sid in datapoint metadata"

        audio = okareo.download_call_recording(call_sid)
        assert isinstance(audio, bytes)
        assert len(audio) > 0
