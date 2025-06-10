# Okareo Python SDK

[![PyPI](https://img.shields.io/pypi/v/okareo?style=flat-square)](https://pypi.python.org/pypi/okareo/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/okareo?style=flat-square)](https://pypi.python.org/pypi/okareo/)
[![PyPI - License](https://img.shields.io/pypi/l/okareo?style=flat-square)](https://pypi.python.org/pypi/okareo/)

---

**PyPI**: [https://pypi.org/project/okareo/](https://pypi.org/project/okareo/)

---

Python library for interacting with Okareo Cloud APIs

## Documentation
[Getting Started, Guides, and API docs](https://docs.okareo.com/)

## Installation

1. Install the package
    ```sh
    pip install okareo
    ```
2. Get your API token from [https://app.okareo.com/](https://app.okareo.com/)
   (Note: You will need to register first.)

3. Go directly to the **"2. Create your API Token"** on the landing page in above app.

4. Set the environment variable `OKAREO_API_KEY` to your generated API token.

## Get Started Example Notebooks

Please see and run this notebook:<br>
https://github.com/okareo-ai/okareo-python-sdk/blob/main/examples/classification_eval.ipynb

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

## Rendering Docs via `pydoc-markdown`

To render the Python SDK documentation, you can use `source/build_docs.sh` in this repository. This will do the following:

1. Install the SDK poetry environment
2. Run `pydoc-markdown` as configured in `pyproject.toml`
3. Perform postprocessing to re-order the generated sidebar file and change heading levels.

The generated docs will be found in the `docs/python-sdk` and can be rendered with [docusaurus](https://docusaurus.io/).

---

All rights reserved for Okareo Inc
