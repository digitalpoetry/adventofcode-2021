.PHONY: install
install:
	pipenv install -d

.PHONY: test
test:
	pipenv run pytest

.PHONY: format
format:
	pipenv run yapf --recursive --in-place ./aoc ./tests

.PHONY: lint
lint:
	pipenv run yapf --recursive --diff ./aoc ./tests
	pipenv run mypy --ignore-missing-imports ./aoc