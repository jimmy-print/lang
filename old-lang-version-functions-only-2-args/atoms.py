from exceptions import LangException

LEFT, RIGHT = 'LEFT', 'RIGHT'


class Int:
    name = 'int'
    def __init__(self, v):
        assert type(v) == int
        self.v = v
        self.r1 = None
        self.r2 = None

    def __call__(self, variables):  # Int does not need access to variables, but it simplifies
        # the code, since all calls to self.r1() or self.r2() can be just self.r*(variables)
        return self.v

class Str:
    name = 'str'
    def __init__(self, s):
        assert type(s) == str
        self.v = s
        self.r1 = None
        self.r2 = None

    def __call__(self, variables):
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

        # TODO show function name since Function.v is NotImplemented
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
    # This function accepts two parameters, both of which can only be integers.

    def __call__(self, variables):
        try:
            self.r1
        except AttributeError:
            raise LangException(f'Argument 1 does not exist for function {type(self).name}')
        try:
            self.r2
        except AttributeError:
            raise LangException(f'Argument 2 does not exist for function {type(self).name}')

        # Potential speed issue here. To type check, every parameter is evaluated before being evaluated again.
        # Instead the program can save self.r1() (for instance) to a variable, then for return self.r1() ...,
        # just put return r1 + r2. TODO
        if type(self.r1(variables)) != int:
            raise LangException(f'Argument 1 must be Int for function {type(self).name}')
        if type(self.r2(variables)) != int:
            raise LangException(f'Argument 2 must be Int for function {type(self).name}')

        return self.r1(variables) + self.r2(variables)

class Subtracter(Function):
    name = 'sub'

    def __call__(self, variables):
        try:
            self.r1
        except AttributeError:
            raise LangException(f'Argument 1 does not exist for function {type(self).name}')
        try:
            self.r2
        except AttributeError:
            raise LangException(f'Argument 2 does not exist for function {type(self).name}')

        # Potential speed issue here. To type check, every parameter is evaluated before being evaluated again.
        # Instead the program can save self.r1() (for instance) to a variable, then for return self.r1() ...,
        # just put return r1 + r2. TODO
        if type(self.r1(variables)) != int:
            raise LangException(f'Argument 1 must be str for function {type(self).name}')
        if type(self.r2(variables)) != int:
            raise LangException(f'Argument 2 must be str for function {type(self).name}')

        return self.r1(variables) - self.r2(variables)

class Printer(Function):
    name = 'print'
    len_args = 1
    arglist_spec = None
    def __call__(self, variables):
        try: self.r1
        except AttributeError:
            raise LangException('Arg 1 does not exist for function \'%s\'' % type(self).name)

        print(self.r1(variables))

class Equals(Function):
    name = 'equals'
    len_args = 2

    def __call__(self, variables):
        try:
            self.r1
        except AttributeError:
            raise LangException(f'Argument 1 does not exist for function {type(self).name}')
        try:
            self.r2
        except AttributeError:
            raise LangException(f'Argument 2 does not exist for function {type(self).name}')

        if self.r1(variables) == self.r2(variables):
            return 1
        return 0

class Variable:
    name = 'var'
    def __init__(self, s):
        assert type(s) == str
        self.v = s
        self.r1 = None
        self.r2 = None

    def __call__(self, variables):
        return variables[self.v]

class VariableNameValuePair:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

class Setter(Function):
    name = 'set'
    def __call__(self, variables):
        try:
            self.r1
        except AttributeError:
            raise LangException('Arg 1 does not exist for function \'%s\'' % type(self).name)
        try:
            self.r2
        except AttributeError:
            raise LangException('Arg 2 does not exist for function \'%s\'' % type(self).name)

        if type(self.r1(variables)) != str:
            raise LangException(f'Arg 1 must be str for function {type(self).name}')

        return VariableNameValuePair(self.r1(variables), self.r2(variables))

functions = Adder, Subtracter, Printer, Setter, Equals
