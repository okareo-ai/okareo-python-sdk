import random
import string
from datetime import datetime
from unittest import mock

from langchain.chains import LLMChain
from langchain.llms.fake import FakeListLLM
from langchain.prompts import PromptTemplate
from okareo_tests.common import API_KEY, OkareoAPIhost, integration, random_string
from pytest_httpx import HTTPXMock

from okareo import Okareo
from okareo.callbacks import CallbackHandler
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
def test_llm_generates_datapoints(
    httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost
) -> None:
    context_token = random_string(10)
    if okareo_api.is_mock:
        httpx_mock.add_response(json=get_mut_response(), status_code=201)

    with mock.patch.object(Okareo.__init__, "__defaults__", (okareo_api.path, 100)):
        handler = CallbackHandler(
            mut_name="langchain_test", context_token=context_token
        )

    llm = FakeListLLM(responses=["4"])
    llm.predict("what is 2+2?", callbacks=[handler])

    if okareo_api.is_mock:
        requests = httpx_mock.get_requests()
        print("requests", requests)
        assert requests[0].method == "POST"
        assert "/v0/register_model" in requests[0].url.path
        assert requests[1].method == "POST"
        assert "/v0/datapoints" in requests[1].url.path
    else:
        okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)
        dp = okareo.find_datapoints(context_token=context_token)
        if isinstance(dp, list):
            assert len(dp) == 1


@integration
def test_llm_auto_generate_model(
    httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost
) -> None:
    context_token = "".join(random.choices(string.ascii_letters, k=10))
    if okareo_api.is_mock:
        httpx_mock.add_response(json=get_mut_response(), status_code=201)

    with mock.patch.object(Okareo.__init__, "__defaults__", (okareo_api.path, 100)):
        handler = CallbackHandler(context_token=context_token)

    llm = FakeListLLM(responses=["4"])
    llm.predict("what is 2+2?", callbacks=[handler])

    if okareo_api.is_mock:
        requests = httpx_mock.get_requests()
        print("requests", requests)
        assert requests[0].method == "POST"
        assert "/v0/register_model" in requests[0].url.path
        assert requests[1].method == "POST"
        assert "/v0/datapoints" in requests[1].url.path
    else:
        okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)
        dp = okareo.find_datapoints(context_token=context_token)
        if isinstance(dp, list):
            assert len(dp) == 1


@integration
def test_chain_generates_datapoints(
    httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost
) -> None:
    context_token = random_string(10)
    if okareo_api.is_mock:
        httpx_mock.add_response(json=get_mut_response(), status_code=201)

    with mock.patch.object(Okareo.__init__, "__defaults__", (okareo_api.path, 100)):
        handler = CallbackHandler(context_token=context_token)

    llm = FakeListLLM(responses=["4"])
    prompt = PromptTemplate.from_template("what is 2+{number}?")
    chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])
    chain.run(number=2)

    if okareo_api.is_mock:
        requests = httpx_mock.get_requests()
        print("requests", requests)
        assert requests[0].method == "POST"
        assert "/v0/register_model" in requests[0].url.path
        assert requests[1].method == "POST"
        assert "/v0/datapoints" in requests[1].url.path
    else:
        okareo = Okareo(api_key=API_KEY, base_path=okareo_api.path)
        dp = okareo.find_datapoints(context_token=context_token)
        if isinstance(dp, list):
            assert len(dp) == 1
