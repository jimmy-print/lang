#include <string>
#include <vector>
#include <iostream>
#include <set>

#ifndef UTIL_H
#define UTIL_H

#define QUOTE_CHAR '\"'
#define OPENING_BRACKET_CHAR '('
#define CLOSING_BRACKET_CHAR ')'
#define LINE_SEPARATOR_CHAR ';'

static const std::set<char> allowed_exposed_chars = {
	'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
	'1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
	'_',
    '.',  // For floats
};

static const std::set<char> operator_chars = {
	'+', '-', '*', '/',
	'!',
	'<', '>',
	'$',
	'=',
};

bool is_whitespace(char c);

template <typename T>
void parr(std::vector<T> arr, std::string sep=" ") {
	for (auto elem : arr) {
		std::cout << elem << sep;
	}
	std::cout << "\n";
}


std::string strip_leading_and_trailing_whitespace(std::string input);

#endif
