"""
    delimiter_check - A program to check for delimiter consistency
    in text files.
    Copyright (C) 2018  Jonas Kaerts

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import re
import sys
from typing import List, Tuple

DEFAULT_DELIMITERS = [('(', ')'),
                      ('{', '}'),
                      ('[', ']')]

LEFT_DELIMITERS, RIGHT_DELIMITERS = zip(*DEFAULT_DELIMITERS)
ALL_DELIMITERS = LEFT_DELIMITERS + RIGHT_DELIMITERS
DELIMITER_REGEX = [re.escape(delimiter) for delimiter in ALL_DELIMITERS]

Match = Tuple[str, int]


class CustomFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
    """
    Formatter for the command line arguments
    """
    pass


def parse_args(args):
    """Parse arguments"""
    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__,
        formatter_class=CustomFormatter)
    parser.add_argument("-i",
                        metavar="INPUT",
                        dest='input_file',
                        help="the input file. Defaults to stdin if not given.")

    return parser.parse_args(args)


def get_matches_from_line(number: int, line: str) -> List[Match]:
    matches = re.findall("|".join(DELIMITER_REGEX), line)
    if matches:
        return [(match, number) for match in matches]
    return []


def delimiters_match(left: str, right: str) -> bool:
    try:
        index = LEFT_DELIMITERS.index(left)
    except ValueError:
        return False
    else:
        return right == RIGHT_DELIMITERS[index]


def matches_top_of_stack(delimiter: str, stack: List[Match]) -> bool:
    return len(stack) != 0 and delimiters_match(stack[-1][0], delimiter)


def main(argv, stdin, stdout):
    delimiters = []  # type: List[Match]
    if len(argv) > 1:
        input_file = argv[1]
    else:
        input_file = stdin

    with open(input_file) as infile:
        # line numbers start at 1, not at zero
        for i, line in enumerate(infile, 1):
            new_matches = get_matches_from_line(i, line)
            for match in new_matches:
                if matches_top_of_stack(match[0], delimiters):
                    delimiters.pop()
                else:
                    delimiters.append(match)

    for match in delimiters:
        if match[0] in LEFT_DELIMITERS:
            print(
                "Line {}: {} unclosed".format(match[1], match[0]),
                file=stdout)
        else:
            print(
                "Line {}: {} extra".format(match[1], match[0]),
                file=stdout)


if __name__ == "__main__":
    main(sys.argv, sys.stdin, sys.stdout)
