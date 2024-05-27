from atoms import *


root = Node("ROOT", None)
root.add(Node("while", None))

while_ = root.nodes[0]
while_.add(Node("=", None))

eq = while_.nodes[0]
eq.add(Node(1, None))
eq.add(Node(1, None))

while_.add(Node("print", None))
print_ = while_.nodes[1]
print_.add(Node("asdf", None))


print(list(thru_giving_depth(root)))

while_stack = [0]
while_node = get_with_stack(root, while_stack)

print(list(thru_giving_depth(while_node)))

print(while_node is root.nodes[0])