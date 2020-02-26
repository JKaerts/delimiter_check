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
import sys
from Matches import MatchDeque


DEFAULT_DELIMITERS = [(r'(', r')'),
                      (r'{', r'}'),
                      (r'[', r']')]

class CustomFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
    pass

def parse_args(module, args=sys.argv[1:]):
    """Parse arguments"""
    parser = argparse.ArgumentParser(
        description=sys.modules[module].__doc__,
        formatter_class=CustomFormatter)
    parser.add_argument("-i",
                        metavar="INPUT",
                        dest='input_file',
                        help="the input file. Defaults to stdin if not given.")

    return parser.parse_args(args)

if __name__ == "__main__":
    delimiter_deque: MatchDeque = MatchDeque.from_list(DEFAULT_DELIMITERS)
    args = parse_args(__name__)
    input_file = args.input_file

    with open(input_file) if input_file is not None else sys.stdin as infile:
        # line numbers start at 1, not at zero
        for i, line in enumerate(infile, 1):
            new_matches = delimiter_deque.get_new_matches(i, line)
            delimiter_deque.append_other_deque(new_matches)

    print(delimiter_deque.report())
