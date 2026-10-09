import logging
import threading
import time
from typing import Any, List, Optional, Set
from unittest import mock
from unittest.mock import Mock

import pytest
from okareo_tests.common import random_string
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo.model_under_test import ModelUnderTest

GLOBAL_PROJECT_RESPONSE = [
    {
        "id": "0156f5d7-4ac4-4568-9d44-24750aa08d1a",
        "name": "Global",
        "onboarding_status": "onboarding_status",
        "tags": [],
        "additional_properties": {},
    }
]


@pytest.fixture
def rnd() -> str:
    return random_string(5)


@pytest.fixture
def okareo_client(httpx_mock: HTTPXMock) -> Okareo:
    httpx_mock.add_response(
        json=GLOBAL_PROJECT_RESPONSE,
        status_code=201,
    )
    return Okareo("foo", "http://mocked.com")


def get_mut_fixture(name: Optional[str] = None) -> dict:
    rnd_str = random_string(5)
    return {
        "id": "0156f5d7-4ac4-4568-9d44-24750aa08d1a",
        "project_id": "0156f5d7-4ac4-4568-9d44-24750aa08d1a",
        "version": 1,
        "name": name if name else f"CI-Async-Tests-{rnd_str}",
        "tags": ["ci-testing"],
        "time_created": "foo",
    }


def long_add_data_point(*k: Any, **kw: Any) -> None:
    time.sleep(1)


def test_non_blocking_call(okareo_client: Okareo, httpx_mock: HTTPXMock) -> None:
    fixture = get_mut_fixture()
    httpx_mock.add_response(status_code=201, json=fixture)

    mut = okareo_client.register_model(name=fixture["name"], tags=fixture["tags"])

    start = time.time()
    with mock.patch(
        "okareo.model_under_test.add_datapoint_v0_datapoints_post"
    ) as endpoint:
        endpoint.sync = Mock(side_effect=long_add_data_point)
        mut.add_data_point_async(
            feedback=0.1,
            context_token="SOME_CONTEXT_TOKEN",
        )
        # check if call was (almost) instant
        assert time.time() - start < 0.1
        # wait for long_add_data_point to execute
        time.sleep(2)
        assert endpoint.sync.called


def test_flush_leftovers(okareo_client: Okareo, httpx_mock: HTTPXMock) -> None:
    fixture = get_mut_fixture()
    httpx_mock.add_response(status_code=201, json=fixture)

    mut = okareo_client.register_model(name=fixture["name"], tags=fixture["tags"])

    start = time.time()
    with mock.patch(
        "okareo.model_under_test.add_datapoint_v0_datapoints_post"
    ) as endpoint:
        endpoint.sync = Mock(side_effect=long_add_data_point)
        mut.add_data_point_async(
            feedback=0.5,
            context_token="SOME_CONTEXT_TOKEN",
        )
        # should wait for long_add_data_point to comlpete
        mut.flush()
        assert time.time() - start > 1
        assert endpoint.sync.called


def test_retry_on_error(okareo_client: Okareo, httpx_mock: HTTPXMock) -> None:
    fixture = get_mut_fixture()
    httpx_mock.add_response(status_code=201, json=fixture)

    mut = okareo_client.register_model(name=fixture["name"], tags=fixture["tags"])

    time.time()
    with mock.patch(
        "okareo.model_under_test.add_datapoint_v0_datapoints_post"
    ) as endpoint:
        endpoint.sync = Mock(side_effect=Exception("Test"))
        mut.add_data_point_async(
            feedback=1,
            context_token="SOME_CONTEXT_TOKEN",
        )
        time.sleep(3)
        # there should be up to 5 retries
        assert endpoint.sync.call_count == 5


def test_send_once_above_queue_size_threshold(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    fixture = get_mut_fixture()
    httpx_mock.add_response(status_code=201, json=fixture)

    mut = okareo_client.register_model(name=fixture["name"], tags=fixture["tags"])

    with mock.patch(
        "okareo.model_under_test.add_datapoint_v0_datapoints_post"
    ) as endpoint:
        with mock.patch("okareo.async_utils._DEFAULT_MAX_BATCH_SIZE", return_value=2):
            endpoint.sync = Mock()
            mut.add_data_point_async(
                feedback=0,
                context_token="SOME_CONTEXT_TOKEN",
            )
            assert not endpoint.sync.called
            mut.add_data_point_async(
                feedback=1,
                context_token="SOME_CONTEXT_TOKEN",
            )
            mut.add_data_point_async(
                feedback=2,
                context_token="SOME_CONTEXT_TOKEN",
            )

            assert not endpoint.sync.called


WORKER_NAME = "OkareoDatapointsProcessor"


def started_since(before: Set[threading.Thread]) -> List[threading.Thread]:
    """Threads alive now that were not alive when `before` was taken.

    The same measure as comparing threading.active_count(), without its noise:
    under `pytest -n auto` other tests' daemon threads end at arbitrary moments,
    which moves the count while nothing in this test changed.
    """
    return [thread for thread in threading.enumerate() if thread not in before]


def register(okareo_client: Okareo, httpx_mock: HTTPXMock) -> ModelUnderTest:
    fixture = get_mut_fixture()
    httpx_mock.add_response(status_code=201, json=fixture)
    return okareo_client.register_model(name=fixture["name"], tags=fixture["tags"])


def slow_add_data_point(*k: Any, **kw: Any) -> None:
    time.sleep(0.05)


def test_building_a_model_starts_no_thread(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    before = set(threading.enumerate())
    mut = register(okareo_client, httpx_mock)

    assert mut.worker_thread is None
    assert started_since(before) == []

    with mock.patch(
        "okareo.model_under_test.add_datapoint_v0_datapoints_post"
    ) as endpoint:
        endpoint.sync = Mock()
        mut.add_data_point_async(feedback=0.1, context_token="SOME_CONTEXT_TOKEN")
        assert [thread.name for thread in started_since(before)] == [WORKER_NAME]
        mut.close()


def test_close_delivers_queued_datapoints_and_stops_the_thread(
    okareo_client: Okareo, httpx_mock: HTTPXMock, capsys: pytest.CaptureFixture
) -> None:
    mut = register(okareo_client, httpx_mock)
    capsys.readouterr()
    before = set(threading.enumerate())

    with mock.patch(
        "okareo.model_under_test.add_datapoint_v0_datapoints_post"
    ) as endpoint:
        endpoint.sync = Mock(side_effect=slow_add_data_point)
        for feedback in range(3):
            mut.add_data_point_async(
                feedback=feedback, context_token="SOME_CONTEXT_TOKEN"
            )
        mut.close()

    delivered = [call.kwargs["body"].feedback for call in endpoint.sync.call_args_list]
    assert delivered == [0, 1, 2]
    assert mut.worker_thread is not None
    assert not mut.worker_thread.is_alive()
    assert started_since(before) == []
    assert capsys.readouterr().out == ""

    mut.close()  # a second close is a no-op
    assert capsys.readouterr().out == ""


def test_with_block_closes_the_model(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    with mock.patch(
        "okareo.model_under_test.add_datapoint_v0_datapoints_post"
    ) as endpoint:
        endpoint.sync = Mock(side_effect=slow_add_data_point)
        with register(okareo_client, httpx_mock) as mut:
            mut.add_data_point_async(feedback=0.1, context_token="SOME_CONTEXT_TOKEN")

    assert endpoint.sync.call_count == 1
    assert mut.worker_thread is not None
    assert not mut.worker_thread.is_alive()


def test_with_block_closes_the_model_when_the_body_raises(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    with mock.patch(
        "okareo.model_under_test.add_datapoint_v0_datapoints_post"
    ) as endpoint:
        endpoint.sync = Mock(side_effect=slow_add_data_point)
        with pytest.raises(RuntimeError, match="boom"):
            with register(okareo_client, httpx_mock) as mut:
                mut.add_data_point_async(
                    feedback=0.1, context_token="SOME_CONTEXT_TOKEN"
                )
                raise RuntimeError("boom")

    assert endpoint.sync.call_count == 1
    assert mut.worker_thread is not None
    assert not mut.worker_thread.is_alive()


def test_close_without_a_thread_is_safe_and_refuses_later_datapoints(
    okareo_client: Okareo, httpx_mock: HTTPXMock, capsys: pytest.CaptureFixture
) -> None:
    mut = register(okareo_client, httpx_mock)
    capsys.readouterr()

    mut.close()
    mut.close()

    assert mut.worker_thread is None
    assert capsys.readouterr().out == ""
    # Closed means closed: nothing is queued and no thread starts.
    assert (
        mut.add_data_point_async(feedback=0.1, context_token="SOME_CONTEXT_TOKEN")
        is False
    )
    assert mut.worker_thread is None
    assert len(mut.queue) == 0


def test_flush_still_delivers_and_prints(
    okareo_client: Okareo, httpx_mock: HTTPXMock, capsys: pytest.CaptureFixture
) -> None:
    mut = register(okareo_client, httpx_mock)
    capsys.readouterr()

    with mock.patch(
        "okareo.model_under_test.add_datapoint_v0_datapoints_post"
    ) as endpoint:
        endpoint.sync = Mock(side_effect=slow_add_data_point)
        mut.add_data_point_async(feedback=0.1, context_token="SOME_CONTEXT_TOKEN")
        mut.flush()

    assert endpoint.sync.call_count == 1
    assert mut.worker_thread is not None
    assert not mut.worker_thread.is_alive()
    assert capsys.readouterr().out == "Shutting down\n"


def test_flush_without_a_thread_still_prints(
    okareo_client: Okareo, httpx_mock: HTTPXMock, capsys: pytest.CaptureFixture
) -> None:
    mut = register(okareo_client, httpx_mock)
    capsys.readouterr()

    mut.flush()

    assert mut.worker_thread is None
    assert capsys.readouterr().out == "Shutting down\n"


def queue_after_barrier(
    mut: ModelUnderTest, barrier: threading.Barrier, feedback: int
) -> None:
    barrier.wait()
    mut.add_data_point_async(feedback=feedback, context_token="SOME_CONTEXT_TOKEN")


def test_concurrent_first_calls_start_one_worker(
    okareo_client: Okareo, httpx_mock: HTTPXMock
) -> None:
    callers = 8
    for _ in range(20):
        mut = register(okareo_client, httpx_mock)
        before = set(threading.enumerate())
        barrier = threading.Barrier(callers)

        with mock.patch(
            "okareo.model_under_test.add_datapoint_v0_datapoints_post"
        ) as endpoint:
            endpoint.sync = Mock()
            threads = [
                threading.Thread(
                    target=queue_after_barrier, args=(mut, barrier, feedback)
                )
                for feedback in range(callers)
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            workers = [t for t in started_since(before) if t.name == WORKER_NAME]
            assert workers == [mut.worker_thread]
            mut.close()

        assert endpoint.sync.call_count == callers


def test_a_full_queue_logs_instead_of_printing(
    okareo_client: Okareo,
    httpx_mock: HTTPXMock,
    capsys: pytest.CaptureFixture,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.WARNING, logger="okareo.async_utils")
    sending = threading.Event()
    release = threading.Event()

    def blocked_send(*k: Any, **kw: Any) -> None:
        sending.set()
        release.wait(5)

    with mock.patch("okareo.async_utils._DEFAULT_MAX_QUEUE_SIZE", 2), mock.patch(
        "okareo.model_under_test.add_datapoint_v0_datapoints_post"
    ) as endpoint:
        mut = register(okareo_client, httpx_mock)
        capsys.readouterr()
        endpoint.sync = Mock(side_effect=blocked_send)
        mut.add_data_point_async(feedback=0, context_token="SOME_CONTEXT_TOKEN")
        assert sending.wait(5)  # the worker is holding the first datapoint
        for feedback in (1, 2, 3):  # the third finds the queue full
            mut.add_data_point_async(
                feedback=feedback, context_token="SOME_CONTEXT_TOKEN"
            )
        release.set()
        mut.close()

    assert capsys.readouterr().out == ""
    records = [r for r in caplog.records if r.name == "okareo.async_utils"]
    assert [(r.levelno, r.getMessage()) for r in records] == [
        (logging.WARNING, "Queue is full, data points might get dropped.")
    ]


def test_a_failing_send_logs_instead_of_printing(
    okareo_client: Okareo,
    httpx_mock: HTTPXMock,
    capsys: pytest.CaptureFixture,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.WARNING, logger="okareo.async_utils")
    mut = register(okareo_client, httpx_mock)
    capsys.readouterr()

    with mock.patch("okareo.async_utils._DEFAULT_ASYNC_CALL_RETRIES", 2), mock.patch(
        "okareo.model_under_test.add_datapoint_v0_datapoints_post"
    ) as endpoint:
        endpoint.sync = Mock(side_effect=Exception("Test"))
        mut.add_data_point_async(feedback=0.1, context_token="SOME_CONTEXT_TOKEN")
        mut.close()

    assert endpoint.sync.call_count == 2
    assert capsys.readouterr().out == ""
    records = [r for r in caplog.records if r.name == "okareo.async_utils"]
    assert [(r.levelno, r.getMessage()) for r in records] == [
        (logging.WARNING, "Error performing async call (attempt 1 of 2)"),
        (logging.WARNING, "Error performing async call (attempt 2 of 2)"),
    ]
    assert all(r.exc_info and str(r.exc_info[1]) == "Test" for r in records)
