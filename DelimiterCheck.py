"""
    DelimiterCheck - A program to chech for delimiter consistency
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

import sys
import getopt
import re
from Matches import Match, MatchDeque, DelimiterPairing


delimiter_list = [(r'(', r')'),
                  (r'{', r'}'),
                  (r'[', r']')]

delim_pairing = DelimiterPairing(delimiter_list)
delimiter_deque: MatchDeque = MatchDeque.from_list(delimiter_list)

# Flatten the dictionary to get a list of all delimiters
all_delimiters_regex = delim_pairing.all_delimiters_regex


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:", ["infile="])
    except getopt.GetoptError:
        print("Incorrect usage.")
        print("python DelimiterCheck.py -i <inputfile>")
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt in ("-i", "--infile"):
                InputFile = arg
            else:
                print("Incorrect usage.")
                print("python DelimiterCheck.py -i <inputfile>")

    # Exit if no input file is provided
    if InputFile == '':
        print("No input file has been provided.")
        sys.exit()

    with open(InputFile) as infile:
        for i, line in enumerate(infile):
            new_matches = delimiter_deque.get_new_matches(i+1, line)
            delimiter_deque.append_other_deque(new_matches)
            
    print(delimiter_deque.report())
