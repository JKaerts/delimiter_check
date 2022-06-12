# SPDX-License-Identifier: GPL-3.0-only

"""A program to check for delimiter consistency in text files.

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

import re
from typing import List, Tuple

DEFAULT_DELIMITERS = [('(', ')'),
                      ('{', '}'),
                      ('[', ']')]

LEFT_DELIMITERS, RIGHT_DELIMITERS = zip(*DEFAULT_DELIMITERS)
ALL_DELIMITERS = LEFT_DELIMITERS + RIGHT_DELIMITERS
DELIMITER_REGEX = [re.escape(delimiter) for delimiter in ALL_DELIMITERS]

Match = Tuple[str, int]


def is_valid_delimiter(delimiter: str) -> bool:
    """
    Check for a given string if it is present in the list of all delimiters.

    >>> is_valid_delimiter('(')
    True
    """
    return delimiter in ALL_DELIMITERS


def get_matches_from_line(number: int, line: str) -> List[Match]:
    """
    Loop through the given line of text in search of delimiters.

    >>> get_matches_from_line(0, '')
    []
    >>> get_matches_from_line(1, 'A (short) text [with {many} delimiters]')
    [('(', 1), (')', 1), ('[', 1), ('{', 1), ('}', 1), (']', 1)]
    """
    matches = re.findall("|".join(DELIMITER_REGEX), line)
    if matches:
        return [(match, number) for match in matches]
    return []


def delimiters_match(left: str, right: str) -> bool:
    """
    Check whether two delimiters match.

    >>> delimiters_match('[', ']')
    True
    >>> delimiters_match(']', '[')
    False
    >>> delimiters_match('[', '}')
    False
    """
    try:
        index = LEFT_DELIMITERS.index(left)
    except ValueError:
        return False
    else:
        return right == RIGHT_DELIMITERS[index]


def matches_top_of_stack(delimiter: str, stack: List[Match]) -> bool:
    """
    Check if a given delimiter cancels out the top of the given list.

    >>> matches_top_of_stack('(', [])
    False
    >>> stack = [(']', 1), ('(', 4)]
    >>> matches_top_of_stack(')', stack)
    True
    >>> matches_top_of_stack('[', stack)
    False
    """
    return len(stack) != 0 and delimiters_match(stack[-1][0], delimiter)


def get_results_from_file(file):
    """
    Read a file and returns nonmatching delimiters with their line numbers.

    >>> from io import StringIO
    >>> file = StringIO('''[a
    ... (b
    ... {c
    ... }d
    ... )e
    ... (f
    ... ]g''')
    >>> get_results_from_file(file)
    [('[', 1), ('(', 6), (']', 7)]
    """
    delimiters = []  # type: List[Match]
    # line numbers start at 1, not at zero
    for i, line in enumerate(file, 1):
        new_matches = get_matches_from_line(i, line)
        for match in new_matches:
            if matches_top_of_stack(match[0], delimiters):
                delimiters.pop()
            else:
                delimiters.append(match)

    return delimiters


def write_results(delimiters, outfile):
    """Write the interpreted results of the program to outfile."""
    for match in delimiters:
        if match[0] in LEFT_DELIMITERS:
            print(
                "Line {}: {} unclosed".format(match[1], match[0]),
                file=outfile)
        else:
            print(
                "Line {}: {} extra".format(match[1], match[0]),
                file=outfile)


def main(argv, stdout):
    """Run the program."""
    input_file = argv[1]
    with open(input_file) as infile:
        delimiters = get_results_from_file(infile)
        write_results(delimiters, stdout)


if __name__ == "__main__":
    def _script_io():
        from sys import argv, stdout

        main(argv, stdout)

    _script_io()
