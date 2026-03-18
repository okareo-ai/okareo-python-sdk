"""Integration tests for audio file upload, download, and scenario creation."""

import io
import os
import struct
import tempfile
import wave

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo


def _make_wav_bytes(duration_s: float = 0.5, sample_rate: int = 16000) -> bytes:
    """Generate a minimal valid WAV file (mono, 16-bit PCM, silence)."""
    n_samples = int(sample_rate * duration_s)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack(f"<{n_samples}h", *([0] * n_samples)))
    return buf.getvalue()


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


@pytest.fixture(scope="module")
def wav_bytes() -> bytes:
    return _make_wav_bytes()


class TestUploadVoice:
    def test_upload_wav_bytes(self, okareo_client: Okareo, wav_bytes: bytes) -> None:
        resp = okareo_client.upload_voice(file_bytes=wav_bytes)
        assert resp.file_id is not None
        assert resp.file_url is not None
        assert "/v0/voice/file/" in resp.file_url
        assert resp.file_duration > 0

    def test_upload_wav_file(self, okareo_client: Okareo, wav_bytes: bytes) -> None:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(wav_bytes)
            tmp_path = f.name
        try:
            resp = okareo_client.upload_voice(file_path=tmp_path)
            assert resp.file_id is not None
            assert resp.file_url is not None
        finally:
            os.unlink(tmp_path)


class TestDownloadVoice:
    def test_roundtrip(self, okareo_client: Okareo, wav_bytes: bytes) -> None:
        """Upload WAV, download, verify valid WAV or MP3 magic bytes."""
        upload_resp = okareo_client.upload_voice(file_bytes=wav_bytes)
        audio_bytes = okareo_client.download_voice(upload_resp.file_url)
        assert len(audio_bytes) > 0
        # Accept WAV (RIFF) or MP3 (frame-sync or ID3 tag)
        is_wav = audio_bytes[:4] == b"RIFF"
        is_mp3 = (
            audio_bytes[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2")
            or audio_bytes[:3] == b"ID3"
        )
        assert is_wav or is_mp3, f"Unexpected audio header: {audio_bytes[:4]}"


class TestCreateScenarioSetWithAudioFiles:
    def test_end_to_end(self, okareo_client: Okareo, wav_bytes: bytes) -> None:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(wav_bytes)
            tmp_path = f.name
        try:
            name = f"audio-test-{random_string(8)}"
            scenario = okareo_client.create_scenario_set_with_audio_files(
                name=name,
                data_list=[
                    {"input": tmp_path, "result": "silence"},
                ],
            )
            assert scenario.scenario_id is not None
            assert scenario.name == name

            data_points = okareo_client.get_scenario_data_points(scenario.scenario_id)
            assert len(data_points) == 1
            dp = data_points[0]
            assert "/v0/voice/file/" in str(dp.input_)
            assert dp.result == "silence"
        finally:
            os.unlink(tmp_path)
