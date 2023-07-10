from copy import deepcopy

INDEX_TOO_BIG = 'INDEX_TOO_BIG'
NO_NODES = 'NO_NODES'

DEPTH_CHAR = '_'


def dupe(s, n):
    out = []
    for _ in range(n):
        out += s
    return ''.join(out)

def get_with_stack(root_node, stack):
    node = root_node
    for i in stack:
        if i >= len(node.nodes) and len(node.nodes) > 0:
            return INDEX_TOO_BIG
        elif not node.nodes:
            return NO_NODES
        node = node.nodes[i]
    return node

def thru_giving_depth(root_node):
    yield (0, root_node)
    stack = [0]
    while True:
        node = get_with_stack(root_node, stack)
        yield (len(stack), node)

        stack.append(0)
        if issubclass(type(get_with_stack(root_node, stack)), Node):
            continue
        elif get_with_stack(root_node, stack) == NO_NODES:
            stack.pop()

        stack[-1] += 1
        while get_with_stack(root_node, stack) == INDEX_TOO_BIG and stack != [1]:
            stack.pop()
            stack[-1] += 1

        if stack == [1]:
            break

def get_vis_stack_str(root_node):
    out = []
    for elem in thru_giving_depth(root_node):
        out.append('|'+dupe(DEPTH_CHAR, elem[0])+str(elem[1].v)+'\n')
    return ''.join(out)


# Do not use the recursive functions except for testing.
def get_vis_recursive_str(node, layer=0, in_testing=False):
    if not in_testing:
        raise DeprecationWarning('Do not use recursive functions.')
    def __(node, layer=0):
        if layer == 0:
            yield'|' + dupe(DEPTH_CHAR, layer) + str(node.v) + '\n'

        for NODE in node.nodes:
            yield '|' + dupe(DEPTH_CHAR, layer + 1) + str(NODE.v) + '\n'
            yield from __(NODE, layer + 1)
    return ''.join(__(node, 0))


def thru(root_node):
    for elem in thru_giving_depth(root_node):
        yield elem[1]

def index(root_node, i):
    for ii, node in enumerate(thru(root_node)):
        if ii == i:
            return node
    raise IndexError('tree index not found (out of range?)')


def get_function(c):
    if c == '+':
        return sum
    elif c == '-':
        def _subtract(iterable):
            if len(iterable) != 2:
                raise TypeError('subtraction is done on 2 numbers.')
            return iterable[0] - iterable[1]
        return _subtract
    elif c == '*':
        def _multiply(iterable):
            result = 1
            for arg in iterable:
                result *= arg
            return result
        return _multiply
    elif c == '/':
        def _divide(iterable):
            if len(iterable) != 2:
                raise TypeError('division is done on 2 numbers.')
            return iterable[0] / iterable[1]
        return _divide
    elif c == 'print':
        def _print(iterable):
            format_string = iterable[0]
            print(format_string.format(*iterable[1:]))
            return None
        return _print
    elif c == '=':
        return lambda iterable: iterable[0] == iterable[1]
    elif c == 'input':
        def _input(iterable):
            format_string = iterable[0]
            return input(format_string.format(*iterable[1:]))
        return _input

    elif c == 'if':
        return lambda iterable: None

    print(f'===LANG ERROR: Your function \'{c}\' is not implemented.===')
    exit(1)


def do(root_node):
    elems_with_OPENING_BRACKET = list(thru_giving_depth(root_node))
    elems_with_OPENING_BRACKET.pop(0)

    # Restructure elems to be without OPENING_BRACKET.
    # (
    #  +
    #  1
    #  2
    # becomes..
    # +
    #  1
    #  2
    # Note that the operation is being done on the 2D list form of these ASTs,
    # not on the node objects themselves.
    elems = []
    for i, elem in enumerate(elems_with_OPENING_BRACKET):
        if i == 0 or len(elems_with_OPENING_BRACKET[i - 1][1].nodes) == 0:
            if len(elem[1].nodes) > 0:
                elem[1].v = elems_with_OPENING_BRACKET[i + 1][1].v
            elems.append(elem)

    # Reconstruct an AST, after restructuring the elems to not have OPENING_BRACKET nodes.
    tree = Node('ROOT', None)
    tree.add(Node(elems[0][1].v, None))
    node = tree.nodes[0]
    past_layer = elems[0][0]
    for elem in elems[1:]:
        if elem[0] > past_layer:
            new_node = Node(elem[1].v, None)
            node.add(new_node)
        elif elem[0] == past_layer:
            new_node = Node(elem[1].v, None)
            node.parent.add(new_node)
        elif elem[0] < past_layer:
            gap = past_layer - elem[0]
            new_node = Node(elem[1].v, None)
            for _ in range(gap):
                node = node.parent
            node.parent.add(new_node)
        node = new_node
        past_layer = elem[0]

    # Execute on the AST.
    stack = [0]
    stop = False
    while not stop:
        stack.append(0)
        if issubclass(type(get_with_stack(tree, stack)), Node):
            continue
        elif get_with_stack(tree, stack) == NO_NODES:
            stack.pop()

        stack[-1] += 1

        while get_with_stack(tree, stack) == INDEX_TOO_BIG and stack != [1]:
            last_arg_node_stack = list(stack)
            last_arg_node_stack[-1] -= 1

            last_arg_node = get_with_stack(tree, last_arg_node_stack)
            parent_func_node = last_arg_node.parent

            f = get_function(parent_func_node.v)

            for node in parent_func_node.nodes:
                assert len(node.nodes) == 0

            args = [node.v for node in parent_func_node.nodes]

            # Find the parent ifs, if there are any.
            if_nodes = []
            st = deepcopy(last_arg_node_stack)
            st.pop()
            while get_with_stack(tree, st).v != 'ROOT':
                n = get_with_stack(tree, st)
                if n.v == 'if' and n is not parent_func_node:
                    # TODO figure out whether object comparison should be done with == or is.
                    if_nodes.append((list(st), n))
                st.pop()

            # Determine if the current parent_func_node is part of the first
            # argument of its closest IF parent.
            parent_func_node_stack = list(last_arg_node_stack)
            parent_func_node_stack.pop()

            is_base = None
            is_first_arg = None

            if not if_nodes:
                is_base = True
            else:
                closest_if_stack = list(if_nodes[0][0])
                closest_if_arg_one_stack = list(closest_if_stack)
                closest_if_arg_one_stack.append(0)

                for i, elem in enumerate(closest_if_arg_one_stack):
                    if elem != parent_func_node_stack[i]:
                        is_first_arg = False
                        break
                else:
                    is_first_arg = True

            if is_base or is_first_arg:
                r = f(args)
            else:
                all_true = all(elem[1].nodes[0].v for elem in if_nodes)
                if all_true:
                    r = f(args)
                else:
                    r = None

            parent_func_node.v = r
            parent_func_node.nodes = []

            stack.pop()
            stack[-1] += 1

        if stack == [1]:
            stop = True

    assert len(tree.nodes) == 1
    return tree.nodes[0].v

class Node:
    def __init__(self, v, parent):
        assert type(v) != Node and type(v) != Data
        self.v = v
        self.nodes = []
        self.parent = parent

    def __repr__(self):
        return f' *{self.v}, {type(self)}* '

    def add(self, n):
        n.parent = self
        self.nodes.append(n)

    @staticmethod
    def _thru(n, in_testing=False):
        if not in_testing:
            raise DeprecationWarning
        yield n
        for node in n.nodes:
            if node is not None:
                yield from Node._thru(node, in_testing)

    def get(self, index, in_testing=False):
        if not in_testing:
            raise DeprecationWarning
        for i, node in enumerate(Node._thru(self, in_testing)):
            if i == index:
                return node
        raise IndexError('tree index not found (out of range?)')

class Data(Node): pass
