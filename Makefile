# Possible targets:
# - env              Create a virtual environment
# - dep              Install all dependencies
# - test             Run the test suite
# - typecheck        Analyze the code with mypy
# - codestyle        Analyze the code with pycodestyle
# - docstyle         Analyze the code with pydocstyle

env:
	python -m venv "venv"

dep:
	pip install -r requirements.txt

test:
	python -m unittest discover

typecheck:
	mypy delimiter_check

codestyle:
	pycodestyle delimiter_check

docstyle:
	pydocstyle delimiter_check
