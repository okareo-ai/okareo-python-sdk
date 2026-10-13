"""The SDK reads a vision Target; it does not create one yet.

A vision Target's row is a browser definition. Every reader learns the kind
one deploy before anything may write it, since production is blue/green on a
shared database. The spec the generated client is made from lists "vision"
among the kinds a stored Target's models may hold, and keeps it out of the
kinds a client may register. A Target of the kind reads through ``get_model``
and ``get_target_by_name`` like any other. The HTTP layer is mocked; nothing
touches the network.
"""

import json
from pathlib import Path
from typing import Any

import pytest
from pytest_httpx import HTTPXMock

from okareo import Okareo

MOCK_UUID = "0156f5d7-4ac4-4568-9d44-24750aa08d1a"
SPEC = Path(__file__).resolve().parent.parent / "openapi.json"
VISION_ROW = {
    "type": "vision",
    "url": "https://shop.example/help",
    "screen_selector": "#chat",
    "browser_config": {"channel": "chrome", "headless": True, "max_parallel": 3},
    "settle_timeout_s": 150.0,
    "secrets": ["SHOP_USER"],
}


def _model_kinds(schema_name: str) -> list[str]:
    schemas = json.loads(SPEC.read_text())["components"]["schemas"]
    models = schemas[schema_name]["properties"]["models"]
    mapping = next(s for s in models["anyOf"] if s.get("type") == "object")
    return list(mapping["propertyNames"]["enum"])


def test_the_spec_reads_the_vision_kind() -> None:
    assert "vision" in _model_kinds("ModelUnderTestResponse")


def test_the_spec_does_not_let_a_client_register_it() -> None:
    assert "vision" not in _model_kinds("ModelUnderTestSchema")


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


def _stored_target() -> dict[str, Any]:
    return {
        "id": MOCK_UUID,
        "project_id": MOCK_UUID,
        "name": "Shop help (UI)",
        "version": 1,
        "models": {"vision": VISION_ROW},
        "tags": [],
        "time_created": "2026-10-13T00:00:00",
    }


def test_get_model_reads_a_vision_target(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(json=_stored_target(), status_code=201)

    mut = okareo_client.get_model("Shop help (UI)")

    assert mut.models == {"vision": VISION_ROW}


def test_get_target_by_name_reads_a_vision_target(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(
        json={"id": MOCK_UUID, "name": "Shop help (UI)", "target": VISION_ROW},
        status_code=200,
    )

    target = okareo_client.get_target_by_name("Shop help (UI)")

    assert target.name == "Shop help (UI)"
    assert target.target == VISION_ROW
    assert target.id == MOCK_UUID
