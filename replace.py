from atoms import *

a = Root()
a.add(Node('+', None))

a.nodes[0].add(Node('-', None))
a.nodes[0].add(Node('+', None))

a.nodes[0].nodes[0].add(Node(1, None))
a.nodes[0].nodes[0].add(Node(2, None))

a.nodes[0].nodes[1].add(Node(3, None))
a.nodes[0].nodes[1].add(Node(4, None))

print(get_vis_stack_str(a, printid=True))

lowers = []

for i, O in enumerate(thru_giving_depth_and_stack(a)):
    if i != 0:
        print(O)
        lowers.append(list(O[:3]))
        lowers[i-1].append(O[3][:])

print()

b = Root('other!')

for lower in lowers:
    print(lower)
    print(get_with_stack(b, lower[-1][:-1]))
    parent = get_with_stack(b, lower[-1][:-1])

    val = lower[1].v
    cl = lower[2]

    parent.add(cl(val, None))

print(get_vis_stack_str(b, printid=True))

# Now use stack to dupe a into b without using deepcopy
# Make new object IDs.
