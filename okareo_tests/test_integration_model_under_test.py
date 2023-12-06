import os

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.model_under_test import CohereModel, OpenAIModel, PineconeDb, ChromaDb
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_api_client.models.scenario_type import ScenarioType
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_type import TestRunType


@pytest.fixture
def rnd() -> str:
    return random_string(5)


@pytest.fixture
def okareo() -> Okareo:
    return Okareo(api_key=API_KEY)

def test_run_test_chromadb_retrieval(rnd: str, okareo: Okareo) -> None:
    seed_data = [
        SeedData(
            input_="which IAM groups have access to s3?",
            result="3cee94071d1bbbac096c0996987d8bb2",
        ),
    ]

    scenario_set_create = ScenarioSetCreate(
        name=f"ci-chromadb-retrieval-{rnd}",
        number_examples=1,
        seed_data=seed_data,
        generation_type=ScenarioType.TEXT_REVERSE_QUESTION,
    )
    scenario = okareo.create_scenario_set(scenario_set_create)

    mut = okareo.register_model(
        name=f"chromadb-{rnd}",
        model=[
            ChromaDb(
                index_name="my-test-index",
                project_id="kwnp6kx",
                top_k=3,
                collection_name="test",
            ),
            CohereModel(
                model_id="embed-english-light-v3.0",
                model_type="embed",
                input_type="search_query",
            ),
        ],
    )

    run_resp = mut.run_test_v2(
        name=f"ci-embedded-chromadb-{rnd}",
        scenario=scenario,
        calculate_metrics=True,
        test_run_type=TestRunType.INFORMATION_RETRIEVAL,
        api_keys={
            "chromadb": "",
            "cohere": os.getenv("COHERE_API_KEY"),
        },
        metrics_kwargs={
            "mrr_at_k": [2, 4, 8],
            "map_at_k": [1, 2],
        },
    )
    assert run_resp.name == f"ci-embedded-chromadb-{rnd}"
    