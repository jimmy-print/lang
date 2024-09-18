#include <iostream>
#include <cassert>

#include "utils.h"
#include "processing.h"


int main()
{
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






	std::cout << "\t-----\n\tAll tests succeeded!\n\t-----\n";
	return 0;
}
