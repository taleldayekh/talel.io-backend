SRC_DIR = talelio_backend/

serve-api:
	pipenv run flask run

fix:
	pipenv run yapf --in-place --recursive $(SRC_DIR) && \
	pipenv run isort $(SRC_DIR)

lint:
	pipenv run pylint --rcfile=setup.cfg $(SRC_DIR)

type-check:
	pipenv run mypy $(SRC_DIR)

test:
	pipenv run pytest --cov=./

test-coverage:
	pipenv run pytest --cov=./ --cov-report=xml

update-requirements:
	pipenv lock -r > requirements.txt

set-githooks-path:
	git config core.hooksPath .githooks
