#include "parser.h"
#include "utils.h"

#include <iostream>
#include <cassert>
#include <algorithm>
#include <numeric>
#include <string>
#include <unordered_map>

#include <unistd.h>

const std::string TRUE("TRUEE");
const std::string FALSE("FALSEEE");
const std::string NOT_RAN("NOT_RAN");

int add(std::vector<int> args) {
		return accumulate(std::begin(args), std::end(args), 0);
}

int subtract(std::vector<int> args) {
		assert(args.size() == 2);
		return (args[0] - args[1]);
}

const std::unordered_map<std::string, int(*)(std::vector<int>)> fs = {
		{"+", add},
		{"-", subtract}
};

void run(node* ast)
{
        std::vector<int> stack = {0};

        int TRASH;

        while (stack != std::vector<int>(1, 1)) {
                stack.push_back(0);
                int status;
                get_with_stack(ast, stack, &status);
                if (status == NORMAL) {
                        std::cout << "\t";
                        parr<int>(stack);
                        std::cout << "jumping forward\n";
                        continue;
                } else if (status == NO_NODES) {

                        stack.pop_back();
                        parr<int>(stack);
                }
                stack.back() ++;
                while (stack != std::vector(1, 1)) {
                        get_with_stack(ast, stack, &status);
                        parr<int>(stack);
                        std::cout << "status: " << status << "\n";
                        if (status != INDEX_TOO_BIG) {
                                std::cout << "broken\n";
                                break;
                        }

                        std::vector<int> last_arg_node_stack(stack);
                        last_arg_node_stack.back() --;
                        node* last_arg_node = get_with_stack(ast, last_arg_node_stack, &TRASH);

                        node* parent_paren_node = last_arg_node->parent;
                        std::vector<int> parent_paren_node_stack(last_arg_node_stack);
                        parent_paren_node_stack.pop_back();

                        node* function_node = parent_paren_node->nodes[0];


                        for (auto current_level_node : parent_paren_node->nodes) {
                                std::cout << "\t\t" << current_level_node->v << "\n";
                                assert(current_level_node->nodes.size() == 0);
                        }

                        std::vector<int> args(parent_paren_node->nodes.size() - 1);
                        for (int i = 1; i < parent_paren_node->nodes.size(); i ++) {
                                args[i - 1] = stoi(parent_paren_node->nodes[i]->v);
                        }

                        std::vector<node*> ancestor_control_nodes;
                        // The paren, not the first 'arg' which is the function node.
                        std::vector<std::vector<int>> ancestor_control_nodes_stacks;

                        std::vector<int> search_stack(last_arg_node_stack);
                        search_stack.pop_back();

                        while (get_with_stack(ast, search_stack, &TRASH)->v != ROOT) {

								node* potential_control_node = get_with_stack(ast, search_stack, &TRASH);
                                if ((potential_control_node->nodes[0]->v == "if" or potential_control_node->nodes[0]->v == "while") and search_stack != parent_paren_node_stack) {
                                        ancestor_control_nodes_stacks.push_back(std::vector<int>(search_stack));
                                        ancestor_control_nodes.push_back(potential_control_node);
                                }
                                search_stack.pop_back();
                        }

                        bool parent_paren_is_top_level = (ancestor_control_nodes.size() == 0);
                        std::string r;
                        if (parent_paren_is_top_level) {
								int(*f)(std::vector<int>) = fs.at(function_node->v);
                                r = std::to_string(f(args));
                        } else {
                                bool all_true = std::all_of(ancestor_control_nodes.begin(), ancestor_control_nodes.end(),
															[](node* n) {return n->nodes[2]->v == TRUE;});
                                if (all_true) {
                                        //r = f(args);
                                } else {
                                        //r = NOT_RAN;
                                }
                        }

                        bool cond_was_false = parent_paren_node->nodes[1]->v == FALSE;

                        std::vector<node*> sliced(parent_paren_node->nodes.begin() + 1, parent_paren_node->nodes.end());
                        bool nothing_ran = std::all_of(sliced.begin(), sliced.end(), [](node* n) {return n->v == NOT_RAN;});

                        if (function_node->v == "while" and not nothing_ran and not cond_was_false) {
                                std::cout << "1\n";
                                exit(1);
                        } else if (function_node->v == "while" and nothing_ran and cond_was_false) {
                                std::cout << "2\n";
                                exit(1);
                        } else {
                                parent_paren_node->v = r;
                                parent_paren_node->nodes = {};
                                stack.pop_back();
                                stack.back() ++;
                                std::cout << "3\n";
                                //exit(1);
                        }
                        std::cout << "stuck\n";
                }

        }
}



