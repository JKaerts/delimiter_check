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
from Matches import MatchDeque
from collections import deque


DEFAULT_DELIMITERS = [(r'(', r')'),
                      (r'{', r'}'),
                      (r'[', r']')]

LEFT_DELIMITERS, RIGHT_DELIMITERS = zip(*DEFAULT_DELIMITERS)
ALL_DELIMITERS = LEFT_DELIMITERS + RIGHT_DELIMITERS
DELIMITER_REGEX = [re.escape(delimiter) for delimiter in ALL_DELIMITERS]

class CustomFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
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
        return deque([(match, linenumber) for match in matches])

def delimiters_match(left, right):
    try:
        index = LEFT_DELIMITERS.index(left)
    except ValueError:
        return False
    else:
        return right == RIGHT_DELIMITERS[index]

if __name__ == "__main__":
    my_deque = deque()
    delimiter_deque: MatchDeque = MatchDeque.from_list(DEFAULT_DELIMITERS)
    args = parse_args()
    input_file = args.input_file

    with open(input_file) if input_file is not None else sys.stdin as infile:
        for i, line in enumerate(infile, 1):
            new_matches = get_matches_from_line(i, line)
            for match in new_matches:
                if len(my_deque) != 0 and delimiters_match(my_deque[-1], match):
                    my_deque.pop()
                else:
                    my_deque.append(match)

    for match in my_deque:
        if match[0] in LEFT_DELIMITERS:
            print(f"Unclosed opening delimiter {self.delim} at line {self.line}")
        else:
            print(f"Superfluous closing delimiter {self.delim} at line {self.line}")

    with open(input_file) if input_file is not None else sys.stdin as infile:
        # line numbers start at 1, not at zero
        for i, line in enumerate(infile, 1):
            new_matches = delimiter_deque.get_new_matches(i, line)
            delimiter_deque.append_other_deque(new_matches)

    print(delimiter_deque.report())
