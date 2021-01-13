LEFT, RIGHT = 'LEFT', 'RIGHT'


class Int:
    """End nodes on a tree"""
    def __init__(self, v):
        assert type(v) == int
        self.v = v
        self.r1 = None
        self.r2 = None

    def __call__(self):
        return self.v


class Function:
    """Not end nodes"""
    def __init__(self):
        self.v = NotImplemented

    def add_left(self, r1):
        self.r1 = r1

    def add_right(self, r2):
        self.r2 = r2

    def __call__(self):
        raise NotImplementedError

    @staticmethod
    def thru(node):
        """depth first iterate"""
        yield node
        if node.r1 is not None:
            yield from Function.thru(node.r1)
        if node.r2 is not None:
            yield from Function.thru(node.r2)

    @staticmethod
    def thru_vis(node, layer=0, side=None):
        gap = ''
        for _ in range(0, layer):
            gap += ' '
        print('%s %s' % (gap, node.v))
        layer += 1
        if node.r1 is not None:
            Function.thru_vis(node.r1, layer, side=LEFT)
        if node.r2 is not None:
            Function.thru_vis(node.r2, layer, side=RIGHT)

    def __getitem__(self, item):
        """indexing using depth first search"""
        for i, node in enumerate(Function.thru(self)):
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


class Adder(Function):
    name = 'add'
    def __call__(self):
        return self.r1() + self.r2()

class Subtracter(Function):
    name = 'sub'
    def __call__(self):
        return self.r1() - self.r2()

functions = Adder, Subtracter
