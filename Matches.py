class Match(NamedTuple):
    """
    Container class which keeps a pair of a delimiter and the line number
    on which it was found
    """
    delimiter: str
    line: int