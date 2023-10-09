SHELL := /bin/bash

GIT_SHA_SHORT := $(shell git rev-parse --short HEAD)
DATE := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
VERSION := $(shell git describe --tags)-$(GIT_SHA_SHORT)


.PHONY: openapi/generate
openapi/generate:
	rm -rf src/okareo_api_client
	openapi-python-generator http://localhost:8000/openapi.json okareo_api_client
	mv -f okareo_api_client src
