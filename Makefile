ifneq (,$(wildcard ./.env))
    include .env
    export
endif

run-cowriter: 
	@poetry run python -m src.main

run-cowriter-job: 
	@poetry run python -m src.job

push-docker-image-to-artifact-registry:
	@gcloud builds submit --tag gcr.io/$(PROJECT_ID)/run_cowriter_job