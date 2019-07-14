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


@dataclass
class Match:
    ''' A Match is a type variable standing for tuple of a string and an integer.
        The string stands for the delimiter found and the integer stands for
        the line on which the delimiter was found.
    '''
    delim: str
    line: int


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

            >>> matches = MatchDeque()
            >>> matches.appendleft(('{', 1))
            >>> matches.appendleft(('[', 5))
            >>> matches.deque
            deque([('[', 5), ('{', 1)])
        '''
        self.deque.appendleft(new_match)

    def appendright(self, new_match: Match):
        ''' Appends a new element to the right of the deque.

            >>> matches = MatchDeque()
            >>> matches.appendright(('{', 1))
            >>> matches.appendright(('[', 5))
            >>> matches.deque
            deque([('{', 1), ('[', 5)])
        '''
        self.deque.append(new_match)

    def popleft(self):
        ''' Removes and returns the leftmost element of the deque.

            >>> matches = MatchDeque([('{', 1), ('[', 5)])
            >>> result = matches.popleft()
            >>> result
            ('{', 1)
            >>> matches.deque
            deque([('[', 5)])
        '''
        return self.deque.popleft()

    def popright(self):
        ''' Removes and returns the rightmost element of the deque.

            >>> matches = MatchDeque([('{', 1), ('[', 5)])
            >>> result = matches.popright()
            >>> result
            ('[', 5)
            >>> matches.deque
            deque([('{', 1)])
        '''
        return self.deque.pop()

    def is_empty(self):
        ''' Checks if the deque is empty.

            >>> matches1 = MatchDeque([('(', 1), ('[', 2), (']', 2)])
            >>> matches1.is_empty()
            False
            >>> matches2 = MatchDeque()
            >>> matches2.is_empty()
            True
        '''
        return not bool(self.deque)
        
    def append_other_deque(self, other):
        while True:
            try:
                new_item = other.popleft()
                if ((not self.is_empty()) and
                        (self.deque[-1].delim in self.delim_table.opening_delimiters) and
                        (self.delim_table._dict[self.deque[-1].delim] == new_item.delim)):
                    self.popright()
                else:
                    self.appendright(new_item)
            except IndexError:
                break
                
    def report(self):
        report_str = ""
        for match in self.deque:
            if match.delim in self.delim_table.opening_delimiters:
                report_str += f"Unclosed opening delimiter {match.delim} at line {match.line}\n"
            else:
                report_str += f"Superfluous closing delimiter {match.delim} at line {match.line}\n"
        return report_str

    def __iter__(self):
        return iter(self.deque)

    def __next__(self):
        return next(self.deque)


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
