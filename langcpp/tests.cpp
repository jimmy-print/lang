#include <iostream>
#include <cassert>
#include <chrono>

#include "utils.h"
#include "processing.h"

#include <unistd.h>


int main()
{
	auto t_start = std::chrono::high_resolution_clock::now();

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



	auto t_end = std::chrono::high_resolution_clock::now();
	std::cout << "\t-----\n\tAll tests succeeded!\n\t-----\n";
	std::chrono::duration<double, std::milli> ms_double = t_end - t_start;
	std::cout << "\tTests took " << ms_double.count() / 1000 << " seconds\n";
	return 0;
}
