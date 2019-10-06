.PHONY: pre-commit dev test clean

pre-commit:
	pre-commit run --all-files

dev:
	pip install -q -e .

test: clean
	tox

clean:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
