#ifndef PARSER_H
#define PARSER_H

#include <vector>
#include <string>
#include <tuple>
#include <cassert>


#define ROOT "ROOT"


#define STR   10000
#define INT   10001
#define FLOAT 10002
#define NULLT 10003
#define CONTR 10004  // Control flow 'function'
#define FUNCT 10005  // 'Real' function name, like +, add, print
#define VAR   10006  // Probably with sigil
#define BRACK 10007  // OPENING_BRACKET_CHAR node
#define NTRAN 10008

#define NULLREPR "VOID"
#define NTRAN_REPR "NTRAN"
struct dynobj {  // A compound struct capable of holding the data of any node in Lang.
    int type;  // Out of the above macros

    int vint;
    std::string vstr;
    float vfloat;
    std::string vnull;
    std::string vcontrol;
    std::string vfunction;
    std::string vvar;
    std::string vbrack;
};
typedef struct dynobj dynobj;

bool operator==(dynobj lhs, dynobj rhs);
    
const std::vector<char> numbers = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'};

struct node {
	std::string v;  // Exactly what is written in the code file.
    dynobj D; 

	std::vector<struct node*> nodes;
	struct node* parent;
};
typedef struct node node;

void print_node(node* n);
void print_tree(node* ast);
void add_node(node* n, std::string v);
void add_node_dynobj(node* n, std::string v, dynobj D);


#define INDEX_TOO_BIG 2
#define NO_NODES 1
#define NORMAL 0
node* get_with_stack(node* root, std::vector<int> stack, int* found_status);

#define DFF_TYPE_MINI std::tuple<node*, int, int, std::vector<int>>
#define DFF_TYPE std::vector<DFF_TYPE_MINI>
DFF_TYPE depth_first_flatten(node* root);
DFF_TYPE depth_first_flatten_not_root(node* n);

int det_type(std::string raw);
void convert_to_typed(node* ast);
std::string extract_string_form(dynobj d);
bool dynobj_is_truthy(dynobj d);

node* get_with_index(node* n, int index);

node* make_ast(std::vector<std::string> toks);
node* deepcopy_node(node* ast);

void free_node(node* n);

#endif
