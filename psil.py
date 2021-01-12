#!/usr/bin/env python3

LEFT, RIGHT = 'LEFT', 'RIGHT'


class Node:
    # node on tree
    def __init__(self, v):
        self.v = v
        self.r1 = None
        self.r2 = None

    def add_left(self, r1):
        self.r1 = r1

    def add_right(self, r2):
        self.r2 = r2

    def __call__(self):
        if self.v == 'A(':
            return self.r1() + self.r2()
        elif type(self.v) == int:
            return self.v

    @staticmethod
    def thru(node):
        """depth first iterate"""
        yield node
        if node.r1 is not None:
            yield from Node.thru(node.r1)
        if node.r2 is not None:
            yield from Node.thru(node.r2)

    @staticmethod
    def thru_vis(node, layer=0, side=None):
        gap = ''
        for _ in range(0, layer):
            gap += ' '
        print('%s %s %s' % (gap, node.v, side))
        layer += 1
        if node.r1 is not None:
            Node.thru_vis(node.r1, layer, side=LEFT)
        if node.r2 is not None:
            Node.thru_vis(node.r2, layer, side=RIGHT)

    def __getitem__(self, item):
        """indexing using depth first search"""
        for i, node in enumerate(Node.thru(self)):
            if i == item:
                return node
        raise IndexError('tree index out of range')

    def get_item_using_branch_path(self, path):
        if path == []:
            return self
        for i in path:
            assert i == LEFT or i == RIGHT or i is None

        tmp_node = self
        for direction in path:
            if direction is None:
                tmp_node = tmp_node
            if direction == LEFT:
                tmp_node = tmp_node.r1
            if direction == RIGHT:
                tmp_node = tmp_node.r2
        return tmp_node


def add_node(root, index, v1, v2):
    to_add_on = root[index]
    assert to_add_on.r1 is None and to_add_on.r2 is None
    to_add_on.add_left(Node(v1))
    to_add_on.add_right(Node(v2))


def add_node_left(root, index, v1):
    to_add_on = root[index]
    assert to_add_on.r1 is None
    to_add_on.add_left(Node(v1))


def add_node_right(root, index, v2):
    to_add_on = root[index]
    assert to_add_on.r2 is None
    to_add_on.add_right(Node(v2))


add_path = [LEFT]
def get_add_paths_and_vals(s):
    for t in s[1:len(s)]:
        if t == 'A(':
            if add_path[-1] == LEFT:
                yield add_path, t
                add_path.append(LEFT)  # add_path for next t
            elif add_path[-1] == RIGHT:
                yield add_path, t
                add_path.append(LEFT)
        elif t == ')':
            add_path.pop()
            if len(add_path) == 0:
                break  # if it's the last closing paren
            if add_path[-1] == LEFT:
                add_path[-1] = RIGHT
            elif add_path[-1] == RIGHT:
                add_path[-1] = RIGHT
        else:
            if add_path[-1] == LEFT:
                yield add_path, t
                add_path[-1] = RIGHT
            elif add_path[-1] == RIGHT:
                yield add_path, t


def get_tree(s):
    root = Node(s[0])
    for find_path, val in get_add_paths_and_vals(s):
        on_node_path = find_path[0:len(find_path) - 1]
        on_node = root.get_item_using_branch_path(on_node_path)

        is_int = None
        try:
            int(val)
        except ValueError:
            is_int = False
        else:
            is_int = True

        direction = find_path[-1]
        if direction == LEFT:
            on_node.add_left(Node(int(val))) if is_int else on_node.add_left(Node(val))
        elif direction == RIGHT:
            on_node.add_right(Node(int(val))) if is_int else on_node.add_right(Node(val))

    return root


tree = get_tree(input('Enter expression: ').strip().split())
print(tree())