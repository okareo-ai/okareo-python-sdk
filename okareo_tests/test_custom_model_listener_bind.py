"""A custom Target's bind_listener: the listener hands it the Run's NATS connection.

A Target whose class defines ``bind_listener(nc, invoke_id)`` is called once,
after the listener has subscribed to invoke.<id> and flushed and before the Run
is created; what it returns (its release) runs before the connection closes,
on failure paths too. A Target without it sees no change. A bind that fails
stops the Run from starting with a clear error rather than a hang.

Every test goes through ``run_test`` or ``submit_test``. The NATS connection is
a stand-in returned by a fake ``nats.connect`` that records the order of
events, and the Okareo endpoints are fakes; nothing touches the network.
"""

import asyncio
import time
import traceback
from typing import Any, Callable, Iterator, List, Optional
from uuid import uuid4

import nats.errors
import pytest

from okareo import listener_binding
from okareo import model_under_test as mut_module
from okareo.error import ListenerBindError, TestRunError
from okareo.model_under_test import (
    CustomMultiturnTarget,
    CustomMultiturnTargetAsync,
    ModelInvocation,
    ModelUnderTest,
    stop_listener_for_run,
)
from okareo_api_client.client import Client
from okareo_api_client.models import ModelUnderTestResponse, TestRunItem, TestRunType


class Recording:
    """The order things happened in, across the stand-in connection, the Target and the Run."""

    def __init__(self) -> None:
        self.events: List[str] = []

    def index(self, event: str) -> int:
        return self.events.index(event)

    def invoke_id(self) -> str:
        """The Run's id on NATS, read off the listener's own subscription."""
        return self.events[0].removeprefix("subscribe invoke.")


class FakeConn:
    """The slice of nats-py's Client the listener and a Target use."""

    def __init__(self, log: Recording, fail_flush: Optional[int] = None) -> None:
        self.log = log
        self.fail_flush = fail_flush
        self.flushes = 0

    async def subscribe(self, subject: str, cb: Any = None) -> None:
        self.log.events.append(f"subscribe {subject}")

    async def flush(self, timeout: int = 10) -> None:
        self.flushes += 1
        self.log.events.append("flush")
        if self.flushes == self.fail_flush:
            raise nats.errors.FlushTimeoutError()

    async def publish(self, subject: str, data: bytes) -> None:
        self.log.events.append(f"publish {subject}")

    async def close(self) -> None:
        self.log.events.append("close")


class Echo(CustomMultiturnTargetAsync):
    async def invoke(  # type: ignore[override]
        self,
        messages: list[dict[str, str]],
        scenario_input: Any = None,
        session_id: Optional[str] = None,
    ) -> ModelInvocation:
        return ModelInvocation("echo", messages, {})


class Binding(Echo):
    """A Target that subscribes a subject of its own on the Run's connection and
    keeps a task running on it, which its release cancels."""

    def __init__(self, name: str, log: Recording, **behaviour: Any) -> None:
        super().__init__(name=name)
        self.log = log
        self.behaviour = behaviour
        self.bound_to: List[tuple] = []
        self.pump: Optional[asyncio.Future] = None

    async def bind_listener(self, nc: Any, invoke_id: str) -> Any:
        self.bound_to.append((nc, invoke_id))
        self.log.events.append("bind")
        if self.behaviour.get("raise_at_bind"):
            raise RuntimeError("bind boom")
        if "hang_for" in self.behaviour:
            await asyncio.sleep(self.behaviour["hang_for"])
        if self.behaviour.get("cancel_at_bind"):
            helper = asyncio.ensure_future(asyncio.sleep(3600))
            helper.cancel()
            await helper  # the usual cleanup idiom: this coroutine ends cancelled
        if "returns" in self.behaviour:
            return self.behaviour["returns"]
        await nc.subscribe(f"own.{invoke_id}.>", cb=None)
        pump = asyncio.ensure_future(asyncio.sleep(3600))
        self.pump = pump

        async def release() -> None:
            self.log.events.append("release")
            pump.cancel()
            if self.behaviour.get("cancel_at_release"):
                await pump  # ends this coroutine cancelled
            if self.behaviour.get("raise_at_release"):
                raise RuntimeError("release boom")
            if "release_takes" in self.behaviour:
                await asyncio.sleep(self.behaviour["release_takes"])
                self.log.events.append("release done")

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


class AnswersAnyName:
    """A client proxy: any name it lacks is a remote call, answered with a string."""

    def __getattr__(self, name: str) -> Callable[..., str]:
        return lambda *_a, **_k: f"remote result of {name}"

    async def invoke(self, messages: Any, *_a: Any, **_k: Any) -> ModelInvocation:
        return ModelInvocation("echo", messages, {})


class Forwarding(Echo):
    """An SDK Target that forwards any name it lacks to a client of its own."""

    def __init__(self, name: str, client: Any) -> None:
        super().__init__(name=name)
        self.client = client

    def __getattr__(self, name: str) -> Any:
        if name == "client":
            raise AttributeError(name)
        return getattr(self.client, name)


def models_of(target: Any) -> dict:
    return {target.type: target.params()}


class FakeOkareo:
    """The fakes around the model: NATS, the listener's credentials, the Run endpoints."""

    def __init__(self, monkeypatch: pytest.MonkeyPatch, log: Recording) -> None:
        self.log = log
        self.conn = FakeConn(log)
        self.run_id = uuid4()

        async def fake_nats_connect(**_kwargs: Any) -> FakeConn:
            return self.conn

        monkeypatch.setattr(mut_module.nats, "connect", fake_nats_connect)
        monkeypatch.setattr(
            mut_module.internal_custom_model_listener_v0_internal_custom_model_listener_get,
            "sync",
            lambda **_k: {
                "jwt": "jwt",
                "seed": "seed",
                "local_nats": "nats://unit.invalid:4222",
            },
        )
        monkeypatch.setattr(mut_module.run_test_v0_test_run_post, "sync", self._run)
        monkeypatch.setattr(
            mut_module.submit_test_v0_test_run_submit_post, "sync", self._submit
        )

    def model(self, models: dict) -> ModelUnderTest:
        return ModelUnderTest(
            client=Client(
                base_url="http://unit.invalid", raise_on_unexpected_status=True
            ),
            api_key="unit-test-key",
            mut=ModelUnderTestResponse(
                id=uuid4(),
                project_id=uuid4(),
                name="bound",
                tags=[],
                time_created="2026-10-27T00:00:00",
            ),
            models=models,
        )

    def _run(self, **_k: Any) -> TestRunItem:
        self.log.events.append("run created")
        return TestRunItem(id=self.run_id, project_id=uuid4(), status="FINISHED")

    def _submit(self, **_k: Any) -> TestRunItem:
        self.log.events.append("run submitted")
        return TestRunItem(id=self.run_id, project_id=uuid4(), status="RUNNING")


@pytest.fixture
def log() -> Recording:
    return Recording()


@pytest.fixture
def fakes(monkeypatch: pytest.MonkeyPatch, log: Recording) -> Iterator[FakeOkareo]:
    fake = FakeOkareo(monkeypatch, log)
    yield fake
    # a submit_test whose test failed midway leaves its listener up
    stop_listener_for_run(fake.run_id)


def run_test(mut: ModelUnderTest) -> TestRunItem:
    return mut.run_test(
        scenario=str(uuid4()), name="bind unit", test_run_type=TestRunType.MULTI_TURN
    )


def refused(mut: ModelUnderTest) -> TestRunError:
    with pytest.raises(TestRunError) as raised:
        run_test(mut)
    return raised.value


# --- the hook is called once, after the flush, before the Run ------------------


def test_the_hook_is_handed_the_connection_after_the_flush_and_before_the_run(
    fakes: FakeOkareo, log: Recording, capsys: pytest.CaptureFixture[str]
) -> None:
    target = Binding("bound", log)

    run_test(fakes.model(models_of(target)))

    invoke_id = log.invoke_id()
    assert log.events == [
        f"subscribe invoke.{invoke_id}",
        "flush",
        "bind",
        f"subscribe own.{invoke_id}.>",
        "flush",  # what the Target subscribed is registered before the Run starts
        "run created",
        "release",
        "close",
    ]
    assert target.bound_to == [(fakes.conn, invoke_id)]
    assert target.pump is not None and target.pump.cancelled()
    assert "the Target is using the Run's NATS connection" in capsys.readouterr().out


def test_a_sync_hook_and_a_sync_release_work_too(
    fakes: FakeOkareo, log: Recording
) -> None:
    run_test(fakes.model(models_of(SyncBinding("sync", log))))

    assert log.events[1:] == [
        "flush",
        "bind",
        "flush",
        "run created",
        "release",
        "close",
    ]


# --- the release runs before the close, on failure paths too -----------------


def test_a_flush_that_fails_after_the_bind_still_releases_before_the_close(
    fakes: FakeOkareo, log: Recording
) -> None:
    fakes.conn.fail_flush = 2  # the flush of what the Target subscribed
    target = Binding("bound", log)

    error = refused(fakes.model(models_of(target)))

    assert "FlushTimeoutError" in str(error)
    assert "run created" not in log.events
    assert log.events[-3:] == ["flush", "release", "close"]
    assert target.pump is not None and target.pump.cancelled()


def test_a_release_that_raises_is_logged_and_the_connection_still_closes(
    fakes: FakeOkareo, log: Recording, capsys: pytest.CaptureFixture[str]
) -> None:
    run_test(fakes.model(models_of(Binding("bound", log, raise_at_release=True))))

    assert log.events[-2:] == ["release", "close"]
    out = capsys.readouterr().out
    assert "bind_listener release failed (RuntimeError: release boom)" in out


def test_a_release_that_ends_cancelled_is_logged_and_the_connection_still_closes(
    fakes: FakeOkareo, log: Recording, capsys: pytest.CaptureFixture[str]
) -> None:
    mut = fakes.model(models_of(Binding("bound", log, cancel_at_release=True)))

    run_test(mut)

    assert log.events[-2:] == ["release", "close"]
    assert not mut.custom_model_thread.is_alive()
    assert "bind_listener release ended cancelled" in capsys.readouterr().out


def test_a_release_that_hangs_is_cut_off_and_the_connection_still_closes(
    fakes: FakeOkareo,
    log: Recording,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(listener_binding, "LISTENER_RELEASE_TIMEOUT_SECONDS", 0.1)

    async def never() -> None:
        log.events.append("release")
        await asyncio.sleep(5)

    run_test(fakes.model(models_of(Binding("bound", log, returns=never))))

    assert log.events[-2:] == ["release", "close"]
    assert "release did not finish within" in capsys.readouterr().out


def test_stop_listener_for_run_waits_for_a_release_longer_than_five_seconds(
    fakes: FakeOkareo, log: Recording
) -> None:
    mut = fakes.model(models_of(Binding("bound", log, release_takes=5.5)))
    submitted = mut.submit_test(
        scenario=str(uuid4()), name="bind unit", test_run_type=TestRunType.MULTI_TURN
    )

    started = time.monotonic()
    assert stop_listener_for_run(submitted.id)
    took = time.monotonic() - started
    log.events.append("stop returned")

    assert took >= 5.5
    assert log.events[-4:] == ["release", "release done", "close", "stop returned"]
    assert not mut.custom_model_thread.is_alive()


# --- no hook: no change ------------------------------------------------------


NO_HOOK = ["subscribe", "flush", "run", "close"]


def first_words(log: Recording) -> List[str]:
    return [event.split(" ")[0] for event in log.events]


def test_a_target_without_the_hook_sees_no_change(
    fakes: FakeOkareo, log: Recording
) -> None:
    run_test(fakes.model(models_of(Echo(name="plain"))))

    assert first_words(log) == NO_HOOK


def test_a_target_given_as_plain_functions_sees_no_change(
    fakes: FakeOkareo, log: Recording
) -> None:
    async def invoke(*_a: Any) -> ModelInvocation:
        return ModelInvocation("echo", [], {})

    run_test(
        fakes.model(
            {
                "custom_target_async": {
                    "type": "custom_target_async",
                    "model_invoker": invoke,
                }
            }
        )
    )

    assert first_words(log) == NO_HOOK


def test_a_proxy_whose_invoke_is_registered_is_not_bound(
    fakes: FakeOkareo, log: Recording
) -> None:
    proxy = AnswersAnyName()

    run_test(
        fakes.model(
            {
                "custom_target_async": {
                    "type": "custom_target_async",
                    "model_invoker": proxy.invoke,
                }
            }
        )
    )

    assert first_words(log) == NO_HOOK


def test_a_target_forwarding_names_to_a_client_is_not_bound(
    fakes: FakeOkareo, log: Recording
) -> None:
    target = Forwarding("forwarding", client=AnswersAnyName())

    run_test(fakes.model(models_of(target)))

    assert first_words(log) == NO_HOOK


def test_a_hook_that_binds_nothing_has_nothing_to_release(
    fakes: FakeOkareo, log: Recording, capsys: pytest.CaptureFixture[str]
) -> None:
    run_test(fakes.model(models_of(Binding("bound", log, returns=None))))

    assert log.events[1:] == ["flush", "bind", "flush", "run created", "close"]
    assert "NATS connection (bind_listener)" not in capsys.readouterr().out


# --- a hook that fails stops the Run from starting ---------------------------


def test_a_hook_that_raises_refuses_the_run(fakes: FakeOkareo, log: Recording) -> None:
    mut = fakes.model(models_of(Binding("bound", log, raise_at_bind=True)))

    error = refused(mut)

    assert "could not hand its NATS connection to the Target" in str(error)
    assert "bind_listener failed: RuntimeError: bind boom" in str(error)
    # nothing to release, and the connection closes
    assert log.events[1:] == ["flush", "bind", "close"]
    assert not mut.custom_model_thread.is_alive()


def test_a_bind_failure_reaches_the_caller_chained_to_the_targets_own_error(
    fakes: FakeOkareo, log: Recording, capsys: pytest.CaptureFixture[str]
) -> None:
    error = refused(fakes.model(models_of(Binding("bound", log, raise_at_bind=True))))

    causes = []
    cause: Optional[BaseException] = error
    while cause is not None:
        causes.append(cause)
        cause = cause.__cause__
    bind_error = next(c for c in causes if isinstance(c, ListenerBindError))
    assert isinstance(bind_error.__cause__, RuntimeError)
    printed = "".join(traceback.format_exception(error))
    assert "in bind_listener" in printed and "bind boom" in printed
    out = capsys.readouterr().out
    assert (
        "bind_listener failed: RuntimeError: bind boom; the Run is not started" in out
    )
    assert "An error occurred in the custom model invocation" not in out


def test_a_hook_that_ends_cancelled_refuses_the_run(
    fakes: FakeOkareo, log: Recording
) -> None:
    error = refused(fakes.model(models_of(Binding("bound", log, cancel_at_bind=True))))

    assert "bind_listener ended cancelled" in str(error)
    assert "run created" not in log.events
    assert log.events[-1] == "close"


def test_a_hook_that_returns_something_else_refuses_the_run(
    fakes: FakeOkareo, log: Recording
) -> None:
    error = refused(fakes.model(models_of(Binding("bound", log, returns="no release"))))

    assert "returned a str" in str(error)
    assert "run created" not in log.events
    assert log.events[-1] == "close"


def test_a_hook_that_hangs_refuses_the_run(
    fakes: FakeOkareo, log: Recording, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(listener_binding, "LISTENER_BIND_TIMEOUT_SECONDS", 0.1)

    error = refused(fakes.model(models_of(Binding("bound", log, hang_for=5))))

    assert "bind_listener did not return within" in str(error)
    assert "run created" not in log.events
    assert log.events[-1] == "close"


def test_the_readiness_wait_names_the_bind_when_the_bind_used_it_up(
    fakes: FakeOkareo, log: Recording, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OKAREO_CUSTOM_MODEL_READY_TIMEOUT", "0.3")

    error = refused(fakes.model(models_of(Binding("bound", log, hang_for=1))))

    assert "The Target's bind_listener did not return within" in str(error)
    assert "Check connectivity to NATS" not in str(error)
    assert "run created" not in log.events
    assert log.events[-1] == "close"
