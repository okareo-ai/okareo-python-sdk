"""End-to-end integration tests for conversation ingestion.

This test validates the complete conversation monitoring flow:
1. Ingest conversations with audio and transcript
2. Verify datapoints are created
3. Verify monitors match and trigger checks
4. Validate transcript_fidelity check execution
"""

import base64
import os
import time
from typing import Any, Dict, List
from uuid import UUID

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.checks import CodeBasedCheck, ModelBasedCheck
from okareo_api_client.models import ScenarioSetCreate
from okareo_api_client.models.datapoint_search import DatapointSearch


# Test data file paths
TEST_AUDIO_FILE = "okareo_tests/audio/call_times.mp3"
TEST_TRANSCRIPT_FILE = "okareo_tests/audio/call_times_transcript.json"


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    """Initialize Okareo client with API key."""
    return Okareo(api_key=API_KEY)


@pytest.fixture(scope="module")
def test_project(okareo_client: Okareo) -> str:
    """Get a test project for conversation ingestion tests."""
    # For monitoring path, we just need a project - no MUT required
    return okareo_client.get_projects()[0].id


@pytest.fixture(scope="module")
def test_audio_bytes() -> bytes:
    """Load test audio file."""
    if not os.path.exists(TEST_AUDIO_FILE):
        pytest.skip(f"Test audio file not found: {TEST_AUDIO_FILE}")
    
    with open(TEST_AUDIO_FILE, "rb") as f:
        return f.read()


@pytest.fixture(scope="module")
def test_transcript() -> Dict[str, Any]:
    """Load expected transcript."""
    if not os.path.exists(TEST_TRANSCRIPT_FILE):
        pytest.skip(f"Test transcript file not found: {TEST_TRANSCRIPT_FILE}")
    
    import json
    with open(TEST_TRANSCRIPT_FILE, "r") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def test_monitor(okareo_client: Okareo, test_project: str) -> str:
    """Create a test monitor with transcript_fidelity check."""
    # TODO: This requires the monitor/filter group API which may need to be added
    # For now, this is a placeholder showing the intended structure
    
    # Create a check for transcript fidelity
    check_name = f"test_transcript_fidelity_{random_string(8)}"
    
    # Note: The actual API for creating monitors may differ
    # This is the conceptual structure we want to test
    monitor_config = {
        "name": f"test_monitor_{random_string(8)}",
        "project_id": test_project,
        "filter": {
            "tags": ["e2e-test"],
        },
        "checks": [
            {
                "type": "transcript_fidelity",
                "name": check_name,
                "threshold": 4.0,
            }
        ]
    }
    
    # Placeholder - actual implementation depends on monitor API
    # return monitor_id
    pytest.skip("Monitor creation API not yet implemented in SDK")


class TestConversationIngestionE2E:
    """End-to-end tests for conversation ingestion and monitoring."""
    
    def test_ingest_with_transcript(
        self,
        okareo_client: Okareo,
        test_project: str,
        test_audio_bytes: bytes,
        test_transcript: Dict[str, Any],
    ) -> None:
        """Test ingesting a conversation with pre-parsed transcript."""
        
        # Encode audio as base64
        audio_b64 = base64.b64encode(test_audio_bytes).decode('utf-8')
        
        # Ingest the conversation (monitoring path - no MUT required)
        call_id = f"e2e_test_call_{random_string(8)}"
        print(f'project_id={test_project}')
        response = okareo_client.ingest_conversations(
            project_id=test_project,
            conversations=[
                {
                    "source_platform": "custom", # twilio | retell | vapi
                    "call_id": call_id,
                    "audio": {
                        "type": "inline_b64",
                        "inline_b64": audio_b64,
                    },
                    "transcript": test_transcript["turns"],
                    "tags": ["e2e-test", "with-transcript"],
                    "metadata": {
                        "test_type": "e2e",
                        "expected_duration": test_transcript["metadata"]["duration_seconds"],
                    },
                }
            ]
        )
        
        # Verify response
        assert response["status"] == "accepted"
        assert len(response["conversations"]) == 1
        assert response["conversations"][0]["call_id"] == call_id
        
        # Wait for async processing to complete
        # The conversation needs to be processed by the TaskListener
        time.sleep(10)
        
        # Query datapoints by context_token (call_id)
        # Each conversation's call_id becomes the context_token for all its datapoints
        search = DatapointSearch(context_token=call_id)
        datapoints = okareo_client.find_datapoints(search)
        
        # Verify datapoints were created (one for the entire conversation)
        assert len(datapoints) == 1, (
            f"Expected exactly 1 datapoint, "
            f"got {len(datapoints)}"
        )
        
        # Verify datapoint structure
        dp = datapoints[0]
        assert dp.context_token == call_id
        
        metadata = getattr(dp.model_metadata, "additional_properties", dp.model_metadata) if hasattr(dp.model_metadata, "additional_properties") else dp.model_metadata
        
        assert "source_platform" in metadata
        assert metadata["source_platform"] == "custom"
        assert "call_id" in metadata
        assert "voice_file_id" in metadata  # Audio was stored

        # Verify turn content matches expected transcript (allowing for missing keys like speaker_id)
        input_val = getattr(dp.input_, "additional_properties", dp.input_) if hasattr(dp.input_, "additional_properties") else dp.input_
        assert len(input_val) == len(test_transcript["turns"])
        for i, turn in enumerate(input_val):
            expected_turn = test_transcript["turns"][i]
            assert turn["role"] == expected_turn["role"]
            assert turn["content"] == expected_turn["content"]
    
    def test_ingest_audio_only_with_diarization(
        self,
        okareo_client: Okareo,
        test_project: str,
        test_audio_bytes: bytes,
        test_transcript: Dict[str, Any],
    ) -> None:
        """Test ingesting audio-only conversation (triggers diarization)."""
        
        # Encode audio as base64
        audio_b64 = base64.b64encode(test_audio_bytes).decode('utf-8')
        
        # Ingest without transcript - will trigger diarization
        call_id = f"e2e_audio_only_{random_string(8)}"
        response = okareo_client.ingest_conversations(
            project_id=test_project,
            conversations=[
                {
                    "source_platform": "custom",
                    "call_id": call_id,
                    "audio": {
                        "type": "inline_b64",
                        "inline_b64": audio_b64,
                    },
                    "diarization": True,
                    "first_turn": "assistant",  # Specify who spoke first
                    "tags": ["e2e-test", "audio-only"],
                    "metadata": {
                        "test_type": "diarization",
                    },
                }
            ]
        )
        
        assert response["status"] == "accepted"
        
        # Wait longer for diarization + ASR processing
        time.sleep(20)
        
        # Query datapoints by context_token
        search = DatapointSearch(context_token=call_id)
        datapoints = okareo_client.find_datapoints(search)
        
        # Verify datapoints were created
        # Note: We can't expect exact turn count since diarization may differ
        # But we should get at least some turns
        assert len(datapoints) > 0, "No datapoints created from audio-only ingestion"
        
        # Verify all datapoints have transcribed content
        for dp in datapoints:
            # At least one of input_ or result should have content
            assert (dp.input_ and len(dp.input_) > 0) or (
                dp.result and len(dp.result) > 0
            ), "Datapoint has no transcribed content"
            
            # Verify audio was stored
            assert "voice_file_id" in dp.model_metadata
    
    def test_batch_ingestion(
        self,
        okareo_client: Okareo,
        test_project: str,
        test_transcript: Dict[str, Any],
    ) -> None:
        """Test ingesting multiple conversations in a single batch."""
        
        batch_size = 3
        conversations = []
        call_ids = []
        
        for i in range(batch_size):
            call_id = f"e2e_batch_{i}_{random_string(6)}"
            call_ids.append(call_id)
            conversations.append({
                "source_platform": "custom",
                "call_id": call_id,
                "transcript": [
                    {
                        "role": "user",
                        "content": f"Batch test conversation {i}",
                        "timestamp_ms": 0,
                    },
                    {
                        "role": "assistant",
                        "content": f"Response {i}",
                        "timestamp_ms": 1000,
                    },
                ],
                "tags": ["e2e-test", "batch"],
            })
        
        # Ingest batch
        response = okareo_client.ingest_conversations(
            project_id=test_project,
            conversations=conversations
        )
        
        assert response["status"] == "accepted"
        assert len(response["conversations"]) == batch_size
        
        # Verify all call_ids are present
        returned_call_ids = [c["call_id"] for c in response["conversations"]]
        for call_id in call_ids:
            assert call_id in returned_call_ids
        
        # Wait for processing
        time.sleep(10)
        
        # Verify datapoints for all conversations
        # Query each conversation individually by context_token
        all_datapoints = []
        for call_id in call_ids:
            search = DatapointSearch(context_token=call_id)
            dps = okareo_client.find_datapoints(search)
            all_datapoints.extend(dps)
        
        # Should have 2 datapoints per conversation (1 user turn + 1 assistant turn)
        assert len(all_datapoints) >= batch_size * 2
        
        # Verify all call_ids are represented
        found_call_ids = set(dp.context_token for dp in all_datapoints)
        for call_id in call_ids:
            assert call_id in found_call_ids
    
    @pytest.mark.skip(reason="Monitor API integration pending")
    def test_monitor_matching_and_check_execution(
        self,
        okareo_client: Okareo,
        test_project: str,
        test_monitor: str,
        test_audio_bytes: bytes,
        test_transcript: Dict[str, Any],
    ) -> None:
        """Test that monitors match ingested conversations and execute checks."""
        
        # This test will be implemented once the monitor API is available
        # It should:
        # 1. Ingest a conversation with tags that match the monitor filter
        # 2. Wait for processing
        # 3. Verify the monitor matched the conversation
        # 4. Verify the transcript_fidelity check was executed
        # 5. Verify check results are available
        
        pass


# Cleanup function for local testing
def teardown_module(module):
    """Clean up test data after all tests complete."""
    # In production, you may want to delete test datapoints, monitors, etc.
    # For now, we'll leave them for manual inspection
    pass
