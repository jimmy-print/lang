#!/usr/bin/env python3

import sys
import colorama
import atoms
from atoms import *

NICHT = '('
BACK = ')'

COMMENT_PREFIX = '#'
assert len(COMMENT_PREFIX) == 1

def is_whitespace(s):
    for c in s:
        if c != ' ':
            return False
    return True


def is_comment(s):
    found_hash = False
    for c in s:
        if not found_hash and c != COMMENT_PREFIX and c != ' ':
            return False
        if c == COMMENT_PREFIX:
            found_hash = True
    return True


def is_int(v):
    try:
        int(v)
        return True
    except ValueError:
        return False


def is_str(v):
    """
    Check if a token is a string in 
    """
    # not that v can be converted into a string type,
    # but that it is literally a string in the code file
    # (set name "john")
    if v[0] == '"' and v[-1] == '"':
        return True
    return False


def chomp(s: str, c: str):
    """
    Remove all instances of an unwanted character in a string.
    :param s: the string in which we take out all instances of the unwanted character.
    :param c: the unwanted character. Must be single character string.

    :returns: a copy of s without any instance of the unwanted character.
    """
    out = []
    for C in s:
        if C != c:
            out.append(C)

    return ''.join(out)


def compress_whitespace(s: str):
    """
    Convert consecutive spaces of length greater than 1 into a single space
    :param s: eg. ' 123  34   3 '
    :returns: eg. ' 123 34 3 '
    """

    out = []
    for i, c in enumerate(s):
        tmp = ''
        if i != len(s) - 1:
            tmp = c
            if c == ' ' and s[i + 1] == ' ':
                pass
            else:
                out.append(tmp)

    out.append(s[-1])
    return ''.join(out)


def get_appropriate_function_class(tok):
    for function in functions:
        if tok == function.name:
            return function
    raise RuntimeError(f'{tok} function not found')


def get_tokens(s):
    split = s.strip().split()

    for i, tok in enumerate(split):
        if not is_whitespace(tok):
            split[i] = tok

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

    on_tok = index(tree, 0)

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
            elif is_str(tok):
                on_tok.add(Thing(str(tok.strip('"')), None))
            elif tok[0] == '$':
                on_tok.add(Variable(tok[1:len(tok)]))
            else:
                on_tok.add(Thing(tok, None))

        if tok == NICHT:
            on_tok = index(tree, II + 1)

    return tree


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print('please provide filename')
        exit()

    with open(filename) as f:
        s = f.read().strip()

    exprs = []
    for S in s.split(';'):
        if not is_whitespace(S):
            exprs.append(compress_whitespace(chomp(S.strip(), '\n')))

    variables = {}

    [print(colorama.Fore.CYAN + '\n'+expr, end='') for expr in exprs]
    print(colorama.Style.RESET_ALL)
    print('----\n')

    for line in exprs:
        if is_whitespace(line) or is_comment(line):
            continue

        tokens = get_tokens(line)

        toktok = []
        for tok in tokens:
            if not is_whitespace(tok):
                toktok.append(tok)

        #print(toktok)
        tree = get_tree(toktok)

        #vis_recursive(tree)
        #Node.vis_with_stack(tree)
        
        #print(get_vis_stack_str(tree))
        
        
        #tree(variables)
        #do(tree)
        print(
            atoms._get_with_stack(tree, [0])
        )

        #print()
