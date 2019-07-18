from __future__ import annotations
import re
from collections import deque
from dataclasses import dataclass
from typing import Tuple, Deque, Dict


class DelimiterPairing:
    def __init__(self, correspondence_list):
        self._dict = dict(correspondence_list)
        self._opening_delimiters = DelimiterPairing.gen_opening_delimiters(self._dict)
        self._all_delimiters = DelimiterPairing.gen_all_delimiters(self._dict)
        self._all_delimiters_regex = DelimiterPairing.gen_all_delimiters_regex(self._dict)

    @staticmethod
    def gen_opening_delimiters(delim_dict):
        return delim_dict.keys()

    @staticmethod
    def gen_all_delimiters(delim_dict):
        return [item for sublist in delim_dict.items() for item in sublist]

    @staticmethod
    def gen_all_delimiters_regex(delim_dict):
        delimiters = DelimiterPairing.gen_all_delimiters(delim_dict)
        return [re.escape(delimiter) for delimiter in delimiters]

    @property
    def opening_delimiters(self):
        return self._opening_delimiters

    @property
    def all_delimiters(self):
        return self._all_delimiters

    @property
    def all_delimiters_regex(self):
        return self._all_delimiters_regex

    def are_compatible(self, first: str, second: str) -> bool:
        ''' Checks if the arguments first and second form a valid pair
            of delimiters.
        '''
        try:
            return self._dict[first] == second
        except KeyError:
            return False


@dataclass
class Match:
    ''' A Match is a type variable standing for tuple of a string and an integer.
        The string stands for the delimiter found and the integer stands for
        the line on which the delimiter was found.
    '''
    delim: str
    line: int

    def report(self, opening: bool):
        if opening:
            return f"Unclosed opening delimiter {self.delim} at line {self.line}"
        else:
            return f"Superfluous closing delimiter {self.delim} at line {self.line}"


class MatchDeque:
    _deque: Deque[Match]
    _delim_table: DelimiterPairing

    def __init__(self, delim_table, match_list=None):
        if match_list is None:
            self._deque = deque()
        else:
            self._deque = deque(match_list)
        self._delim_table = delim_table

    @classmethod
    def from_list(cls, delim_list, match_list=None):
        return MatchDeque(DelimiterPairing(delim_list), match_list)

    @property
    def deque(self):
        return self._deque

    @property
    def delim_table(self):
        return self._delim_table

    def appendleft(self, new_match: Match):
        ''' Appends a new element to the left of the deque.

            >>> matches = MatchDeque.from_list([('(', ')'), ('[', ']'), ('{', '}')])
            >>> matches.appendleft(('{', 1))
            >>> matches.appendleft(('[', 5))
            >>> matches.deque
            deque([('[', 5), ('{', 1)])
        '''
        self.deque.appendleft(new_match)

    def appendright(self, new_match: Match):
        ''' Appends a new element to the right of the deque.

            If the delimiter of the new element matches the rightmost one
            in the deque, they annihilate.
            Otherwise, just add it to the end.

            >>> matches = MatchDeque.from_list([('(', ')'), ('[', ']'), ('{', '}')])
            >>> matches.appendright(Match('{', 1))
            >>> matches.appendright(Match('[', 5))
            >>> matches.deque
            deque([Match(delim='{', line=1), Match(delim='[', line=5)])
            >>> matches.appendright(Match(']', 7))
            >>> matches.deque
            deque([Match(delim='{', line=1)])
        '''
        try:
            final_delim = self.deque[-1].delim
            new_delim = new_match.delim
            if self.delim_table.are_compatible(final_delim, new_delim):
                self.popright()
            else:
                self.deque.append(new_match)
        except IndexError:
            self.deque.append(new_match)

    def popleft(self):
        ''' Removes and returns the leftmost element of the deque.

            >>> matches = MatchDeque.from_list([('(', ')'), ('[', ']'), ('{', '}')],
            ...                                [Match('{', 1), Match('[', 5)])
            >>> result = matches.popleft()
            >>> result
            Match(delim='{', line=1)
            >>> matches.deque
            deque([Match(delim='[', line=5)])
        '''
        return self.deque.popleft()

    def popright(self):
        ''' Removes and returns the rightmost element of the deque.

            >>> matches = MatchDeque.from_list([('(', ')'), ('[', ']'), ('{', '}')],
            ...                                [Match('{', 1), Match('[', 5)])
            >>> result = matches.popright()
            >>> result
            Match(delim='[', line=5)
            >>> matches.deque
            deque([Match(delim='{', line=1)])
        '''
        return self.deque.pop()

    def is_empty(self):
        ''' Checks if the deque is empty.

            >>> matches1 = MatchDeque.from_list([('(', ')'), ('[', ']'), ('{', '}')],
            ...                                 [Match('(', 1), Match('[', 2), Match(']', 2)])
            >>> matches1.is_empty()
            False
            >>> matches2 = MatchDeque([('(', ')'), ('[', ']'), ('{', '}')])
            >>> matches2.is_empty()
            True
        '''
        return not bool(self.deque)

    def get_new_matches(self, line_number: int, line_text: str) -> MatchDeque:
        regex = self.delim_table.all_delimiters_regex
        matches = re.findall("|".join(regex), line_text)
        if matches:
            return MatchDeque(self.delim_table, [Match(match, line_number) for match in matches])
        return MatchDeque(self.delim_table)

    def append_other_deque(self, other):
        for new_item in other:
            self.appendright(new_item)

    def report(self):
        report_strings = [match.report(match.delim in self.delim_table.opening_delimiters) for match in self.deque]
        return '\n'.join(report_strings)

    def __iter__(self):
        return iter(self.deque)

    def __next__(self):
        return next(self.deque)


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
