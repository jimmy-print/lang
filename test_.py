import lang
from lang import *
import unittest
import atoms

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

class TestCalculatorStyleExpressionEvaluation(unittest.TestCase):
    def setUp(self):
        self.tests = {
            '(* (* 3 4) (* 2 3) 3 4 5 6 7)': 181440,
            '(* (* (* (* 1 2 3) 1 (/ 45 (+ 1 2 3))) 4 5) (+ 2 3))': 4500,
            '(/ (/ (+ (- (* 2 3 (- 4 5)) (* 1 2 3)) (+ 1 2)) 2) 3)': -1.5
        }

    def test_all_lines(self):
        for expr in self.tests:
            result = lang.do(lang.get_tree(lang.get_tokens(expr)))
            #print(f'expr: {expr}, result: {result}')
            self.assertEqual(result, self.tests[expr])

def reset_vardict_and_run_expr(expr):
    atoms.global_variables = {}
    return do(get_tree(get_tokens(expr)))

class TestVariables(unittest.TestCase):
    def test_value_exists_and_is_equal(self):
        reset_vardict_and_run_expr('(set "a" 1)')
        self.assertDictEqual(
            atoms.global_variables,
            {'a': 1}
        )

    def test_value_can_be_changed(self):
        reset_vardict_and_run_expr('(set "a" 1)')
        reset_vardict_and_run_expr('(set "a" 2)')
        self.assertDictEqual(
            atoms.global_variables,
            {'a': 2}
        )

    def test_int_value_can_be_read(self):
        reset_vardict_and_run_expr('(set "a" 1)')
        res = do(get_tree(get_tokens('($ "a")')))
        self.assertEqual(res, 1)

    def test_str_value_can_be_read(self):
        reset_vardict_and_run_expr('(set "a" "b")')
        res = do(get_tree(get_tokens('($ "a")')))
        self.assertEqual(res, "b")


class TestIf(unittest.TestCase):
    def test_positive(self):
        reset_vardict_and_run_expr('''
(if 1
    (set "a" 1))''')
        self.assertDictEqual(atoms.global_variables, {'a': 1})

    def test_negative(self):
        reset_vardict_and_run_expr('''
(if 0
    (set "a" 1))''')
        self.assertDictEqual(atoms.global_variables, {})

    def test_nested(self):
        reset_vardict_and_run_expr('''
(if 1
    (if 1
        (set "a" 1)))''')
        self.assertDictEqual(atoms.global_variables, {'a': 1})
        reset_vardict_and_run_expr('''
(if 1
    (if 0
        (set "a" 1)))''')
        self.assertDictEqual(atoms.global_variables, {})
        reset_vardict_and_run_expr('''
(if 0
    (if 1
        (set "a" 1)))''')
        self.assertDictEqual(atoms.global_variables, {})


if __name__ == '__main__':
    unittest.main()
