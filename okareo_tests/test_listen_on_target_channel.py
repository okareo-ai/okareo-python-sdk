"""Listen-only mode: a custom multi-turn Target answered on its own channel with
no Run submitted.

Until now the listener was opened by submitting a Run and subscribed to a
channel made for that Run (``invoke.<target id>_<uuid>``), so a process that
wanted to answer Okareo before any Run existed had nowhere to wait.
``ModelUnderTest.listen_on_target_channel`` asks for the Target's own channel
(the server falls back to the Target's id when no per-Run id is given),
subscribes to it, and stays up, with no Run to watch, until it is stopped.
A fake NATS connection and a fake credentials endpoint; nothing touches the
network.
"""

from typing import Any, Iterator

import pytest
from okareo_tests.test_submit_test_custom_multiturn_listener import (
    EchoAsync,
    FakeNats,
    make_mut,
)

from okareo import model_under_test as mut_module
from okareo.error import TestRunError
from okareo.model_under_test import ModelUnderTest
from okareo.target_listener import TargetListener

LISTENERS: list[TargetListener] = []


@pytest.fixture(autouse=True)
def stop_listeners() -> Iterator[None]:
    yield
    for listener in LISTENERS:
        listener.stop()
    LISTENERS.clear()


@pytest.fixture
def asked(monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    """The credentials endpoint, recording what it was asked."""
    calls: list[dict] = []

    def creds(**kwargs: Any) -> dict:
        calls.append(kwargs)
        return {"jwt": "jwt", "seed": "seed", "local_nats": ""}

    monkeypatch.setattr(
        mut_module.internal_custom_model_listener_v0_internal_custom_model_listener_get,
        "sync",
        creds,
    )
    return calls


@pytest.fixture
def fake_nats(monkeypatch: pytest.MonkeyPatch) -> FakeNats:
    fake = FakeNats()

    async def connect(
        self: ModelUnderTest, jwt: str, seed: str, local: str
    ) -> FakeNats:
        import asyncio

        fake.loop = asyncio.get_running_loop()
        return fake

    monkeypatch.setattr(ModelUnderTest, "connect_nats", connect)
    return fake


def listen(mut: ModelUnderTest) -> TargetListener:
    listener = mut.listen_on_target_channel()
    LISTENERS.append(listener)
    return listener


def test_it_asks_for_the_targets_own_channel_and_subscribes_to_it(
    asked: list[dict], fake_nats: FakeNats
) -> None:
    mut = make_mut(EchoAsync(name="echo"))
    listener = listen(mut)
    assert asked == [
        {"client": mut.client, "api_key": "unit-test-key", "mut_id": str(mut.mut_id)}
    ], "no per-Run id: the server falls back to the Target's own channel"
    assert listener.channel == f"invoke.{mut.mut_id}"
    assert list(fake_nats.subs) == [listener.channel]


def test_it_answers_what_okareo_sends_with_no_run_submitted(
    asked: list[dict], fake_nats: FakeNats, monkeypatch: pytest.MonkeyPatch
) -> None:
    def no_run(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("listen-only mode submits no Run and watches none")

    monkeypatch.setattr(mut_module.submit_test_v0_test_run_submit_post, "sync", no_run)
    monkeypatch.setattr(ModelUnderTest, "_fetch_test_run_async", no_run)
    mut = make_mut(EchoAsync(name="echo"))
    listen(mut)
    fake_nats.deliver(
        {
            "message_history": [{"role": "user", "content": "hello"}],
            "scenario_input": {"envelope": {"run_id": "r", "role": "sign_in"}},
            "session_id": "s1",
            "call_type": "invoke",
        }
    )
    fake_nats.wait_for_publish(1)
    assert fake_nats.published[0][1]["actual"] == "olleh"


def test_it_stays_up_until_it_is_stopped(
    asked: list[dict], fake_nats: FakeNats
) -> None:
    mut = make_mut(EchoAsync(name="echo"))
    listener = listen(mut)
    assert listener.wait(timeout=0.5) is False, "nothing ends it but a stop"
    assert listener.is_listening()
    listener.stop()
    assert listener.wait(timeout=3) is True
    assert not listener.is_listening() and fake_nats.closed
    assert listener.describe().startswith("connected: no")


def test_a_listener_that_cannot_connect_raises_naming_why(
    asked: list[dict], monkeypatch: pytest.MonkeyPatch
) -> None:
    async def refused(self: ModelUnderTest, jwt: str, seed: str, local: str) -> Any:
        raise RuntimeError("connect refused")

    monkeypatch.setattr(ModelUnderTest, "connect_nats", refused)
    mut = make_mut(EchoAsync(name="echo"))
    with pytest.raises(TestRunError, match="connect refused"):
        listen(mut)
