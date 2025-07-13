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

dynobj NOT_RAN;

dynobj add(std::vector<dynobj> args) {
    int ret_type;
    if (std::any_of(args.cbegin(), args.cend(), [](dynobj D){ return D.type == FLOAT; })) {
        // If any arguments to (+ ... ... ...) is a float, the return type will decay to float.
        ret_type = FLOAT;
    } else if (std::all_of(args.cbegin(), args.cend(), [](dynobj D){ return D.type == INT; })) {
        // All arguments must be int for the return type to stay as int.
        ret_type = INT;
    }

    if (not std::all_of(args.cbegin(), args.cend(), [](dynobj D){ return D.type == FLOAT or D.type == INT;})) {
        // Arguments include a type other than int or float.
        throw std::runtime_error("add + function received invalid argument(s) of type other than int or float.");
    }

    dynobj ret;
    if (ret_type == FLOAT) {
        float sum = 0.0;
        for (auto D : args) {
            if (D.type == FLOAT) {
                sum += D.vfloat;
            } else if (D.type == INT) {
                sum += (float) D.vint;
            } else {
                throw std::runtime_error("this should never happen, should've been caught previously");
            }
        }
        ret.type = FLOAT;
        ret.vfloat = sum;
    } else if (ret_type == INT) {
        int sum = 0;
        for (auto D : args) {
            if (D.type == FLOAT) {
                sum += (int) D.vfloat;
            } else if (D.type == INT) {
                sum += D.vint;
            } else {
                throw std::runtime_error("this should never happen, should've been caught previously");
            }
        }
        ret.type = INT;
        ret.vint = sum;
    }
    return ret;
}

dynobj multiply(std::vector<dynobj> args) {
    int ret_type;
    if (std::any_of(args.cbegin(), args.cend(), [](dynobj D){ return D.type == FLOAT; })) {
        ret_type = FLOAT;
    } else if (std::all_of(args.cbegin(), args.cend(), [](dynobj D){ return D.type == INT; })) {
        ret_type = INT;
    }

    if (not std::all_of(args.cbegin(), args.cend(), [](dynobj D){ return D.type == FLOAT or D.type == INT;})) {
        throw std::runtime_error("multiply * function received invalid argument(s) of type other than int or float.");
    }

    dynobj ret;
    if (ret_type == FLOAT) {
        float prod = 1.0;
        for (auto D : args) {
            if (D.type == FLOAT) {
                prod *= D.vfloat;
            } else if (D.type == INT) {
                prod *= (float) D.vint;
            } else {
                throw std::runtime_error("this should never happen, should've been caught previously");
            }
        }
        ret.type = FLOAT;
        ret.vfloat = prod;
    } else if (ret_type == INT) {
        int prod = 1;
        for (auto D : args) {
            if (D.type == FLOAT) {
                prod *= (int) D.vfloat;
            } else if (D.type == INT) {
                prod *= D.vint;
            } else {
                throw std::runtime_error("this should never happen, should've been caught previously");
            }
        }
        ret.type = INT;
        ret.vint = prod;
    }
    return ret;
}

dynobj subtract(std::vector<dynobj> args) {
    assert(args.size() == 2);
    int ret_type;
    if (std::any_of(args.cbegin(), args.cend(), [](dynobj D){ return D.type == FLOAT; })) {
        // If any arguments to (- ... ...) is a float, the return type will decay to float.
        ret_type = FLOAT;
    } else if (std::all_of(args.cbegin(), args.cend(), [](dynobj D){ return D.type == INT; })) {
        // All arguments must be int for the return type to stay as int.
        ret_type = INT;
    }

    if (not std::all_of(args.cbegin(), args.cend(), [](dynobj D){ return D.type == FLOAT or D.type == INT;})) {
        // Arguments include a type other than int or float.
        throw std::runtime_error("minus - function received invalid argument(s) of type other than int or float.");
    }

    dynobj ret;
    if (ret_type == FLOAT) {
        float init = (args[0].type == FLOAT) ? args[0].vfloat : (float) args[0].vint;
        init -= (args[1].type == FLOAT) ? args[1].vfloat : (float) args[1].vint;
        ret.type = FLOAT;
        ret.vfloat = init;
    } else if (ret_type == INT) {
        float init = (args[0].type == FLOAT) ? (int) args[0].vfloat : args[0].vint;
        init -= (args[1].type == FLOAT) ? (int) args[1].vfloat : args[1].vint;
        ret.type = INT;
        ret.vint = init;
    }
    return ret;
}


dynobj lessthan(std::vector<dynobj> args) {
    assert(args.size() == 2);
    
    if (not std::all_of(args.cbegin(), args.cend(), [](dynobj D){ return D.type == FLOAT or D.type == INT;})) {
        // Arguments include a type other than int or float.
        throw std::runtime_error("lessthan < function received invalid argument(s) of type other than int or float.");
    }

    dynobj ret;
    ret.type = INT;
    if (args[0].type == INT and args[1].type == INT) {
        ret.vint = args[0].vint < args[1].vint;
    } else if (args[0].type == INT and args[1].type == FLOAT) {
        ret.vint = (float) args[0].vint < args[1].vfloat;
    } else if (args[0].type == FLOAT and args[1].type == FLOAT) {
        ret.vint = args[0].vfloat < args[1].vfloat;
    } else if (args[0].type == FLOAT and args[1].type == INT) {
        ret.vint = args[0].vfloat < (float) args[1].vint;
    }
    return ret;
}

dynobj modulo(std::vector<dynobj> args) {
    assert(args.size() == 2);
    
    if (not std::all_of(args.cbegin(), args.cend(), [](dynobj D){ return D.type == INT;})) {
        throw std::runtime_error("modulo % function received invalid argument(s) of type other than int");
    }

    dynobj ret;
    ret.type = INT;
    ret.vint = args[0].vint % args[1].vint;
    return ret;
}

dynobj equals(std::vector<dynobj> args) {
    assert(args.size() == 2);
    
    dynobj ret;
    ret.type = INT;
    ret.vint = args[0] == args[1];
    return ret;
}

dynobj print(std::vector<dynobj> args) {
    std::cout << "\033[0;30;46m";
    std::string sep(" ");
    int i = 0;
    for (auto D : args) {
        std::cout << extract_string_form(D) << ((i == args.size() - 1) ? "" : sep);
        i++;
    }
    std::cout << "\033[0m\n";
    dynobj ret;
    ret.type = NULLT;
    ret.vnull = NULLREPR;
    return ret;
}

dynobj while_(std::vector<dynobj> args) {
    dynobj ret;
    ret.type = NULLT;
    ret.vnull = NULLREPR;
    return ret;
}

dynobj if_(std::vector<dynobj> args) {
    dynobj ret;
    ret.type = NULLT;
    ret.vnull = NULLREPR;
    return ret;
}

std::unordered_map<std::string, dynobj> global_vars;

dynobj setvar(std::vector<dynobj> args) {
    // (set "disciples" 12);
    assert(args.size() == 2);

    if (not (args[0].type == STR)) {
        throw std::runtime_error("variable name must be of string type");
    }

    global_vars[args[0].vstr]= args[1];
    
    dynobj ret;
    ret.type = NULLT;
    ret.vnull = NULLREPR;
    return ret;
}

dynobj getvar(std::vector<dynobj> args) {
    // ($ "disciples") -> 12;
    assert(args.size() == 1);

    if (not (args[0].type == STR)) {
        throw std::runtime_error("variable name must be of string type");
    }
    dynobj var_value = global_vars.at(args[0].vstr);
    return var_value;
}

dynobj wait(std::vector<dynobj> args) {
    sleep(1);
    dynobj ret;
    ret.type = NULLT;
    ret.vnull = NULLREPR;
    return ret;
}

const std::unordered_map<std::string, dynobj(*)(std::vector<dynobj>)> functions = {
    {"+", add},
    {"-", subtract},
    {"<", lessthan},
    {"%", modulo},
    {"=", equals},
    {"*", multiply},
    
    {"print", print},
    
    {"while", while_},
    {"if", if_},
    
    {"set", setvar},
    {"$", getvar},

    {"wait", wait}
};

void run(node* ast)
{
    std::vector<int> stack = {0};

    int TRASH;

    NOT_RAN.type = NTRAN;

    node* orig_tree = deepcopy_node(ast);

    while (stack != std::vector<int>(1, 1)) {
        stack.push_back(0);
        int status;
        get_with_stack(ast, stack, &status);
        if (status == NORMAL) {
            continue;
        } else if (status == NO_NODES) {
            stack.pop_back();
        }
        stack.back() ++;
        while (stack != std::vector(1, 1)) {
            get_with_stack(ast, stack, &status);
            if (status != INDEX_TOO_BIG) {
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
                assert(current_level_node->nodes.size() == 0);
            }

            std::vector<dynobj> args(parent_paren_node->nodes.size() - 1);
            for (int i = 1; i < parent_paren_node->nodes.size(); i ++) {
                args[i - 1] = parent_paren_node->nodes[i]->D;
            }

            std::vector<node*> ancestor_control_nodes;
            // The paren, not the first 'arg' which is the function node.
            std::vector<std::vector<int>> ancestor_control_nodes_stacks;

            std::vector<int> search_stack(last_arg_node_stack);

            search_stack.pop_back();
            search_stack.pop_back();

            while (get_with_stack(ast, search_stack, &TRASH)->v != ROOT) {

                node* potential_control_node = get_with_stack(ast, search_stack, &TRASH);
                if ((potential_control_node->nodes[0]->v == "if" or potential_control_node->nodes[0]->v == "while")) {
                    ancestor_control_nodes_stacks.push_back(std::vector<int>(search_stack));
                    //parr<int>(search_stack);
                    ancestor_control_nodes.push_back(potential_control_node);
                }
                search_stack.pop_back();
            }

            //            std::for_each(ancestor_control_nodes.begin(), ancestor_control_nodes.end(), [](node* n) {print_node(n);});
            bool all_true = std::all_of(ancestor_control_nodes.begin(), ancestor_control_nodes.end(),
                                            [](node* n) {return dynobj_is_truthy(n->nodes[1]->D);});
            bool directly_execute = false;
            if (ancestor_control_nodes.size() == 1) {
                if (belongs_to(ancestor_control_nodes[0]->nodes[1], parent_paren_node)) {
                    directly_execute = true;
                }
            } else if (ancestor_control_nodes.size() > 1) {
                if (belongs_to(ancestor_control_nodes[0]->nodes[1], parent_paren_node)) {
                    ancestor_control_nodes.erase(ancestor_control_nodes.begin());
                    all_true = std::all_of(ancestor_control_nodes.begin(), ancestor_control_nodes.end(),
                                            [](node* n) {return dynobj_is_truthy(n->nodes[1]->D);});
                }
            }

            /*
            // Figure out if the parent_paren is the first arg of a top level control node.
            if (ancestor_control_nodes.size() == 1) {
                if (parent_paren_node == ancestor_control_nodes[0]->nodes[1]) {
                    directly_execute = true;
                }
            }
            */

            dynobj r;
            dynobj(*f)(std::vector<dynobj>);
            try {
                f = functions.at(function_node->D.vfunction);
            } catch (std::exception &e) {
                std::cout << e.what() << "\n";
                std::cout << "the function name that threw this exception is: " << extract_string_form(function_node->D) << "\n";
            }
            if (directly_execute) {
                r = f(args);
            } else {
                if (all_true) {
                    r = f(args);
                } else {
                    r = NOT_RAN;
                }
            }


            bool cond_was_false = not dynobj_is_truthy(parent_paren_node->nodes[1]->D);

            std::vector<node*> sliced(parent_paren_node->nodes.begin() + 1, parent_paren_node->nodes.end());
            bool nothing_ran = std::all_of(sliced.begin(), sliced.end(), [](node* n) {return n->D == NOT_RAN;});

            if (function_node->v == "while" and not nothing_ran and not cond_was_false) {
                std::vector<int> while_stack(stack);
                while_stack.pop_back();

                node* orig_while_node = get_with_stack(orig_tree, while_stack, &TRASH);
                //print_node(orig_while_node);
                
                DFF_TYPE lowers;
                DFF_TYPE pkg = depth_first_flatten(orig_while_node);

                int i = 0;
                for (auto a : pkg) {
                    if (i != 0) {
                        lowers.push_back(DFF_TYPE_MINI(a));
                        std::get<3>(lowers[i - 1]) = std::vector<int>(std::get<3>(a));
                    }
                    i++;
                }

                node* to_be_replaced_while_node = get_with_stack(ast, while_stack, &TRASH);
                for (auto n : to_be_replaced_while_node->nodes) {
                    free_node(n);
                }
                to_be_replaced_while_node->nodes = {};

                int jj = 0;
                for (auto b : lowers) {
                    std::vector<int> asdf = std::get<3>(b);
                    asdf.pop_back();
                    node* parent = get_with_stack(to_be_replaced_while_node, asdf, &TRASH);
                    if (jj == 0) {
                        assert( parent == to_be_replaced_while_node );
                    }
                    jj++;
                    
                    dynobj D = std::get<0>(b)->D;
                    std::string v = std::get<0>(b)->v;
                    add_node_dynobj(parent, v, D);                }
                stack.pop_back();
            } else {
                parent_paren_node->D = r;
                parent_paren_node->v = extract_string_form(parent_paren_node->D);
                for (auto n : parent_paren_node->nodes) {
                    free_node(n);
                }
                parent_paren_node->nodes = {};
                stack.pop_back();
                stack.back() ++;
            }
        }
    }


    free_node(orig_tree);
    free_node(ast);
}

