SHELL := /bin/bash

GIT_SHA_SHORT := $(shell git rev-parse --short HEAD)
DATE := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
VERSION := $(shell git describe --tags)-$(GIT_SHA_SHORT)
OPENAPI_SPEC ?= "https://api.okareo.com/openapi.json" # use in prod
# OPENAPI_SPEC ?= "http://localhost:8000/openapi.json" # use in local development

.PHONY: spec/update
spec/update:
	wget -q $(OPENAPI_SPEC) -O openapi.json


.PHONY: openapi/generate
openapi/generate:
	rm -rf src/okareo_api_client
	openapi-python-client generate --path openapi.json --meta poetry
	mv -f okareo-api-client/okareo_api_client src
	rm -rf okareo-api-client

.PHONY: openapi/update
openapi/update: spec/update openapi/generate
	echo "API Client Regenerated"
