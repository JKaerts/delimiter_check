#! /bin/bash

set -e

full=false
test=false
analysis=false
clean=false

while test $# -gt 0
do
	case "$1" in
		--full) full=true
			;;
		--test) test=true
			;;
		--analysis) analysis=true
			;;
		--clean) clean=true
			;;
	esac
	shift
done

venvpython="./venv/bin/python3"
venvbin="./venv/bin"

do_full_build () {
	do_cleanup
	python3 -m venv venv
	$venvpython -m pip install --upgrade pip-tools
	$venvpython -m pip install -r requirements.txt
	$venvpython -m build
}

do_test () {
	$venvpython -m unittest discover
}

do_analysis () {
	echo "Mypy"
	echo "----"
	$venvbin/mypy delimiter_check
	echo "Pycodestyle"
	echo "-----------"
	$venvbin/pycodestyle delimiter_check
	echo "Pydocstyle"
	echo "----------"
	$venvbin/pydocstyle delimiter_check
}

do_cleanup () {
	if [[ -d "./venv" ]]
	then
		rm -rf "./venv"
	fi
	
	if [[ -d "./delimiter_check.egg-info" ]]
	then
		rm -rf "./delimiter_check.egg-info"
	fi
	
	if [[ -d "./dist" ]]
	then
		rm -rf "./dist"
	fi
	
	if [[ -d "./mypy_cache" ]]
	then
		rm -rf "./mypy_cache"
	fi
}

if $full
then
	do_full_build
fi

if $test
then
	do_test
fi

if $analysis
then
	do_analysis
fi

if $clean
then
	do_cleanup
fi

exit 0
