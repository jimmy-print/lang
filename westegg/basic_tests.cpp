#include "utils.h"
#include <iostream>

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



	std::cout << "\t-----\n\tAll tests succeeded!\n\t-----\n";

	return 0;
}
