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

DEFAULT_DELIMITERS = [('(', ')'),
                      ('{', '}'),
                      ('[', ']')]

LEFT_DELIMITERS, RIGHT_DELIMITERS = zip(*DEFAULT_DELIMITERS)
ALL_DELIMITERS = LEFT_DELIMITERS + RIGHT_DELIMITERS
DELIMITER_REGEX = [re.escape(delimiter) for delimiter in ALL_DELIMITERS]

class CustomFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
    """
    Formatter for the command line arguments
    """
    pass

def parse_args(args=sys.argv[1:]):
    """Parse arguments"""
    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__,
        formatter_class=CustomFormatter)
    parser.add_argument("-i",
                        metavar="INPUT",
                        dest='input_file',
                        help="the input file. Defaults to stdin if not given.")

    return parser.parse_args(args)

def get_matches_from_line(linenumber, line):
    matches = re.findall("|".join(DELIMITER_REGEX), line)
    if matches:
        return [(match, linenumber) for match in matches]
    return []

def delimiters_match(left, right):
    try:
        index = LEFT_DELIMITERS.index(left)
    except ValueError:
        return False
    else:
        return right == RIGHT_DELIMITERS[index]

def matches_top_of_stack(delimiter, stack):
    return len(stack) != 0 and delimiters_match(stack[-1][0], delimiter)

if __name__ == "__main__":
    delimiters = []
    args = parse_args()
    input_file = args.input_file

    with open(input_file) if input_file is not None else sys.stdin as infile:
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
            print("Line {}: {} unclosed".format(match[1], match[0]))
        else:
            print("Line {}: {} extra".format(match[1], match[0]))
