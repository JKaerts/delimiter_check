from collections import deque
from typing import Tuple, Deque


Match = Tuple[str, int]


class MatchDeque:
    _deque: Deque[Match]

    def __init__(self, match_list=None):
        if match_list is None:
            self._deque = deque()
        else:
            self._deque = deque(match_list)

    @property
    def deque(self):
        return self._deque

    def appendleft(self, new_match: Match):
        self.deque.appendleft(new_match)

    def appendright(self, new_match: Match):
        self.deque.append(new_match)

    def popleft(self):
        return self.deque.popleft()

    def popright(self):
        return self.deque.pop()

    def is_empty(self):
        return not bool(self.deque)

    def __iter__(self):
        return iter(self.deque)

    def __next__(self):
        return next(self.deque)
