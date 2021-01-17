from exceptions import PsilException

LEFT, RIGHT = 'LEFT', 'RIGHT'


class Int:
    def __init__(self, v):
        assert type(v) == int
        self.v = v
        self.r1 = None
        self.r2 = None

    def __call__(self):
        return self.v

class Str:
    def __init__(self, s):
        assert type(s) == str
        self.v = s
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
    len_args = 2
    def __call__(self):
        if type(self.r1) == Int or super(type(self.r2)) == Function:
            pass
        elif type(self.r2) == Int or super(type(self.r2)) == Function:
            pass
        else:
            raise PsilException('All argument types must be Int or Function for function \'%s\'' % type(self).name)

        try:
            self.r1
        except AttributeError:
            raise PsilException('Argument 1 is missing for function \'%s\'' % type(self).name)
        try:
            self.r2
        except AttributeError:
            raise PsilException('Argument 2 is missing for function \'%s\'' % type(self).name)
        return self.r1() + self.r2()

class Subtracter(Function):
    name = 'sub'
    len_args = 2
    def __call__(self):
        if type(self.r1) == Int or super(type(self.r2)) == Function:
            pass
        elif type(self.r2) == Int or super(type(self.r2)) == Function:
            pass
        else:
            raise PsilException('All argument types must be Int or Function for function \'%s\'' % type(self).name)

        try:
            self.r1
        except AttributeError:
            raise PsilException('Argument 1 is missing for function \'%s\'' % type(self).name)
        try:
            self.r2
        except AttributeError:
            raise PsilException('Argument 2 is missing for function \'%s\'' % type(self).name)
        return self.r1() - self.r2()

class Printer(Function):
    name = 'print'
    def __call__(self):
        try:
            self.r1
        except AttributeError:
            raise PsilException('Argument 1 is missing for function \'%s\'' % type(self).name)
        try:
            self.r2
        except AttributeError: pass
        else:
            raise PsilException('Argument 2 is not accepted by the \'%s\' function' % type(self).name)
        print(self.r1())

class Setter(Function):
    name = 'set'

functions = Adder, Subtracter, Printer, Setter
