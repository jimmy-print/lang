import sys

class Node:
    def __init__(self, v):
        self.v = v
        self.nodes = []

    def append(self, v):
        self.nodes.append(v)

    @staticmethod
    def vis(n, layer=0):
        gap = ''
        for _ in range(layer):
            gap += '-'
        print(gap, n.v, sep='')
        for node in n.nodes:
            if node is not None:
                Node.vis(node, layer+1)

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


class Foo:
    def __repr__(self):
        return 'O'


if __name__ == '__main__':
    line = '(add (addd (adddd 123 2 ) 34 ) (addddd 1 (adddddd 23 5 ) ) )'
    tokens = line.split()
#    print(tokens)

    i = 0
    root = Node('(add')

