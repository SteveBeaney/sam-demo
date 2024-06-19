SHELL := /bin/bash

build:
	sam build

deploy:
	sam deploy --no-confirm-changeset

delete:
	sam delete --no-prompts

test:
	.venv/bin/pytest .

coverage:
	.venv/bin/coverage run -m pytest
	.venv/bin/coverage report -m

coverage_anotate:
	.venv/bin/coverage run -m pytest
	.venv/bin/coverage annotate

coverage_clean:
	find . -name "*,cover" -type f -delete

flake8:
	.venv/bin/flake8 ./functions

