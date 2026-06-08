"""Integration tests for voice SDK method wrappers.

Tests: PhoneTarget, Simulation.augmentation, generate_driver_prompt,
find_test_runs, re_evaluate, download_call_recording.

Requires OKAREO_API_KEY in environment.
"""
import os
from typing import Union
from uuid import UUID

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import (
    CustomModel,
    Driver,
    ModelInvocation,
    PhoneTarget,
    Simulation,
    Target,
)
from okareo_api_client.models.find_test_data_point_payload import (
    FindTestDataPointPayload,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_type import TestRunType

TARGET_PHONE = os.getenv("TWILIO_TO_PHONE", "+17623004777")


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


# ============================================================================
# PhoneTarget
# ============================================================================


class TestPhoneTarget:
    def test_params_emits_twilio_format(self) -> None:
        pt = PhoneTarget(phone_number="+15551234567")
        params = pt.params()
        assert params["type"] == "voice"
        assert params["edge_type"] == "twilio"
        assert params["to_phone_number"] == "+15551234567"
        assert params["account_sid"] == ""
        assert params["auth_token"] == ""
        assert params["from_phone_number"] is None

    def test_params_with_max_parallel(self) -> None:
        pt = PhoneTarget(phone_number="+15551234567", max_parallel_requests=5)
        params = pt.params()
        assert params["max_parallel_requests"] == 5

    def test_target_to_dict(self) -> None:
        t = Target(name="Test Agent", target=PhoneTarget(phone_number="+15551234567"))
        d = t.to_dict()
        assert d["name"] == "Test Agent"
        assert d["target"]["to_phone_number"] == "+15551234567"


# ============================================================================
# Simulation augmentation
# ============================================================================


class TestSimulationAugmentation:
    def test_to_dict_without_augmentation(self) -> None:
        sim = Simulation(max_turns=3)
        d = sim.to_dict()
        assert "augmentation" not in d

    def test_to_dict_with_augmentation(self) -> None:
        aug = {"noise": {"noise_profile": "cafeteria", "noise_snr_db": 10}}
        sim = Simulation(max_turns=3, augmentation=aug)
        d = sim.to_dict()
        assert d["augmentation"] == aug

    def test_to_dict_augmentation_none_omitted(self) -> None:
        sim = Simulation(max_turns=3, augmentation=None)
        d = sim.to_dict()
        assert "augmentation" not in d


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

    def test_with_kwargs(self, okareo: Okareo) -> None:
        driver = okareo.generate_driver_prompt(
            "angry customer demanding a refund",
            temperature=0.9,
            voice_instructions="Speak with frustration.",
        )
        assert driver.temperature == 0.9
        assert driver.voice_instructions == "Speak with frustration."

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
        )

        runs = okareo.find_test_runs(name=unique_name)
        assert len(runs) >= 1
        assert all(r["name"] == unique_name for r in runs)


# ============================================================================
# re_evaluate
# ============================================================================


class TestReEvaluate:
    def _resolve_check(self, okareo: Okareo) -> str:
        checks = okareo.get_all_checks()
        for name in ["levenshtein_distance", "compression_ratio", "is_json"]:
            for c in checks:
                if c.name == name and c.id is not None:
                    return str(c.id)
        raise AssertionError("Could not resolve a check for re-evaluate test.")

    def test_creates_new_run(self, okareo: Okareo, rnd: str) -> None:
        check_id = self._resolve_check(okareo)
        scenario = okareo.create_scenario_set(
            ScenarioSetCreate(
                name=f"reeval-scenario-{rnd}",
                seed_data=[
                    SeedData(input_=f"input-{i}", result=f"result-{i}")
                    for i in range(2)
                ],
            )
        )
        mut = okareo.register_model(
            name=f"reeval-model-{rnd}",
            model=_SimpleModel(name=f"reeval-model-{rnd}"),
        )
        source_run = mut.run_test(
            name=f"reeval-source-{rnd}",
            scenario=scenario,
            test_run_type=TestRunType.NL_GENERATION,
        )
        assert source_run.id is not None

        new_run = okareo.re_evaluate(
            test_run_id=str(source_run.id),
            checks=[check_id],
            name=f"reeval-dest-{rnd}",
        )
        assert str(new_run.id) != str(source_run.id)
        assert new_run.status == "FINISHED"
