#!/usr/bin/env python3

import atoms
import sys
from atoms import Function, Adder, Int, Str
from exceptions import PsilException


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
            raise PsilException('Syntax')

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

    return out


def get_add_paths_and_vals(s):
    add_path = [atoms.LEFT]
    for t in s[1:len(s)]:
        if '(' in t:
            if add_path[-1] == atoms.LEFT:
                yield add_path, t
                add_path.append(atoms.LEFT)  # add_path for next t
            elif add_path[-1] == atoms.RIGHT:
                yield add_path, t
                add_path.append(atoms.LEFT)
        elif t == ')':
            add_path.pop()
            if len(add_path) == 0:
                break  # if it's the last closing paren
            if add_path[-1] == atoms.LEFT:
                add_path[-1] = atoms.RIGHT
            elif add_path[-1] == atoms.RIGHT:
                add_path[-1] = atoms.RIGHT
        else:
            if add_path[-1] == atoms.LEFT:
                yield add_path, t
                add_path[-1] = atoms.RIGHT
            elif add_path[-1] == atoms.RIGHT:
                yield add_path, t


def get_tree(s):
    def get_function(function):
        for func in atoms.functions:
            if func.name == function:
                return func
        raise PsilException('Function \'%s\' does not exist' % function)

    def get_type_of_value(value):
        # Either return Int, Str, or Function
        if value[0] == '"' and value[-1] == '"':
            return atoms.Str
        if value[0] == '\'' or value[-1] == '\'':
            raise PsilException('Use double quotes for strings.')
        if value[0] == '(':
            return atoms.Function
        return atoms.Int

    root_function = get_function(s[0].strip('('))
    root = root_function()
    for find_path, val in get_add_paths_and_vals(s):
        on_node_path = find_path[0:len(find_path) - 1]
        on_node = root.get_item_using_branch_path(on_node_path)

        type_ = get_type_of_value(val)

        if type_ == atoms.Function:
            type_of_function = get_function(val.strip('('))

        direction = find_path[-1]
        if direction == atoms.LEFT:
            if type_ == atoms.Int:
                on_node.add_left(Int(int(val)))
            elif type_ == atoms.Str:
                on_node.add_left(Str(str(val.strip('"'))))
            elif type_ == atoms.Function:
                on_node.add_left(type_of_function())
        elif direction == atoms.RIGHT:
            if type_ == atoms.Int:
                on_node.add_right(Int(int(val)))
            elif type_ == atoms.Str:
                on_node.add_right(Str(str(val.strip('"'))))
            elif type_ == atoms.Function:
                on_node.add_right(type_of_function())

    return root

def is_whitespace(s):
    for c in s:
        if c != ' ':
            return False
    return True

if __name__ == '__main__':
    if len(sys.argv) != 1:
        s = sys.argv[1]
        tree = get_tree(get_tokens(s))
        tree()
        exit()
    try:
        while True:
            try:
                s = input('>> ')
                if is_whitespace(s):
                    continue
                tree = get_tree(get_tokens(s))
                tree()
            except KeyboardInterrupt:
                print()
            except PsilException as e:
                print('*Exception*')
                print(e)
    except EOFError:
        print()
        exit()
