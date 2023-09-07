DOCKER_IMAGE := ahmedbesbes/cowriter
VERSION := $(shell git describe --always --dirty --long)

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

run-cowriter: 
	@poetry run python -m src.main

run-cowriter-job: 
	@poetry run python -m src.job

run-web-agent: 
	@rm -rf db/ && poetry run python -m src.actions.web_searcher 

build-image:
	@docker build . -t $(DOCKER_IMAGE):$(VERSION)

push-docker-image-to-artifact-registry:
	@gcloud builds submit --tag gcr.io/$(PROJECT_ID)/run_cowriter_job

lint:
	@poetry run black .

test: 
	@poetry run coverage run -m pytest
	@poetry run coverage report
	@poetry run coverage html