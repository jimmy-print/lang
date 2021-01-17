from exceptions import PsilException

LEFT, RIGHT = 'LEFT', 'RIGHT'


class Int:
    name = 'int'
    def __init__(self, v):
        assert type(v) == int
        self.v = v
        self.r1 = None
        self.r2 = None

    def __call__(self):
        return self.v

class Str:
    name = 'str'
    def __init__(self, s):
        assert type(s) == str
        self.v = s
        self.r1 = None
        self.r2 = None

    def __call__(self):
        return self.v


class Function:
    """Not end nodes"""
    name = NotImplemented
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
    arglist_spec = Int, Int
    def __call__(self):
        try: self.r1
        except AttributeError:
            raise PsilException('Arg 1 does not exist for function \'%s\'' % type(self).name)
        try: self.r2
        except AttributeError:
            raise PsilException('Arg 2 does not exist for function \'%s\'' % type(self).name)

        if type(self.r1) == Function:
            pass
        else:
            if type(self.r1) == type(self).arglist_spec[0]:
                pass
            else:
                raise PsilException(
                    'Arg 1 should be type \'%s\', but it is type \'%s\''
                    % (type(self).arglist_spec[0].name, type(self.r1).name))
        if type(self.r2) == Function:
            pass
        else:
            if type(self.r2) == type(self).arglist_spec[1]:
                pass
            else:
                raise PsilException(
                    'Arg 2 should be type \'%s\', but it is type \'%s\''
                    % (type(self).arglist_spec[1].name, type(self.r2).name))

        return self.r1() + self.r2()

class Subtracter(Function):
    name = 'sub'
    len_args = 2
    arglist_spec = Int, Int
    def __call__(self):
        try: self.r1
        except AttributeError:
            raise PsilException('Arg 1 does not exist for function \'%s\'' % type(self).name)
        try: self.r2
        except AttributeError:
            raise PsilException('Arg 2 does not exist for function \'%s\'' % type(self).name)

        if type(self.r1) == Function:
            pass
        else:
            if type(self.r1) == type(self).arglist_spec[0]:
                pass
            else:
                raise PsilException(
                    'Arg 1 for function \'%s\' should be type \'%s\', but it is type \'%s\''
                    % (type(self).name, type(self).arglist_spec[0].name, type(self.r1).name))
        if type(self.r2) == Function:
            pass
        else:
            if type(self.r2) == type(self).arglist_spec[1]:
                pass
            else:
                raise PsilException(
                    'Arg 2 for function \'%s\' should be type \'%s\', but it is type \'%s\''
                    % (type(self).name, type(self).arglist_spec[1].name, type(self.r2).name))

        return self.r1() - self.r2()

class Printer(Function):
    name = 'print'
    len_args = 1
    arglist_spec = None
    def __call__(self):
        try: self.r1
        except AttributeError:
            raise PsilException('Arg 1 does not exist for function \'%s\'' % type(self).name)
        print(self.r1())

class Setter(Function):
    name = 'set'

functions = Adder, Subtracter, Printer, Setter
