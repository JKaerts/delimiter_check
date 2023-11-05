"""Build script for the project."""
import shutil
import subprocess
import venv
from pathlib import Path

# The directory in which the virtual environment will be stored. Can be
# configured.
VENV_DIRECTORY = 'venv'
venv_binaries = f'.\\{VENV_DIRECTORY}\\Scripts'
interpreter = f'.\\{VENV_DIRECTORY}\\Scripts\\python.exe'


def create_environment():
    """Create a virtual environment in the specified folder."""
    venv.create(VENV_DIRECTORY, with_pip=True)

    subprocess.run(
        [interpreter, '-m', 'pip', 'install', '--upgrade', 'pip-tools'],
        check=True
    )
    subprocess.run(
        [interpreter, '-m', 'pip', 'install', '-r', 'requirements.txt'],
        check=True
    )


def build_wheel():
    """Build a wheel from the sources."""
    subprocess.run([interpreter, '-m', 'build'], check=True)


def run_tests():
    """Run all the tests."""
    subprocess.run([interpreter, '-m', 'unittest', 'discover'], check=True)


def run_mypy():
    """Typecheck the project."""
    subprocess.run(
        [f'{venv_binaries}\\mypy.exe', 'delimiter_check'],
        check=True
    )


def run_lint():
    """Lint the project."""
    subprocess.run(
        [f'{venv_binaries}\\pylint.exe', 'delimiter_check'],
        check=True
    )


def clean():
    """Clean all build artifacts and temporary files."""
    dirs_to_clean = [
        r'.\venv',
        r'.\delimiter_check.egg-info',
        r'.\dist',
        r'.\.mypy_cache'
    ]

    for directory in dirs_to_clean:
        if Path(directory).exists():
            shutil.rmtree(directory)


def main(argv):
    """Main handler function for the build script."""
    if len(argv) != 2:
        print("""
Usage:

    python do.py [command]

where 'command' can be

    venv    Create a virtual environment
    wheel   Build a wheel
    test    Run the tests
    clean   Clean all build artifacts
    mypy    Run the typechecker
    lint    Run the linter
""")
    return
    command = argv[1]
    if command == 'venv':
        create_environment()
    elif command == 'wheel':
        build_wheel()
    elif command == 'test':
        run_tests()
    elif command == 'clean':
        clean()
    elif command == 'mypy':
        run_mypy()
    elif command == 'lint':
        run_lint()
    else:
        print(f"Unknown option {command}")


if __name__ == '__main__':
    import sys
    main(sys.argv)
