import subprocess
import sys


def show_help():
    print('''Build targets
  help        - Show this message
  test        - Run the test suite
  typecheck   - Run mypy to check the typing of the project
  stylecheck  - Use pycodestyle to check pep8-compliance
''')


if len(sys.argv) == 1:
    show_help()
    sys.exit()

arg = sys.argv[1]

if arg == 'help':
    show_help()
elif arg == 'test':
    subprocess.run(['python', '-m', 'unittest', 'discover', '-v'])
elif arg == 'typecheck':
    subprocess.run(['mypy', 'delimiter_check'])
elif arg == 'stylecheck':
    subprocess.run(['pycodestyle', '.'])
