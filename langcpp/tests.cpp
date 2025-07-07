#include <iostream>
#include <cassert>
#include <chrono>
#include <tuple>

#include "utils.h"
#include "lexer.h"
#include "parser.h"


void test_strip_whitespace() {
    std::string file = R"(

         int main()
{}

ff


)";
	std::string stripped = R"(int main()
{}

ff)";
	assert(strip_leading_and_trailing_whitespace(file) == stripped);


	std::string a = " \n\n    f  ";
	std::string as = "f";
	assert(strip_leading_and_trailing_whitespace(a) == as);


	std::string b = "   \n\n   \n";
	assert(strip_leading_and_trailing_whitespace(b) == std::string(""));
}


void test_lexer() {
   	std::string factorial_program_one_line = R"(
(while (< ($ "i") ($ "limit"))
    (print "number: %" ($ "i"))

    (set "j" 1)
    (set "t" 1)
    (while (! (= ($ "j") (+ ($ "i") 1)))
        (set "t" (* ($ "t") ($ "j")))
        (set "j" (+ ($ "j") 1))
    )
    (print "factorial of % is %" ($ "i") ($ "t"))

    (set "i" (+ ($ "i") 1))

);
)";
	std::vector<std::string> toks = {
                                     "(", "while", "(", "<", "(", "$", "\"i\"", ")", "(", "$", "\"limit\"", ")", ")",
                                     "(", "print", "\"number: %\"", "(", "$", "\"i\"", ")", ")",
                                     "(", "set", "\"j\"", "1", ")",

                                     "(", "set", "\"t\"", "1", ")",
                                     "(", "while", "(", "!", "(", "=", "(", "$", "\"j\"", ")", "(", "+", "(", "$", "\"i\"", ")", "1", ")", ")", ")",
                                     "(", "set", "\"t\"", "(", "*", "(", "$", "\"t\"", ")", "(", "$", "\"j\"", ")", ")", ")",
                                     "(", "set", "\"j\"", "(", "+", "(", "$", "\"j\"", ")", "1", ")", ")",
                                     ")",
                                     "(", "print", "\"factorial of % is %\"", "(", "$", "\"i\"", ")", "(", "$", "\"t\"", ")", ")",
                                     "(", "set", "\"i\"", "(", "+", "(", "$", "\"i\"", ")", "1", ")", ")",


                                     ")",};
	assert(lex(factorial_program_one_line) == toks);

	/////
	std::string program1_to_test_final_char_lexes_correctly = R"(
(+ 2 3 (print "af));
)";
	bool exception_thrown = false;
	try {
		lex(program1_to_test_final_char_lexes_correctly);
	} catch (const std::runtime_error &e) {
		exception_thrown = true;
	}
	assert(exception_thrown);


	/////
	std::string program2_to_test_final_char_lexes_correctly = R"(
(while (= 1 1) af
)";
	std::vector<std::string> toks_for_program_2 = {"(", "while", "(", "=", "1", "1", ")", "af"};
	assert(lex(program2_to_test_final_char_lexes_correctly) == toks_for_program_2);


	/////
	std::string program3_to_test_final_char_lexes_correctly = R"(
(while (= 1 "1") af "fds"
)";
	std::vector<std::string> toks_for_program_3 = {"(", "while", "(", "=", "1", "\"1\"", ")", "af", "\"fds\""};
	assert(lex(program3_to_test_final_char_lexes_correctly) == toks_for_program_3);
}


void test_tree_constructs_correctly_and_depth_first_flattening() {
	node* root = new node();
	root->v = "ROOT";
	root->nodes = {};
	root->parent = NULL;

	add_node(root, "first elem");
	add_node(root->nodes[0], "first elem's first elem");
	add_node(root, "second elem");
	add_node(root->nodes[1], "bb");

	assert(root->nodes[0]->v == "first elem");
	assert(root->nodes[0]->nodes.size() == 1);
	assert(root->nodes[0]->parent == root);

	assert(root->nodes[0]->nodes[0]->v == "first elem's first elem");
	assert(root->nodes[0]->nodes[0]->nodes.size() == 0);
	assert(root->nodes[0]->nodes[0]->parent == root->nodes[0]);

	assert(root->nodes[1]->v == "second elem");
	assert(root->nodes[1]->nodes.size() == 1);
	assert(root->nodes[1]->parent == root);

	assert(root->nodes[1]->nodes[0]->v == "bb");
	assert(root->nodes[1]->nodes[0]->nodes.size() == 0);
	assert(root->nodes[1]->nodes[0]->parent == root->nodes[1]);


    DFF_TYPE out_v = depth_first_flatten(root);

	std::tuple<node*, int, int, std::vector<int>> top_out_v(root, 0, 0, {});
	assert(out_v[0] == top_out_v);
	std::tuple<node*, int, int, std::vector<int>> first_out_v(root->nodes[0], 1, 1, {0});
	assert(out_v[1] == first_out_v);
	std::tuple<node*, int, int, std::vector<int>> second_out_v(root->nodes[0]->nodes[0], 2, 2, {0, 0});
	assert(out_v[2] == second_out_v);
	std::tuple<node*, int, int, std::vector<int>> third_out_v(root->nodes[1], 1, 3, {1});
	assert(out_v[3] == third_out_v);
	std::tuple<node*, int, int, std::vector<int>> fourth_out_v(root->nodes[1]->nodes[0], 2, 4, {1, 0});
	assert(out_v[4] == fourth_out_v);

	free_node(root);
}

void test_belongs_to() {
    node* root = new node();
	root->v = "ROOT";
	root->nodes = {};
	root->parent = NULL;

	add_node(root, "first elem");
	add_node(root->nodes[0], "first elem's first elem");
	add_node(root, "second elem");
	add_node(root->nodes[1], "bb");
    
    assert( belongs_to(root, root->nodes[0]->nodes[0]) );

    node* other_node = new node();
    other_node->v = "a";
    other_node->nodes = {};
    other_node->parent = NULL;
    assert( ! belongs_to(root, other_node) );

}


int main()
{
	auto t_start = std::chrono::high_resolution_clock::now();

    // Tests start now
    test_strip_whitespace();
    test_lexer();
    test_tree_constructs_correctly_and_depth_first_flattening();

    test_belongs_to();

    // End of tests

	auto t_end = std::chrono::high_resolution_clock::now();
	std::cout << "\t-----\n\tAll tests succeeded!\n\t-----\n";
	std::chrono::duration<double, std::milli> ms_double = t_end - t_start;
	std::cout << "\tTests took " << ms_double.count() / 1000 << " seconds\n";

    /*
	node* root = new node();
	root->v = "ROOT";
	root->nodes = {};
	root->parent = NULL;

	add_node(root, "first elem");
	add_node(root->nodes[0], "first elem's first elem");
   	add_node(root->nodes[0], "first elem's 2nd elem");
	add_node(root, "second elem");
	add_node(root->nodes[1], "bb");

    print_tree(root);

    node* copy = deepcopy_node(root);
    
    print_tree(copy);
    */                                   
                                                     
	return 0;
}
