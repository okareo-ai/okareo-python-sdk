"""Unit tests for the client-level Project (project separation, Phase 7).

Hermetic — every network call is mocked. Covers: validation at construction and in
set_project; precedence (per-call / explicitly-set field → client-level → server
default); fill-on-copy for caller-built payloads (UNSET only — an explicit None is
an explicitly-set field and wins); Project name validation; and the lifecycle
methods' parsers (the GET routes' 201, the hand-written PATCH module's 200).

Precedence is asserted on the request a public method actually sends, never on the
private resolver — a method that forgets to call the resolver has to fail here.
"""

import json
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

import httpx
import pytest
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo_api_client.models.datapoint_filter_search_payload import (
    DatapointFilterSearchPayload,
)
from okareo_api_client.models.datapoint_search import DatapointSearch
from okareo_api_client.types import UNSET

GLOBAL_ID = "0156f5d7-4ac4-4568-9d44-24750aa08d1a"
OTHER_ID = "8a2b45f1-9c63-4b21-b7d8-1f2e3a4b5c6d"

PROJECTS_JSON = [
    {"id": GLOBAL_ID, "name": "Global", "onboarding_status": "s", "tags": []},
    {"id": OTHER_ID, "name": "Billing Agent", "onboarding_status": "s", "tags": []},
]

MUT_JSON = {
    "id": "3f2b9a1c-5d6e-4f80-9a1b-2c3d4e5f6a7b",
    "project_id": GLOBAL_ID,
    "name": "CI target",
    "tags": [],
    "time_created": "2024-01-01T00:00:00",
}

SCENARIO_JSON = {
    "project_id": GLOBAL_ID,
    "scenario_id": "6b1f0c2d-8e3a-4d5b-9c7e-1a2b3c4d5e6f",
    "time_created": "2024-01-01T00:00:00",
    "type": "SEED",
}

VOICE_JSON = {
    "file_id": "9c8b7a6d-5e4f-4a3b-8c9d-0e1f2a3b4c5d",
    "file_url": "https://example.com/audio.mp3",
    "file_duration": 1000.0,
    "time_created": "2024-01-01T00:00:00",
}


def _mock_projects(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json=PROJECTS_JSON, status_code=201)


def _sent_body(httpx_mock: HTTPXMock) -> Any:
    """The JSON body of the last outgoing request."""
    return json.loads(httpx_mock.get_requests()[-1].content)


def _mock_upload(httpx_mock: HTTPXMock) -> Dict[str, bytes]:
    """Answer the scenario-set upload, capturing the body it was sent.

    A multipart body streams from an open file handle, so it can only be read
    while the request is in flight — hence a callback rather than reading
    ``get_requests()[-1].content`` afterwards.
    """
    captured: Dict[str, bytes] = {}

    def respond(request: httpx.Request) -> httpx.Response:
        captured["content"] = request.read()
        return httpx.Response(200, json=SCENARIO_JSON)

    httpx_mock.add_callback(respond, method="POST")
    return captured


def _multipart_project_id(content: bytes) -> Optional[str]:
    """The ``project_id`` part of a multipart body, or None when it has none."""
    body = content.decode()
    marker = 'name="project_id"'
    if marker not in body:
        return None
    return body.split(marker, 1)[1].split("\r\n\r\n", 1)[1].split("\r\n", 1)[0]


def _scenario_file(tmp_path: Path) -> str:
    path = tmp_path / "scenario.jsonl"
    path.write_text('{"input": "hello", "result": "world"}\n')
    return str(path)


class TestConstructionValidation:
    def test_valid_project_id_is_stored_normalized(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project=OTHER_ID.upper())
        assert client.project_id == OTHER_ID  # normalized through UUID

    def test_unknown_project_id_fails_loudly(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        with pytest.raises(ValueError, match="Unknown project"):
            Okareo("k", "http://mocked.com", project=str(uuid.uuid4()))

    def test_no_project_keeps_server_default_semantics(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")
        assert client.project_id is None


class TestProjectByName:
    """A Project may be named by its name as well as its id — names are unique
    per organization (case-insensitively), so a name resolves to exactly one."""

    def test_constructor_accepts_a_project_name(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project="Billing Agent")
        assert client.project_id == OTHER_ID

    def test_name_match_is_case_insensitive(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project="billing AGENT")
        assert client.project_id == OTHER_ID

    def test_surrounding_whitespace_is_ignored(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project="  Billing Agent  ")
        assert client.project_id == OTHER_ID

    def test_set_project_accepts_a_name(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")
        _mock_projects(httpx_mock)  # set_project fetches fresh
        client.set_project("Billing Agent")
        assert client.project_id == OTHER_ID

    def test_unknown_name_names_every_available_project(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        with pytest.raises(ValueError) as exc:
            Okareo("k", "http://mocked.com", project="Billing Team")
        message = str(exc.value)
        assert "Unknown project 'Billing Team'" in message
        assert f"Global ({GLOBAL_ID})" in message
        assert f"Billing Agent ({OTHER_ID})" in message

    def test_a_name_is_never_mistaken_for_an_id(self, httpx_mock: HTTPXMock) -> None:
        # An id that parses as a UUID but matches no Project must not fall
        # through to a name lookup and quietly succeed.
        _mock_projects(httpx_mock)
        with pytest.raises(ValueError, match="Unknown project"):
            Okareo("k", "http://mocked.com", project=str(uuid.uuid4()))


class TestSetProject:
    def test_set_project_validates_against_fresh_list(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")
        _mock_projects(httpx_mock)  # set_project fetches fresh
        client.set_project(OTHER_ID)
        assert client.project_id == OTHER_ID

    def test_set_project_none_clears(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project=GLOBAL_ID)
        client.set_project(None)
        assert client.project_id is None


class TestPrecedence:
    """Precedence — per-call > client-level > server default — proven through the
    public methods, on the request each one actually sends. Asserting on the
    helper instead would prove the helper works while proving nothing about
    whether a method calls it."""

    def test_per_call_project_wins_over_client_level(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project=GLOBAL_ID)
        httpx_mock.add_response(json=MUT_JSON, status_code=201)

        client.register_model(name="CI target", project_id=OTHER_ID)

        assert _sent_body(httpx_mock)["project_id"] == OTHER_ID

    def test_client_level_project_fills_an_omitted_project_id(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project=GLOBAL_ID)
        httpx_mock.add_response(json=MUT_JSON, status_code=201)

        client.register_model(name="CI target")

        assert _sent_body(httpx_mock)["project_id"] == GLOBAL_ID

    def test_no_project_anywhere_sends_no_project_id(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")
        httpx_mock.add_response(json=MUT_JSON, status_code=201)

        client.register_model(name="CI target")

        assert "project_id" not in _sent_body(httpx_mock)

    def test_find_test_runs_scopes_to_the_client_project(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project=GLOBAL_ID)
        httpx_mock.add_response(json=[], status_code=200)

        client.find_test_runs()

        assert _sent_body(httpx_mock)["project_id"] == GLOBAL_ID

    def test_find_test_runs_per_call_project_wins(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project=GLOBAL_ID)
        httpx_mock.add_response(json=[], status_code=200)

        client.find_test_runs(project_id=OTHER_ID)

        assert _sent_body(httpx_mock)["project_id"] == OTHER_ID

    def test_upload_voice_scopes_to_the_client_project(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project=OTHER_ID)
        httpx_mock.add_response(json=VOICE_JSON, status_code=201)

        client.upload_voice(file_bytes=b"audio-bytes")

        assert _sent_body(httpx_mock)["project_id"] == OTHER_ID

    def test_ingest_conversations_scopes_to_the_client_project(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project=OTHER_ID)
        httpx_mock.add_response(json={"status": "ok"}, status_code=200)

        client.ingest_conversations(
            conversations=[{"source_platform": "custom", "call_id": "c"}]
        )

        assert _sent_body(httpx_mock)["project_id"] == OTHER_ID


class TestUploadScenarioSet:
    """`upload_scenario_set` is Project-scoped like every other write, and its
    Project travels in the multipart body."""

    def test_upload_uses_the_client_project(
        self, httpx_mock: HTTPXMock, tmp_path: Path
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project=OTHER_ID)
        sent = _mock_upload(httpx_mock)

        client.upload_scenario_set(
            scenario_name="CI upload", file_path=_scenario_file(tmp_path)
        )

        assert _multipart_project_id(sent["content"]) == OTHER_ID

    def test_per_call_project_wins_over_client_project(
        self, httpx_mock: HTTPXMock, tmp_path: Path
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project=OTHER_ID)
        sent = _mock_upload(httpx_mock)

        client.upload_scenario_set(
            scenario_name="CI upload",
            file_path=_scenario_file(tmp_path),
            project_id=GLOBAL_ID,
        )

        assert _multipart_project_id(sent["content"]) == GLOBAL_ID

    def test_no_project_anywhere_sends_no_project_id(
        self, httpx_mock: HTTPXMock, tmp_path: Path
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")
        sent = _mock_upload(httpx_mock)

        client.upload_scenario_set(
            scenario_name="CI upload", file_path=_scenario_file(tmp_path)
        )

        assert _multipart_project_id(sent["content"]) is None


class TestFillOnCopy:
    def test_find_datapoints_body_gains_client_project(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project=GLOBAL_ID)
        httpx_mock.add_response(json=[], status_code=200)

        search = DatapointSearch(context_token="tok")
        client.find_datapoints(search)

        sent = json.loads(httpx_mock.get_requests()[-1].content)
        assert sent["project_id"] == GLOBAL_ID
        # the caller's object is never mutated
        assert isinstance(search.project_id, type(UNSET))

    def test_find_datapoints_filter_body_gains_uuid_project(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project=GLOBAL_ID)
        httpx_mock.add_response(json=[], status_code=200)

        client.find_datapoints_filter(DatapointFilterSearchPayload(filters=[]))

        sent = json.loads(httpx_mock.get_requests()[-1].content)
        assert sent["project_id"] == GLOBAL_ID

    def test_explicitly_set_field_wins(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com", project=GLOBAL_ID)
        httpx_mock.add_response(json=[], status_code=200)

        client.find_datapoints(
            DatapointSearch(context_token="tok", project_id=OTHER_ID)
        )

        sent = json.loads(httpx_mock.get_requests()[-1].content)
        assert sent["project_id"] == OTHER_ID

    def test_no_client_project_leaves_field_unset(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")
        httpx_mock.add_response(json=[], status_code=200)

        client.find_datapoints(DatapointSearch(context_token="tok"))

        sent = json.loads(httpx_mock.get_requests()[-1].content)
        assert "project_id" not in sent


class TestProjectLifecycle:
    def test_get_project_fetches_one_by_id(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")
        httpx_mock.add_response(
            json={
                "id": OTHER_ID,
                "name": "Billing Agent",
                "onboarding_status": "s",
                "tags": [],
            },
            # the GET routes answer 201 — the parser the SDK relies on
            status_code=201,
        )

        project = client.get_project(OTHER_ID)

        request = httpx_mock.get_requests()[-1]
        assert request.method == "GET"
        assert request.url.path == f"/v0/projects/{OTHER_ID}"
        assert str(project.id) == OTHER_ID
        assert project.name == "Billing Agent"

    def test_archive_project_parses_200(self, httpx_mock: HTTPXMock) -> None:
        # The hand-written PATCH module parses 200 (not the PUT/GET routes'
        # SDK-load-bearing 201) — with raise_on_unexpected_status=True a wrong
        # parser would raise on every success.
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")
        httpx_mock.add_response(
            json={
                "id": OTHER_ID,
                "name": "Billing Agent",
                "onboarding_status": "s",
                "tags": [],
                "is_archived": True,
            },
            status_code=200,
        )

        response = client.archive_project(OTHER_ID)

        request = httpx_mock.get_requests()[-1]
        assert request.method == "PATCH"
        assert json.loads(request.content) == {"is_archived": True}
        assert response.additional_properties["is_archived"] is True

    def test_unarchive_project_sends_false(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")
        httpx_mock.add_response(
            json={
                "id": OTHER_ID,
                "name": "Billing Agent",
                "onboarding_status": "s",
                "tags": [],
                "is_archived": False,
            },
            status_code=200,
        )

        client.unarchive_project(OTHER_ID)

        assert json.loads(httpx_mock.get_requests()[-1].content) == {
            "is_archived": False
        }

    def test_update_project_sends_only_given_fields(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")
        httpx_mock.add_response(
            json={
                "id": OTHER_ID,
                "name": "Renamed",
                "onboarding_status": "s",
                "tags": [],
            },
            status_code=200,
        )

        client.update_project(OTHER_ID, name="Renamed")

        assert json.loads(httpx_mock.get_requests()[-1].content) == {"name": "Renamed"}


class TestProjectNameValidation:
    """The server refuses a Project name with leading or trailing whitespace —
    two Projects that look identical in the picker are distinct rows. The SDK
    refuses it locally so the caller does not pay a round trip to find out."""

    def test_create_project_refuses_surrounding_whitespace(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")

        with pytest.raises(ValueError, match="whitespace"):
            client.create_project(name=" Billing Agent ")

        # nothing left the machine — only the construction-time projects fetch
        assert len(httpx_mock.get_requests()) == 1

    def test_update_project_refuses_surrounding_whitespace(
        self, httpx_mock: HTTPXMock
    ) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")

        with pytest.raises(ValueError, match="whitespace"):
            client.update_project(OTHER_ID, name="Billing Agent\n")

        assert len(httpx_mock.get_requests()) == 1

    def test_a_clean_name_is_sent_unchanged(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")
        httpx_mock.add_response(
            json={
                "id": OTHER_ID,
                "name": "Billing Agent",
                "onboarding_status": "s",
                "tags": [],
            },
            status_code=201,
        )

        client.create_project(name="Billing Agent")

        assert _sent_body(httpx_mock)["name"] == "Billing Agent"

    def test_update_without_a_name_is_unaffected(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")
        httpx_mock.add_response(
            json={
                "id": OTHER_ID,
                "name": "Billing Agent",
                "onboarding_status": "s",
                "tags": ["ops"],
            },
            status_code=200,
        )

        client.update_project(OTHER_ID, tags=["ops"])

        assert _sent_body(httpx_mock) == {"tags": ["ops"]}


class TestIngestConversationsGuard:
    def test_requires_a_project_somewhere(self, httpx_mock: HTTPXMock) -> None:
        _mock_projects(httpx_mock)
        client = Okareo("k", "http://mocked.com")
        with pytest.raises(ValueError, match="requires a project_id"):
            client.ingest_conversations(
                conversations=[{"source_platform": "custom", "call_id": "c"}]
            )
