# Complete build script for the project
param(
	[switch]$Full = $false,
	[switch]$Test = $false,
	[switch]$Analysis = $false,
	[switch]$Clean = $false
)

$VenvPython = ".\venv\Scripts\python.exe"
$VenvBin = ".\venv\Scripts"

function Do-FullBuild {
	Do-Cleanup
	python -m venv venv
	Invoke-Expression "$VenvPython -m pip install --upgrade pip-tools"
	Invoke-Expression "$VenvPython -m pip install -r requirements.txt"
	Invoke-Expression "$VenvPython -m build"
}

function Do-Test {
	Invoke-Expression "$VenvPython -m unittest discover"
}

function Do-Analysis {
	"Mypy"
	"----"
	Invoke-Expression "$VenvBin\mypy.exe delimiter_check"
	"Pycodestyle"
	"-----------"
	Invoke-Expression "$VenvBin\pycodestyle.exe delimiter_check"
	"Pydocstyle"
	"----------"
	Invoke-Expression "$VenvBin\pydocstyle.exe delimiter_check"
}

function Do-Cleanup {
	if (Test-Path ".\venv") {
		Remove-Item ".\venv" -Recurse
	}
	if (Test-Path ".\delimiter_check.egg-info") {
		Remove-Item ".\delimiter_check.egg-info" -Recurse
	}
	if (Test-Path ".\dist") {
		Remove-Item ".\dist" -Recurse
	}
	if (Test-Path ".\.mypy_cache") {
		Remove-Item ".\.mypy_cache" -Recurse
	}
}

if ($Full) {
	Do-FullBuild
}

if ($Test) {
	Do-Test
}

if ($Analysis) {
	Do-Analysis
}

if ($Clean) {
	Do-Cleanup
}