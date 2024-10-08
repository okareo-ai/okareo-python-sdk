from typing import Any

import autogen  # type: ignore
from okareo_tests.common import API_KEY, OPENAI_API_KEY, random_string

from okareo import Okareo
from okareo.autogen_logger import AutogenLogger, OkareoLogger
from okareo_api_client.models.datapoint_search import DatapointSearch

OPENAI_MODEL = "gpt-4-0125-preview"


def get_logger_config() -> dict[str, Any]:
    context_token = random_string(10)
    logger_config = {
        "api_key": API_KEY,
        "mut_name": "test_autogen_logger-" + context_token,
        "tags": ["autogen-groupchat"],
        "context_token": context_token,
        "log_new_agent": True,
    }
    return logger_config


def create_autogen_assistant() -> Any:
    gpt4_config = {
        "cache_seed": 42,  # change the cache_seed for different trials
        "temperature": 0,
        "config_list": [
            {
                "model": OPENAI_MODEL,
                "api_key": OPENAI_API_KEY,
            }
        ],
        "timeout": 120,
    }

    coder = autogen.AssistantAgent(
        name="coder",
        llm_config=gpt4_config,
        system_message="""You are the Coder. Given a user query, You write python/shell code to solve tasks.""",
        description="Writes code that helps answer user queries.",
    )
    return coder


def test_autogen_autogenlogger() -> None:

    logger_config = get_logger_config()
    logger = AutogenLogger(logger_config)

    with logger:
        create_autogen_assistant()

    okareo = Okareo(api_key=API_KEY)
    dp = okareo.find_datapoints(
        DatapointSearch(context_token=logger_config["context_token"])
    )
    assert isinstance(dp, list)


def test_autogen_okareologger() -> None:

    logger_config = get_logger_config()
    logger = OkareoLogger(logger_config)

    autogen.runtime_logging.start(logger=logger)
    create_autogen_assistant()
    autogen.runtime_logging.stop()

    okareo = Okareo(api_key=API_KEY)
    dp = okareo.find_datapoints(
        DatapointSearch(context_token=logger_config["context_token"])
    )
    assert isinstance(dp, list)
