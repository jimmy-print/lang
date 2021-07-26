class Node:  # aka Function
    def __init__(self, v, parent):
        self.v = v
        self.nodes = []
        self.parent = parent

    def add(self, v):
        v.parent = self
        self.nodes.append(v)

    @staticmethod
    def vis(n, layer=0):
        gap = ''
        for _ in range(layer):
            gap += ' '
            print(gap, n.v)
        for node in n.nodes:
            if node is not None:
                Node.vis(node, layer + 1)

    @staticmethod
    def thru(n):
        yield n
        for node in n.nodes:
            if node is not None:
                yield from Node.thru(node)

    def get(self, index):
        for i, node in enumerate(Node.thru(self)):
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
        if len(self.nodes) != type(self).expected_args_len + 1:
            raise RuntimeError('print function takes exactly 1 argument')
        print(self.nodes[1](variables))


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
        assert self.nodes[1](variables) is True or self.nodes[1](variables) is False
        return not self.nodes[1](variables)


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

class Setter(Node):
    name = 'set'

    def __call__(self, variables):
        variables[self.nodes[1](variables)] = self.nodes[2](variables)


class Exelist(Node):
    name = 'exelist'

    def __call__(self, variables):
        for node in self.nodes:
            node(variables)
            # TODO: implement returning


class Root(Node):
    # returns the return value of its first node. it should only have one son node.
    def __call__(self, variables):
        assert len(self.nodes) == 1
        return self.nodes[0](variables)

functions = Adder, Subtracter, Printer, Exelist, If, Equals, Input, Setter, Not, Int, Modulo, While, Lesser