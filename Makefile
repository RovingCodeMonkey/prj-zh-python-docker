.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

build-server:
	docker-compose -f build/docker-compose.yml build

run:
	docker-compose -f build/docker-compose.yml up

run-detach:
	docker-compose -f build/docker-compose.yml up -d

stop:
	docker-compose -f build/docker-compose.yml down

db-migrate: run-detach
	docker-compose -f build/docker-compose.yml exec code-challenge alembic -c /usr/code-challenge/src/migrations/alembic.ini revision --autogenerate

db-upgrade: run-detach
	docker-compose -f build/docker-compose.yml exec code-challenge alembic -c /usr/code-challenge/src/migrations/alembic.ini upgrade head

db-downgrade: run-detach
	docker-compose -f build/docker-compose.yml exec code-challenge alembic -c /usr/code-challenge/src/migrations/alembic.ini downgrade -1

test: run-detach
	docker-compose -f build/docker-compose.yml exec code-challenge pytest /usr/code-challenge/src/tests -c /usr/code-challenge/src/setup.cfg

format: run-detach
	docker-compose -f build/docker-compose.yml exec code-challenge black --preview /usr/code-challenge/src
	docker-compose -f build/docker-compose.yml exec code-challenge isort /usr/code-challenge/src

lint: run-detach
	docker-compose -f build/docker-compose.yml exec code-challenge black --check --diff /usr/code-challenge/src
	docker-compose -f build/docker-compose.yml exec code-challenge isort --check-only /usr/code-challenge/src
	docker-compose -f build/docker-compose.yml exec code-challenge flake8 --config /usr/code-challenge/src/setup.cfg /usr/code-challenge/src

type-check: run-detach
	docker-compose -f build/docker-compose.yml exec code-challenge mypy /usr/code-challenge/src

test-one: clean-test run-detach
	docker-compose -f build/docker-compose.yml exec code-challenge pytest $(filter-out $@, $(MAKECMDGOALS)) --no-cov -x --ff

test-all: clean-test lint type-check test
