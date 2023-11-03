$VenvPython = ".\venv\Scripts\python.exe"

# Creation of the virtual environment is an expensive operation.
# It needs to be built if it doesn't yet exist or if the requirements
# file is more recent (and hence the dependencies need an update)
$createVenv = (-not (Test-Path ".\venv")) `
	-or ( `
		(Get-Item ".\venv").CreationTime `
		-lt `
		(Get-Item ".\requirements.txt").LastWriteTime `
	)

if ($createVenv) {
	python -m venv venv
	Invoke-Expression "$VenvPython -m pip install --upgrade pip-tools"
	Invoke-Expression "$VenvPython -m pip install -r requirements.txt"
}

Invoke-Expression "$VenvPython -m build"