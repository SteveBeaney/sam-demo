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
	.venv/bin/coverage report

lint:
	.venv/bin/flake8 functions
