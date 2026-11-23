from uuid import UUID

import pytest
from okareo_tests.common import random_string
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo_api_client.models import ScenarioSetCreate, ScenarioSetGenerate
from okareo_api_client.models.scenario_type import ScenarioType
from okareo_api_client.types import Unset

MOCK_UUID = "0156f5d7-4ac4-4568-9d44-24750aa08d1a"
MOCK_HOST = "http://mocked.com"


@pytest.fixture
def okareo_client(httpx_mock: HTTPXMock) -> Okareo:
    httpx_mock.add_response(
        json=[
            {
                "id": MOCK_UUID,
                "name": "Global",
                "onboarding_status": "onboarding_status",
                "tags": [],
                "additional_properties": {},
            }
        ],
        status_code=201,
    )
    return Okareo("api-key", MOCK_HOST)


def test_generate_scenarios_empty(okareo_client: Okareo, httpx_mock: HTTPXMock) -> None:
    # The server answers a generation that yields no rows with a 422 whose detail is a one-element list.
    httpx_mock.add_response(
        url=f"{MOCK_HOST}/v0/scenario_sets_generate",
        status_code=422,
        json={
            "detail": [
                f"No scenario rows generated for scenario_id={MOCK_UUID}. "
                "Please check the input data and try again."
            ]
        },
    )
    scenario_set_generate = ScenarioSetGenerate(
        source_scenario_id=UUID(MOCK_UUID),
        name=f"generated scenario synonyms set {random_string(5)}",
        number_examples=1,
        generation_type=ScenarioType.SYNONYMS,
        synonym_sets=[["sit", "sit amet"]],
    )
    # expect a warning since no synonyms are found in the source scenario rows
    with pytest.warns(
        UserWarning,
        match="No scenario rows generated for scenario_id",
    ) as record:
        generated_scenario = okareo_client.generate_scenario_set(scenario_set_generate)
        assert generated_scenario is not None
        assert isinstance(generated_scenario.scenario_id, Unset)
        assert generated_scenario.time_created
        assert generated_scenario.type_ == "SYNONYMS"
        if not record:
            pytest.fail("Expected warning for empty generated scenario.")


def test_create_scenario_empty_seed_data(
    okareo_client: Okareo,
) -> None:
    scenario_set_create = ScenarioSetCreate(
        name=f"my test scenario set {random_string(5)}",
        seed_data=[],
    )
    with pytest.raises(
        ValueError, match="Non-empty seed data is required to create a scenario set"
    ):
        okareo_client.create_scenario_set(scenario_set_create)
