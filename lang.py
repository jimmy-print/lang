#!/usr/bin/env python3

import sys
import colorama
from atoms import *

OPENING_BRACKET = '('
CLOSING_BRACKET = ')'

QUOTE_CHAR = '"'

COMMENT_PREFIX = '#'
SIGIL_CHAR_STR = '$'
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
    print(repr(s))
    out.append(s[-1])
    return ''.join(out)

allowed_exposed_chars = [
	'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
	'1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
	'_',
    '.',
]

operator_chars = [
	'+', '-', '*', '/',
	'!',
	'<', '>',
	'$',
    '%',
	'=',
]
def get_tokens(expression):
    processing_a_string = False
    on_last_char = False

    tok = ""
    toks = []
    for i, char in enumerate(expression):
        try:
            next_char = expression[i + 1]
        except IndexError:
            pass
        if i + 1 == len(expression):
            on_last_char = True

        i += 1
        cut_off_tok = False

        if char == QUOTE_CHAR:
            processing_a_string = not processing_a_string

        if processing_a_string:
            tok += char
            if on_last_char:
                raise RuntimeError("unbalanced closing apostrophe")
            if next_char == QUOTE_CHAR:
                tok += QUOTE_CHAR
                cut_off_tok = True
        else:
            if char == OPENING_BRACKET or char == CLOSING_BRACKET:
                tok += char
                cut_off_tok = True
            if char in allowed_exposed_chars:
                tok += char
                if on_last_char:
                    cut_off_tok = True
                else:
                    if next_char not in allowed_exposed_chars:
                        cut_off_tok = True
            if char in operator_chars:
                tok += char
                cut_off_tok = True
        if cut_off_tok:
            toks.append(tok)
            tok = ""
    return toks

def expand_sigil(toks):
    new_toks = []
    next_iter_dont_push = False
    i = 0
    while i < len(toks):
        if toks[i] == SIGIL_CHAR_STR:
            new_toks.append(OPENING_BRACKET)
            new_toks.append(SIGIL_CHAR_STR)
            new_toks.append(f"{QUOTE_CHAR}{toks[i + 1]}{QUOTE_CHAR}")
            new_toks.append(CLOSING_BRACKET)

            i += 2
        else:
            new_toks.append(toks[i])
            i += 1
    return new_toks
            
def get_tree(tokens):
    tree = Root()

    on_tok = index(tree, 0)

    II = -1
    for __, tok in enumerate(tokens):
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

    for n, line in enumerate(exprs):
        tokens = expand_sigil(get_tokens(line))
        tokens_wo_whitespace = filter(lambda token: not is_whitespace(token), tokens)
        tree = get_tree(tokens_wo_whitespace)

        run(tree)
        print()

