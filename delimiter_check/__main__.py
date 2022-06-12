# SPDX-FileCopyrightText: 2022 Jonas Kaerts
#
# SPDX-License-Identifier: GPL-3.0-only

from . import main
from sys import argv, stdout


def mainfunc():
    main(argv, stdout)


if __name__ == "__main__":
    mainfunc()
