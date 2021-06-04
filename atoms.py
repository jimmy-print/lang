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
    def __call__(self):
        return self.v


class Adder(Node):
    # the name class field is the function name.
    # add function must thus be called by (add x y z ...)
    name = 'add'

    def __call__(self):
        out = 0
        for node in self.nodes:
            if type(node()) != str:
                out += node()
        return out


class Subtracter(Node):
    name = 'sub'
    expected_args_len = 2

    def __call__(self):
        if len(self.nodes) != type(
                self).expected_args_len + 1:  # + 1, because the nodes include the function name as a string
            raise RuntimeError('sub function takes exactly two arguments')
        return self.nodes[1]() - self.nodes[2]()


class Printer(Node):
    name = 'print'
    expected_args_len = 1

    def __call__(self):
        if len(self.nodes) != type(self).expected_args_len + 1:
            raise RuntimeError('print function takes exactly 1 argument')
        print(self.nodes[1]())


class If(Node):
    name = 'if'

    def __call__(self):
        if self.nodes[1]() == True:
            assert type(self.nodes[2]) == Exelist
            self.nodes[2]()


class Equals(Node):
    name = 'eq'

    def __call__(self):
        if self.nodes[1]() == self.nodes[2]():
            return True
        return False


class Exelist(Node):
    name = 'exelist'

    def __call__(self):
        for node in self.nodes:
            node()
            # TODO: implement returning


class Root(Node):
    # returns the return value of its first node. it should only have one son node.
    def __call__(self):
        assert len(self.nodes) == 1
        return self.nodes[0]()

functions = Adder, Subtracter, Printer, Exelist, If, Equals
