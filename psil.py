#!/usr/bin/env python3

LEFT, RIGHT = 'LEFT', 'RIGHT'
LEFT_FUNC, RIGHT_FUNC = 'LEFT_FUNC', 'RIGHT_FUNC'
class Atom:
    def __init__(self, val):
        assert type(val) == int
        self.v = val
    def __call__(self):
        return self.v

class Add:
    def __init__(self, *args):
        self.args = args
    def __call__(self):
        sum = 0
        for arg in self.args:
            sum += arg()
        return sum

class Node:
    # node on tree
    def __init__(self, v):
        self.v = v
        self.r1 = None
        self.r2 = None
        self.been = False
    def add_left(self, r1):
        self.r1 = r1
    def add_right(self, r2):
        self.r2 = r2

    @staticmethod
    def thru(node):
        '''depth first iterate'''
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
        '''indexing using depth first search'''
        for i, node in enumerate(Node.thru(self)):
            if i == item:
                return node
        raise IndexError('tree index out of range')

    def get_item_using_branch_path(self, path):
        assert path != []
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

root_test = Node(0)
add_node(root_test, 0, 1, 2)
add_node(root_test, 1, 3, 4)
add_node(root_test, 4, 5, 6)
#Node.thru_vis(root_test)
assert root_test.get_item_using_branch_path([RIGHT, LEFT]).v == 5

string = input()
s = string.split()
add_path = [None]
add_paths = []
def get_add_paths_and_vals(s):
    for t in s[1:len(s)]:
        if t == 'A(':
            if add_path[-1] == None:
                add_path.append(LEFT_FUNC)
            elif add_path[-1] == LEFT_FUNC or add_path[-1] == LEFT:
                add_path.pop()
                add_path.append(RIGHT_FUNC)
        elif t == ')':
            add_path.pop()
            continue
        else:
            if add_path[-1] == LEFT_FUNC or add_path[-1] == RIGHT_FUNC or add_path[-1] == None:
                add_path.append(LEFT)
            elif add_path[-1] == LEFT:
                add_path.pop()
                add_path.append(RIGHT)
        yield add_path, t

def get_converted_add_paths_and_vals(s):
    # convert LEFT_FUNC and RIGHT_FUNC to LEFT and RIGHT
    for add_path, t in get_add_paths_and_vals(s):
        new = []
        for path in add_path:
            if path == LEFT_FUNC:
                new.append(LEFT)
            elif path == RIGHT_FUNC:
                new.append(RIGHT)
            else:
                new.append(path)
        yield new, t

def get_tree(s):
    root = Node(s[0])
    for find_path, val in get_converted_add_paths_and_vals(s):
        on_node_path = find_path[0:len(find_path)-1]
        on_node = root.get_item_using_branch_path(on_node_path)

        direction = find_path[-1]
        if direction == LEFT:
            on_node.add_left(Node(val))
        elif direction == RIGHT:
            on_node.add_right(Node(val))

    return root

Node.thru_vis(get_tree(s))
