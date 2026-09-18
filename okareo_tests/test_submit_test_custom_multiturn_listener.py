"""submit_test for custom multi-turn Targets: the listener outlives the submit call.

Before this change the submit path started the NATS listener, posted the Run,
returned the accepted Run, and then stopped the listener in a ``finally`` -- so
every turn the server sent afterwards failed with "no responders". These tests
drive ``ModelUnderTest`` with a fake NATS connection and fake endpoints; nothing
touches the network.
"""

import asyncio
import json
import threading
import time
from types import SimpleNamespace
from typing import Any, Callable, Iterator
from uuid import uuid4

import pytest
from pytest_httpx import HTTPXMock

from okareo import Okareo
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

RUN_ID = uuid4()
PROJECT_ID = uuid4()
BASE_URL = "http://unit.invalid"


class EchoAsync(CustomMultiturnTargetAsync):
    async def invoke(  # type: ignore[override]
        self,
        messages: list[dict[str, str]],
        scenario_input: Any = None,
        session_id: str | None = None,
    ) -> ModelInvocation:
        last = messages[-1]["content"] if messages else ""
        return ModelInvocation(last[::-1], messages, {})


class EchoSync(CustomMultiturnTarget):
    def invoke(  # type: ignore[override]
        self,
        messages: list[dict[str, str]],
        scenario_input: Any = None,
        session_id: str | None = None,
    ) -> ModelInvocation:
        last = messages[-1]["content"] if messages else ""
        return ModelInvocation(last[::-1], messages, {})


class FakeNats:
    """The slice of nats-py's Client the listener uses, driven from the test thread."""

    def __init__(self) -> None:
        self.subs: dict[str, Callable[..., Any]] = {}
        self.published: list[tuple[str, dict]] = []
        self.closed = False
        self.loop: asyncio.AbstractEventLoop | None = None

    async def subscribe(self, subject: str, cb: Callable[..., Any]) -> None:
        self.subs[subject] = cb

    async def flush(self) -> None:
        return None

    async def publish(self, subject: str, data: bytes) -> None:
        self.published.append((subject, json.loads(data.decode())))

    async def close(self) -> None:
        self.closed = True

    def deliver(self, payload: dict) -> None:
        """Hand the listener one message, as the server would over invoke.<id>."""
        assert self.loop is not None and len(self.subs) == 1
        (cb,) = self.subs.values()
        msg = SimpleNamespace(data=json.dumps(payload).encode(), reply="_INBOX.1")
        asyncio.run_coroutine_threadsafe(cb(msg), self.loop).result(timeout=3)

    def wait_for_publish(self, count: int, timeout: float = 3.0) -> None:
        deadline = time.monotonic() + timeout
        while len(self.published) < count and time.monotonic() < deadline:
            time.sleep(0.02)
        assert len(self.published) >= count, self.published


def run_item(status: str, failure_message: str | None = None) -> TestRunItem:
    return TestRunItem(
        id=RUN_ID,
        project_id=PROJECT_ID,
        status=status,
        failure_message=failure_message,
    )


LIVE_MUTS: list[ModelUnderTest] = []


@pytest.fixture(autouse=True)
def stop_listeners() -> Iterator[None]:
    """A listener left running (a failed assertion mid-test) is a non-daemon
    thread, and it would hold the whole test process open at exit."""
    yield
    for mut in LIVE_MUTS:
        mut._internal_cleanup_custom_model(
            mut.custom_model_thread_stop_event, mut.custom_model_thread
        )
    LIVE_MUTS.clear()


def make_mut(
    target: CustomMultiturnTarget | CustomMultiturnTargetAsync,
) -> ModelUnderTest:
    response = ModelUnderTestResponse(
        id=uuid4(),
        project_id=PROJECT_ID,
        name=target.name,
        tags=[],
        time_created="2026-09-18T00:00:00",
    )
    mut = ModelUnderTest(
        client=Client(base_url=BASE_URL, raise_on_unexpected_status=True),
        api_key="unit-test-key",
        mut=response,
        models={target.type: target.params()},
    )
    LIVE_MUTS.append(mut)
    return mut


@pytest.fixture
def fake_nats(monkeypatch: pytest.MonkeyPatch) -> FakeNats:
    fake = FakeNats()

    async def fake_connect(
        self: ModelUnderTest, jwt: str, seed: str, local: str
    ) -> FakeNats:
        fake.loop = asyncio.get_running_loop()
        return fake

    monkeypatch.setattr(ModelUnderTest, "connect_nats", fake_connect)
    monkeypatch.setattr(
        mut_module.internal_custom_model_listener_v0_internal_custom_model_listener_get,
        "sync",
        lambda **kwargs: {"jwt": "jwt", "seed": "seed", "local_nats": ""},
    )
    return fake


@pytest.fixture
def submit_endpoint(monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    calls: list[dict] = []

    def fake_submit(**kwargs: Any) -> TestRunItem:
        calls.append(kwargs)
        return run_item("RUNNING")

    def refuse_run(**kwargs: Any) -> TestRunItem:
        raise AssertionError("the run_test endpoint must not be used by submit_test")

    monkeypatch.setattr(
        mut_module.submit_test_v0_test_run_submit_post, "sync", fake_submit
    )
    monkeypatch.setattr(mut_module.run_test_v0_test_run_post, "sync", refuse_run)
    return calls


def statuses(*values: str) -> Iterator[TestRunItem]:
    for value in values:
        yield run_item(value)
    while True:
        yield run_item(values[-1])


def patch_fetch(monkeypatch: pytest.MonkeyPatch, items: Iterator[TestRunItem]) -> None:
    lock = threading.Lock()

    def fake_fetch(
        self: ModelUnderTest, test_run_id: Any, timeout_seconds: float = 30.0
    ) -> TestRunItem:
        with lock:
            return next(items)

    async def fake_fetch_async(
        self: ModelUnderTest, test_run_id: Any, timeout_seconds: float = 30.0
    ) -> TestRunItem:
        with lock:
            return next(items)

    monkeypatch.setattr(ModelUnderTest, "_fetch_test_run", fake_fetch)
    monkeypatch.setattr(ModelUnderTest, "_fetch_test_run_async", fake_fetch_async)


def submit(mut: ModelUnderTest) -> TestRunItem:
    return mut.submit_test(
        scenario=str(uuid4()),
        name="submit-spike unit",
        test_run_type=TestRunType.MULTI_TURN,
        checks=[],
    )


# --- the listener outlives the submit call ---------------------------------


def test_submit_test_keeps_the_listener_alive_until_the_server_closes_the_run(
    fake_nats: FakeNats,
    submit_endpoint: list[dict],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    patch_fetch(monkeypatch, statuses("RUNNING"))
    mut = make_mut(EchoAsync(name="echo"))

    accepted = submit(mut)

    assert accepted.id == RUN_ID and accepted.status == "RUNNING"
    assert len(submit_endpoint) == 1
    assert mut.custom_model_thread is not None and mut.custom_model_thread.is_alive()

    fake_nats.deliver(
        {
            "message_history": [{"role": "user", "content": "hello"}],
            "scenario_input": "spike",
            "session_id": "s1",
            "call_type": "invoke",
        }
    )
    fake_nats.wait_for_publish(1)
    assert fake_nats.published[0][1]["actual"] == "olleh"
    assert mut.custom_model_thread.is_alive()

    fake_nats.deliver({"close": "True"})
    mut.custom_model_thread.join(timeout=3)
    assert not mut.custom_model_thread.is_alive()
    assert fake_nats.published[-1][1] == {"status": "disconnected"}
    assert fake_nats.closed

    out = capsys.readouterr().out
    assert "submitted" in out and "listener stays up" in out
    assert "server sent end-of-run close" in out
    assert "turns answered 1" in out and "turns failed 0" in out


def test_listener_stops_itself_when_the_run_reaches_a_terminal_status(
    fake_nats: FakeNats,
    submit_endpoint: list[dict],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("OKAREO_LISTENER_STATUS_POLL_SECONDS", "0.1")
    patch_fetch(monkeypatch, statuses("RUNNING", "RUNNING", "FINISHED"))
    mut = make_mut(EchoAsync(name="echo"))

    submit(mut)
    assert mut.custom_model_thread is not None
    mut.custom_model_thread.join(timeout=5)

    assert not mut.custom_model_thread.is_alive()
    assert fake_nats.closed
    out = capsys.readouterr().out
    assert "is FINISHED; stopping listener" in out
    assert "server close received no" in out


def test_run_test_still_stops_the_listener_when_it_returns(
    fake_nats: FakeNats, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        mut_module.run_test_v0_test_run_post,
        "sync",
        lambda **kwargs: run_item("FINISHED"),
    )
    mut = make_mut(EchoAsync(name="echo"))

    finished = mut.run_test(
        scenario=str(uuid4()),
        name="run_test unit",
        test_run_type=TestRunType.MULTI_TURN,
    )

    assert finished.status == "FINISHED"
    assert mut.custom_model_thread is not None
    assert not mut.custom_model_thread.is_alive()
    assert fake_nats.closed


def test_listener_is_stopped_when_the_submit_call_fails(
    fake_nats: FakeNats, monkeypatch: pytest.MonkeyPatch
) -> None:
    def failing_submit(**kwargs: Any) -> TestRunItem:
        raise RuntimeError("submit exploded")

    monkeypatch.setattr(
        mut_module.submit_test_v0_test_run_submit_post, "sync", failing_submit
    )
    mut = make_mut(EchoAsync(name="echo"))

    with pytest.raises(RuntimeError, match="submit exploded"):
        submit(mut)

    assert mut.custom_model_thread is not None
    assert not mut.custom_model_thread.is_alive()
    assert fake_nats.closed


def test_submit_test_no_longer_falls_back_to_run_test_for_sync_custom_targets(
    fake_nats: FakeNats,
    submit_endpoint: list[dict],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    patch_fetch(monkeypatch, statuses("RUNNING"))
    mut = make_mut(EchoSync(name="echo-sync"))

    accepted = submit(mut)

    assert accepted.status == "RUNNING"
    assert len(submit_endpoint) == 1
    assert "Falling back to run_test" not in capsys.readouterr().out
    assert mut.custom_model_thread is not None and mut.custom_model_thread.is_alive()

    fake_nats.deliver({"close": "True"})
    mut.custom_model_thread.join(timeout=3)
    assert not mut.custom_model_thread.is_alive()


def test_submit_listener_is_a_daemon_so_a_finished_process_can_exit(
    fake_nats: FakeNats, submit_endpoint: list[dict], monkeypatch: pytest.MonkeyPatch
) -> None:
    patch_fetch(monkeypatch, statuses("RUNNING"))
    mut = make_mut(EchoAsync(name="echo"))

    submit(mut)

    assert mut.custom_model_thread is not None and mut.custom_model_thread.daemon


def test_okareo_wait_for_test_run_stops_the_listener_that_answers_that_run(
    fake_nats: FakeNats,
    submit_endpoint: list[dict],
    monkeypatch: pytest.MonkeyPatch,
    httpx_mock: HTTPXMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    patch_fetch(monkeypatch, statuses("RUNNING"))
    mut = make_mut(EchoAsync(name="echo"))
    submit(mut)
    assert mut.custom_model_thread is not None and mut.custom_model_thread.is_alive()

    httpx_mock.add_response(
        method="GET", url=f"{BASE_URL}/v0/projects", status_code=201, json=[]
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/v0/test_runs/{RUN_ID}",
        status_code=201,
        json={"id": str(RUN_ID), "project_id": str(PROJECT_ID), "status": "FINISHED"},
    )
    okareo = Okareo(api_key="unit-test-key", base_path=BASE_URL)

    finished = okareo.wait_for_test_run(RUN_ID, poll_interval=0.01)

    assert finished.status == "FINISHED"
    mut.custom_model_thread.join(timeout=3)
    assert not mut.custom_model_thread.is_alive()
    assert "listener" in capsys.readouterr().out and fake_nats.closed
    assert str(RUN_ID) not in mut_module._LIVE_LISTENERS


# --- waiting for a submitted Run --------------------------------------------


def test_wait_for_test_run_returns_the_finished_run(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    patch_fetch(monkeypatch, statuses("RUNNING", "FINISHED"))
    mut = make_mut(EchoAsync(name="echo"))

    finished = mut.wait_for_test_run(RUN_ID, poll_interval=0.01)

    assert finished.status == "FINISHED"
    out = capsys.readouterr().out
    assert "RUNNING at +" in out and "FINISHED at +" in out


def test_wait_for_test_run_raises_with_the_servers_failure_message(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    patch_fetch(
        monkeypatch, iter([run_item("FAILED", failure_message="Driver refused")])
    )
    mut = make_mut(EchoAsync(name="echo"))

    with pytest.raises(TestRunError, match="Driver refused"):
        mut.wait_for_test_run(RUN_ID, poll_interval=0.01)


def test_wait_for_test_run_retries_a_failed_poll(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    attempts = {"n": 0}

    def flaky_fetch(
        self: ModelUnderTest, test_run_id: Any, timeout_seconds: float = 30.0
    ) -> TestRunItem:
        attempts["n"] += 1
        if attempts["n"] == 1:
            raise ConnectionError("connection reset")
        return run_item("FINISHED")

    monkeypatch.setattr(ModelUnderTest, "_fetch_test_run", flaky_fetch)
    mut = make_mut(EchoAsync(name="echo"))

    finished = mut.wait_for_test_run(RUN_ID, poll_interval=0.01)

    assert finished.status == "FINISHED" and attempts["n"] == 2
    assert (
        "poll failed (ConnectionError: connection reset); retrying"
        in capsys.readouterr().out
    )


def test_wait_for_test_run_gives_up_after_the_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    patch_fetch(monkeypatch, statuses("RUNNING"))
    mut = make_mut(EchoAsync(name="echo"))

    with pytest.raises(TestRunError, match="did not finish within"):
        mut.wait_for_test_run(RUN_ID, poll_interval=0.01, timeout=0.05)


def test_each_poll_is_one_get_with_its_own_timeout(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/v0/test_runs/{RUN_ID}",
        status_code=201,
        json={"id": str(RUN_ID), "project_id": str(PROJECT_ID), "status": "FINISHED"},
    )
    mut = make_mut(EchoAsync(name="echo"))

    finished = mut.wait_for_test_run(RUN_ID, poll_interval=0.01)

    assert finished.status == "FINISHED"
    request = httpx_mock.get_requests()[0]
    assert request.headers["api-key"] == "unit-test-key"
    assert request.extensions["timeout"]["read"] == 30.0


def test_okareo_wait_for_test_run_polls_by_run_id(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET", url=f"{BASE_URL}/v0/projects", status_code=201, json=[]
    )
    run_url = f"{BASE_URL}/v0/test_runs/{RUN_ID}"
    body = {"id": str(RUN_ID), "project_id": str(PROJECT_ID)}
    httpx_mock.add_response(
        method="GET", url=run_url, status_code=201, json={**body, "status": "RUNNING"}
    )
    httpx_mock.add_response(
        method="GET", url=run_url, status_code=201, json={**body, "status": "FINISHED"}
    )

    okareo = Okareo(api_key="unit-test-key", base_path=BASE_URL)
    finished = okareo.wait_for_test_run(RUN_ID, poll_interval=0.01)

    assert finished.status == "FINISHED"
    assert (
        len([r for r in httpx_mock.get_requests() if r.url.path.endswith(str(RUN_ID))])
        == 2
    )


# --- the connection tells you what happened to it ---------------------------


def test_nats_connection_events_each_log_a_line(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    captured: dict[str, Any] = {}

    async def fake_connect(**kwargs: Any) -> object:
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(mut_module.nats, "connect", fake_connect)
    mut = make_mut(EchoAsync(name="echo"))
    mut._custom_model_listener_stats.update({"invoke_id": "abc"})

    asyncio.run(mut.connect_nats("", "", "nats://fake:4222"))

    assert {"disconnected_cb", "reconnected_cb", "closed_cb", "error_cb"} <= set(
        captured
    )
    asyncio.run(captured["disconnected_cb"]())
    asyncio.run(captured["reconnected_cb"]())
    asyncio.run(captured["error_cb"](TimeoutError("ping timeout")))
    asyncio.run(captured["closed_cb"]())

    out = capsys.readouterr().out
    assert "disconnected from NATS" in out
    assert "reconnected to NATS after" in out
    assert "NATS error: TimeoutError: ping timeout" in out
    assert "closed for good" in out
    assert mut._custom_model_listener_stats["disconnects"] == 1
    assert mut._custom_model_listener_stats["reconnects"] == 1


def test_a_normal_listener_shutdown_is_not_reported_as_a_lost_connection(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    captured: dict[str, Any] = {}

    async def fake_connect(**kwargs: Any) -> object:
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(mut_module.nats, "connect", fake_connect)
    mut = make_mut(EchoAsync(name="echo"))
    asyncio.run(mut.connect_nats("", "", "nats://fake:4222"))
    mut._custom_model_listener_stats["stopping"] = True

    asyncio.run(captured["disconnected_cb"]())
    asyncio.run(captured["closed_cb"]())

    out = capsys.readouterr().out
    assert "disconnected from NATS" not in out and "closed for good" not in out
    assert mut._custom_model_listener_stats.get("disconnects", 0) == 0
