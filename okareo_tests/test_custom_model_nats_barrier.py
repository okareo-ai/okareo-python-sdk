"""Unit tests for the custom-multiturn NATS readiness barrier.

Regression coverage for the "Unable to connect to custom model on client."
race: the client used to start the run before its NATS listener had subscribed
to invoke.{id}, so the server could publish to an unsubscribed channel. The fix
has the listener signal readiness only after subscribe()+flush(), and the run
waits on that signal before creating the run.

These tests fake the NATS connection, so they run offline (no server, no creds).
They exercise the listener's readiness/error contract directly, which is what
the barrier in _run_test_internal depends on.
"""

import asyncio
import contextlib
import threading
import types
from typing import Any, Dict, List, Tuple

from okareo.model_under_test import ModelUnderTest


class _FakeConn:
    def __init__(self) -> None:
        self.subscribed: List[str] = []
        self.flushed = False
        self.closed = False

    async def subscribe(self, subject: str, cb: Any = None) -> None:
        self.subscribed.append(subject)

    async def flush(self, timeout: int = 10) -> None:
        self.flushed = True

    async def close(self) -> None:
        self.closed = True


def _fake_self(connect_impl: Any) -> Any:
    s = types.SimpleNamespace()
    s.connect_nats = connect_impl

    async def _process_single_message(*args: Any, **kwargs: Any) -> None:
        return None

    s.process_single_message = _process_single_message
    return s


async def _run_listener(
    connect_impl: Any, invoke_id: str = "inv-1", ready_wait_s: float = 2.0
) -> Tuple[threading.Event, Dict[str, Any]]:
    stop = threading.Event()
    ready = threading.Event()
    err: Dict[str, Any] = {}
    task = asyncio.ensure_future(
        ModelUnderTest._internal_run_custom_model_listener(
            _fake_self(connect_impl),
            stop,
            "jwt",
            "seed",
            "local",
            invoke_id,
            ready,
            err,
        )
    )
    # Wait until the listener reaches a terminal setup state (ready is set on
    # both success and failure paths), then let the keep-alive loop exit.
    for _ in range(int(ready_wait_s / 0.01)):
        if ready.is_set():
            break
        await asyncio.sleep(0.01)
    stop.set()
    await asyncio.wait_for(task, timeout=2)
    return ready, err


def test_ready_signaled_only_after_subscribe_and_flush() -> None:
    conn = _FakeConn()

    async def connect(*_a: Any) -> _FakeConn:
        return conn

    ready, err = asyncio.run(_run_listener(connect))

    assert ready.is_set()
    assert err == {}
    assert conn.subscribed == ["invoke.inv-1"]
    assert conn.flushed is True  # flush forces server-side SUB registration
    assert conn.closed is True  # finally still closes the connection


def test_connect_failure_captured_and_waiter_released() -> None:
    async def connect(*_a: Any) -> _FakeConn:
        raise RuntimeError("connect boom")

    ready, err = asyncio.run(_run_listener(connect))

    # The finally releases the barrier even on failure, so the caller can wake,
    # read the captured error, and raise an attributable TestRunError instead of
    # blocking until a server-side timeout.
    assert ready.is_set()
    assert isinstance(err.get("error"), RuntimeError)
    assert "connect boom" in str(err["error"])


def test_flush_failure_captured_not_false_ready() -> None:
    class _FlushFails(_FakeConn):
        async def flush(self, timeout: int = 10) -> None:
            raise RuntimeError("flush boom")

    conn = _FlushFails()

    async def connect(*_a: Any) -> _FakeConn:
        return conn

    ready, err = asyncio.run(_run_listener(connect))

    # A flush failure must surface as an error, not a false "ready".
    assert ready.is_set()  # released via finally
    assert isinstance(err.get("error"), RuntimeError)
    assert "flush boom" in str(err["error"])


def test_ready_not_signaled_while_connect_hangs() -> None:
    async def connect(*_a: Any) -> _FakeConn:
        await asyncio.sleep(5)  # hang
        return _FakeConn()

    async def probe() -> bool:
        stop = threading.Event()
        ready = threading.Event()
        err: Dict[str, Any] = {}
        task = asyncio.ensure_future(
            ModelUnderTest._internal_run_custom_model_listener(
                _fake_self(connect), stop, "jwt", "seed", "local", "inv", ready, err
            )
        )
        await asyncio.sleep(0.3)
        not_ready = not ready.is_set()  # the barrier would correctly keep waiting
        stop.set()
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task
        return not_ready

    assert asyncio.run(probe()) is True
