#include <vector>
#include <string>
#include <tuple>

#ifndef PARSER_H
#define PARSER_H

#define ROOT "ROOT"

struct node {
	std::string v;
	std::vector<struct node*> nodes;
	struct node* parent;
};
typedef struct node node;

void print_node(node* n);
void add_node(node* n, std::string v);

#define INDEX_TOO_BIG 2
#define NO_NODES 1
#define NORMAL 0
node* get_with_stack(node* root, std::vector<int> stack, int* found_status);

std::vector<
	std::tuple<node*, int, int, std::vector<int>>
	   > dfs_tree(node* root);
#define FORMAT std::vector<std::tuple<node*, int, int, std::vector<int>>>


node* get_with_index(node* n, int index);

node get_ast(std::vector<std::string> toks);


void free_node(node* n);

#endif
