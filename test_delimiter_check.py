"""Tests for the delimiter_check script"""
from io import StringIO
import unittest

from delimiter_check import delimiters_match, \
    get_matches_from_line, \
    get_results_from_file, \
    is_valid_delimiter, \
    matches_top_of_stack


class TestReadingFile(unittest.TestCase):
    def test_correct_results(self):
        file = StringIO('[a\n(b\n{c\n}d\n)e\n(f\n]g')
        self.assertEqual(
            [('[', 1), ('(', 6), (']', 7)],
            get_results_from_file(file))


class TestStackMatching(unittest.TestCase):
    def test_empty_stack_returns_false(self):
        self.assertFalse(matches_top_of_stack('(', []))

    def test_matches_correct_delimiter(self):
        # A ']' has been found on line 1 and a '(' has been found on line 4
        current_matches = [(']', 1), ('(', 4)]
        new_delimiter = ')'
        self.assertTrue(matches_top_of_stack(
            delimiter=new_delimiter,
            stack=current_matches))

    def test_delimiters_must_have_right_order(self):
        # A '(' has been found on line 1 and a ']' has been found on line 4
        current_matches = [('(', 1), (']', 4)]
        new_delimiter = '['
        self.assertFalse(matches_top_of_stack(
            delimiter=new_delimiter,
            stack=current_matches))


if __name__ == '__main__':
    unittest.main()
