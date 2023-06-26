import colorama

INDEX_TOO_BIG = 'INDEX_TOO_BIG'
NO_NODES = 'NO_NODES'

def dupe(s, n):
    out = []
    for _ in range(n):
        out += s
    return ''.join(out)


def _get_with_stack(root_node, stack):
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
        node = _get_with_stack(root_node, stack)
        yield (len(stack), node)

        stack.append(0)
        if issubclass(type(_get_with_stack(root_node, stack)), Node):
            continue
        elif _get_with_stack(root_node, stack) == NO_NODES:
            stack.pop()

        stack[-1] += 1
        while _get_with_stack(root_node, stack) == INDEX_TOO_BIG and stack != [1]:
            stack.pop()
            stack[-1] += 1

        if stack == [1]:
            break

def get_vis_stack_str(root_node):
    out = []
    for elem in thru_giving_depth(root_node):
        out.append('|'+dupe('-', elem[0])+str(elem[1].v)+'\n')
    return ''.join(out)


# Do not use the recursive functions except for testing.
def get_vis_recursive_str(node, layer=0, in_testing=False):
    if not in_testing:
        raise DeprecationWarning('Do not use recursive functions.')
    def __(node, layer=0):
        if layer == 0:
            yield'|' + dupe('-', layer) + str(node.v) + '\n'

        for NODE in node.nodes:
            yield '|' + dupe('-', layer + 1) + str(NODE.v) + '\n'
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


class Node:  # aka Function
    def __init__(self, v, parent):
        self.v = v
        self.nodes = []
        self.parent = parent

    def __repr__(self):
        return f'val: {self.v}, type: {type(self)}'

    def add(self, v):
        v.parent = self
        self.nodes.append(v)

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


class Thing(Node):
    def __call__(self, variables):
        return self.v


class Modulo(Node):
    name = '%'

    def __call__(self, variables):
        return self.nodes[1](variables) % self.nodes[2](variables)

class Adder(Node):
    # the name class field is the function name.
    # add function must thus be called by (add x y z ...)
    name = '+'

    def __call__(self, variables):
        out = 0
        for i, node in enumerate(self.nodes[1:len(self.nodes)]):
            val = node(variables)
            if type(val) != str:
                out += val
            else:
                raise ValueError(f'argument #{i} to add function does not return int')
        return out


class Subtracter(Node):
    name = '-'
    expected_args_len = 2

    def __call__(self, variables):
        if len(self.nodes) != type(
                self).expected_args_len + 1:  # + 1, because the nodes include the function name as a string
            raise RuntimeError('sub function takes exactly two arguments')
        return self.nodes[1](variables) - self.nodes[2](variables)


class Printer(Node):
    name = 'print'
    expected_args_len = 1

    def __call__(self, variables):
        to_print = self.nodes[1](variables).format(
            *[node(variables) for node in self.nodes[2:len(self.nodes)]]
        )
        print(to_print)


class If(Node):
    name = 'if'

    def __call__(self, variables):
        assert type(self.nodes[2]) == Exelist

        if self.nodes[1](variables) is True:
            self.nodes[2](variables)


class While(Node):
    name = 'while'

    def __call__(self, variables):
        assert type(self.nodes[2]) == Exelist

        while self.nodes[1](variables) is True:
            self.nodes[2](variables)


class Equals(Node):
    name = '='

    def __call__(self, variables):
        if self.nodes[1](variables) == self.nodes[2](variables):
            return True
        return False


class Lesser(Node):
    name = '<'

    def __call__(self, variables):
        val0 = self.nodes[1](variables)
        val1 = self.nodes[2](variables)

        assert type(val0) == int and type(val1) == int

        return val0 < val1


class Not(Node):
    name = '!'

    def __call__(self, variables):
        val = self.nodes[1](variables)
        assert (val is True) or (val is False)
        return not val


class Int(Node):
    name = 'int'

    def __call__(self, variables):
        return int(self.nodes[1](variables))


class Input(Node):
    name = 'input'

    def __call__(self, variables):
        return input(self.nodes[1](variables))


class Variable:
    def __init__(self, s):
        assert type(s) == str
        self.v = s
        self.nodes = []

    def __call__(self, variables):
        return variables[self.v]
    
    def __repr__(self):
        return f'val: {self.v}, type: {type(self)}'
    

class Setter(Node):
    name = 'set'

    def __call__(self, variables):
        variables[self.nodes[1](variables)] = self.nodes[2](variables)


class Exelist(Node):
    name = '{'

    def __call__(self, variables):
        for node in self.nodes:
            node(variables)
            # TODO: implement returning


class Root(Node):
    # returns the return value of its first node. it should only have one son node.
    def __call__(self, variables):
        assert len(self.nodes) == 1
        return self.nodes[0](variables)
    
class VarOther(Node):
    name = 'var'

    def __call__(self, variables):
        return variables[self.nodes[1].v]

functions = Adder, Subtracter, Printer, Exelist, If, Equals, Input, Setter, Not, Int, Modulo, While, Lesser, VarOther
