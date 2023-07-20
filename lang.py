#!/usr/bin/env python3

import sys
import colorama
from atoms import *

OPENING_BRACKET = '('
CLOSING_BRACKET = ')'

COMMENT_PREFIX = '#'
assert len(COMMENT_PREFIX) == 1


def is_whitespace(s):
    for c in s:
        if c != ' ':
            return False
    return True


def is_int(v):
    try:
        int(v)
        return True
    except ValueError:
        return False


def is_str(v):
    """
    Check if a token is a string in Lang.
    :param s: A token, e.g. '(', '"name"', '12'.
    :returns: True if 
    """
    # not that v can be converted into a string type,
    # but that it is literally a string in the code file
    # (set name "john")
    if v[0] == '"' and v[-1] == '"':
        return True
    return False


def rm_char_instances(s: str, c: str):
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
            raise LangError(
                'Opening and closing brackets must be attached without spaces '
                'to functions and last arguments, respectively.')

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
        if OPENING_BRACKET in tok:
            outout.append(OPENING_BRACKET)
            outout.append(tok[1:len(tok)])
        else:
            outout.append(tok)

    return outout


def get_tree(tokens):
    tree = Root()

    on_tok = index(tree, 0)

    II = -1
    for i, tok in enumerate(tokens):
        II += 1
        if tok == CLOSING_BRACKET:
            # now we change on_tok to the nicht above the on_tok
            on_tok = on_tok.parent

            II -= 1

            continue

        if tok == OPENING_BRACKET:
            on_tok.add(Node(tok, None))
        else:
            if is_int(tok):
                on_tok.add(Data(int(tok), None))
            elif is_str(tok):
                on_tok.add(Data(str(tok.strip('"')), None))
            else:
                on_tok.add(Node(tok, None))

        if tok == OPENING_BRACKET:
            on_tok = index(tree, II + 1)

    return tree


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print('Please provide a filename!')
        exit(0)

    with open(filename) as f:
        raw_code_w_o_front_back_whitespace = f.read().strip()

    raw_exprs = raw_code_w_o_front_back_whitespace.split(';')

    # When the last expression is followed by a semicolon, the list returned
    # by s.split(';') has an empty string as its last value. This value, if
    # present, must be removed as it fucks up the compress_whitespace function.
    if raw_exprs[-1] == '':
        raw_exprs.pop()

    exprs = []
    for raw_expr in raw_exprs:
        no_newlines = rm_char_instances(raw_expr, '\n')
        also_no_redundant_spaces = compress_whitespace(no_newlines)
        exprs.append(also_no_redundant_spaces)

    for line in exprs:
        print(line)

        tokens = get_tokens(line)

        toktok = []
        for tok in tokens:
            if not is_whitespace(tok):
                toktok.append(tok)

        tree = get_tree(toktok)

        print(f'Top-level return: {do(tree)}')
        print()
