.PHONY: clean clean-test clean-pyc clean-build install develop

# Check git is installed
GIT_INSTALLED := $(shell conda --version > /dev/null 2>&1; echo $$?)

## Remove all build, test, coverage and compiler artifacts
clean: clean-build clean-pyc clean-test

## Remove build artifacts
clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +

## Remove compiler artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

## Remove test and coverage artifacts
clean-test:
	rm -fr .tox/
	rm -f .coverage .coverage.*
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -f coverage.xml

## Run tests with the default py.test
test:
	py.test tests \
		--junitxml=.junit/test-results.xml \
		--cov=src/some_package \
		--cov-report=html \
		--cov-report=xml \
		--cov-report=term

## Builds source and wheel package
dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

## Install the package in the active environment
install: clean
	python -m pip install .

## Install development package in the active environment
develop: clean
	python -m pip install -e .[dev]
 	ifeq (0, $(GIT_INSTALLED))
		if [ ! -d ".git" ]; then git init; fi
 	endif
	pre-commit install