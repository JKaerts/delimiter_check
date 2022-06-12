# SPDX-FileCopyrightText: 2022 Jonas Kaerts
#
# SPDX-License-Identifier: GPL-3.0-only

# Possible targets:
# - env              Create a virtual environment
# - test             Run the test suite
# - typecheck        Analyze the code with mypy
# - codestyle        Analyze the code with pycodestyle
# - docstyle         Analyze the code with pydocstyle
# - wheel            Make the wheel file
# - clean            Clean all temporary files

VENV = venv
BIN = $(VENV)\Scripts
ACTIVATE = $(VENV)\Scripts\Activate.ps1
PYTHON = $(VENV)\Scripts\python.exe
PIP = $(VENV)\Scripts\pip.exe
deletefolder = IF EXIST $(1) (rd /s /q $(1))

# 'env' is an easy to type alias for the activate script
env: $(ACTIVATE)

$(ACTIVATE): requirements.txt
	python -m venv "venv"
	$(PIP) install -r requirements.txt

test: $(ACTIVATE)
	$(PYTHON) -m unittest discover

typecheck: $(ACTIVATE)
	$(BIN)\mypy.exe delimiter_check

codestyle: $(ACTIVATE)
	$(BIN)\pycodestyle.exe delimiter_check

docstyle: $(ACTIVATE)
	$(BIN)\pydocstyle.exe delimiter_check

wheel: $(ACTIVATE)
	$(PYTHON) -m build

clean:
	$(call deletefolder, .mypy_cache)
	$(call deletefolder, delimiter_check.egg-info)
	$(call deletefolder, dist)
	$(call deletefolder, venv)
