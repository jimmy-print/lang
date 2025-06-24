#include "parser.h"
#include "utils.h"
#include <unistd.h>
#include <tuple>
#include <algorithm>



void print_node(node* n) {
	std::cout << "Node value: " << n->v << " || ";
	std::cout << "Nodes: ";

	for (auto n : n->nodes) {
		std::cout << n->v << " ";
	}
	std::cout << "\n";
}

void print_tree(node* ast) {
    DFF_TYPE pkg = depth_first_flatten(ast);
    for (auto a : pkg) {
        for (int i = 0; i < std::get<1>(a); i++) {
            std::cout << "-";
        }
        std::cout << std::get<0>(a)->v << " | " << std::get<0>(a) << "\n";
    }
}

void add_node(node* n, std::string v) {
	node* new_node = new node();
	new_node->v = v;
	new_node->nodes = {};
	new_node->parent = n;

	n->nodes.push_back(new_node);
}

void add_node_dynobj(node* n, std::string v, dynobj D) {
	node* new_node = new node();
	new_node->v = v;
	new_node->nodes = {};
	new_node->parent = n;
    new_node->D = D;

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

DFF_TYPE depth_first_flatten(node* root)
{
    // Return format:
    // Tup: (ptr to node, depth of node, index of node, stack index pointing to node.)
	std::vector<std::tuple<node*, int, int, std::vector<int>>> out_v;

	out_v.push_back(
                    std::tuple<node*, int, int, std::vector<int>>(root, 0, 0, {}));

	std::vector<int> stack = {0};
    int index = 0;
	while (true) {
		int status;
		node* n = get_with_stack(root, stack, &status);

        index ++;
		out_v.push_back(
                        std::tuple<node*, int, int, std::vector<int>>(n, stack.size(), index, stack));

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
		}

		if (stack == std::vector<int>{root->nodes.size()}) {
			break;
		}
	}

	return out_v;
}

int det_type(std::string raw) {
    if (raw[0] == QUOTE_CHAR and raw[raw.size() - 1] == QUOTE_CHAR) {
        return STR;
    }
    if (std::all_of(raw.begin(), raw.end(), [](char c) {
                                                auto a = std::find(numbers.begin(), numbers.end(), c);
                                                return (a != numbers.end());
        })) {
        return INT;
    }

    int count = 0;
    for (auto c : raw) {
        if (c == '.') {
            count ++;
        }
    }

    if (count == 1) {
        return FLOAT;
    }

    if (raw == NULLREPR) {
        return NULLT;
    }

    if (raw == std::string{OPENING_BRACKET_CHAR}) {
        return BRACK;
    }

    return FUNCT;  // Rn if the function name somehow gets past lexer with its predefined
    // legal function chars, and gets here, it could still be a really crazy function name.
}

void convert_to_typed(node* ast) {
    DFF_TYPE pkg = depth_first_flatten(ast);
    for (auto a : pkg) {
        node* n = std::get<0>(a);

        std::string raw = n->v;
        int type = det_type(raw);

        dynobj D;
        D.type = type;
        switch (type) {
        case STR:
            D.vstr = raw;
            D.vstr.erase(0, 1);  // To remove the " "
            D.vstr.pop_back();
            break;
        case INT:
            D.vint = stoi(raw);
            break;
        case FLOAT:
            D.vfloat = stof(raw);
            break;
        case NULLT:
            D.vnull = raw;
            assert(raw == NULLREPR);
            break;
        case CONTR:
            D.vcontrol = raw;
            break;
        case FUNCT:
            D.vfunction = raw;
            break;
        case VAR:
            D.vvar = raw;
            break;
        case BRACK:
            D.vbrack = raw;
            break;
        }
        n->D = D;
    }
}

std::string extract_string_form(dynobj d) {
    switch (d.type) {
    case STR:
        return d.vstr;
    case INT:
        return std::to_string(d.vint);
    case FLOAT:
        return std::to_string(d.vfloat);
    case NULLT:
        return d.vnull;
    case CONTR:
        return d.vcontrol;
    case FUNCT:
        return d.vfunction;
    case VAR:
        return d.vvar;
    case BRACK:
        return d.vbrack;
    case NTRAN:
        return NTRAN_REPR;
    }
}

bool dynobj_is_truthy(dynobj d) {
    // We define truthy as any INT non 0 or any STR except "". Other types ARE FALSE.
    switch (d.type) {
    case INT:
        if (d.vint == 0) {
            return false;
        }
        return true;
    case STR:
        if (d.vstr == "") {
            return false;
        }
        return true;
    }
    return false;
}

bool operator==(dynobj lhs, dynobj rhs) {
    return (
            lhs.type == rhs.type and
            extract_string_form(lhs) == extract_string_form(rhs)
            );
}

node* get_with_index(node* n, int index) {
    DFF_TYPE pkg = depth_first_flatten(n);

    for (auto tup : pkg) {
        int INDEX = std::get<2>(tup);
        if (INDEX == index) {
            //                std::cout << "\t\t" << std::get<0>(tup)->v << "\n";
            return std::get<0>(tup);
        }
    }
}

node* make_ast(std::vector<std::string> toks) {
    node* root = new node();
    root->v = ROOT;
    root->nodes = {};
    root->parent = NULL;

	node* on_node = root;

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
			on_node = get_with_index(root, index + 1);
		}
	}

    return root;
}

node* deepcopy_node(node* ast)
{
    node* copy = new node();
    copy->v = ast->v;
    copy->D = ast->D;

    node* upper_node = copy;

	std::vector<int> stack = {0};
    int index = 0;
	while (true) {
		int status;
		node* old_node = get_with_stack(ast, stack, &status);

        index ++;

        node* new_copy = new node();
        upper_node->nodes.push_back(new_copy);
        new_copy->v = old_node->v;
        new_copy->D = old_node->D;
        new_copy->parent = upper_node;

		stack.push_back(0);
		int NEWstat;
		get_with_stack(ast, stack, &NEWstat);
		if (NEWstat == NORMAL) {
            upper_node = new_copy;
			continue;
		} else if (NEWstat == NO_NODES) {
			stack.pop_back();

		}
		stack[stack.size() - 1] ++;
		int new_stat;
		get_with_stack(ast, stack, &new_stat);
		while (new_stat == INDEX_TOO_BIG && stack.size() > 1) {
			stack.pop_back();
			stack[stack.size() - 1] ++;
			get_with_stack(ast, stack, &new_stat);
            upper_node = upper_node->parent;
		}

		if (stack == std::vector<int>{ast->nodes.size()}) {
			break;
		}
	}

    return copy;
}

void free_node(node* n) {
	DFF_TYPE all_nodes = depth_first_flatten(n);
	for (auto tup : all_nodes) {
		delete std::get<0>(tup);
	}

}
