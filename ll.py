import sys

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

class Thing(Node):
    def __call__(self):
        return self.v
    
class Adder(Node):
    def __call__(self):
        out = 0
        for node in self.nodes:
            if type(node()) != str:
                out += node()
        return out

NICHT = '('
BACK = ')'
ADD = 'ADD'

def is_int(v):
    try:
        int(v)
        return True
    except ValueError:
        return False

def get_tree(l):
    tokens = l.split()

    tree = Adder(NICHT, None)

    on_tok_i = 0
    on_tok = tree.get(0)

    i = -1
    for _, tok in enumerate(tokens[1:len(tokens)]):
        i += 1
        if tok == BACK:
            # now we change on_tok to the nicht above the on_tok
            on_tok = on_tok.parent

            i -= 1
            continue

        if tok == NICHT:
            on_tok.add(Adder(tok, None))
        else:
            if is_int(tok):
                on_tok.add(Thing(int(tok), None))
            else:
                on_tok.add(Thing(tok, None))

        if tok == NICHT:
            on_tok = tree.get(i + 1)
    return tree

if __name__ == '__main__':
    get_tree('( ADD ( ADD ( ADD 123 23 3 ) ( ADD 1 ( ADD 1 2 3 4 ) 4 ) 23 2 ) 8 2 1 )')()
