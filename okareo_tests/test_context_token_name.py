"""The conversation's id is called a context token; the older session ID names still work.

A custom Target's own id for a conversation (often called a session ID or a
conversation ID) is named "context token". These tests hold both names to the
same behaviour: the endpoint configs accept either keyword and send the same
wire key, and a custom Target is handed the id whichever name its methods use.
Nothing here touches the network.
"""

import asyncio
from typing import Any, Iterator, Optional
from uuid import uuid4

import pytest

from okareo.model_under_test import (
    CustomMultiturnTarget,
    CustomMultiturnTargetAsync,
    EndSessionConfig,
    ModelInvocation,
    ModelUnderTest,
    SessionConfig,
    TurnConfig,
)
from okareo_api_client.client import Client
from okareo_api_client.models import ModelUnderTestResponse

CONTEXT_TOKEN = "conversation-42"
SCENARIO_INPUT = {"goal": "book a table"}
MESSAGES = [{"role": "user", "content": "hello"}]

# What each Target method was handed, keyed by method name. The Targets are attrs
# classes, so a test cannot hang a recorder on the instance.
SEEN: dict[str, Optional[str]] = {}


@pytest.fixture(autouse=True)
def clear_seen() -> Iterator[None]:
    SEEN.clear()
    yield
    SEEN.clear()


def make_mut(
    target: CustomMultiturnTarget | CustomMultiturnTargetAsync,
) -> ModelUnderTest:
    return ModelUnderTest(
        client=Client(base_url="http://unit.invalid", raise_on_unexpected_status=True),
        api_key="unit-test-key",
        mut=ModelUnderTestResponse(
            id=uuid4(),
            project_id=uuid4(),
            name=target.name,
            tags=[],
            time_created="2026-11-19T00:00:00",
        ),
        models={target.type: target.params()},
    )


class SessionIdNamedTarget(CustomMultiturnTarget):
    """A Target written against the older parameter name."""

    def invoke(  # type: ignore[override]
        self,
        messages: list[dict[str, str]],
        scenario_input: Any = None,
        session_id: Optional[str] = None,
    ) -> ModelInvocation:
        SEEN["invoke"] = session_id
        return ModelInvocation("ok", messages, {})

    def end_session(self, session_id: str) -> None:
        SEEN["end_session"] = session_id


class SessionIdNamedTargetAsync(CustomMultiturnTargetAsync):
    """An async Target written against the older parameter name."""

    async def invoke(  # type: ignore[override]
        self,
        messages: list[dict[str, str]],
        scenario_input: Any = None,
        session_id: Optional[str] = None,
    ) -> ModelInvocation:
        SEEN["invoke"] = session_id
        return ModelInvocation("ok", messages, {})

    async def end_session(self, session_id: str) -> None:
        SEEN["end_session"] = session_id


def test_a_target_naming_session_id_is_handed_the_id() -> None:
    target = SessionIdNamedTarget(name="old-name")
    mut = make_mut(target)

    mut.call_custom_invoker([], MESSAGES, SCENARIO_INPUT, CONTEXT_TOKEN, "invoke")
    mut.call_custom_invoker([], None, None, CONTEXT_TOKEN, "end_session")

    assert SEEN == {"invoke": CONTEXT_TOKEN, "end_session": CONTEXT_TOKEN}


def test_an_async_target_naming_session_id_is_handed_the_id() -> None:
    target = SessionIdNamedTargetAsync(name="old-name-async")
    mut = make_mut(target)

    asyncio.run(
        mut.call_custom_invoker_async(
            [], MESSAGES, SCENARIO_INPUT, CONTEXT_TOKEN, "invoke"
        )
    )
    asyncio.run(
        mut.call_custom_invoker_async([], None, None, CONTEXT_TOKEN, "end_session")
    )

    assert SEEN == {"invoke": CONTEXT_TOKEN, "end_session": CONTEXT_TOKEN}


class ContextTokenNamedTarget(CustomMultiturnTarget):
    """A Target written against the new parameter name."""

    def invoke(  # type: ignore[override]
        self,
        messages: list[dict[str, str]],
        scenario_input: Any = None,
        context_token: Optional[str] = None,
    ) -> ModelInvocation:
        SEEN["invoke"] = context_token
        return ModelInvocation("ok", messages, {})

    def end_session(self, context_token: str) -> None:
        SEEN["end_session"] = context_token


class ContextTokenNamedTargetAsync(CustomMultiturnTargetAsync):
    """An async Target written against the new parameter name."""

    async def invoke(  # type: ignore[override]
        self,
        messages: list[dict[str, str]],
        scenario_input: Any = None,
        context_token: Optional[str] = None,
    ) -> ModelInvocation:
        SEEN["invoke"] = context_token
        return ModelInvocation("ok", messages, {})

    async def end_session(self, context_token: str) -> None:
        SEEN["end_session"] = context_token


def test_a_target_naming_context_token_is_handed_the_id() -> None:
    target = ContextTokenNamedTarget(name="new-name")
    mut = make_mut(target)

    mut.call_custom_invoker([], MESSAGES, SCENARIO_INPUT, CONTEXT_TOKEN, "invoke")
    mut.call_custom_invoker([], None, None, CONTEXT_TOKEN, "end_session")

    assert SEEN == {"invoke": CONTEXT_TOKEN, "end_session": CONTEXT_TOKEN}


def test_an_async_target_naming_context_token_is_handed_the_id() -> None:
    target = ContextTokenNamedTargetAsync(name="new-name-async")
    mut = make_mut(target)

    asyncio.run(
        mut.call_custom_invoker_async(
            [], MESSAGES, SCENARIO_INPUT, CONTEXT_TOKEN, "invoke"
        )
    )
    asyncio.run(
        mut.call_custom_invoker_async([], None, None, CONTEXT_TOKEN, "end_session")
    )

    assert SEEN == {"invoke": CONTEXT_TOKEN, "end_session": CONTEXT_TOKEN}


# The three endpoint configs read the id out of a response with a JSONPath.
ENDPOINT_CONFIGS = [SessionConfig, TurnConfig, EndSessionConfig]


@pytest.mark.parametrize("config_class", [SessionConfig, TurnConfig])
def test_the_context_token_path_is_sent_under_the_session_id_path_key(
    config_class: type,
) -> None:
    by_new_name = config_class(
        "https://api.example.com", response_context_token_path="response.id"
    )
    by_old_name = config_class(
        "https://api.example.com", response_session_id_path="response.id"
    )

    assert by_new_name.to_dict()["response_session_id_path"] == "response.id"
    assert "response_context_token_path" not in by_new_name.to_dict()
    assert by_new_name.to_dict() == by_old_name.to_dict()


def test_end_session_config_sends_no_path_under_either_name() -> None:
    by_new_name = EndSessionConfig(
        "https://api.example.com", response_context_token_path="response.id"
    )

    assert (
        by_new_name.to_dict() == EndSessionConfig("https://api.example.com").to_dict()
    )


@pytest.mark.parametrize("config_class", ENDPOINT_CONFIGS)
def test_both_attribute_names_read_the_same_path(config_class: type) -> None:
    by_new_name = config_class(
        "https://api.example.com", response_context_token_path="response.id"
    )
    by_old_name = config_class(
        "https://api.example.com", response_session_id_path="response.id"
    )

    for config in (by_new_name, by_old_name):
        assert config.response_context_token_path == "response.id"
        assert config.response_session_id_path == "response.id"


@pytest.mark.parametrize("config_class", ENDPOINT_CONFIGS)
def test_both_keywords_with_different_paths_are_refused(config_class: type) -> None:
    with pytest.raises(ValueError) as refused:
        config_class(
            "https://api.example.com",
            response_context_token_path="response.id",
            response_session_id_path="response.thread_id",
        )

    message = str(refused.value)
    assert "\n" not in message
    assert "response_context_token_path" in message
    assert "response_session_id_path" in message


@pytest.mark.parametrize("config_class", ENDPOINT_CONFIGS)
def test_both_keywords_with_the_same_path_are_accepted(config_class: type) -> None:
    config = config_class(
        "https://api.example.com",
        response_context_token_path="response.id",
        response_session_id_path="response.id",
    )

    assert config.response_context_token_path == "response.id"
