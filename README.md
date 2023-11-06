# Okareo Python SDK

[![PyPI](https://img.shields.io/pypi/v/okareo?style=flat-square)](https://pypi.python.org/pypi/okareo/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/okareo?style=flat-square)](https://pypi.python.org/pypi/okareo/)
[![PyPI - License](https://img.shields.io/pypi/l/okareo?style=flat-square)](https://pypi.python.org/pypi/okareo/)

---

**PyPI**: [https://pypi.org/project/okareo/](https://pypi.org/project/okareo/)

---

Python SDK for interacting with Okareo Cloud APIs

## Installation

1. Install the package
    ```sh
    pip install okareo
    ```
2. Get your API token from [https://app.okareo.com/](https://app.okareo.com/).
   (Note: You will need to register first.)

3. Go directly to the **"2. Create your API Token"** on the landing page in above app.

4. Set the environment variable `OKAREO_API_KEY` to your generated API token.

## Get Started Example

Please see and run this notebook:<br>
https://github.com/okareo-ai/okareo-python-sdk/blob/main/examples/scenario_set.ipynb

See additional examples under:<br>
https://github.com/okareo-ai/okareo-python-sdk/tree/main/examples

## Using Okareo LangChain Callbacks Handler

We provide a LangChain callback handler that lets you easily integrate your current workflows with the Okareo platform.

If don't have LangChain dependencies installed in your environment, you can install the base ones (that will help you run the examples) with:
```sh
pip install okareo[langchain]
```

Integrating callbacks into your chain is as easy as importing the SDK in your module add adding the following
```
from okareo.callbacks import CallbackHandler
...
handler = CallbackHandler(mut_name="my-model", context_token="context-token")
llm = OpenAI(temperature=0.3, callbacks=[handler])

```
During the LangChain LLM runs we will collect input and output information so you can analyze it further with the Okareo toolkit.

You can also see an usage example in [./examples/langchain_callback_example.py](./examples/langchain_callback_example.py)

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.9+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Update/regenerate client api code

Our client code is auto-generated from the OpenAPI spec of the Okareo API. In order to update the code in repo install
[openapi-python-generator](https://github.com/MarcoMuellner/openapi-python-generator).
```sh
pip install openapi-python-generator
```

Then, updating the client code to the latest production server spec is as easy as running.
```sh
make openapi/update
```
or, you you want to use your development api server spc, you can use it as a source with
```sh
OPENAPI_SPEC="http://localhost:8000/openapi.json" make openapi/update
```

If you have the `openapi.json` already in the project dir you can simply run
```sh
make openapi/generate
```
to only trigger code generation, without fetching the OpenAPI spec json.



### Testing


In order to run the tests from okareo_tests directory use pytest.
For tests to run you need to have the `OKAREO_API_KEY` environment variable set to a valid API key.

```sh
poetry run pytest
```

Some of the tests use `@integration` decorator which injects `okareo_api` parameter into the tested function which can be then used to run the test against mocked version of the Okareo API and the actual running server.
```python
@integration
def test_function(httpx_mock: HTTPXMock, okareo_api: OkareoAPIhost):
  if f okareo_api.is_mock:
    ...
  integration_env_path = okareo_api.path
  ...
```

In case you want to point them at a different API backend, you can utilize the `BASE_URL` environment variable
```sh
BASE_URL="http://localhost:8000" poetry run pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [Github project page
 ](https://pages.github.com/) automatically as part each release.

### Releasing

Trigger the [Draft release workflow](https://github.com/okareo-ai/okareo/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/okareo-ai/okareo/releases) and publish it. When
 a release is published, it'll trigger [release](https://github.com/okareo-ai/okareo/blob/master/.github/workflows/release.yml) workflow which creates PyPI
 release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

All rights reserved for Okareo Inc
