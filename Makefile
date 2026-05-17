.ONESHELL:
SHELL := /bin/bash
VENV := env
PYTHON := $(VENV)/bin/python
PYTEST := $(VENV)/bin/pytest

.PHONY: install test build release

install:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install hatch pytest
	$(PYTHON) -m pip install -e .

test:
	$(PYTEST) tests/ -v

build:
	$(PYTHON) -m hatch build

release:
	git tag -a "v$(VERSION)" -m "Release v$(VERSION)"
	git push origin "v$(VERSION)"
	@echo "Release v$(VERSION) tagged and pushed. Create a GitHub release from the tag to trigger publishing."
