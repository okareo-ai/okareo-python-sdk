import time
from typing import Any, Optional
from unittest import mock
from unittest.mock import Mock

import pytest
from okareo_tests.common import random_string
from pytest_httpx import HTTPXMock

from okareo import Okareo

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
        "id": "1",
        "project_id": "1",
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
