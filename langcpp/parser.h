#ifndef PARSER_H
#define PARSER_H

#include <vector>
#include <string>
#include <tuple>


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

#define DFF_TYPE std::vector<std::tuple<node*, int, int, std::vector<int>>>
DFF_TYPE depth_first_flatten(node* root);


node* get_with_index(node* n, int index);

node* make_ast(std::vector<std::string> toks);


void free_node(node* n);

#endif
