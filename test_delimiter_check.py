from delimiter_check import *
import unittest


class TestMatching(unittest.TestCase):
    def test_parentheses_match(self):
        self.assertTrue(delimiters_match(left='(', right=')'))

    def test_braces_match(self):
        self.assertTrue(delimiters_match(left='{', right='}'))

    def test_brackets_match(self):
        self.assertTrue(delimiters_match(left='[', right=']'))

    def test_order_matters(self):
        self.assertFalse(delimiters_match(left=')', right='('))
        self.assertFalse(delimiters_match(left='}', right='{'))
        self.assertFalse(delimiters_match(left=']', right='['))


class TestLineParsing(unittest.TestCase):
    def test_empty_line_returns_empty_list(self):
        self.assertEqual([], get_matches_from_line(number=0, line=""))

    def test_all_matches_are_delimiters(self):
        line_text = "A (short) text [with {many} delimiters]"
        found_matches = get_matches_from_line(number=0, line=line_text)
        found_delimiters, _ = zip(*found_matches)

        self.assertTrue(all([delimiter in ALL_DELIMITERS for delimiter in found_delimiters]))

    def test_finds_delimiters_in_order(self):
        line_text = "A (short) text [with {many} delimiters]"
        expected_delimiters = ['(', ')', '[', '{', '}', ']']
        found_matches = get_matches_from_line(number=0, line=line_text)
        found_delimiters, _ = zip(*found_matches)

        self.assertEqual(expected_delimiters, list(found_delimiters))

    def test_found_matches_contains_line_number(self):
        line_text = "A (short) text [with {many} delimiters]"
        found_matches = get_matches_from_line(number=4, line=line_text)
        _, found_linenumbers = zip(*found_matches)

        self.assertTrue(all([number == 4 for number in found_linenumbers]))


class TestStackMatching(unittest.TestCase):
    def test_empty_stack_returns_false(self):
        self.assertFalse(matches_top_of_stack('(', []))

    def test_matches_correct_delimiter(self):
        # A ']' has been found on line 1 and a '(' has been found on line 4
        current_matches = [(']', 1), ('(', 4)]
        new_delimiter = ')'
        self.assertTrue(matches_top_of_stack(delimiter=new_delimiter, stack=current_matches))

    def test_delimiters_must_have_right_order(self):
        # A '(' has been found on line 1 and a ']' has been found on line 4
        current_matches = [('(', 1), (']', 4)]
        new_delimiter = '['
        self.assertFalse(matches_top_of_stack(delimiter=new_delimiter, stack=current_matches))


if __name__ == '__main__':
    unittest.main()
