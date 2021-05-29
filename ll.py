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
        if len(self.nodes) != type(self).expected_args_len + 1:  # + 1, because the nodes include the function name as a string
            raise RuntimeError('sub function takes exactly two arguments')
        return self.nodes[1]() - self.nodes[2]()

class Printer(Node):
    name = 'print'
    expected_args_len = 1
    def __call__(self):
        if len(self.nodes) != type(self).expected_args_len + 1:
            raise RuntimeError('print function takes exactly 1 argument')
        print(self.nodes[1]())

class Root(Node):
    # returns the return value of its first node. it should only have one son node.
    def __call__(self):
        return self.nodes[0]()

NICHT = '('
BACK = ')'

def is_int(v):
    try:
        int(v)
        return True
    except ValueError:
        return False


functions = Adder, Subtracter, Printer
def get_appropriate_function_class(tok):
    for function in functions:
        if tok == function.name:
            return function
    raise RuntimeError(f'{tok} function not found')


def get_tokens(s):
    split = s.strip().split()
    def remove_all_instances_of_right_paren(string):
        out = []
        for c in string:
            if c != ')':
                out.append(c)
        return ''.join(out)

    out = []

    # Check if (add 1 1 ) or ( add 1 1) or ( add 1 1 )
    for tok in split:
        if tok == ')' or tok == '(':
            raise RuntimeError('Syntax')

    for tok in split:
        if ')' not in tok:
            out.append(tok)
        else:
            out.append(remove_all_instances_of_right_paren(tok))
            len_of_right_paren = 0
            for c in tok:
                if c == ')':
                    len_of_right_paren += 1
            for _ in range(len_of_right_paren):
                out.append(')')

    outout = []
    for tok in out:
        if NICHT in tok:
            outout.append(NICHT)
            outout.append(tok[1:len(tok)])
        else:
            outout.append(tok)

    return outout


def get_tree(tokens):
    tree = Root('ROOT', None)

    on_tok = tree.get(0)

    II = -1
    for i, tok in enumerate(tokens):
        II += 1
        if tok == BACK:
            # now we change on_tok to the nicht above the on_tok
            on_tok = on_tok.parent

            II -= 1

            continue

        if tok == NICHT:
            # scan the one forward tok to determine appropriate function
            function_class = get_appropriate_function_class(tokens[i + 1])
            on_tok.add(function_class(tok, None))
        else:
            if is_int(tok):
                on_tok.add(Thing(int(tok), None))
            else:
                on_tok.add(Thing(tok, None))

        if tok == NICHT:
            on_tok = tree.get(II + 1)

    return tree


if __name__ == '__main__':
    s = '(print (add 2 3 4 45))'
    tokens = get_tokens(s)
    tree = get_tree(tokens)
    tree()