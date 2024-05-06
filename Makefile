NAME := hyperexponential_task
POETRY := $(shell command -v poetry 2> /dev/null)

.DEFAULT_GOAL := help

.PHONY: help
help:
		@echo "Please use 'make <target>' where <target> is one of"
		@echo ""
		@echo "  install     install packages and prepare environment"
		@echo "  lint        run the code linters"
		@echo "  format      reformat code"
		@echo "  test        run all the tests"
		@echo "  clean       remove all temporary files"
		@echo ""

.PHONY: install
install:
		@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
		$(POETRY) install

.PHONY: lint
lint: $(INSTALL_STAMP)
		$(POETRY) run flake8 .
		$(POETRY) run mypy .
		$(POETRY) run bandit -c pyproject.toml . -r

.PHONY: format
format: $(INSTALL_STAMP)
		$(POETRY) run black .

.PHONY: test
test: $(INSTALL_STAMP)
		$(POETRY) run pytest ./tests/ --cov

.PHONY: clean
clean:
		find . -type d -name "__pycache__" | xargs rm -rf {};
		rm -rf .coverage .mypy_cache .pytest_cache