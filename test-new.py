import ll
import unittest

class Test(unittest.TestCase):
    def setUp(self):
        self.tests = {
            '( ADD 1 2 )': 3,
            '( ADD ( ADD 34 2 ) ( ADD 1 -100 ) )': -63,
            '( ADD ( ADD ( ADD 123 23 3 ) ( ADD 1 ( ADD 1 2 3 4 ) 4 ) 23 2 ) 8 2 -1 )': 198,
        }

    def test_all_lines(self):
        for expr in self.tests:
            self.assertEqual(ll.get_tree(expr)(), self.tests[expr])

if __name__ == '__main__':
    unittest.main()
