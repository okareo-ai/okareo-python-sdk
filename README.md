# Okareo Python SDK

[![PyPI](https://img.shields.io/pypi/v/okareo?style=flat-square)](https://pypi.python.org/pypi/okareo/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/okareo?style=flat-square)](https://pypi.python.org/pypi/okareo/)
[![PyPI - License](https://img.shields.io/pypi/l/okareo?style=flat-square)](https://pypi.python.org/pypi/okareo/)

---

**PyPI**: [https://pypi.org/project/okareo/](https://pypi.org/project/okareo/)

---

Python SDK for interacting with Okareo Cloud APIs

## Installation

```sh
pip install okareo
```

## Get Started Example

Please see and run this notebook: https://github.com/okareo-ai/okareo-python-sdk/blob/main/examples/example.ipynb

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
[openapi-generators](https://github.com/openapi-generators/openapi-python-client).

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

```sh
pytest
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
