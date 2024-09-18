#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <set>

#include "utils.h"
#include "processing.h"


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
		lex(line);
	}


	return 0;
}
