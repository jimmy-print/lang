#!/usr/bin/env python3

import atoms
from atoms import Function, Adder, Int


def get_add_paths_and_vals(s):
    add_path = [atoms.LEFT]
    for t in s[1:len(s)]:
        if t == 'ADD(':
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
    root = Adder()
    for find_path, val in get_add_paths_and_vals(s):
        on_node_path = find_path[0:len(find_path) - 1]
        on_node = root.get_item_using_branch_path(on_node_path)

        try:
            int(val)
        except ValueError:
            is_int = False
        else:
            is_int = True

        direction = find_path[-1]
        if direction == atoms.LEFT:
            on_node.add_left(Int(int(val))) if is_int else on_node.add_left(Adder())
        elif direction == atoms.RIGHT:
            on_node.add_right(Int(int(val))) if is_int else on_node.add_right(Adder())

    return root


if __name__ == '__main__':
    try:
        while True:
            s = input('>> ')
            if s == '':
                continue
            tree = get_tree(s.strip().split())
            print('Answer: %s' % tree())
    except EOFError:
        print()
        exit()
