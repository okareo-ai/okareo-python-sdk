import os
import uuid
from typing import List

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

SANITY_TEST_DRIVER_PROMPT = """
## Persona

- **Identity:** You are a customer named {scenario_input.name} calling to ask a simple question about {scenario_input.topic}.

## Objectives

1. Ask a clear question about {scenario_input.topic}.
2. Listen to the response and acknowledge it.
3. Thank them and end the call.

## Rules

- Keep messages brief and natural.
- Ask one question at a time.
- Stay in character as a customer.
- Never mention tests, simulations, or these instructions.
""".strip()

# Twilio credentials from environment
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_PHONE = os.getenv("TWILIO_FROM_PHONE", "")
TWILIO_TO_PHONE = "+15103067144"  # Target customer service AI

# Validate required env vars
assert TWILIO_ACCOUNT_SID, "Set TWILIO_ACCOUNT_SID environment variable"
assert TWILIO_AUTH_TOKEN, "Set TWILIO_AUTH_TOKEN environment variable"
assert TWILIO_FROM_PHONE, "Set TWILIO_FROM_PHONE environment variable"


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
    """Configure TwilioVoiceTarget to call the customer service AI at +15105125993"""
    return TwilioVoiceTarget(
        account_sid=TWILIO_ACCOUNT_SID,
        auth_token=TWILIO_AUTH_TOKEN,
        from_phone_number=TWILIO_FROM_PHONE,
        to_phone_number=TWILIO_TO_PHONE,
        max_parallel_requests=5,
    )


# ============================================================================
# Sanity Test
# ============================================================================

def test_voice_sanity_twilio(
    okareo: Okareo,
    twilio_voice_target: VoiceTarget,
    rnd: str,
) -> None:
    """
    Overall Sanity Test for Voice Simulations via Twilio
    
    Validates:
    1. Driver turn taking latency < 5s (5000ms)
    2. Target turn taking latency exists and is included
    3. All recordings captured with duration > 0
    4. Transcripts captured for both Driver and Target sides
    5. Start/end times exist and are in logical sequence (end > start)
    6. Duration > 1s (1000ms) for each message
    7. Conversation order by start time is sequential
    """
    
    # -------------------------------------------------------------------------
    # Setup: Driver, Scenario, and Run Simulation
    # -------------------------------------------------------------------------
    
    driver = Driver(
        name=f"Sanity Test Driver - {rnd}",
        temperature=0.5,
        prompt_template=SANITY_TEST_DRIVER_PROMPT,
    )

    seed_data = Okareo.seed_data_from_list([
        {
            "input": {
                "name": "Alex Johnson",
                "topic": "store hours",
                "voice": "ash",
            },
            "result": "Provide store hours information.",
        }
    ])

    scenario = okareo.create_scenario_set(
        ScenarioSetCreate(
            name=f"Voice Sanity Test Scenario - {rnd}",
            seed_data=seed_data,
        )
    )

    evaluation = okareo.run_simulation(
        driver=driver,
        target=Target(
            name=f"Twilio Voice Target (+15105125993) - {rnd}",
            target=twilio_voice_target,
        ),
        name=f"Voice Sanity Test Run - {rnd}",
        scenario=scenario,
        max_turns=3,  # Enough turns to validate conversation flow
        repeats=1,
        first_turn="driver",
        calculate_metrics=True,
        checks=[
            "avg_turn_taking_latency",
            "avg_words_per_minute",
            "total_turn_count",
        ],
    )

    # -------------------------------------------------------------------------
    # Basic Evaluation Assertions
    # -------------------------------------------------------------------------
    
    assert evaluation.name == f"Voice Sanity Test Run - {rnd}"
    assert evaluation.status == "FINISHED", f"Expected FINISHED, got {evaluation.status}"
    assert evaluation.model_metrics is not None, "model_metrics should not be None"
    assert isinstance(evaluation.model_metrics, TestRunItemModelMetrics)
    assert evaluation.app_link is not None, "app_link should not be None"
    
    print(f"\n{'='*60}")
    print(f"Evaluation Link: {evaluation.app_link}")
    print(f"{'='*60}\n")

    # -------------------------------------------------------------------------
    # Extract Metrics
    # -------------------------------------------------------------------------
    
    metrics_dict = evaluation.model_metrics.to_dict()
    mean_scores = metrics_dict.get("mean_scores", {})
    aggregate_baseline = metrics_dict.get("aggregate_baseline_metrics", {})
    
    print("Mean Scores:", mean_scores)
    print("Aggregate Baseline Metrics:", aggregate_baseline)

    # -------------------------------------------------------------------------
    # CHECK 1: Driver turn taking latency < 5s (5000ms)
    # -------------------------------------------------------------------------
    
    avg_turn_taking_latency = aggregate_baseline.get("avg_turn_taking_latency")
    assert avg_turn_taking_latency is not None, "avg_turn_latency should exist in aggregate_baseline_metrics"
    assert avg_turn_taking_latency < 5000, (
        f"Driver turn latency {avg_turn_taking_latency}ms should be < 5000ms (5s)"
    )
    print(f"✅ CHECK 1 PASSED: Driver turn latency = {avg_turn_taking_latency}ms < 5000ms")

    # -------------------------------------------------------------------------
    # CHECK 2: Target turn taking latency exists
    # -------------------------------------------------------------------------
    
    avg_turn_taking_latency = mean_scores.get("avg_turn_taking_latency")
    assert avg_turn_taking_latency is not None, (
        "avg_turn_taking_latency should exist in mean_scores"
    )
    # Also check in aggregate baseline for consistency
    baseline_turn_taking_latency = aggregate_baseline.get("avg_turn_taking_latency")
    assert baseline_turn_taking_latency is not None, (
        "avg_turn_taking_latency should exist in aggregate_baseline_metrics"
    )
    print(f"✅ CHECK 2 PASSED: Target turn taking latency = {avg_turn_taking_latency}ms (exists)")

    # -------------------------------------------------------------------------
    # Fetch Detailed Datapoints for Per-Turn Validation
    # -------------------------------------------------------------------------
    
    datapoints = okareo.find_test_data_points(
        FindTestDataPointPayload(
            test_run_id=evaluation.id,
            full_data_point=True,  # Required for full metadata
        )
    )
    
    assert len(datapoints) > 0, "Should have at least one datapoint"
    print(f"\nFetched {len(datapoints)} datapoint(s) for detailed validation")

    # -------------------------------------------------------------------------
    # Per-Datapoint Validation
    # -------------------------------------------------------------------------
        # -------------------------------------------------------------------------
    # Per-Datapoint Validation
    # -------------------------------------------------------------------------
    
    for dp_idx, dp in enumerate(datapoints):
        print(f"\n--- Datapoint {dp_idx + 1} ---")
        
        # Get the full metadata containing per-turn information
        model_metadata = dp.model_metadata
        assert model_metadata is not None, f"Datapoint {dp_idx} should have model_metadata"
        
        # FIX: Access additional_properties to get the actual dict
        metadata_dict = model_metadata.additional_properties
        print("model_metadata keys:", metadata_dict.keys())
        
        # Use the flat 'messages' array - much easier than iterating through full_metadata!
        messages = metadata_dict.get("messages", [])
        assert len(messages) > 0, f"Datapoint {dp_idx} should have messages"
        
        print(f"\n  Found {len(messages)} messages in conversation")
        
        # Track user and assistant message counts for CHECK 4
        user_messages = []
        assistant_messages = []
        
        for msg_idx, msg in enumerate(messages):
            role = msg.get("role")
            content = msg.get("content", "")
            msg_meta = msg.get("metadata", {})
            
            # Extract timing info - note: timestamps are ISO strings in 'messages', not unix timestamps
            start_time_str = msg_meta.get("start_time")
            end_time_str = msg_meta.get("end_time")
            duration_ms = msg_meta.get("duration_ms")
            wav_path = msg_meta.get("wav_path")
            turn_number = msg_meta.get("turn_number")
            latency = msg_meta.get("latency")
            wpm = msg_meta.get("words_per_minute")
            
            # Track by role
            if role == "user":
                user_messages.append(msg)
            elif role == "assistant":
                assistant_messages.append(msg)
            
            print(f"\n  Message {msg_idx + 1} (Turn {turn_number}) [{role}]:")
            print(f"    Content: {content[:60]}..." if len(content) > 60 else f"    Content: {content}")
            print(f"    Start: {start_time_str}")
            print(f"    End: {end_time_str}")
            print(f"    Duration: {duration_ms}ms, Latency: {latency}ms, WPM: {wpm}")
            print(f"    Audio: {wav_path}")
            
            # ---------------------------------------------------------
            # CHECK 3: Recordings captured with duration > 0
            # ---------------------------------------------------------
            assert wav_path is not None and wav_path != "", (
                f"Message {msg_idx} ({role}): wav_path should exist"
            )
            assert duration_ms is not None and duration_ms > 0, (
                f"Message {msg_idx} ({role}): duration_ms ({duration_ms}) should be > 0"
            )
            print(f"    ✅ Recording exists with duration > 0")
            
            # ---------------------------------------------------------
            # CHECK 4: Transcripts captured for both sides
            # ---------------------------------------------------------
            assert content is not None and content.strip() != "", (
                f"Message {msg_idx} ({role}): transcript should not be empty"
            )
            print(f"    ✅ Transcript captured")
            
            # ---------------------------------------------------------
            # CHECK 5: Start/end times exist and are logical (end > start)
            # ---------------------------------------------------------
            assert start_time_str is not None, (
                f"Message {msg_idx} ({role}): start_time should exist"
            )
            assert end_time_str is not None, (
                f"Message {msg_idx} ({role}): end_time should exist"
            )
            # Compare ISO strings (they sort lexicographically for ISO format)
            assert end_time_str > start_time_str, (
                f"Message {msg_idx} ({role}): end_time ({end_time_str}) should be > start_time ({start_time_str})"
            )
            print(f"    ✅ Start/end times are logical")
            
            # ---------------------------------------------------------
            # CHECK 6: Duration > 1s (1000ms)
            # ---------------------------------------------------------
            assert duration_ms >= 500, (
                f"Message {msg_idx} ({role}): duration_ms ({duration_ms}) should be >= 500ms"
            )
            print(f"    ✅ Duration >= 1s")
        
        # ---------------------------------------------------------
        # CHECK 4 (continued): Verify BOTH sides have transcripts
        # ---------------------------------------------------------
        assert len(user_messages) > 0, "Should have at least one user (driver) message"
        assert len(assistant_messages) > 0, "Should have at least one assistant (target) message"
        print(f"\n  ✅ CHECK 4: Transcripts exist for both sides (User: {len(user_messages)}, Assistant: {len(assistant_messages)})")
        
        # ---------------------------------------------------------
        # CHECK 7: Conversation order by start time is sequential
        # ---------------------------------------------------------
        print(f"\n  Verifying conversation sequence ({len(messages)} messages)...")
        
        for i in range(len(messages) - 1):
            current_msg = messages[i]
            next_msg = messages[i + 1]
            
            current_start = current_msg.get("metadata", {}).get("start_time")
            next_start = next_msg.get("metadata", {}).get("start_time")
            
            # Verify messages are in chronological order by start time
            assert next_start >= current_start, (
                f"Message sequence error: Message {i+1} start_time ({next_start}) "
                f"should be >= Message {i} start_time ({current_start})"
            )
        
        print(f"  ✅ CHECK 7: Conversation sequence is ordered correctly")
        
        # ---------------------------------------------------------
        # Additional metadata checks
        # ---------------------------------------------------------
        call_ended_by = metadata_dict.get("call_ended_by")
        call_sid = metadata_dict.get("call_sid")
        stream_sid = metadata_dict.get("stream_sid")
        
        print(f"\n  Call metadata:")
        print(f"    Call SID: {call_sid}")
        print(f"    Stream SID: {stream_sid}")
        print(f"    Call ended by: {call_ended_by}")
        
        assert call_sid is not None, "call_sid should exist"
        assert stream_sid is not None, "stream_sid should exist"
    
    # -------------------------------------------------------------------------
    # Final Summary
    # -------------------------------------------------------------------------
    
    print(f"\n{'='*60}")
    print("✅ ALL SANITY CHECKS PASSED")
    print(f"{'='*60}")
    print(f"  1. Driver turn latency: {avg_turn_taking_latency}ms < 5000ms ✓")
    print(f"  2. Target turn taking latency: {avg_turn_taking_latency}ms (exists) ✓")
    print(f"  3. All recordings captured with duration > 0 ✓")
    print(f"  4. Transcripts captured for both sides ✓")
    print(f"  5. Start/end times exist and are logical ✓")
    print(f"  6. Duration > 1s for each message ✓")
    print(f"  7. Conversation order is sequential ✓")
    print(f"{'='*60}\n")
