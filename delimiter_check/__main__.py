# SPDX-FileCopyrightText: 2022 Jonas Kaerts
#
# SPDX-License-Identifier: GPL-3.0-only
"""The code executed when running the module with 'python -m'."""

from . import main
from sys import argv, stdout


def mainfunc():
    """Run the program."""
    main(argv, stdout)


if __name__ == "__main__":
    mainfunc()
