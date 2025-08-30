import time
from datetime import datetime
from unittest import mock

import litellm  # type: ignore
from litellm import completion
from okareo_tests.common import API_KEY, OkareoAPIhost, integration, random_string
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo.litellm_logger import LiteLLMLogger, LiteLLMProxyLogger
from okareo_api_client.models.datapoint_search import DatapointSearch
from okareo_api_client.models.model_under_test_response import ModelUnderTestResponse


def get_mut_response() -> dict:
    return ModelUnderTestResponse(
        "id",
        "my-project",
        "langchain_test",
        ["ci-run"],
        datetime.now().isoformat(),
    ).to_dict()


@integration
def dtest_litellm_baselogger(httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost) -> None:
    context_token = random_string(10)
    if okareo_api.is_mock:
        httpx_mock.add_response(json=get_mut_response(), status_code=201)

    with mock.patch.object(Okareo.__init__, "__defaults__", (okareo_api.path, 100)):
        handler = LiteLLMLogger(
            api_key=API_KEY,
            mut_name="test_litellm_baselogger-" + context_token,
            context_token=context_token,
        )

    litellm.callbacks = [handler]  # type: ignore
    model = "gpt-3.5-turbo"
    response = "ModelResponse(id='chatcmpl-90E2ohwLpPXSIuPRzm0fc905yVjZh', choices=[Choices(finish_reason='stop', index=0, message=Message(content='Barack Obama is an American politician who served as the 44th President of the United States from 2009 to 2017. He is a member of the Democratic Party and was the first African American to be elected to the presidency. Before becoming president, he served as a U.S. Senator from Illinois and worked as a community organizer and civil rights attorney. He is widely regarded as one of the most influential and charismatic leaders in modern American history.', role='assistant'))], created=1709841014, model='gpt-3.5-turbo-0125', object='chat.completion', system_fingerprint='fp_2b778c6b35', usage=Usage(completion_tokens=92, prompt_tokens=12, total_tokens=104))"
    messages = [{"content": "who is obama?", "role": "user"}]
    response = completion(model=model, messages=messages, mock_response=response)

    # needs to wait for callback to finish
    time.sleep(2)

    if okareo_api.is_mock:
        requests = httpx_mock.get_requests()
        assert requests[0].method == "POST"
        assert "/v0/register_model" in requests[0].url.path
        assert requests[1].method == "POST"
        assert "/v0/datapoints" in requests[1].url.path
    else:
        okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)
        dp = okareo.find_datapoints(DatapointSearch(context_token=context_token))
        assert isinstance(dp, list)


@integration
def dtest_litellm_openailogger(
    httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost
) -> None:
    context_token = random_string(10)
    if okareo_api.is_mock:
        httpx_mock.add_response(json=get_mut_response(), status_code=201)

    with mock.patch.object(Okareo.__init__, "__defaults__", (okareo_api.path, 100)):
        handler = LiteLLMProxyLogger(
            api_key=API_KEY,
            mut_name="test_litellm_openailogger-" + context_token,
            context_token=context_token,
        )

    litellm.callbacks = [handler]  # type: ignore
    model = "gpt-3.5-turbo"
    response = "ModelResponse(id='chatcmpl-90E2ohwLpPXSIuPRzm0fc905yVjZh', choices=[Choices(finish_reason='stop', index=0, message=Message(content='Barack Obama is an American politician who served as the 44th President of the United States from 2009 to 2017. He is a member of the Democratic Party and was the first African American to be elected to the presidency. Before becoming president, he served as a U.S. Senator from Illinois and worked as a community organizer and civil rights attorney. He is widely regarded as one of the most influential and charismatic leaders in modern American history.', role='assistant'))], created=1709841014, model='gpt-3.5-turbo-0125', object='chat.completion', system_fingerprint='fp_2b778c6b35', usage=Usage(completion_tokens=92, prompt_tokens=12, total_tokens=104))"
    messages = [{"content": "who is obama?", "role": "user"}]
    response = completion(model=model, messages=messages, mock_response=response)

    # needs to wait for callback to finish
    time.sleep(2)

    if okareo_api.is_mock:
        requests = httpx_mock.get_requests()
        assert requests[0].method == "POST"
        assert "/v0/register_model" in requests[0].url.path
        assert requests[1].method == "POST"
        assert "/v0/datapoints" in requests[1].url.path
    else:
        okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)
        dp = okareo.find_datapoints(DatapointSearch(context_token=context_token))
        assert isinstance(dp, list)
