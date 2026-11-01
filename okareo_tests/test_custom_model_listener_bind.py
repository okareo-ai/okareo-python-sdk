"""A custom Target's bind_listener: the listener hands it the Run's NATS connection.

A Target whose class defines ``bind_listener(nc, invoke_id)`` is called once,
after the listener has subscribed to invoke.<id> and flushed and before the Run
is created; what it returns (its release) runs before the connection closes,
on failure paths too. A Target without it sees no change. A bind that fails
stops the Run from starting with a clear error rather than a hang.

Every test goes through ``run_test`` or ``submit_test``. The stand-ins (a fake
``nats.connect`` whose connection records the order of events, the Targets,
the Okareo endpoints) are in ``listener_bind_fakes``; nothing touches the
network.
"""

import asyncio
import time
import traceback
from typing import Any, Iterator, Optional

import pytest
from okareo_tests.listener_bind_fakes import (
    A_TURN,
    NO_HOOK,
    AnswersAnyName,
    Binding,
    Echo,
    FakeOkareo,
    Forwarding,
    Recording,
    SlowTurn,
    SyncBinding,
    first_words,
    models_of,
    refused,
    run_test,
    submit_test,
)

from okareo import listener_binding
from okareo import model_under_test as mut_module
from okareo.error import ListenerBindError
from okareo.model_under_test import ModelInvocation, stop_listener_for_run


@pytest.fixture
def log() -> Recording:
    return Recording()


@pytest.fixture
def fakes(monkeypatch: pytest.MonkeyPatch, log: Recording) -> Iterator[FakeOkareo]:
    fake = FakeOkareo(monkeypatch, log)
    yield fake
    # a submit_test whose test failed midway leaves its listener up
    stop_listener_for_run(fake.run_id)


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


def test_model_under_test_still_names_the_hook_okareo_vision_checks_for() -> None:
    """okareo-vision refuses its client relay unless okareo.model_under_test has
    LISTENER_BIND_HOOK; the re-export is the SDK saying it calls the hook."""
    assert (
        mut_module.LISTENER_BIND_HOOK
        is listener_binding.LISTENER_BIND_HOOK
        == "bind_listener"
    )


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


def test_a_sync_release_that_ends_cancelled_is_logged_and_the_connection_still_closes(
    fakes: FakeOkareo, log: Recording, capsys: pytest.CaptureFixture[str]
) -> None:
    mut = fakes.model(models_of(SyncBinding("sync", log, cancel_at_release=True)))

    run_test(mut)

    assert log.events[-2:] == ["release", "close"]
    assert not mut.custom_model_thread.is_alive()
    out = capsys.readouterr().out
    assert "bind_listener release ended cancelled; closing NATS anyway" in out
    assert ": exiting; turns answered" in out


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


# --- stopping waits for the release, and only a bound listener waits for it --


def test_stop_listener_for_run_waits_for_a_release_longer_than_five_seconds(
    fakes: FakeOkareo, log: Recording
) -> None:
    mut = fakes.model(models_of(Binding("bound", log, release_takes=5.5)))
    submitted = submit_test(mut)

    started = time.monotonic()
    assert stop_listener_for_run(submitted.id)
    took = time.monotonic() - started
    log.events.append("stop returned")

    assert took >= 5.5
    assert log.events[-4:] == ["release", "release done", "close", "stop returned"]
    assert not mut.custom_model_thread.is_alive()


def test_stop_listener_for_run_waits_for_a_release_the_listener_began_on_its_own(
    fakes: FakeOkareo, log: Recording
) -> None:
    """The server's end-of-run close stands in for the status poll's self-stop:
    either way the listener stops itself, and wait_for_test_run then calls
    stop_listener_for_run while the release runs. The handle is dropped only
    after the release and the close, so the call finds it and waits."""
    target = Binding("bound", log, release_takes=1.5)
    mut = fakes.model(models_of(target))
    submitted = submit_test(mut)

    fakes.conn.deliver({"close": True})
    assert target.releasing.wait(5)
    found = stop_listener_for_run(submitted.id)
    log.events.append("stop returned")

    assert found is True
    assert log.events[-4:] == ["release", "release done", "close", "stop returned"]
    assert not mut.custom_model_thread.is_alive()


def test_run_test_waits_five_seconds_for_a_target_without_the_hook_then_says_so(
    fakes: FakeOkareo, log: Recording, capsys: pytest.CaptureFixture[str]
) -> None:
    target = SlowTurn("plain", takes=5.5)
    mut = fakes.model(models_of(target))

    def a_turn_still_answering_when_the_run_returns() -> None:
        fakes.conn.deliver(A_TURN)
        assert target.answering.wait(5)

    fakes.during_run = a_turn_still_answering_when_the_run_returns

    started = time.monotonic()
    run_test(mut)
    took = time.monotonic() - started

    assert took < 6  # the 5 s it always had, not the release's 30 s on top
    out = capsys.readouterr().out
    assert out.count("still running 5s after it was told to stop") == 1
    mut.custom_model_thread.join(5)
    assert not mut.custom_model_thread.is_alive()


def test_stop_listener_for_run_waits_five_seconds_for_a_target_without_the_hook(
    fakes: FakeOkareo, log: Recording, capsys: pytest.CaptureFixture[str]
) -> None:
    target = SlowTurn("plain", takes=5.5)
    mut = fakes.model(models_of(target))
    submitted = submit_test(mut)
    fakes.conn.deliver(A_TURN)
    assert target.answering.wait(5)

    started = time.monotonic()
    assert stop_listener_for_run(submitted.id)
    took = time.monotonic() - started

    assert took < 6
    out = capsys.readouterr().out
    assert out.count("still running 5s after it was told to stop") == 1
    mut.custom_model_thread.join(5)
    assert not mut.custom_model_thread.is_alive()


# --- no hook: no change ------------------------------------------------------


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


def test_a_sync_hook_that_ends_cancelled_refuses_the_run(
    fakes: FakeOkareo, log: Recording
) -> None:
    mut = fakes.model(models_of(SyncBinding("sync", log, cancel_at_bind=True)))

    error = refused(mut)

    assert "bind_listener ended cancelled" in str(error)
    assert "run created" not in log.events
    assert log.events[1:] == ["flush", "bind", "close"]
    assert not mut.custom_model_thread.is_alive()


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


# --- the readiness wait names what used it up --------------------------------


def test_the_readiness_wait_names_the_bind_when_the_bind_used_it_up(
    fakes: FakeOkareo, log: Recording, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OKAREO_CUSTOM_MODEL_READY_TIMEOUT", "0.3")

    error = refused(fakes.model(models_of(Binding("bound", log, hang_for=1))))

    assert "The Target's bind_listener did not return within" in str(error)
    assert "Check connectivity to NATS" not in str(error)
    assert "run created" not in log.events
    assert log.events[-1] == "close"


def test_the_readiness_wait_names_nats_when_the_connect_used_it_up(
    fakes: FakeOkareo, log: Recording, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OKAREO_CUSTOM_MODEL_READY_TIMEOUT", "0.3")
    fakes.connect_takes = 1.0

    error = refused(fakes.model(models_of(Binding("bound", log))))

    assert "did not subscribe to NATS within" in str(error)
    assert "bind_listener" not in str(error)
    assert "run created" not in log.events


def test_a_listener_that_connects_after_the_readiness_wait_gave_up_does_not_bind(
    fakes: FakeOkareo, log: Recording, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OKAREO_CUSTOM_MODEL_READY_TIMEOUT", "0.3")
    fakes.connect_takes = 1.0
    target = Binding("bound", log)
    mut = fakes.model(models_of(target))

    refused(mut)

    # the Run was never created, so the Target is never handed its connection
    assert not mut.custom_model_thread.is_alive()
    assert log.events[1:] == ["flush", "close"]
    assert target.bound_to == []
