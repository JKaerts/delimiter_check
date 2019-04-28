import unittest
from collections import deque
from Matches import Match, DelimiterStack

class TestDelimiterStack(unittest.TestCase):
    def test_is_empty(self):
        test_stack = DelimiterStack([('(', 1),('[', 2),(']', 2)])
        self.assertFalse(test_stack.is_empty())
        test_stack = DelimiterStack()
        self.assertTrue(test_stack.is_empty())
        
    def test_stack_property(self):
        test_stack = DelimiterStack([('(', 1),('[', 2),(']', 2)])
        self.assertEqual(test_stack.stack, deque([('(', 1),('[', 2),(']', 2)]))
        with self.assertRaises(AttributeError):
            test_stack.stack = deque([('(', 1)])
        
if __name__ == "__main__":
    unittest.main()