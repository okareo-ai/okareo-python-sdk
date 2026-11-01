"""The stand-ins for test_custom_model_listener_bind: a recording NATS connection, the Targets, and the Okareo endpoints.

A fake ``nats.connect`` hands the listener ``FakeConn``, which records the
order of events and can deliver what the server would send on
``invoke.<id>``. The Okareo endpoints the listener and the Run use are faked
too, so nothing touches the network. Kept out of the test module so the tests
read as tests; pytest does not collect this file.
"""

import asyncio
import json
import threading
from typing import Any, Callable, Coroutine, List, Optional
from uuid import uuid4

import nats.errors
import pytest

from okareo import model_under_test as mut_module
from okareo.error import TestRunError
from okareo.model_under_test import (
    CustomMultiturnTarget,
    CustomMultiturnTargetAsync,
    ModelInvocation,
    ModelUnderTest,
)
from okareo_api_client.client import Client
from okareo_api_client.models import ModelUnderTestResponse, TestRunItem, TestRunType

# The events of a run with a Target that has no bind_listener, by first word.
NO_HOOK = ["subscribe", "flush", "run", "close"]
# One turn of a conversation, as the server sends it on invoke.<id>.
A_TURN = {
    "args": [],
    "message_history": [{"role": "user", "content": "hi"}],
    "scenario_input": "x",
}


class Recording:
    """The order things happened in, across the stand-in connection, the Target and the Run."""

    def __init__(self) -> None:
        self.events: List[str] = []

    def index(self, event: str) -> int:
        return self.events.index(event)

    def invoke_id(self) -> str:
        """The Run's id on NATS, read off the listener's own subscription."""
        return self.events[0].removeprefix("subscribe invoke.")


class Msg:
    """The slice of nats-py's Msg the listener reads."""

    def __init__(self, payload: dict) -> None:
        self.data = json.dumps(payload).encode()
        self.reply = "_INBOX.reply"


class FakeConn:
    """The slice of nats-py's Client the listener and a Target use."""

    def __init__(self, log: Recording, fail_flush: Optional[int] = None) -> None:
        self.log = log
        self.fail_flush = fail_flush
        self.flushes = 0
        self.on_invoke: Optional[Callable[[Msg], Coroutine[Any, Any, None]]] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None

    async def subscribe(self, subject: str, cb: Any = None) -> None:
        self.log.events.append(f"subscribe {subject}")
        if subject.startswith("invoke."):
            self.on_invoke = cb
            self.loop = asyncio.get_running_loop()

    async def flush(self, timeout: int = 10) -> None:
        self.flushes += 1
        self.log.events.append("flush")
        if self.flushes == self.fail_flush:
            raise nats.errors.FlushTimeoutError()

    async def publish(self, subject: str, data: bytes) -> None:
        self.log.events.append(f"publish {subject}")

    async def close(self) -> None:
        self.log.events.append("close")

    def deliver(self, payload: dict) -> None:
        """Hand the listener what the server sends on invoke.<id>, on the listener's own loop."""
        assert self.on_invoke is not None and self.loop is not None
        asyncio.run_coroutine_threadsafe(self.on_invoke(Msg(payload)), self.loop)


class Echo(CustomMultiturnTargetAsync):
    async def invoke(  # type: ignore[override]
        self,
        messages: list[dict[str, str]],
        scenario_input: Any = None,
        session_id: Optional[str] = None,
    ) -> ModelInvocation:
        return ModelInvocation("echo", messages, {})


class SlowTurn(Echo):
    """A Target with no bind_listener whose turn takes ``takes`` seconds to answer."""

    def __init__(self, name: str, takes: float) -> None:
        super().__init__(name=name)
        self.takes = takes
        self.answering = threading.Event()

    async def invoke(  # type: ignore[override]
        self,
        messages: list[dict[str, str]],
        scenario_input: Any = None,
        session_id: Optional[str] = None,
    ) -> ModelInvocation:
        self.answering.set()
        await asyncio.sleep(self.takes)
        return ModelInvocation("late", messages, {})


class Binding(Echo):
    """A Target that subscribes a subject of its own on the Run's connection and
    keeps a task running on it, which its release cancels."""

    def __init__(self, name: str, log: Recording, **behaviour: Any) -> None:
        super().__init__(name=name)
        self.log = log
        self.behaviour = behaviour
        self.bound_to: List[tuple] = []
        self.pump: Optional[asyncio.Future] = None
        self.releasing = threading.Event()

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
            self.releasing.set()
            pump.cancel()
            if self.behaviour.get("cancel_at_release"):
                await pump  # ends this coroutine cancelled
            if self.behaviour.get("raise_at_release"):
                raise RuntimeError("release boom")
            if "release_takes" in self.behaviour:
                await asyncio.sleep(self.behaviour["release_takes"])
                self.log.events.append("release done")

        return release


def read_a_future_it_cancelled() -> None:
    """How a plain function ends cancelled: it reads the result of a future it
    cancelled, which raises asyncio.CancelledError straight away."""
    future = asyncio.get_running_loop().create_future()
    future.cancel()
    future.result()


class SyncBinding(CustomMultiturnTarget):
    """A Target whose bind_listener and release are plain functions."""

    def __init__(self, name: str, log: Recording, **behaviour: Any) -> None:
        super().__init__(name=name)
        self.log = log
        self.behaviour = behaviour

    def invoke(  # type: ignore[override]
        self,
        messages: list[dict[str, str]],
        scenario_input: Any = None,
        session_id: Optional[str] = None,
    ) -> ModelInvocation:
        return ModelInvocation("echo", messages, {})

    def bind_listener(self, nc: Any, invoke_id: str) -> Callable[[], None]:
        self.log.events.append("bind")
        if self.behaviour.get("cancel_at_bind"):
            read_a_future_it_cancelled()

        def release() -> None:
            self.log.events.append("release")
            if self.behaviour.get("cancel_at_release"):
                read_a_future_it_cancelled()

        return release


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
    """The fakes around the model: NATS, the listener's credentials, the Run endpoints.

    ``connect_takes`` delays the NATS connect; ``during_run`` runs inside the
    Run call, before it returns, as the server's turns would arrive."""

    def __init__(self, monkeypatch: pytest.MonkeyPatch, log: Recording) -> None:
        self.log = log
        self.conn = FakeConn(log)
        self.run_id = uuid4()
        self.connect_takes = 0.0
        self.during_run: Optional[Callable[[], None]] = None

        async def fake_nats_connect(**_kwargs: Any) -> FakeConn:
            await asyncio.sleep(self.connect_takes)
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
        if self.during_run is not None:
            self.during_run()
        self.log.events.append("run created")
        return TestRunItem(id=self.run_id, project_id=uuid4(), status="FINISHED")

    def _submit(self, **_k: Any) -> TestRunItem:
        self.log.events.append("run submitted")
        return TestRunItem(id=self.run_id, project_id=uuid4(), status="RUNNING")


def run_test(mut: ModelUnderTest) -> TestRunItem:
    return mut.run_test(
        scenario=str(uuid4()), name="bind unit", test_run_type=TestRunType.MULTI_TURN
    )


def submit_test(mut: ModelUnderTest) -> TestRunItem:
    return mut.submit_test(
        scenario=str(uuid4()), name="bind unit", test_run_type=TestRunType.MULTI_TURN
    )


def refused(mut: ModelUnderTest) -> TestRunError:
    with pytest.raises(TestRunError) as raised:
        run_test(mut)
    return raised.value


def first_words(log: Recording) -> List[str]:
    return [event.split(" ")[0] for event in log.events]
