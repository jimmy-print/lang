import ll
import unittest

class Test(unittest.TestCase):
    def setUp(self):
        self.tests = {
            '(add 1 2)': 3,
            '(add (add 34 2) (add 1 -100))': -63,
            '(add (add (add 123 23 3) (add 1 (add 1 2 3 4) 4) 23 2) 8 2 -1)': 198,
            '(add (sub (sub 2 3) (add 4 5)) 1 2 3 (sub 3 4))': -5,
            '(add 1 (add 2 (sub 3 4)) 2)': 4,

        }

    def test_all_lines(self):
        for expr in self.tests:
            print(expr)
            self.assertEqual(ll.get_tree(ll.get_tokens(expr))(), self.tests[expr])

if __name__ == '__main__':
    unittest.main()
