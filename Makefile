# Possible targets:
# - env              Create a virtual environment
# - test             Run the test suite
# - typecheck        Analyze the code with mypy
# - codestyle        Analyze the code with pycodestyle
# - docstyle         Analyze the code with pydocstyle

VENV = venv
SCRIPTS = $(VENV)\Scripts
ACTIVATE = $(VENV)\Scripts\Activate.ps1
PYTHON = $(VENV)\Scripts\python.exe
PIP = $(VENV)\Scripts\pip.exe

env: $(ACTIVATE)

$(ACTIVATE): requirements.txt
	python -m venv "venv"
	$(PIP) install -r requirements.txt

test: $(ACTIVATE)
	$(PYTHON) -m unittest discover

typecheck: $(ACTIVATE)
	$(SCRIPTS)\mypy.exe delimiter_check

analysis: $(ACTIVATE)
	$(SCRIPTS)\pycodestyle.exe delimiter_check
	$(SCRIPTS)\pydocstyle.exe delimiter_check

wheel: $(ACTIVATE)
	$(PYTHON) -m build

