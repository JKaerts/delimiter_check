import unittest
from Matches import Match, DelimiterStack

class TestDelimiterStack(unittest.TestCase):
    def test_is_empty(self):
        test_stack = DelimiterStack([('(', 1),('[', 2),(']', 2)])
        self.assertFalse(test_stack.is_empty())
        test_stack = DelimiterStack()
        self.assertTrue(test_stack.is_empty())
        
        
if __name__ == "__main__":
    unittest.main()