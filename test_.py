import ll
from ll import *
import unittest

class TestGetTree(unittest.TestCase):
    def setUp(self):
        self.tests = {
            '(+ 1 2)': 3,
            '(+ (+ 34 2) (+ 1 -100))': -63,
            '(+ (+ (+ 123 23 3) (+ 1 (+ 1 2 3 4) 4) 23 2) 8 2 -1)': 198,
            '(+ (- (- 2 3) (+ 4 5)) 1 2 3 (- 3 4))': -5,
            '(+ 1 (+ 2 (- 3 4)) 2)': 4,

        }

    def test_all_lines(self):
        for expr in self.tests:
            result = ll.get_tree(ll.get_tokens(expr))({})
            #print(f'expr: {expr}, result: {result}')
            self.assertEqual(result, self.tests[expr])

class CompareRecursiveToStack(unittest.TestCase):
    def setUp(self):
        files_to_test = ['prime.la, format.la, new.what']
        big_str = []
        for file in files_to_test:
            with open('prime.la') as f:
                s = f.read().strip()
                big_str.append(s)
        big_str = ''.join(big_str)
        exprs = []
        for S in big_str.split(';'):
            if not is_whitespace(S):
                exprs.append(compress_whitespace(chomp(S.strip(), '\n')))
        
        self.trees = [] 
        for line in exprs:
            if is_whitespace(line) or is_comment(line):
                continue
            
            tokens = get_tokens(line)

            toktok = []
            for tok in tokens:
                if not is_whitespace(tok):
                    toktok.append(tok)

            tree = get_tree(toktok)
            self.trees.append(tree)

    def test_vis_strs_same(self):
        for tree in self.trees:
            self.assertEqual(get_vis_stack_str(tree), get_vis_recursive_str(tree, 0, in_testing=True))

    def test_thru_same(self):
        for tree in self.trees:
            self.assertEqual(list(thru(tree)), list(Node._thru(tree, in_testing=True)))

if __name__ == '__main__':
    unittest.main()
