import json
from datetime import datetime
from uuid import UUID

import pytest
from pytest_httpx import HTTPXMock

from okareo.augmentations import (
    Augmentation,
    BackchannelAugmentation,
    BargeInAugmentation,
    CAPAugmentation,
    DirectedSpeechAugmentation,
    DropoutAugmentation,
    NoiseAugmentation,
    SecondarySpeakerAugmentation,
)
from okareo.model_under_test import OpenAIModel, Simulation, Target
from okareo.okareo import Okareo
from okareo_api_client.models.scenario_set_response import ScenarioSetResponse
from okareo_api_client.models.scenario_type import ScenarioType

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
            prompt="Your dog is eating your lunch. Tell him to stop.",
            lpf_cutoff_hz=800,
            gain_db=-8.0,
        ),
        noise=NoiseAugmentation(probability=0.3, profile="cafeteria", snr_db=10),
        secondary_speaker=SecondarySpeakerAugmentation(
            probability=0.2,
            voice="voice-id",
            prompt="You are a nearby companion who occasionally adds a short interjection.",
            lpf_cutoff_hz=800,
            gain_db=-8.0,
            inter_speaker_pause_ms=1000,
        ),
        backchannel=BackchannelAugmentation(probability=0.3),
        barge_in=BargeInAugmentation(
            probability=0.05,
            replacement_text="hold on",
            prompt="Interrupt the speaker and get them to pause.",
        ),
        dropout=DropoutAugmentation(probability=0.2),
    )

    assert augmentation.to_dict() == {
        "cap": {"probability": 0.3, "pause_ms": 1000},
        "directed_speech": {
            "probability": 0.3,
            "prompt": "Your dog is eating your lunch. Tell him to stop.",
            "lpf_cutoff_hz": 800,
            "gain_db": -8.0,
        },
        "noise": {
            "probability": 0.3,
            "profile": "cafeteria",
            "snr_db": 10,
        },
        "secondary_speaker": {
            "probability": 0.2,
            "voice": "voice-id",
            "prompt": "You are a nearby companion who occasionally adds a short interjection.",
            "lpf_cutoff_hz": 800,
            "gain_db": -8.0,
            "inter_speaker_pause_ms": 1000,
        },
        "backchannel": {"probability": 0.3},
        "barge_in": {
            "probability": 0.05,
            "replacement_text": "hold on",
            "prompt": "Interrupt the speaker and get them to pause.",
        },
        "dropout": {"probability": 0.2},
    }


def test_dropout_augmentation_serializes_probability_only() -> None:
    assert Augmentation(dropout=DropoutAugmentation(probability=0.2)).to_dict() == {
        "dropout": {"probability": 0.2}
    }
    assert DropoutAugmentation().to_dict() == {}


def test_start_at_turn_is_forwarded_for_every_strategy_that_takes_it() -> None:
    """cap and noise deliberately do not take it."""
    assert Augmentation(
        barge_in=BargeInAugmentation(prompt="hey", start_at_turn=2)
    ).to_dict() == {"barge_in": {"prompt": "hey", "start_at_turn": 2}}
    assert Augmentation(
        backchannel=BackchannelAugmentation(utterance="mm", start_at_turn=4)
    ).to_dict() == {"backchannel": {"utterance": "mm", "start_at_turn": 4}}
    assert Augmentation(
        directed_speech=DirectedSpeechAugmentation(probability=0.3, start_at_turn=5)
    ).to_dict() == {"directed_speech": {"probability": 0.3, "start_at_turn": 5}}
    assert Augmentation(
        secondary_speaker=SecondarySpeakerAugmentation(voice="Cathy", start_at_turn=6)
    ).to_dict() == {"secondary_speaker": {"voice": "Cathy", "start_at_turn": 6}}


def test_dropout_start_at_turn_is_forwarded() -> None:
    """start_at_turn holds the drop off until that driver turn.

    Transcript numbering: the target's greeting is turn 0, the first driver
    turn is 1. Omitted means the server default of 1 (every turn).
    """
    assert Augmentation(
        dropout=DropoutAugmentation(probability=1.0, start_at_turn=3)
    ).to_dict() == {"dropout": {"probability": 1.0, "start_at_turn": 3}}


def test_noise_and_dropout_compose() -> None:
    simulation = Simulation(
        augmentation=Augmentation(
            noise=NoiseAugmentation(profile="traffic", snr_db=15),
            dropout=DropoutAugmentation(probability=0.2),
        )
    )

    assert simulation.to_dict()["augmentation"] == {
        "noise": {"profile": "traffic", "snr_db": 15},
        "dropout": {"probability": 0.2},
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
        time_created=datetime.now(),
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
