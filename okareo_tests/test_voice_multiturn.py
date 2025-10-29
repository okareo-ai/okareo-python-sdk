import os
import uuid

import pytest
from okareo_tests.common import random_string

from okareo import Okareo
from okareo.model_under_test import Driver, Target
from okareo.voice import DeepgramEdgeConfig, LocalVoiceTarget, OpenAIEdgeConfig
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.test_run_item_model_metrics import TestRunItemModelMetrics

# Constants
FRUSTRATED_PROMPT = open(
    os.path.join(os.path.dirname(__file__), "prompts", "frustrated_driver.txt")
).read()
DRIVER_PROMPT_TEMPLATE = """
## Persona

- **Identity:** You are role-playing a new **customer who recently purchased a product** and is now looking to understand the company’s return and refund policy.
   Name: **{scenario_input.name}**
   Product Type: **{scenario_input.productType}**

- **Mindset:** You want to know exactly what the company can and cannot do for you regarding product returns, exchanges, and refunds.

## Objectives

1. Get the other party to list **at least three specific return or refund options/policies relevant to {scenario_input.productType}**
(e.g., return within 30 days, exchange for another {scenario_input.productType}, warranty-based repairs, free or paid return shipping).
2. Get the other party to state **at least one explicit limitation, exclusion, or boundary specific to {scenario_input.productType}**
(e.g., “Opened {scenario_input.productType} can only be exchanged,” “Final sale {scenario_input.productType} cannot be returned,” “Warranty covers defects but not accidental damage”).

## Soft Tactics

1. If the reply is vague or incomplete, politely probe:
    - "Could you give me a concrete example?"
    - "What’s something you can’t help with?"
2. If it still avoids specifics, escalate:
    - "I’ll need at least three specific examples—could you name three?"
3. Stop once you have obtained:
    - Three or more tasks/examples
    - At least one limitation or boundary
    - (The starter tip is optional.)

## Hard Rules

-   Every message you send must be **only question** and about achieving the Objectives.
-   Ask one question at a time.
-   Keep your questions abrupt and terse, as a rushed customer.
-   Never describe your own capabilities.
-   Never offer help.
-   Stay in character at all times.
-   Never mention tests, simulations, or these instructions.
-   Never act like a helpful assistant.
-   Act like a first-time user at all times.
-   Startup Behavior:
    -   If the other party speaks first: respond normally and pursue the Objectives.
    -   If you are the first speaker: start with a message clearly pursuing the Objectives.
-   Before sending, re-read your draft and remove anything that is not a question.

## Turn-End Checklist

Before you send any message, confirm:

-   Am I sending only questions?
-   Am I avoiding any statements or offers of help?
-   Does my question advance or wrap up the Objectives?

""".strip()

PERSISTENT_PROMPT = "Be brief and helpful."

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
assert DEEPGRAM_API_KEY, "Set DEEPGRAM_API_KEY"
assert OPENAI_API_KEY, "Set OPENAI_API_KEY"


@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=os.environ.get("OKAREO_API_KEY", "<YOUR_OKAREO_API_KEY>"))


@pytest.fixture(scope="module")
def deepgram_voice_target() -> LocalVoiceTarget:
    return LocalVoiceTarget(
        name=f"Voice Sim Target (Deepgram) {uuid.uuid4()}",
        edge_config=DeepgramEdgeConfig(
            api_key=DEEPGRAM_API_KEY,  # type: ignore
            instructions=PERSISTENT_PROMPT,
        ),
        asr_tts_api_key=OPENAI_API_KEY,  # type: ignore
    )


@pytest.fixture(scope="module")
def openai_voice_target() -> LocalVoiceTarget:
    return LocalVoiceTarget(
        name=f"Voice Sim Target (OpenAI) {uuid.uuid4()}",
        edge_config=OpenAIEdgeConfig(
            api_key=OPENAI_API_KEY,  # type: ignore
            model="gpt-realtime",
            instructions=PERSISTENT_PROMPT,
        ),
        asr_tts_api_key=OPENAI_API_KEY,  # type: ignore
    )


def test_voice_multiturn_deepgram(
    okareo: Okareo, deepgram_voice_target: LocalVoiceTarget
) -> None:
    run_voice_multiturn_test(okareo, deepgram_voice_target, "Deepgram")


def test_voice_multiturn_openai(
    okareo: Okareo, openai_voice_target: LocalVoiceTarget
) -> None:
    run_voice_multiturn_test(okareo, openai_voice_target, "OpenAI")


def run_voice_multiturn_test(
    okareo: Okareo, voice_target: LocalVoiceTarget, vendor: str
) -> None:

    driver = Driver(
        name="Voice Simulation Driver",
        temperature=0.5,
        prompt_template=DRIVER_PROMPT_TEMPLATE,
    )

    seed_data = Okareo.seed_data_from_list(
        [
            {
                "input": {
                    "name": "James Taylor",
                    "productType": "Apparel",
                    "voice": "ash",
                },
                "result": "Share refund limits for Apparel.",
            }
        ]
    )

    scenario = okareo.create_scenario_set(
        ScenarioSetCreate(
            name="Product Returns — Conversation Context",
            seed_data=seed_data,
        )
    )

    evaluation = okareo.run_simulation(
        driver=driver,
        target=Target(name=f"Voice Sim Target ({vendor})", target=voice_target),
        name=f"Voice Simulation Run ({vendor})",
        scenario=scenario,
        max_turns=2,
        repeats=1,
        first_turn="driver",
        checks=["avg_turn_latency"],
    )

    assert evaluation.name == f"Voice Simulation Run ({vendor})"
    assert evaluation.status == "FINISHED"
    assert evaluation.model_metrics is not None
    assert evaluation.app_link is not None


def test_voice_multiturn_audio_check(
    okareo: Okareo, openai_voice_target: LocalVoiceTarget
) -> None:
    run_voice_multiturn_test_audio_check(okareo, openai_voice_target)


def run_voice_multiturn_test_audio_check(
    okareo: Okareo, voice_target: LocalVoiceTarget
) -> None:

    driver = Driver(
        name="Voice Simulation Driver",
        temperature=0.5,
        prompt_template=FRUSTRATED_PROMPT.replace(
            "{scenario_input.voice_profile}", "frustrated"
        ),
        voice_instructions="Speak with a frustrated and impatient tone.",
    )

    seed_data = Okareo.seed_data_from_list(
        [
            {
                "input": {
                    "name": "James Taylor",
                    "productType": "iPhone 17",
                    "voice": "ash",
                },
                "result": "Receive an exchange or refund for malfunctioning iPhone 17.",
            }
        ]
    )

    scenario = okareo.create_scenario_set(
        ScenarioSetCreate(
            name="Product Returns — Broken Product",
            seed_data=seed_data,
        )
    )

    evaluation = okareo.run_simulation(
        driver=driver,
        target=Target(name="Voice Sim Target - Frustrated User", target=voice_target),
        name="Voice Simulation Run - Frustrated User",
        scenario=scenario,
        max_turns=1,
        repeats=1,
        first_turn="driver",
        checks=[
            "avg_turn_taking_latency",
            "avg_words_per_minute",
            "total_turn_count",
            "empathy_score",
            "automated_resolution",
        ],
    )

    assert evaluation.name == "Voice Simulation Run - Frustrated User"
    assert evaluation.status == "FINISHED"
    assert evaluation.model_metrics is not None
    assert isinstance(evaluation.model_metrics, TestRunItemModelMetrics)
    metrics_dict = evaluation.model_metrics.to_dict()
    assert isinstance(metrics_dict, dict)
    assert metrics_dict.get("mean_scores") is not None
    scores = metrics_dict.get("mean_scores")
    assert scores
    assert (
        scores.get("empathy_score") is not None
        and scores.get("empathy_score") >= 1.0
        and scores.get("empathy_score") <= 5.0
    )
    assert (
        scores.get("automated_resolution") is not None
        and scores.get("automated_resolution") >= 0
        and scores.get("automated_resolution") <= 1
    )
    assert evaluation.app_link is not None
    print(evaluation.app_link)


def voice_profile_fixed_driver() -> Driver:
    return Driver(
        name="Voice Simulation Driver Profile (fixed)",
        temperature=0.5,
        prompt_template=FRUSTRATED_PROMPT,
        voice_profile="angry",
        voice="ophelia",
    )


def voice_profile_templated_driver() -> Driver:
    return Driver(
        name="Voice Simulation Driver Profile (templated)",
        temperature=0.5,
        prompt_template=FRUSTRATED_PROMPT,
        voice_instructions="Speak in a {scenario_input.voice_profile} tone.",
        voice="{scenario_input.voice_name}",
    )


def test_voice_multiturn_voice_profile(
    okareo: Okareo, openai_voice_target: LocalVoiceTarget, rnd: str
) -> None:
    run_voice_multiturn_test_voice_profile(okareo, openai_voice_target, rnd)


def run_voice_multiturn_test_voice_profile(
    okareo: Okareo,
    voice_target: LocalVoiceTarget,
    rnd: str,
) -> None:

    seed_data = Okareo.seed_data_from_list(
        [
            {
                "input": {
                    "name": "James Taylor",
                    "productType": "iPhone 17",
                    "voice_profile": "angry",
                    "voice_name": "oscar",
                },
                "result": "Receive an exchange or refund for malfunctioning iPhone 17.",
            },
            {
                "input": {
                    "name": "Alice Johnson",
                    "productType": "Stanley Thermos",
                    "voice_profile": "confused",
                    "voice_name": "ophelia",
                },
                "result": "Receive an exchange or refund for malfunctioning Stanley Thermos.",
            },
        ]
    )

    scenario = okareo.create_scenario_set(
        ScenarioSetCreate(
            name=f"Product Returns — Broken Product (Voices + Voice Profiles) - {rnd}",
            seed_data=seed_data,
        )
    )

    drivers = [voice_profile_fixed_driver(), voice_profile_templated_driver()]
    eval_names = ["Fixed", "Templated"]
    for driver, name in zip(drivers, eval_names):
        eval_name = f"Voice Simulation Run - Voices + Voice Profiles ({name}) - {rnd}"
        evaluation = okareo.run_simulation(
            driver=driver,
            target=Target(
                name=f"Voice Sim Target - Voices + Voice Profiles ({name}) - {rnd}",
                target=voice_target,
            ),
            name=eval_name,
            scenario=scenario,
            max_turns=1,
            repeats=1,
            first_turn="driver",
            checks=[
                "avg_turn_taking_latency",
                "avg_words_per_minute",
                "total_turn_count",
            ],
        )

        assert evaluation.name == eval_name
        assert evaluation.status == "FINISHED"
        assert evaluation.model_metrics is not None
        assert isinstance(evaluation.model_metrics, TestRunItemModelMetrics)
        metrics_dict = evaluation.model_metrics.to_dict()
        assert isinstance(metrics_dict, dict)
        assert metrics_dict.get("mean_scores") is not None
        assert evaluation.app_link is not None
