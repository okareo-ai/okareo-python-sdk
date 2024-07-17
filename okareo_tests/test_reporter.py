import os
import shutil
from datetime import datetime

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo
from okareo.reporter import JSONReporter
from okareo_api_client.models.test_run_item import TestRunItem


@pytest.fixture(scope="module")
def rnd() -> str:
    return f'{random_string(5)} {datetime.now().strftime("%Y%m%d%H%M%S")}'


@pytest.fixture(scope="module")
def okareo_client() -> Okareo:
    return Okareo(api_key=API_KEY)


def test_new_jsonreporter(okareo_client: Okareo) -> None:
    json_data = {
        "id": "af197dd9-8d93-4ae3-9407-d0e19050bd44",
        "project_id": "5ff115a2-f4b0-4100-bbde-87a54428add4",
        "mut_id": "374b760a-ddf3-4295-aa41-57f6da65b67f",
        "scenario_set_id": "c6a6d412-734f-4799-8dc6-667aa75a8e30",
        "name": "CLI Evaluation-078355E56D - EVAL",
        "tags": [],
        "type": "NL_GENERATION",
        "start_time": "2024-03-19T16:27:37.171934",
        "end_time": "2024-03-19T16:28:06.531265",
        "test_data_point_count": 3,
        "model_metrics": {
            "mean_scores": {
                "coherence": 3.6041134314518946,
                "consistency": 3.6666003818872697,
                "fluency": 2.0248845922814245,
                "relevance": 2.3333201448723386,
                "overall": 2.907229637623232,
            },
            "scores_by_row": [
                {
                    "scenario_index": 1,
                    "coherence": 4.999831347314708,
                    "consistency": 4.999918368197127,
                    "fluency": 0,
                    "relevance": 4.998501009778189,
                    "overall": 3.749562681322506,
                    "test_id": "6b7cbe8d-c653-4dce-8de9-137a61566876",
                },
                {
                    "scenario_index": 2,
                    "coherence": 1,
                    "consistency": 1.000000023588648,
                    "fluency": 3,
                    "relevance": 1.0000000195556844,
                    "overall": 1.500000010786083,
                    "test_id": "d3dac533-334a-4c61-8495-08d7c82bcfcf",
                },
                {
                    "scenario_index": 3,
                    "coherence": 4.812508947040976,
                    "consistency": 4.999882753876036,
                    "fluency": 3.0746537768442743,
                    "relevance": 1.001459405283143,
                    "overall": 3.472126220761107,
                    "test_id": "bd40e350-5af3-4ccf-861c-d1a1889ed889",
                },
            ],
        },
        "error_matrix": [],
        "app_link": "https://app.okareo.com/project/5ff115a2-f4b0-4100-bbde-87a54428add4/eval/af197dd9-8d93-4ae3-9407-d0e19050bd44",
    }

    eval_item = TestRunItem.from_dict(json_data)
    reporter = JSONReporter([eval_item])
    assert reporter
    reporter.log()
    report_path = "_temp_reports_"
    os.environ["OKAREO_REPORT_DIR"] = report_path
    reporter.log()
    report_path_exists = os.path.exists(report_path)
    assert report_path_exists
    if os.path.isdir(report_path):
        shutil.rmtree(report_path)
    os.environ["OKAREO_REPORT_DIR"] = ""
