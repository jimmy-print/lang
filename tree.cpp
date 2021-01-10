#include <stdlib.h>
#include <stdio.h>

#include <vector>

struct Node {
	int v;
	struct Node *n1;
	struct Node *n2;
};

void depth_first_search(struct Node *node, struct Node *up_node, int i)
{
	printf("%d %d\n", node->v, i);
	if (node->n1 != NULL) {
		i++;
		depth_first_search(node->n1, node, i);
	}
	if (node->n2 != NULL) {
		i++;
		depth_first_search(node->n2, node, i);
	}
}

int main()
{
	struct Node root_node = {0, NULL, NULL};
	struct Node left_node = {1, NULL, NULL};
	struct Node right_node = {2, NULL, NULL};
	struct Node right_left_node = {3, NULL, NULL};
	struct Node right_right_node = {4, NULL, NULL};

	struct Node right_left_left_node = {5, NULL, NULL};
	struct Node right_left_right_node = {6, NULL, NULL};
	struct Node right_right_left_node = {7, NULL, NULL};
	struct Node right_right_right_node = {8, NULL, NULL};
	
	root_node.n1 = &left_node;
	root_node.n2 = &right_node;
	right_node.n1 = &right_left_node;
	right_node.n2 = &right_right_node;

	right_left_node.n1 = &right_left_left_node;
	right_left_node.n2 = &right_left_right_node;
	right_right_node.n1 = &right_right_left_node;
	right_right_node.n2 = &right_right_right_node;

	depth_first_search(&root_node, &root_node, 0);

}
