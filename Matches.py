from collections import deque
from typing import NamedTuple, Deque


class Match(NamedTuple):
    """
    Container class which keeps a pair of a delimiter and the line number
    on which it was found
    """
    delimiter: str
    line: int


class DelimiterStack:
    _stack: Deque[Match]

    def __init__(self, match_list=None):
        if match_list is None:
            self._stack = deque()
        else:
            self._stack = deque(match_list)

    @property
    def stack(self):
        return self._stack

    def is_empty(self):
        return not bool(self.stack)
