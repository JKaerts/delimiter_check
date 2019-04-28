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
from Matches import DelimiterStack


delimiter_dictionary = {r'(': r')',
                        r'{': r'}',
                        r'[': r']'}
opening_delimiters = delimiter_dictionary.keys()
delimiter_stack: DelimiterStack = DelimiterStack()

# Flatten the dictionary to get a list of all delimiters
all_delimiters = [item for sublist in delimiter_dictionary.items() for item in sublist]
all_delimiters_regex = [re.escape(delimiter) for delimiter in all_delimiters]

def append_to_stack(original: DelimiterStack, new: DelimiterStack) -> None:
    while True:
        try:
            new_item = new.stack.popleft()
            if ((not original.is_empty()) and
                    (original.stack[-1][0] in opening_delimiters) and
                    (delimiter_dictionary[original.stack[-1][0]] == new_item[0])):
                original.stack.pop()
            else:
                original.stack.append(new_item)
        except IndexError:
            break


def get_new_matches(line_number: int, line_text: str) -> DelimiterStack:
    matches = re.findall("|".join(all_delimiters_regex), line_text)
    if matches:
        return DelimiterStack([(match, line_number) for match in matches])
    return DelimiterStack()


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

    with open('Chapter1.tex') as infile:
        for i, line in enumerate(infile):
            new_matches = get_new_matches(i+1, line)
            append_to_stack(delimiter_stack, new_matches)

    for match in delimiter_stack.stack:
        if match[0] in opening_delimiters:
            print("Unclosed opening delimiter " +
                  match[0] +
                  " at line " +
                  str(match[1]))
        else:
            print("Superfluous closing delimiter " +
                  match[0] +
                  " at line " +
                  str(match[1]))
