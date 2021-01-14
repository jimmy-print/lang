#!/usr/bin/env python3

import atoms
import sys
from atoms import Function, Adder, Int
from exceptions import PsilException


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
    root_function = get_function(s[0].strip('('))
    root = root_function()
    for find_path, val in get_add_paths_and_vals(s):
        on_node_path = find_path[0:len(find_path) - 1]
        on_node = root.get_item_using_branch_path(on_node_path)

        try:
            int(val)
        except ValueError:
            is_int = False
        else:
            is_int = True

        type_of_function = None
        if not is_int:
            type_of_function = get_function(val.strip('('))

        direction = find_path[-1]
        if direction == atoms.LEFT:
            on_node.add_left(Int(int(val))) if is_int else on_node.add_left(type_of_function())
        elif direction == atoms.RIGHT:
            on_node.add_right(Int(int(val))) if is_int else on_node.add_right(type_of_function())

    return root


if __name__ == '__main__':
    if len(sys.argv) != 1:
        s = sys.argv[1]
        tree = get_tree(s.strip().split())
        print(tree())
        exit()
    try:
        while True:
            try:
                s = input('>> ')
                if s == '':
                    continue
                tree = get_tree(s.strip().split())
                tree()
            except KeyboardInterrupt:
                print()
            except PsilException as e:
                print(e)
    except EOFError:
        print()
        exit()
