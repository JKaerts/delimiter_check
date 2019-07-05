from collections import deque
from typing import Tuple, Deque


Match = Tuple[str, int]


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

    def popleft(self):
        return self.stack.popleft()

    def pop(self):
        return self.stack.pop()

    def is_empty(self):
        return not bool(self.stack)
