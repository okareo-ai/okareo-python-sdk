from typing import Any

from autogen import ConversableAgent  # type: ignore
from okareo_tests.common import API_KEY, OPENAI_API_KEY, random_string

from okareo import Okareo
from okareo.autogen_logger import AutogenLogger
from okareo_api_client.models.datapoint_search import DatapointSearch


def get_logger_config() -> dict[str, Any]:
    logger_config = {
        "api_key": API_KEY,
        "tags": ["autogen-test"],
        "group_name": f"test_autogen_group_{random_string(5)}",
    }
    return logger_config


def get_gpt_config() -> dict[str, Any]:
    gpt4_config_list = [
        {
            "model": "gpt-4-0125-preview",
            "api_key": OPENAI_API_KEY,
        }
    ]

    gpt4_config = {
        "cache_seed": 42,  # change the cache_seed for different trials
        "temperature": 0,
        "config_list": gpt4_config_list,
        "timeout": 120,
    }

    return gpt4_config


def call_autogen_agents(message: str) -> None:
    gpt_config = get_gpt_config()

    cathy = ConversableAgent(
        "cathy",
        system_message="Your name is Cathy and you are a part of a duo of comedians.",
        llm_config=gpt_config,
        human_input_mode="NEVER",  # Never ask for human input.
    )

    joe = ConversableAgent(
        "joe",
        system_message="Your name is Joe and you are a part of a duo of comedians.",
        llm_config=gpt_config,
        human_input_mode="NEVER",  # Never ask for human input.
    )

    joe.initiate_chat(cathy, message=message, max_turns=1)


def test_autogen_logger() -> None:
    logger_config = get_logger_config()
    autogen_logger = AutogenLogger(logger_config)

    with autogen_logger:
        call_autogen_agents("Tell me a joke")

    session_id_0 = autogen_logger.logger.session_id
    okareo = Okareo(api_key=API_KEY)
    dp = okareo.find_datapoints(DatapointSearch(context_token=session_id_0))

    assert isinstance(dp, list)
