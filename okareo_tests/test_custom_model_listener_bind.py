"""A custom Target's bind_listener: the listener hands it the Run's NATS connection.

A Target that defines ``bind_listener(nc, invoke_id)`` is called once, after the
listener has subscribed to invoke.<id> and flushed and before it signals ready;
what it returns (its release) runs before the connection closes, on failure
paths too. A Target without it sees no change. A bind that fails stops the
listener's start with a clear error rather than a hang.

The NATS connection is a stand-in that records the order of events; nothing
touches the network.
"""

import asyncio
import threading
from types import SimpleNamespace
from typing import Any, Callable, Dict, List, Optional
from uuid import uuid4

import pytest

from okareo import model_under_test as mut_module
from okareo.error import TestRunError
from okareo.model_under_test import (
    CustomMultiturnTarget,
    CustomMultiturnTargetAsync,
    ListenerBindError,
    ModelInvocation,
    ModelUnderTest,
)
from okareo_api_client.client import Client
from okareo_api_client.models import ModelUnderTestResponse, TestRunType


class Recording:
    """The order things happened in, across the stand-in connection, the hook and ready."""

    def __init__(self) -> None:
        self.events: List[str] = []

    def index(self, event: str) -> int:
        return self.events.index(event)


class FakeConn:
    def __init__(self, log: Recording) -> None:
        self.log = log
        self.subs: Dict[str, Any] = {}

    async def subscribe(self, subject: str, cb: Any = None) -> None:
        self.subs[subject] = cb
        self.log.events.append(f"subscribe {subject}")

    async def flush(self, timeout: int = 10) -> None:
        self.log.events.append("flush")

    async def publish(self, subject: str, data: bytes) -> None:
        self.log.events.append(f"publish {subject}")

    async def close(self) -> None:
        self.log.events.append("close")


class ReadyEvent(threading.Event):
    def __init__(self, log: Recording) -> None:
        super().__init__()
        self.log = log

    def set(self) -> None:
        if not self.is_set():
            self.log.events.append("ready")
        super().set()


class Echo(CustomMultiturnTargetAsync):
    async def invoke(  # type: ignore[override]
        self,
        messages: list[dict[str, str]],
        scenario_input: Any = None,
        session_id: Optional[str] = None,
    ) -> ModelInvocation:
        return ModelInvocation("echo", messages, {})


class Binding(Echo):
    """A Target that subscribes a subject of its own on the Run's connection."""

    def __init__(self, name: str, log: Recording, **behaviour: Any) -> None:
        super().__init__(name=name)
        self.log = log
        self.behaviour = behaviour
        self.bound_to: List[tuple] = []

    async def bind_listener(self, nc: Any, invoke_id: str) -> Any:
        self.bound_to.append((nc, invoke_id))
        self.log.events.append("bind")
        if self.behaviour.get("raise_at_bind"):
            raise RuntimeError("bind boom")
        if self.behaviour.get("hang_at_bind"):
            await asyncio.sleep(5)
        if "returns" in self.behaviour:
            return self.behaviour["returns"]
        await nc.subscribe(f"own.{invoke_id}.>", cb=None)

        async def release() -> None:
            self.log.events.append("release")
            if self.behaviour.get("raise_at_release"):
                raise RuntimeError("release boom")

        return release


class SyncBinding(CustomMultiturnTarget):
    def __init__(self, name: str, log: Recording) -> None:
        super().__init__(name=name)
        self.log = log

    def invoke(  # type: ignore[override]
        self,
        messages: list[dict[str, str]],
        scenario_input: Any = None,
        session_id: Optional[str] = None,
    ) -> ModelInvocation:
        return ModelInvocation("echo", messages, {})

    def bind_listener(self, nc: Any, invoke_id: str) -> Callable[[], None]:
        self.log.events.append("bind")
        return lambda: self.log.events.append("release")


class StopRaises:
    """A stop event whose check fails: a failure after the bind."""

    def is_set(self) -> bool:
        raise RuntimeError("loop boom")

    def set(self) -> None:
        pass


def fake_self(log: Recording, models: Optional[dict]) -> Any:
    conn = FakeConn(log)

    async def connect(*_a: Any) -> FakeConn:
        return conn

    async def process_single_message(*_a: Any, **_k: Any) -> None:
        return None

    return SimpleNamespace(
        connect_nats=connect,
        process_single_message=process_single_message,
        models=models,
        conn=conn,
    )


def listen(
    log: Recording, models: Optional[dict], stop_event: Any = None
) -> Dict[str, Any]:
    """Run the listener coroutine until it is ready, then stop it; its error holder."""
    me = fake_self(log, models)
    stop = stop_event if stop_event is not None else threading.Event()
    ready = ReadyEvent(log)
    err: Dict[str, Any] = {}

    async def run() -> None:
        task = asyncio.ensure_future(
            ModelUnderTest._internal_run_custom_model_listener(
                me, stop, "jwt", "seed", "local", "inv-1", ready, err
            )
        )
        for _ in range(300):
            if ready.is_set():
                break
            await asyncio.sleep(0.01)
        if isinstance(stop, threading.Event):
            stop.set()
        await asyncio.wait_for(task, timeout=3)

    asyncio.run(run())
    return err


def models_of(target: Any) -> dict:
    return {target.type: target.params()}


# --- the hook is called once, after the flush, before ready ------------------


def test_the_hook_is_handed_the_connection_after_the_flush_and_before_ready(
    capsys: pytest.CaptureFixture[str],
) -> None:
    log = Recording()
    target = Binding("bound", log)

    err = listen(log, models_of(target))

    assert err == {}
    assert log.events == [
        "subscribe invoke.inv-1",
        "flush",
        "bind",
        "subscribe own.inv-1.>",
        "flush",  # what the Target subscribed is registered before the Run starts
        "ready",
        "release",
        "close",
    ]
    assert len(target.bound_to) == 1
    nc, invoke_id = target.bound_to[0]
    assert isinstance(nc, FakeConn) and invoke_id == "inv-1"
    assert "the Target is using the Run's NATS connection" in capsys.readouterr().out


def test_a_sync_hook_and_a_sync_release_work_too() -> None:
    log = Recording()

    err = listen(log, models_of(SyncBinding("sync", log)))

    assert err == {}
    assert log.events == [
        "subscribe invoke.inv-1",
        "flush",
        "bind",
        "flush",
        "ready",
        "release",
        "close",
    ]


# --- the release runs before the close, on failure paths too -----------------


def test_a_failure_after_the_bind_still_releases_before_the_close() -> None:
    log = Recording()

    err = listen(log, models_of(Binding("bound", log)), stop_event=StopRaises())

    assert "loop boom" in str(err.get("error"))
    assert log.index("ready") < log.index("release") < log.index("close")


def test_a_release_that_raises_is_logged_and_the_connection_still_closes(
    capsys: pytest.CaptureFixture[str],
) -> None:
    log = Recording()

    err = listen(log, models_of(Binding("bound", log, raise_at_release=True)))

    assert err == {}  # a shutdown-time failure does not fail the Run
    assert log.index("release") < log.index("close")
    out = capsys.readouterr().out
    assert "bind_listener release failed (RuntimeError: release boom)" in out


def test_a_release_that_hangs_is_cut_off_and_the_connection_still_closes(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(mut_module, "LISTENER_RELEASE_TIMEOUT_SECONDS", 0.1)
    log = Recording()

    async def never() -> None:
        log.events.append("release")
        await asyncio.sleep(5)

    err = listen(log, models_of(Binding("bound", log, returns=never)))

    assert err == {}
    assert log.index("release") < log.index("close")
    assert "release did not finish within" in capsys.readouterr().out


# --- no hook: no change ------------------------------------------------------


NO_HOOK = [
    "subscribe invoke.inv-1",
    "flush",
    "ready",
    "close",
]


def test_a_target_without_the_hook_sees_no_change() -> None:
    log = Recording()

    assert listen(log, models_of(Echo(name="plain"))) == {}
    assert log.events == NO_HOOK


def test_a_target_given_as_plain_functions_sees_no_change() -> None:
    log = Recording()

    async def invoke(*_a: Any) -> ModelInvocation:
        return ModelInvocation("echo", [], {})

    models = {
        "custom_target_async": {"type": "custom_target_async", "model_invoker": invoke}
    }
    assert listen(log, models) == {}
    assert log.events == NO_HOOK


def test_a_listener_with_no_models_sees_no_change() -> None:
    log = Recording()

    assert listen(log, None) == {}
    assert log.events == NO_HOOK


def test_a_hook_that_binds_nothing_has_nothing_to_release(
    capsys: pytest.CaptureFixture[str],
) -> None:
    log = Recording()

    assert listen(log, models_of(Binding("bound", log, returns=None))) == {}
    assert log.events == [
        "subscribe invoke.inv-1",
        "flush",
        "bind",
        "flush",
        "ready",
        "close",
    ]
    assert "NATS connection (bind_listener)" not in capsys.readouterr().out


# --- a hook that fails stops the listener's start ----------------------------


def test_a_hook_that_raises_lands_in_the_error_holder() -> None:
    log = Recording()

    err = listen(log, models_of(Binding("bound", log, raise_at_bind=True)))

    error = err.get("error")
    assert isinstance(error, ListenerBindError)
    assert "bind_listener failed: RuntimeError: bind boom" in str(error)
    # the waiter is released, there is nothing to release, the connection closes
    assert log.events == [
        "subscribe invoke.inv-1",
        "flush",
        "bind",
        "ready",
        "close",
    ]


def test_a_hook_that_returns_something_else_lands_in_the_error_holder() -> None:
    log = Recording()

    err = listen(log, models_of(Binding("bound", log, returns="not a release")))

    assert isinstance(err.get("error"), ListenerBindError)
    assert "returned a str" in str(err["error"])
    assert log.index("close") == len(log.events) - 1


def test_a_hook_that_hangs_lands_in_the_error_holder(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(mut_module, "LISTENER_BIND_TIMEOUT_SECONDS", 0.1)
    log = Recording()

    err = listen(log, models_of(Binding("bound", log, hang_at_bind=True)))

    assert isinstance(err.get("error"), ListenerBindError)
    assert "did not return within" in str(err["error"])
    assert "close" in log.events


def test_run_test_refuses_to_start_when_the_bind_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    log = Recording()
    conn = FakeConn(log)

    async def connect(self: ModelUnderTest, *_a: Any) -> FakeConn:
        return conn

    def no_run(**_k: Any) -> None:
        raise AssertionError("the Run must not be created when the bind failed")

    monkeypatch.setattr(ModelUnderTest, "connect_nats", connect)
    monkeypatch.setattr(
        mut_module.internal_custom_model_listener_v0_internal_custom_model_listener_get,
        "sync",
        lambda **_k: {"jwt": "jwt", "seed": "seed", "local_nats": ""},
    )
    monkeypatch.setattr(mut_module.run_test_v0_test_run_post, "sync", no_run)
    target = Binding("bound", log, raise_at_bind=True)
    mut = ModelUnderTest(
        client=Client(base_url="http://unit.invalid", raise_on_unexpected_status=True),
        api_key="unit-test-key",
        mut=ModelUnderTestResponse(
            id=uuid4(),
            project_id=uuid4(),
            name="bound",
            tags=[],
            time_created="2026-10-27T00:00:00",
        ),
        models=models_of(target),
    )

    with pytest.raises(TestRunError) as raised:
        mut.run_test(
            scenario=str(uuid4()),
            name="bind unit",
            test_run_type=TestRunType.MULTI_TURN,
        )

    assert "could not hand its NATS connection to the Target" in str(raised.value)
    assert "bind boom" in str(raised.value)
    assert mut.custom_model_thread is not None
    mut.custom_model_thread.join(timeout=3)
    assert not mut.custom_model_thread.is_alive()
    assert log.events[-1] == "close"
