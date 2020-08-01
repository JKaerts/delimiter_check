.PHONY: help test typecheck stylecheck
style_args = --max-line-length=100

help:
	@echo 'Build targets:'
	@echo '  test        - Run the test suite'
	@echo '  typecheck   - Run mypy to check the typing of the project'
	@echo ''
	@echo 'Code style targets:'
	@echo '  stylecheck  - Use pycodestyle to check pep8-compliance'

test:
	python -m unittest

typecheck:
	mypy ./delimiter_check/delimiter_check.py

stylecheck:
	pycodestyle $(style_args) .
