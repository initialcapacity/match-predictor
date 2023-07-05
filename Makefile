SHELL = /usr/bin/env bash -o pipefail

default: help

.PHONY: help
help:
	# Usage:
	@sed -n '/^\([a-z][^:]*\).*/s//    make \1/p' $(MAKEFILE_LIST)

.PHONY: backend/install
backend/install:
	cd backend; \
	python3 -m venv env; \
	source env/bin/activate; \
	pip install -r requirements.txt; \

.PHONY: backend/types
backend/types:
	cd backend; \
	source env/bin/activate; \
	mypy matchpredictor test fakecsvprovider; \

.PHONY: backend/test
backend/test: backend/types
	cd backend; \
	source env/bin/activate; \
	python -m unittest; \

.PHONY: backend/measure
backend/measure:
	cd backend; \
	source env/bin/activate; \
	python -m unittest discover -p "measure_*.py"; \

.PHONY: backend/report
backend/report:
	cd backend; \
	source env/bin/activate; \
	python report.py; \

.PHONY: backend/run
backend/run:
	cd backend; \
	source env/bin/activate; \
	source .env; \
	python -m matchpredictor; \

.PHONY: frontend/lint
frontend/lint:
	npm --prefix frontend run lint

.PHONY: frontend/test
frontend/test: frontend/lint
	npm --prefix frontend test

.PHONY: frontend/install
frontend/install:
	npm --prefix frontend install

.PHONY: frontend/run
frontend/run:
	npm --prefix frontend start

.PHONY: integration/install
integration/install:
	npm --prefix integration-tests install

.PHONY: integration/test
integration/test:
	source backend/env/bin/activate; \
	cd integration-tests; \
	./run; \

.PHONY: integration/run
integration/run:
	source backend/env/bin/activate; \
	cd integration-tests; \
	KEEP_OPEN=true ./run; \

.PHONY: install
install: backend/install frontend/install integration/install

.PHONY: unittest
unittest: backend/test frontend/test

.PHONY: test
test: unittest integration/test

