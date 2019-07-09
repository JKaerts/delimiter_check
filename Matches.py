from collections import deque
from typing import Tuple, Deque

''' A Match is a type variable standing for tuple of a string and an integer.
    The string stands for the delimiter found and the integer stands for
    the line on which the delimiter was found.
'''
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

    def __iter__(self):
        return iter(self.deque)

    def __next__(self):
        return next(self.deque)


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
