#!/bin/bash

poetry install
poetry run pydoc-markdown
# reorder the contents of sidebar.json
poetry run python docs/build_docs_postprocess.py
