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
import time
import types
from typing import Any, Dict, List, Tuple

import pytest

from okareo import model_under_test as mut_module
from okareo.model_under_test import ModelUnderTest, TestRunError
from okareo_api_client.models.test_run_type import TestRunType


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


# --- Barrier in _run_test_internal (offline, real run_test) ---------------------
#
# The listener contract above is necessary but not sufficient: the fix lives in
# the ordering inside _run_test_internal (parse budget -> creds -> start thread
# -> wait for ready -> create run) and in the listener bounding its own connect
# with that budget. These tests drive the real run_test with the HTTP calls and
# NATS connect replaced, so the whole path runs without a server.


class _OrderConn(_FakeConn):
    def __init__(self, events: Dict[str, Any]) -> None:
        super().__init__()
        self._events = events

    async def flush(self, timeout: int = 10) -> None:
        await super().flush(timeout)
        self._events["order"].append("flush")


def _make_mut(
    monkeypatch: Any,
    connect_impl: Any,
    local_nats: str = "nats://nats.internal:4222",
) -> Tuple[Any, Dict[str, Any]]:
    events: Dict[str, Any] = {"creds": 0, "run": 0, "order": []}

    def fake_creds(**kwargs: Any) -> Dict[str, str]:
        events["creds"] += 1
        return {"jwt": "j", "seed": "s", "local_nats": local_nats}

    def fake_run(self: Any, *args: Any, **kwargs: Any) -> Any:
        events["run"] += 1
        events["order"].append("run")
        return types.SimpleNamespace(id="run-1")

    monkeypatch.setattr(
        mut_module.internal_custom_model_listener_v0_internal_custom_model_listener_get,
        "sync",
        fake_creds,
    )
    monkeypatch.setattr(
        ModelUnderTest, "_validate_run_test_params", lambda self, *a, **k: {}
    )
    monkeypatch.setattr(ModelUnderTest, "_call_run_test_method", fake_run)
    monkeypatch.setattr(ModelUnderTest, "connect_nats", connect_impl)

    # Bypass __init__ (it starts a worker thread) and type as Any so the
    # stand-in client/ids below satisfy mypy.
    mut: Any = ModelUnderTest.__new__(ModelUnderTest)
    mut.client = object()
    mut.api_key = "k"
    mut.mut_id = "mut"
    mut.name = "mut"
    mut.models = {"custom_target": object()}
    return mut, events


def _run(mut: Any) -> Any:
    return mut.run_test("scn", "name", test_run_type=TestRunType.MULTI_TURN)


def test_run_is_created_only_after_subscribe_and_flush(monkeypatch: Any) -> None:
    events_ref: Dict[str, Any] = {}

    async def connect(self: Any, *_a: Any) -> _FakeConn:
        await asyncio.sleep(0.2)
        return _OrderConn(events_ref)

    monkeypatch.setenv("OKAREO_CUSTOM_MODEL_READY_TIMEOUT", "5")
    mut, events = _make_mut(monkeypatch, connect)
    events_ref.update(events)
    events_ref["order"] = events["order"]

    result = _run(mut)

    assert result.id == "run-1"
    assert events["order"] == ["flush", "run"]
    assert not mut.custom_model_thread.is_alive()


def test_flush_timeout_keeps_its_own_name(monkeypatch: Any) -> None:
    from nats.errors import FlushTimeoutError

    class _NoPong(_FakeConn):
        async def flush(self, timeout: int = 10) -> None:
            raise FlushTimeoutError()

    async def connect(self: Any, *_a: Any) -> _FakeConn:
        return _NoPong()

    monkeypatch.setenv("OKAREO_CUSTOM_MODEL_READY_TIMEOUT", "5")
    mut, events = _make_mut(monkeypatch, connect)

    with pytest.raises(TestRunError) as exc:
        _run(mut)

    # nats-py's FlushTimeoutError subclasses asyncio.TimeoutError; it must not be
    # relabelled as the setup budget expiring.
    assert "FlushTimeoutError" in str(exc.value)
    assert "did not complete within" not in str(exc.value)
    assert events["run"] == 0


def test_error_message_redacts_nats_url_userinfo(monkeypatch: Any) -> None:
    async def connect(self: Any, *_a: Any) -> _FakeConn:
        raise RuntimeError("refused")

    monkeypatch.setenv("OKAREO_CUSTOM_MODEL_READY_TIMEOUT", "5")
    mut, events = _make_mut(
        monkeypatch, connect, local_nats="nats://nsuser:s3cretpw@nats.internal:4222"
    )

    with pytest.raises(TestRunError) as exc:
        _run(mut)

    assert "(nats://nats.internal:4222)" in str(exc.value)
    assert "s3cretpw" not in str(exc.value)
    assert "nsuser" not in str(exc.value)


def test_hung_connect_is_cancelled_at_budget_and_thread_exits(
    monkeypatch: Any,
) -> None:
    async def connect(self: Any, *_a: Any) -> _FakeConn:
        await asyncio.sleep(5)  # longer than the budget; must be cancelled
        return _FakeConn()

    monkeypatch.setenv("OKAREO_CUSTOM_MODEL_READY_TIMEOUT", "1")
    mut, events = _make_mut(monkeypatch, connect)

    start = time.monotonic()
    with pytest.raises(TestRunError) as exc:
        _run(mut)
    elapsed = time.monotonic() - start

    msg = str(exc.value)
    assert "failed to connect to NATS (nats://nats.internal:4222)" in msg
    assert (
        "TimeoutError: listener setup (connect/subscribe/flush) did not complete within 1s"
        in msg
    )
    assert events["run"] == 0
    # The listener cancelled its own connect, so the cleanup join did not have
    # to wait out its 5s timeout and the thread is gone.
    assert not mut.custom_model_thread.is_alive()
    assert elapsed < 4


def test_connect_error_is_attributable(monkeypatch: Any) -> None:
    async def connect(self: Any, *_a: Any) -> _FakeConn:
        raise RuntimeError("auth boom")

    monkeypatch.setenv("OKAREO_CUSTOM_MODEL_READY_TIMEOUT", "5")
    mut, events = _make_mut(monkeypatch, connect)

    with pytest.raises(TestRunError) as exc:
        _run(mut)

    assert (
        "failed to connect to NATS (nats://nats.internal:4222): RuntimeError: auth boom"
        in str(exc.value)
    )
    assert events["run"] == 0


@pytest.mark.parametrize(
    "value, fragment",
    [
        ("abc", "must be a number of seconds"),
        ("", "must be a number of seconds"),
        ("0", "must be between 0 and 86400"),
        ("-1", "must be between 0 and 86400"),
        ("inf", "must be between 0 and 86400"),
    ],
)
def test_bad_budget_is_rejected_before_creds(
    monkeypatch: Any, value: str, fragment: str
) -> None:
    async def connect(self: Any, *_a: Any) -> _FakeConn:
        return _FakeConn()

    monkeypatch.setenv("OKAREO_CUSTOM_MODEL_READY_TIMEOUT", value)
    mut, events = _make_mut(monkeypatch, connect)

    with pytest.raises(TestRunError) as exc:
        _run(mut)

    assert "OKAREO_CUSTOM_MODEL_READY_TIMEOUT" in str(exc.value)
    assert fragment in str(exc.value)
    assert events["creds"] == 0
    assert events["run"] == 0
