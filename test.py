import lang
import unittest

class TestReturnValues(unittest.TestCase):
    # and also test that the expression evaluates without errors
    def setUp(self):
        self.tests = {
            "(add 1 2)": 3,
            "(add (add 34 2) (add -1 100))": 135,
            "(add (add (add 123 2) 34) (add 1 (add 23 5)))": 188,
            "(sub (sub (add 1 2) 49) 12)": -58,
            "(equals 1 1)": 1,
            "(equals 1 0)": 0,
            "(equals (add 2 3) (sub 10 5))": 1,
            "(equals \"asdf\" \"asdf\")": 1,
            "(print 1)": None,
            "(print \"test\")": None,
            "(print (add 1 1))": None,
        }

    def test_all_lines(self):
        for expr in self.tests:
            self.assertEqual(lang.get_tree(lang.get_tokens(expr))({}), self.tests[expr])

if __name__ == '__main__':
    unittest.main()
