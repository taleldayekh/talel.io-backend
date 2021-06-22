SRC_DIR = talelio_backend/

start-postgres-development:
	export DB_URI=postgresql://test_user:test_password@localhost:5432/test_db && \
	docker compose up -d postgres-development && \
	until pg_isready -h localhost -p 5432 -U test_user ; do echo "Waiting for PostgreSQL" ; done && \
	cd $(SRC_DIR) && alembic upgrade head

stop-postgres-development:
	docker-compose down

serve-api:
	pipenv run python3 -m talelio_backend.app

fix:
	pipenv run yapf --in-place --recursive $(SRC_DIR) && \
	pipenv run isort $(SRC_DIR)

lint:
	pipenv run pylint --rcfile=setup.cfg $(SRC_DIR)

type-check:
	pipenv run mypy $(SRC_DIR)

test:
	pipenv run python3 -m pytest --cov=. -v -s

test-unit:
	pipenv run python3 -m pytest --cov-report=xml --cov-report term --cov=. ./$(SRC_DIR)/tests/unit -v -s

test-integration:
	pipenv run python3 -m pytest --cov-report=xml --cov-report term --cov=. ./$(SRC_DIR)/tests/integration -v -s

test-e2e:
	pipenv run python3 -m pytest --cov-report=xml --cov-report term --cov=. ./$(SRC_DIR)/tests/e2e -v -s

update-requirements:
	pipenv lock -r > requirements.txt

set-githooks-path:
	git config core.hooksPath .githooks
