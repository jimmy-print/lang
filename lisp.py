code = '''
(add 3 (add 4 (12634781248976)))
'''

# separate code into lines
lines = []
for l in code.strip().split('\n'):
    lines.append(l)

class Atom:
    # (1)
    def __init__(self, val):
        assert type(val) == int
        self.v = val
    def __call__(self):
        return self.v

class Add:
    # (add 1 2)
    # or (add 1 (add 2 3))
    def __init__(self, *args):
        self.args = args
    def __call__(self):
        sum = 0
        for arg in self.args:
            sum += arg()
        return sum

class Sub:
    # (sub 2 1)
    # sub first by second
    def __init__(self, *args):
        self.args = args
    def __call__(self):
        ans = self.args[0]()
        for arg in self.args[1:len(self.args)]:
            ans -= arg()
        return ans


print(lines)
s = lines[0]
# first find index of innermost (
left_paren_i = 0
for c in s:
    left_paren_i += 1
    if c == ')':
        break
for c in reversed(s[0:left_paren_i]):
    left_paren_i -= 1
    if c == '(':
        break

# second find index of innermost )
right_paren_i = left_paren_i - 1
for c in s[left_paren_i:len(s) - 1]:
    right_paren_i += 1
    if c == ')':
        break

# now slice
innermost_atom = s[left_paren_i:right_paren_i + 1]
innermost_no_parens = innermost_atom.strip('(').strip(')')
print(innermost_no_parens)
innermost = Atom(int(innermost_no_parens))


# go out one level

# find next left paren
middle_left_paren_i = left_paren_i
for c in reversed(s[0:left_paren_i]):
    middle_left_paren_i -= 1
    if c == '(':
        break
middle_right_paren_i = right_paren_i
for c in s[right_paren_i:len(s) - 1]:
    middle_right_paren_i += 1
    if c == ')':
        break

# slice
middle_atom = s[middle_left_paren_i:middle_right_paren_i + 1]
middle_no_parens_list = [c for c in middle_atom]
middle_no_parens_list.pop(0)
middle_no_parens_list.pop(len(middle_atom) - 2)  # not 1 because first index already popped
middle_no_parens = ''.join(middle_no_parens_list)
print(middle_no_parens)

middle_list = middle_no_parens.split()
middle = Add(Atom(int(middle_list[1])), innermost)
print(middle())


# get final level
# all lines begin and end with ( and )
final_left_paren_i = 0
final_right_paren_i = len(s) - 1
final_no_parens_list = [c for c in s]
final_no_parens_list.pop(0)
final_no_parens_list.pop()
final_no_parens = ''.join(final_no_parens_list)
final_list = final_no_parens.split()
final = Add(Atom(int(final_list[1])), middle)
print(final())
