SHELL := /bin/bash

GIT_SHA_SHORT := $(shell git rev-parse --short HEAD)
DATE := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
VERSION := $(shell git describe --tags)-$(GIT_SHA_SHORT)
OPENAPI_SPEC ?= "https://api.okareo.com/openapi.json"

.PHONY: openapi/generate
openapi/generate:
	rm -rf src/okareo_api_client
	openapi-python-generator $(OPENAPI_SPEC) okareo_api_client
	mv -f okareo_api_client src
