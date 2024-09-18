#include <vector>
#include <string>
#include <iostream>

#include "utils.h"

std::vector<std::string> lex(std::string line)
{
	std::vector<std::string> toks;
	std::string tok;  // The current token that is being constructed

	bool cut_off_tok;

	bool processing_a_string;

	int i = 0;
	for (auto c : line) {
		char next_c = line[i + 1];
		// TODO issues with the last char.

		i++;


		cut_off_tok = false;
		// During each iteration of this for loop,
		// at the end, if cut_off_tok is true, then
		// what is currently stored in the string buffer will be
		// appended to the final list of tokens.


		if (c == QUOTE_CHAR) {
			processing_a_string = !processing_a_string;
		}


		if (processing_a_string) {
			// Treat it as one massive tok.
			tok.append(std::string(1, c));
			if (next_c == QUOTE_CHAR) {
				tok.append(std::string(1, QUOTE_CHAR));
				cut_off_tok = true;
			}
		}
		else if (!processing_a_string) {
			if (c == OPENING_BRACKET_CHAR) {
				tok.append(std::string(1, c));
				cut_off_tok = true;
			}
			if (c == CLOSING_BRACKET_CHAR) {
				tok.append(std::string(1, c));
				cut_off_tok = true;
			}

			if (allowed_function_chars.find(c) != allowed_function_chars.end()) {
				tok.append(std::string(1, c));
				if (! (allowed_function_chars.find(next_c) != allowed_function_chars.end())) {
					cut_off_tok = true;
				}
			}
			if (operator_chars.find(c) != operator_chars.end()) {
				tok.append(std::string(1, c));
				cut_off_tok = true;
				// this lack of look-forward means that operators can only be  1 char long.
			}

			if (c == '\n' or c == ' ') {
				// Do nothing.
			}
		}


		if (cut_off_tok) {
			toks.push_back(tok);
			tok = "";
		}

	}

	std::cout << "toks: ";
	parr<std::string>(toks, "\n");

	return toks;
}
