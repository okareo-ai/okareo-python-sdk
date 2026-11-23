import random
import string
import uuid
from datetime import datetime

from langchain.chains import LLMChain
from langchain.llms.fake import FakeListLLM
from langchain.prompts import PromptTemplate
from okareo_tests.common import random_string
from pytest_httpx import HTTPXMock

from okareo.callbacks import CallbackHandler
from okareo_api_client.models.model_under_test_response import ModelUnderTestResponse

MOCK_GLOBAL_RESPONSE = [
    {
        "id": "0156f5d7-4ac4-4568-9d44-24750aa08d1a",
        "name": "Global",
        "onboarding_status": "onboarding_status",
        "tags": [],
        "additional_properties": {},
    }
]


MOCK_UUID = str(uuid.uuid4())
MOCK_HOST = "http://mocked.com"
MOCK_API_KEY = "api-key"


def get_mut_response() -> dict:
    return ModelUnderTestResponse(
        id=uuid.UUID(MOCK_UUID),
        project_id=uuid.UUID(MOCK_UUID),
        name="langchain_test",
        tags=["ci-run"],
        time_created=datetime.now().isoformat(),
    ).to_dict()


def test_llm_generates_datapoints(httpx_mock: HTTPXMock) -> None:
    context_token = random_string(10)
    httpx_mock.add_response(
        json=MOCK_GLOBAL_RESPONSE,
        status_code=201,
    )
    httpx_mock.add_response(json=get_mut_response(), status_code=201)

    handler = CallbackHandler(
        api_key=MOCK_API_KEY,
        mut_name="langchain_test",
        context_token=context_token,
        base_path=MOCK_HOST,
    )

    llm = FakeListLLM(responses=["4"])
    llm.predict("what is 2+2?", callbacks=[handler])

    requests = httpx_mock.get_requests()
    assert requests[1].method == "POST"
    assert "/v0/register_model" in requests[1].url.path
    assert requests[2].method == "POST"
    assert "/v0/datapoints" in requests[2].url.path


def test_llm_auto_generate_model(httpx_mock: HTTPXMock) -> None:
    context_token = "".join(random.choices(string.ascii_letters, k=10))
    httpx_mock.add_response(
        json=MOCK_GLOBAL_RESPONSE,
        status_code=201,
    )
    httpx_mock.add_response(json=get_mut_response(), status_code=201)

    handler = CallbackHandler(
        api_key=MOCK_API_KEY, context_token=context_token, base_path=MOCK_HOST
    )

    llm = FakeListLLM(responses=["4"])
    llm.predict("what is 2+2?", callbacks=[handler])

    requests = httpx_mock.get_requests()
    assert requests[1].method == "POST"
    assert "/v0/register_model" in requests[1].url.path
    assert requests[2].method == "POST"
    assert "/v0/datapoints" in requests[2].url.path


def test_chain_generates_datapoints(httpx_mock: HTTPXMock) -> None:
    context_token = random_string(10)
    httpx_mock.add_response(
        json=MOCK_GLOBAL_RESPONSE,
        status_code=201,
    )
    httpx_mock.add_response(json=get_mut_response(), status_code=201)

    handler = CallbackHandler(
        api_key=MOCK_API_KEY, context_token=context_token, base_path=MOCK_HOST
    )

    llm = FakeListLLM(responses=["4"])
    prompt = PromptTemplate.from_template("what is 2+{number}?")
    chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])
    chain.run(number=2)

    requests = httpx_mock.get_requests()
    assert requests[1].method == "POST"
    assert "/v0/register_model" in requests[1].url.path
    assert requests[2].method == "POST"
    assert "/v0/datapoints" in requests[2].url.path
