import json
from datetime import datetime
from typing import Any
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


def test_end_at_turn_is_forwarded_for_every_strategy_that_takes_it() -> None:
    assert Augmentation(
        barge_in=BargeInAugmentation(prompt="hey", start_at_turn=2, end_at_turn=4)
    ).to_dict() == {"barge_in": {"prompt": "hey", "start_at_turn": 2, "end_at_turn": 4}}
    assert Augmentation(
        backchannel=BackchannelAugmentation(utterance="mm", end_at_turn=4)
    ).to_dict() == {"backchannel": {"utterance": "mm", "end_at_turn": 4}}
    assert Augmentation(
        directed_speech=DirectedSpeechAugmentation(probability=0.3, end_at_turn=5)
    ).to_dict() == {"directed_speech": {"probability": 0.3, "end_at_turn": 5}}
    assert Augmentation(
        secondary_speaker=SecondarySpeakerAugmentation(voice="Cathy", end_at_turn=6)
    ).to_dict() == {"secondary_speaker": {"voice": "Cathy", "end_at_turn": 6}}
    assert Augmentation(
        dropout=DropoutAugmentation(probability=1.0, end_at_turn=3)
    ).to_dict() == {"dropout": {"probability": 1.0, "end_at_turn": 3}}


def test_a_single_turn_window_serializes_both_ends() -> None:
    """The customer-facing shape: fire on turn 3 and nowhere else.

    probability=1.0 is part of the idiom, not incidental -- the window bounds
    WHERE the strategy may fire, and the probability is still drawn inside it,
    so the default 0.1 would leave this doing nothing nine runs in ten.
    """
    assert Augmentation(
        dropout=DropoutAugmentation(probability=1.0, start_at_turn=3, end_at_turn=3)
    ).to_dict() == {
        "dropout": {"probability": 1.0, "start_at_turn": 3, "end_at_turn": 3}
    }


def test_end_at_turn_is_omitted_when_unset() -> None:
    """Unset means unbounded; the key must not reach the server at all, so
    existing configs serialize exactly as they did before the parameter."""
    payload = Augmentation(
        dropout=DropoutAugmentation(probability=0.5, start_at_turn=2)
    ).to_dict()

    assert payload == {"dropout": {"probability": 0.5, "start_at_turn": 2}}
    assert "end_at_turn" not in payload["dropout"]


def test_interrupt_options_are_forwarded_for_directed_and_secondary_speaker() -> None:
    """``interrupt`` moves the remark over the agent's next reply, timed with
    barge-in's offset window; all four keys reach the server as given."""
    assert Augmentation(
        directed_speech=DirectedSpeechAugmentation(
            probability=1.0,
            interrupt=True,
            min_offset_ms=900,
            max_offset_ms=1100,
            seed=3,
        )
    ).to_dict() == {
        "directed_speech": {
            "probability": 1.0,
            "interrupt": True,
            "min_offset_ms": 900,
            "max_offset_ms": 1100,
            "seed": 3,
        }
    }
    assert Augmentation(
        secondary_speaker=SecondarySpeakerAugmentation(
            voice="Cathy - Coworker",
            prompt="Ask the caller: did you have coffee?",
            interrupt=True,
            start_at_turn=2,
            end_at_turn=2,
        )
    ).to_dict() == {
        "secondary_speaker": {
            "voice": "Cathy - Coworker",
            "prompt": "Ask the caller: did you have coffee?",
            "start_at_turn": 2,
            "end_at_turn": 2,
            "interrupt": True,
        }
    }


def test_interrupt_options_are_omitted_when_unset() -> None:
    """Unset keys never reach the server, so in-turn configs serialize exactly
    as they did before the toggle existed (the server refuses offsets without
    ``interrupt``)."""
    payload = Augmentation(
        secondary_speaker=SecondarySpeakerAugmentation(
            voice="Cathy - Coworker", inter_speaker_pause_ms=120
        )
    ).to_dict()

    assert payload == {
        "secondary_speaker": {
            "voice": "Cathy - Coworker",
            "inter_speaker_pause_ms": 120,
        }
    }


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


def test_new_entry_fields_serialize_on_the_single_strategy_path() -> None:
    """``utterance`` on the two speaker kinds (the server reads secondary
    speaker's as ``secondary_utterance``) and CAP's ``consecutive_messages``."""
    assert Augmentation(
        directed_speech=DirectedSpeechAugmentation(utterance="Hold on, sweetie!")
    ).to_dict() == {"directed_speech": {"utterance": "Hold on, sweetie!"}}
    assert Augmentation(
        secondary_speaker=SecondarySpeakerAugmentation(
            voice="Cathy - Coworker", utterance="Did you have coffee?"
        )
    ).to_dict() == {
        "secondary_speaker": {
            "voice": "Cathy - Coworker",
            "utterance": "Did you have coffee?",
        }
    }
    assert Augmentation(
        cap=CAPAugmentation(probability=1.0, consecutive_messages=3)
    ).to_dict() == {"cap": {"probability": 1.0, "consecutive_messages": 3}}


@pytest.mark.parametrize(
    "build",
    [
        lambda: BargeInAugmentation(utterance="No thank you.", prompt="Decline."),
        lambda: DirectedSpeechAugmentation(utterance="Hold on!", prompt="Aside."),
        lambda: SecondarySpeakerAugmentation(utterance="Coffee?", prompt="Ask."),
    ],
)
def test_utterance_and_prompt_are_mutually_exclusive(build: Any) -> None:
    with pytest.raises(ValueError, match="prompt or utterance, not both"):
        build()


def test_barge_in_replacement_text_beside_prompt_is_unchanged_outside_a_plan() -> None:
    """Existing callers send ``replacement_text`` beside ``prompt``; the server
    ignores it outside a plan, so it must not be read as ``utterance`` there."""
    assert Augmentation(
        barge_in=BargeInAugmentation(replacement_text="hold on", prompt="Interrupt.")
    ).to_dict() == {"barge_in": {"replacement_text": "hold on", "prompt": "Interrupt."}}


@pytest.mark.parametrize(
    "build",
    [
        lambda: Augmentation(barge_in=BargeInAugmentation(prompt="Hi.", count=2)),
        lambda: Augmentation(backchannel=BackchannelAugmentation(count=2)),
    ],
)
def test_count_is_refused_outside_a_plan(build: Any) -> None:
    """The single-strategy path has no per-turn play count; the server would
    drop it silently."""
    with pytest.raises(ValueError, match="count only applies inside a plan"):
        build()


def test_plan_serializes_to_turn_keyed_wire_shape() -> None:
    """Turn keys become strings in turn order, each entry gets its ``type``
    from its class, ``None`` / ``[]`` turns pass through, and ``noise`` stays
    beside the plan."""
    augmentation = Augmentation(
        noise=NoiseAugmentation(profile="cafeteria", snr_db=10),
        plan={
            4: [BargeInAugmentation(prompt="Ask to speak to a pharmacist.")],
            2: [
                BackchannelAugmentation(
                    utterance="OK, good.", min_offset_ms=1500, max_offset_ms=2500
                ),
                BargeInAugmentation(utterance="No thank you.", count=2),
            ],
            1: None,
            3: [
                SecondarySpeakerAugmentation(
                    voice="Cathy - Coworker",
                    utterance="Did you have coffee?",
                    interrupt=True,
                    lpf_cutoff_hz=800,
                    gain_db=-8,
                ),
                CAPAugmentation(consecutive_messages=4),
            ],
            5: [],
        },
    )

    payload = augmentation.to_dict()

    assert list(payload["plan"]) == ["1", "2", "3", "4", "5"]
    assert payload == {
        "noise": {"profile": "cafeteria", "snr_db": 10},
        "plan": {
            "1": None,
            "2": [
                {
                    "type": "backchannel",
                    "utterance": "OK, good.",
                    "min_offset_ms": 1500,
                    "max_offset_ms": 2500,
                },
                {"type": "barge_in", "utterance": "No thank you.", "count": 2},
            ],
            "3": [
                {
                    "type": "secondary_speaker",
                    "voice": "Cathy - Coworker",
                    "utterance": "Did you have coffee?",
                    "interrupt": True,
                    "lpf_cutoff_hz": 800,
                    "gain_db": -8,
                },
                {"type": "cap", "consecutive_messages": 4},
            ],
            "4": [{"type": "barge_in", "prompt": "Ask to speak to a pharmacist."}],
            "5": [],
        },
    }
    assert Simulation(augmentation=augmentation).to_dict()["augmentation"] == payload


def test_plan_entry_types_cover_every_turn_level_strategy() -> None:
    plan = Augmentation(
        plan={
            1: [DropoutAugmentation()],
            2: [DirectedSpeechAugmentation(prompt="Talk to your dog.")],
        }
    ).to_dict()["plan"]

    assert plan == {
        "1": [{"type": "dropout"}],
        "2": [{"type": "directed_speech", "prompt": "Talk to your dog."}],
    }


@pytest.mark.parametrize(
    "entry",
    [
        BargeInAugmentation(prompt="Interrupt.", start_at_turn=2),
        BargeInAugmentation(prompt="Interrupt.", end_at_turn=2),
    ],
)
def test_plan_entries_refuse_turn_window_keys(entry: BargeInAugmentation) -> None:
    with pytest.raises(ValueError, match="the turn key \\(2\\) is the turn"):
        Augmentation(plan={2: [entry]})


def test_plan_refuses_strategies_beside_it_other_than_noise() -> None:
    with pytest.raises(ValueError, match="can't be combined with barge_in"):
        Augmentation(
            barge_in=BargeInAugmentation(prompt="Interrupt."),
            plan={2: [BargeInAugmentation(utterance="No thank you.")]},
        )


def test_plan_refuses_noise_and_cap_pause_entries() -> None:
    with pytest.raises(ValueError, match="NoiseAugmentation is run-wide"):
        Augmentation(plan={1: [NoiseAugmentation(profile="cafeteria")]})
    with pytest.raises(ValueError, match="cap pause_ms can't be set"):
        Augmentation(plan={1: [CAPAugmentation(pause_ms=500)]})


@pytest.mark.parametrize("turn", [0, -1, True, "x", "02x", 1.5])
def test_plan_refuses_turns_that_are_not_positive_integers(turn: Any) -> None:
    with pytest.raises(ValueError, match="counted from 1"):
        Augmentation(plan={turn: [BargeInAugmentation(utterance="Hi.")]})


def test_plan_accepts_digit_string_turns_but_not_the_same_turn_twice() -> None:
    plan = {"3": [DropoutAugmentation()]}
    assert Augmentation(plan=plan).to_dict() == {  # type: ignore[arg-type]
        "plan": {"3": [{"type": "dropout"}]}
    }
    with pytest.raises(ValueError, match="lists turn 2 twice"):
        Augmentation(plan={2: [DropoutAugmentation()], "2": None})  # type: ignore[dict-item]


def test_plan_refuses_entries_that_are_not_strategy_configs() -> None:
    with pytest.raises(TypeError, match="not dict"):
        Augmentation(plan={2: [{"type": "barge_in", "utterance": "Hi."}]})  # type: ignore[list-item]
    with pytest.raises(TypeError, match="must be a list"):
        Augmentation(plan={2: BargeInAugmentation(utterance="Hi.")})  # type: ignore[dict-item]


def test_plan_reads_barge_in_replacement_text_as_utterance() -> None:
    """Inside a plan the server reads the older name as exact words, so the SDK
    sends it as ``utterance`` and applies the same exclusivity."""
    assert Augmentation(
        plan={2: [BargeInAugmentation(replacement_text="No thank you.")]}
    ).to_dict() == {"plan": {"2": [{"type": "barge_in", "utterance": "No thank you."}]}}
    with pytest.raises(ValueError, match="prompt or utterance, not both"):
        Augmentation(
            plan={2: [BargeInAugmentation(replacement_text="No.", prompt="Decline.")]}
        )
    with pytest.raises(ValueError, match="utterance or replacement_text"):
        Augmentation(
            plan={2: [BargeInAugmentation(replacement_text="No.", utterance="No.")]}
        )
