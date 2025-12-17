import os
import uuid

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import Driver, Target, TwilioVoiceTarget, VoiceTarget
from okareo_api_client.models.find_test_data_point_payload import FindTestDataPointPayload
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.test_run_item_model_metrics import TestRunItemModelMetrics


# ============================================================================
# Constants
# ============================================================================

DRIVER_STARTS_PROMPT = """
## Persona
- **Identity:** You are a customer named {scenario_input.name} calling about {scenario_input.topic}.

## Rules
- Start with a greeting and your question.
- Keep messages brief.
""".strip()

TARGET_STARTS_PROMPT = """
## Persona
- **Identity:** You are a customer named {scenario_input.name} who received a call about {scenario_input.topic}.

## Rules
- Wait for the agent to greet you first.
- Respond naturally to their greeting.
""".strip()

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_PHONE = os.getenv("TWILIO_FROM_PHONE", "")
TWILIO_TO_PHONE = "+15105125993"


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(scope="module")
def rnd() -> str:
    return random_string(5)


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    return Okareo(api_key=os.environ.get("OKAREO_API_KEY", "<YOUR_OKAREO_API_KEY>"))


@pytest.fixture(scope="module")
def twilio_voice_target() -> VoiceTarget:
    return TwilioVoiceTarget(
        account_sid=TWILIO_ACCOUNT_SID,
        auth_token=TWILIO_AUTH_TOKEN,
        from_phone_number=TWILIO_FROM_PHONE,
        to_phone_number=TWILIO_TO_PHONE,
        max_parallel_requests=1,
    )


# ============================================================================
# Test: Driver Starts First
# ============================================================================

def test_voice_driver_starts_first(
    okareo: Okareo,
    twilio_voice_target: VoiceTarget,
    rnd: str,
) -> None:
    """
    Test: first_turn="driver"
    
    Validates:
    - First message is from "user" (driver)
    - Greeting transcript is captured (non-empty)
    - Audio recording exists
    """
    
    driver = Driver(
        name=f"Driver Starts Test - {rnd}",
        temperature=0.5,
        prompt_template=DRIVER_STARTS_PROMPT,
    )

    seed_data = Okareo.seed_data_from_list([
        {
            "input": {"name": "Sarah Miller", "topic": "return policy", "voice": "coral"},
            "result": "Get return policy information.",
        }
    ])

    scenario = okareo.create_scenario_set(
        ScenarioSetCreate(
            name=f"Driver Starts Scenario - {rnd}",
            seed_data=seed_data,
        )
    )

    evaluation = okareo.run_simulation(
        driver=driver,
        target=Target(name=f"Twilio Target - {rnd}", target=twilio_voice_target),
        name=f"Driver Starts Test - {rnd}",
        scenario=scenario,
        max_turns=2,
        repeats=1,
        first_turn="driver",  # <-- DRIVER STARTS
        calculate_metrics=True,
        checks=["total_turn_count"],
    )

    assert evaluation.status == "FINISHED"
    print(f"\nEvaluation Link: {evaluation.app_link}")

    # Fetch datapoints
    datapoints = okareo.find_test_data_points(
        FindTestDataPointPayload(test_run_id=evaluation.id, full_data_point=True)
    )
    assert len(datapoints) > 0

    # Validate first message
    metadata_dict = datapoints[0].model_metadata.additional_properties
    messages = metadata_dict.get("messages", [])
    assert len(messages) > 0, "Should have messages"

    first_msg = messages[0]
    first_role = first_msg.get("role")
    first_content = first_msg.get("content", "")
    first_wav = first_msg.get("metadata", {}).get("wav_path")

    # CHECK: First speaker is driver ("user")
    assert first_role == "user", f"Expected first speaker 'user', got '{first_role}'"
    
    # CHECK: Greeting transcript captured
    assert first_content.strip() != "", "Driver greeting transcript should not be empty"
    
    # CHECK: Audio recording exists
    assert first_wav is not None and first_wav != "", "Driver greeting audio should exist"

    print(f"✅ First speaker: {first_role}")
    print(f"✅ Greeting: \"{first_content}\"")
    print(f"✅ Audio: {first_wav}")


# ============================================================================
# Test: Target Starts First
# ============================================================================

def test_voice_target_starts_first(
    okareo: Okareo,
    twilio_voice_target: VoiceTarget,
    rnd: str,
) -> None:
    """
    Test: first_turn="target"
    
    Validates:
    - First message is from "assistant" (target)
    - Greeting transcript is captured (non-empty)
    - Audio recording exists
    """
    
    driver = Driver(
        name=f"Target Starts Test - {rnd}",
        temperature=0.5,
        prompt_template=TARGET_STARTS_PROMPT,
    )

    seed_data = Okareo.seed_data_from_list([
        {
            "input": {"name": "Mike Johnson", "topic": "order status", "voice": "ash"},
            "result": "Get order status information.",
        }
    ])

    scenario = okareo.create_scenario_set(
        ScenarioSetCreate(
            name=f"Target Starts Scenario - {rnd}",
            seed_data=seed_data,
        )
    )

    evaluation = okareo.run_simulation(
        driver=driver,
        target=Target(name=f"Twilio Target - {rnd}", target=twilio_voice_target),
        name=f"Target Starts Test - {rnd}",
        scenario=scenario,
        max_turns=2,
        repeats=1,
        first_turn="target",  # <-- TARGET STARTS
        calculate_metrics=True,
        checks=["total_turn_count"],
    )

    assert evaluation.status == "FINISHED"
    print(f"\nEvaluation Link: {evaluation.app_link}")

    # Fetch datapoints
    datapoints = okareo.find_test_data_points(
        FindTestDataPointPayload(test_run_id=evaluation.id, full_data_point=True)
    )
    assert len(datapoints) > 0

    # Validate first message
    metadata_dict = datapoints[0].model_metadata.additional_properties
    messages = metadata_dict.get("messages", [])
    assert len(messages) > 0, "Should have messages"

    first_msg = messages[0]
    first_role = first_msg.get("role")
    first_content = first_msg.get("content", "")
    first_wav = first_msg.get("metadata", {}).get("wav_path")

    # CHECK: First speaker is target ("assistant")
    assert first_role == "assistant", f"Expected first speaker 'assistant', got '{first_role}'"
    
    # CHECK: Greeting transcript captured
    assert first_content.strip() != "", "Target greeting transcript should not be empty"
    
    # CHECK: Audio recording exists
    assert first_wav is not None and first_wav != "", "Target greeting audio should exist"

    print(f"✅ First speaker: {first_role}")
    print(f"✅ Greeting: \"{first_content}\"")
    print(f"✅ Audio: {first_wav}")

# ============================================================================
# Test: Concurrent Driver Messages
# ============================================================================

def test_voice_concurrent_driver_messages(
    okareo: Okareo,
    twilio_voice_target: VoiceTarget,
    rnd: str,
) -> None:
    """
    Test: concurrent_ask_probability=1.0
    
    Validates:
    - Driver sends 2 consecutive messages before target responds
    - Message sequence: user → user → assistant
    """
    
    driver = Driver(
        name=f"Concurrent Driver Test - {rnd}",
        temperature=0.5,
        prompt_template=DRIVER_STARTS_PROMPT,
    )

    seed_data = Okareo.seed_data_from_list([
        {
            "input": {"name": "Jane Doe", "topic": "shipping options", "voice": "ash"},
            "result": "Get shipping information.",
        }
    ])

    scenario = okareo.create_scenario_set(
        ScenarioSetCreate(
            name=f"Concurrent Driver Scenario - {rnd}",
            seed_data=seed_data,
        )
    )

    evaluation = okareo.run_simulation(
        driver=driver,
        target=Target(name=f"Twilio Target - {rnd}", target=twilio_voice_target),
        name=f"Concurrent Driver Test - {rnd}",
        scenario=scenario,
        max_turns=2,
        repeats=1,
        first_turn="driver",
        concurrent_ask_probability=1.0,  # <-- DRIVER SENDS 2 MESSAGES IN A ROW
        calculate_metrics=True,
        checks=["total_turn_count"],
    )

    assert evaluation.status == "FINISHED"
    print(f"\nEvaluation Link: {evaluation.app_link}")

    # Fetch datapoints
    datapoints = okareo.find_test_data_points(
        FindTestDataPointPayload(test_run_id=evaluation.id, full_data_point=True)
    )
    assert len(datapoints) > 0

    # Validate message sequence
    metadata_dict = datapoints[0].model_metadata.additional_properties
    messages = metadata_dict.get("messages", [])
    
    assert len(messages) >= 3, f"Should have at least 3 messages (user, user, assistant), got {len(messages)}"

    # CHECK: First two messages are from driver ("user")
    first_role = messages[0].get("role")
    second_role = messages[1].get("role")
    third_role = messages[2].get("role")

    assert first_role == "user", f"Message 1: expected 'user', got '{first_role}'"
    assert second_role == "user", f"Message 2: expected 'user', got '{second_role}'"
    assert third_role == "assistant", f"Message 3: expected 'assistant', got '{third_role}'"

    print(f"✅ Message 1: {first_role} - \"{messages[0].get('content', '')[:50]}...\"")
    print(f"✅ Message 2: {second_role} - \"{messages[1].get('content', '')[:50]}...\"")
    print(f"✅ Message 3: {third_role} - \"{messages[2].get('content', '')[:50]}...\"")
    print(f"✅ Concurrent driver messages confirmed: user → user → assistant")
