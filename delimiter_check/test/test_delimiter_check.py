# SPDX-FileCopyrightText: 2022 Jonas Kaerts
#
# SPDX-License-Identifier: GPL-3.0-only

"""Tests for the delimiter_check script"""
import unittest

from delimiter_check.delimiter_check import matches_top_of_stack


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
