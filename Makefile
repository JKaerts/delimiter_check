help:
	@echo 'Possible targets:'
	@echo 'help'
	@echo 'env'
	@echo 'test'
	@echo 'test-verbose'
	@echo 'typecheck'
	@echo 'codestyle'
	@echo 'docstyle'

env:
	python -m venv "venv"

test:
	python -m unittest discover

test-verbose:
	python -m unittest discover -v

typecheck:
	mypy delimiter_check

codestyle:
	pycodestyle delimiter_check

docstyle:
	pydocstyle delimiter_check
	