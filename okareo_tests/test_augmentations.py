import json
from datetime import datetime
from uuid import UUID

import pytest
from okareo.augmentations import (
    Augmentation,
    BackchannelAugmentation,
    BargeInAugmentation,
    CAPAugmentation,
    DirectedSpeechAugmentation,
    NoiseAugmentation,
    SecondarySpeakerAugmentation,
)
from okareo.model_under_test import OpenAIModel, Simulation, Target
from okareo.okareo import Okareo
from okareo_api_client.models.scenario_set_response import ScenarioSetResponse
from okareo_api_client.models.scenario_type import ScenarioType
from pytest_httpx import HTTPXMock

MOCK_UUID = "0156f5d7-4ac4-4568-9d44-24750aa08d1a"


@pytest.fixture
def okareo_client(httpx_mock: HTTPXMock) -> Okareo:
    httpx_mock.add_response(
        json=[
            {
                "id": MOCK_UUID,
                "name": "Global",
                "onboarding_status": "onboarding_status",
                "tags": [],
                "additional_properties": {},
            }
        ],
        status_code=201,
    )
    return Okareo("foo", "http://mocked.com")


def test_simulation_serializes_augmentation_wrappers() -> None:
    simulation = Simulation(
        augmentation=Augmentation(
            noise=NoiseAugmentation(probability=0.3, profile="cafeteria", snr_db=10),
        )
    )

    assert simulation.to_dict()["augmentation"] == {
        "noise": {
            "probability": 0.3,
            "profile": "cafeteria",
            "snr_db": 10,
        }
    }


def test_augmentation_wrapper_shapes_match_server_contract() -> None:
    augmentation = Augmentation(
        cap=CAPAugmentation(probability=0.3, pause_ms=1000),
        directed_speech=DirectedSpeechAugmentation(
            probability=0.3,
            lpf_cutoff_hz=800,
            gain_db=-8.0,
        ),
        noise=NoiseAugmentation(probability=0.3, profile="cafeteria", snr_db=10),
        secondary_speaker=SecondarySpeakerAugmentation(
            probability=0.2,
            voice="voice-id",
        ),
        backchannel=BackchannelAugmentation(probability=0.3),
        barge_in=BargeInAugmentation(probability=0.05, replacement_text="hold on"),
    )

    assert augmentation.to_dict() == {
        "cap": {"probability": 0.3, "pause_ms": 1000},
        "directed_speech": {
            "probability": 0.3,
            "lpf_cutoff_hz": 800,
            "gain_db": -8.0,
        },
        "noise": {
            "probability": 0.3,
            "profile": "cafeteria",
            "snr_db": 10,
        },
        "secondary_speaker": {"probability": 0.2, "voice": "voice-id"},
        "backchannel": {"probability": 0.3},
        "barge_in": {"probability": 0.05, "replacement_text": "hold on"},
    }


def test_run_simulation_serializes_augmentation_payload(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(
        json={
            "id": MOCK_UUID,
            "name": "driver",
            "temperature": 0.6,
            "model_id": "gpt-4o-mini",
            "prompt_template": "{scenario_input}",
            "time_created": datetime.now().isoformat(),
        },
        status_code=201,
    )
    httpx_mock.add_response(
        json={
            "id": MOCK_UUID,
            "project_id": MOCK_UUID,
            "name": "target",
            "tags": [],
            "time_created": datetime.now().isoformat(),
            "version": 1,
            "models": {
                "openai": {
                    "type": "openai",
                    "model_id": "gpt-4o-mini",
                    "temperature": 0,
                    "system_prompt_template": "Be helpful",
                }
            },
        },
        status_code=201,
    )
    httpx_mock.add_response(
        json={
            "id": MOCK_UUID,
            "project_id": MOCK_UUID,
            "mut_id": MOCK_UUID,
            "scenario_set_id": MOCK_UUID,
            "name": "voice sim",
            "type": "MULTI_TURN",
        },
        status_code=201,
    )

    scenario = ScenarioSetResponse(
        scenario_id=UUID(MOCK_UUID),
        project_id=UUID(MOCK_UUID),
        name="scenario",
        time_created=datetime.now().isoformat(),
        type_=ScenarioType.SEED,
    )

    okareo_client.run_simulation(
        name="voice sim",
        scenario=scenario,
        target=Target(
            name="target",
            target=OpenAIModel(
                model_id="gpt-4o-mini",
                temperature=0,
                system_prompt_template="Be helpful",
            ),
        ),
        augmentation=Augmentation(
            noise=NoiseAugmentation(probability=0.3, profile="cafeteria", snr_db=10)
        ),
    )

    request = httpx_mock.get_requests()[-1]
    body = json.loads(request.content.decode("utf-8"))
    assert body["simulation_params"]["augmentation"] == {
        "noise": {
            "probability": 0.3,
            "profile": "cafeteria",
            "snr_db": 10,
        }
    }
