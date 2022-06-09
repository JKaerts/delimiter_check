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
delete = IF EXIST $(1) (rd /s /q $(1))

# 'env' is an easy to type alias for the activate script
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

clean:
	$(call delete, .mypy_cache)
	$(call delete, delimiter_check.egg-info)
	$(call delete, dist)
	$(call delete, venv)
