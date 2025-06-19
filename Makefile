PHONY = help install install-dev test test-cov run init-db format lint type secure

help:
	@echo "---------------HELP-----------------"
	@echo "To install the project type -> make install"
	@echo "To install the project for development type -> make install-dev"
	@echo "To run application -> make run"
	@echo "To test the project type [exclude slow tests] -> make test"
	@echo "To test the project [only slow tests] -> make test-slow"
	@echo "To test with coverage [all tests] -> make test-cov"
	@echo "To run load test -> make load-test"
	@echo "To format code type -> make format"
	@echo "To check linter type -> make lint"
	@echo "To run type checker -> make type-check"
	@echo "To run all security related commands -> make secure"
	@echo "------------------------------------"

install:
	pipenv install --deploy

install-dev:
	pipenv install --dev

format:
	pipenv run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place src --exclude=__init__.py
	pipenv run black src tests --config pyproject.toml

lint:
	pipenv run flake8 src
	pipenv run black src tests --check --diff --config pyproject.toml

run:
	pipenv run uvicorn src.seaapi.adapters.entrypoints.application:app --host 0.0.0.0 --port 8000 --reload

migrations:
	pipenv run alembic -c src/seaapi/adapters/db/alembic.ini revision --autogenerate

migrate:
	pipenv run alembic -c src/seaapi/adapters/db/alembic.ini upgrade head

test:
	TEST_RUN="TRUE" pipenv run pytest -svvv --order-group-scope=module  -m "not slow" tests

test-slow:
	TEST_RUN="TRUE" pipenv run pytest -svvv --order-group-scope=module -m "slow" tests

test-cov:
	TEST_RUN="TRUE" pipenv run pytest -svvv --order-group-scope=module --cov-report html --cov=src tests

load-test:
	cd .artillery && yarn start

type:
	pipenv run pytype --config=pytype.cfg src/*

secure:
	pipenv run bandit -r src --config pyproject.toml