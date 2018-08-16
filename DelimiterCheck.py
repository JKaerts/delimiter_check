import sys
import getopt
import re
from collections import deque
from typing import NamedTuple, Deque

class Match(NamedTuple):
    delimiter: str
    line: int


delimiter_dictionary = {r'(': r')',
                        r'{': r'}',
                        r'[': r']'}
opening_delimiters = delimiter_dictionary.keys()
delimiter_stack: Deque[Match] = deque()

all_delimiters = [item for sublist in delimiter_dictionary.items() for item in sublist]
all_delimiters_regex = [re.escape(delimiter) for delimiter in all_delimiters]

def is_empty(test_deque: Deque) -> bool:
    try:
        a = test_deque[0]
    except IndexError:
        return True
    else:
        return False


def append_to_stack(original: Deque[Match], new: Deque[Match]) -> None:
    while True:
        try:
            new_item = new.popleft()
            if ((not is_empty(original)) and
                    (original[-1][0] in opening_delimiters) and
                    (delimiter_dictionary[original[-1][0]] == new_item[0])):
                original.pop()
            else:
                original.append(new_item)
        except IndexError:
            break


def get_new_matches(line_number: int, line_text: str) -> Deque[Match]:
    matches = re.findall("|".join(all_delimiters_regex), line_text)
    if matches:
        return deque([(match, line_number) for match in matches])
    else:
        return deque()


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

    for match in delimiter_stack:
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