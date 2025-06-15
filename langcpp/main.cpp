#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <set>

#include "utils.h"
#include "lexer.h"
#include "parser.h"
#include "execute.h"


int main(int argc, char** argv)
{
		std::string code_file_name;
		if (argc > 1) {
				code_file_name = argv[1];
		} else {
				std::cout << "Please provide a code file to run\n";
				return 0;
		}

		std::ifstream stream(code_file_name);
		if (stream.fail()) {
				std::cout << "Couldn't open file with name '" << code_file_name << "'\n";
				return 0;
		}
		std::string raw((std::istreambuf_iterator<char>(stream)),
						(std::istreambuf_iterator<char>()));
		stream.close();

		// Now, remove leading and trailing whitespace from the raw string.
		std::string stripped = strip_leading_and_trailing_whitespace(raw);


		// Split string using ; char.
		std::stringstream ss(stripped);
		std::vector<std::string> splitted;
		std::string temp;
		while (std::getline(ss, temp, LINE_SEPARATOR_CHAR)) {
				splitted.push_back(temp);
		}

		// Remove leading and trailing whitespace for each splitted line.
		for (unsigned int i = 0; i < splitted.size(); i++) {
				splitted[i] = strip_leading_and_trailing_whitespace(splitted[i]);
		}

		// Now turn each line into a series of tokens.
		for (auto line : splitted) {
				std::cout << "Line: " << line << "\n";
				std::vector<std::string> toks = lex(line);

				for (auto s : toks) {
						std::cout << s << " ";
				}
				std::cout << "\n";

				node* ast = make_ast(toks);

				DFF_TYPE pkg = depth_first_flatten(ast);
				for (auto a : pkg) {
						for (int i = 0; i < std::get<1>(a); i++) {
								std::cout << " ";
						}
						std::cout << std::get<0>(a)->v;
						std::cout << " | Stack: ";
						parr<int>(std::get<3>(a));
						std::cout << "\n";
				}


				run(ast);

				std::cout << "--------\n";
				pkg = depth_first_flatten(ast);
				for (auto a : pkg) {
						for (int i = 0; i < std::get<1>(a); i++) {
								std::cout << " ";
						}
						std::cout << std::get<0>(a)->v;
						std::cout << " | Stack: ";
						parr<int>(std::get<3>(a));
						std::cout << "\n";
				}
        }


		return 0;
}
