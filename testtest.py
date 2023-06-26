import atoms
import ll

t = ll.get_tree(
    ['(', '+', '1', '2', ')']
)

print(t.v)
print('\t'+t.nodes[0].v)
[print('\t\t'+str(node.v)) for node in t.nodes[0].nodes]