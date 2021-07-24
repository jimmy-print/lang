#!/usr/bin/env python3

import sys
from atoms import *

NICHT = '('
BACK = ')'

def is_int(v):
    try:
        int(v)
        return True
    except ValueError:
        return False


def get_appropriate_function_class(tok):
    for function in functions:
        if tok == function.name:
            return function
    raise RuntimeError(f'{tok} function not found')


def get_tokens(s):
    split = s.strip().split()
    def remove_all_instances_of_right_paren(string):
        out = []
        for c in string:
            if c != ')':
                out.append(c)
        return ''.join(out)

    out = []

    # Check if (add 1 1 ) or ( add 1 1) or ( add 1 1 )
    for tok in split:
        if tok == ')' or tok == '(':
            raise RuntimeError('Syntax')

    for tok in split:
        if ')' not in tok:
            out.append(tok)
        else:
            out.append(remove_all_instances_of_right_paren(tok))
            len_of_right_paren = 0
            for c in tok:
                if c == ')':
                    len_of_right_paren += 1
            for _ in range(len_of_right_paren):
                out.append(')')

    outout = []
    for tok in out:
        if NICHT in tok:
            outout.append(NICHT)
            outout.append(tok[1:len(tok)])
        else:
            outout.append(tok)

    return outout


def get_tree(tokens):
    tree = Root('ROOT', None)

    on_tok = tree.get(0)

    II = -1
    for i, tok in enumerate(tokens):
        II += 1
        if tok == BACK:
            # now we change on_tok to the nicht above the on_tok
            on_tok = on_tok.parent

            II -= 1

            continue

        if tok == NICHT:
            # scan the one forward tok to determine appropriate function
            function_class = get_appropriate_function_class(tokens[i + 1])
            on_tok.add(function_class(tok, None))
        else:
            if is_int(tok):
                on_tok.add(Thing(int(tok), None))
            else:
                on_tok.add(Thing(tok, None))

        if tok == NICHT:
            on_tok = tree.get(II + 1)

    return tree


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print('please provide filename')
        exit()

    with open(filename) as f:
        s = f.read().strip()

    for line in s.split('\n'):
        tokens = get_tokens(line)
        tree = get_tree(tokens)
        tree()
