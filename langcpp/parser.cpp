#include "parser.h"
#include "utils.h"
#include <unistd.h>
#include <tuple>



void print_node(node* n) {
	std::cout << "Node value: " << n->v << " || ";
	std::cout << "Nodes: ";

	for (auto n : n->nodes) {
		std::cout << n->v << " ";
	}
	std::cout << "\n";
}

void add_node(node* n, std::string v) {
	node* new_node = new node();
	new_node->v = v;
	new_node->nodes = {};
	new_node->parent = n;

	n->nodes.push_back(new_node);
}

node* get_with_stack(node* root, std::vector<int> stack, int* found_status) {
	node* n = root;
	for (auto i : stack) {
		if (i >= n->nodes.size() && n->nodes.size() > 0) {
			*found_status = INDEX_TOO_BIG;
			return NULL;
		} else if (n->nodes.size() == 0) {
			*found_status = NO_NODES;
			return NULL;
		}
		n = n->nodes[i];
	}
	*found_status = NORMAL;
	return n;
}

std::vector<
	std::tuple<node*, int, int, std::vector<int>>
	   > dfs_tree(node* root)
{
    // Return format:
    // Tup: (ptr to node, depth of node, index of node, stack index pointing to node.)
	std::vector<std::tuple<node*, int, int, std::vector<int>>> out_v;

	out_v.push_back(
		std::tuple<node*, int, int, std::vector<int>>(root, 0, 0, {}));
//	print_node(root);
	std::vector<int> stack = {0};
    int index = 0;
	while (true) {
		int status;
		node* n = get_with_stack(root, stack, &status);	

        /*
		for (int i = 0; i < stack.size(); i ++) {
			std::cout << " ";
		}
        */
//		print_node(n);
        index ++;
		out_v.push_back(
			std::tuple<node*, int, int, std::vector<int>>(n, stack.size(), index, stack));


//		parr<int>(stack);

		stack.push_back(0);
		int NEWstat;
		get_with_stack(root, stack, &NEWstat);	
		if (NEWstat == NORMAL) {
			continue;
		} else if (NEWstat == NO_NODES) {
			stack.pop_back();
		}
		stack[stack.size() - 1] ++;
		int new_stat;
		get_with_stack(root, stack, &new_stat);
		while (new_stat == INDEX_TOO_BIG && stack.size() > 1) {
			stack.pop_back();
			stack[stack.size() - 1] ++;
			get_with_stack(root, stack, &new_stat);
//			std::cout << "\t"; parr<int>(stack); std::cout << new_stat << "\n";
		}

		if (stack == std::vector<int>{root->nodes.size()}) {
			break;
		}
	}

	return out_v;
}

node* get_with_index(node* n, int index) {
		std::vector<std::tuple<node*, int, int, std::vector<int>>> pkg; 
        pkg = dfs_tree(n);
        
        for (auto tup : pkg) {
            int INDEX = std::get<2>(tup);
            if (INDEX == index) {
//                std::cout << "\t\t" << std::get<0>(tup)->v << "\n";
                return std::get<0>(tup);
            }
        }
}

node get_ast(std::vector<std::string> toks) {
	node root = {ROOT, {}, NULL};
	node* on_node = &root;

	int index = -1; // The index of the flattened AST (one-dimensional array of nodes produced using depth-first search.)
	// that we are currently..??? while constructing the AST.
	for (auto tok : toks) {
		index ++;
		if (tok == std::string(1, CLOSING_BRACKET_CHAR)) {
			on_node = on_node->parent;
			index --;
			continue;
		}

		add_node(on_node, tok);
		if (tok == std::string(1, OPENING_BRACKET_CHAR)) {
			on_node = get_with_index(&root, index + 1);
		}
	}

    return root;
}

void free_node(node* n) {
	std::vector<std::tuple<node*, int, int, std::vector<int>>> out_v = dfs_tree(n);
	for (auto tup : out_v) {
		delete std::get<0>(tup);
	}

}
