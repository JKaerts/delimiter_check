style_args = --max-line-length=100

.PHONY: stylecheck
stylecheck:
	pycodestyle $(style_args) .

.PHONY: typecheck
typecheck:
	mypy ./delimiter_check/delimiter_check.py

.PHONY: test
test:
	python -m unittest