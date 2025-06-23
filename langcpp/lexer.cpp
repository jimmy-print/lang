#include <vector>
#include <string>
#include <iostream>

#include "utils.h"

std::vector<std::string> lex(std::string line)
{
	std::vector<std::string> toks;
	std::string tok;  // The current token that is being constructed

	bool cut_off_tok;

	bool processing_a_string = false;

	bool on_last_char = false;
	int i = 0;
	for (auto c : line) {
		char next_c = line[i + 1];
		if (((long unsigned int) (i + 1)) == line.size()) {
			// So, if @next_c is now reading past the last char in @line.
			on_last_char = true;
			// At this point, @next_c should not be read in any subsequent lines of code.
			// Therefore, below, this case is handled in 2 ways:
			//  1. If the last char is within an unterminated string, we detect that
			//     and throw a runtime error. This way, 'next_c == QUOTE_CHAR' is never ran.
			//  2. If the last char is part of a function, so like 'f' in (abc "a" "b" (abcdef <-,
			//     we still add it to the current tok and then add that tok to the toks.
			//  Otherwise, the last char is guaranteed to be either whitespace, quote char, or
			//  a bracket. These ones can be handled normally. In the case of the quote_char,
			//  the *previous* for loop iteration would've added the current c, the last char, to the tok,
			//  which was then added to toks on that last loop.
		}
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
			if (on_last_char) {
				throw std::runtime_error("unbalanced closing apostrophe");
			}

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

			if (allowed_exposed_chars.find(c) != allowed_exposed_chars.end()) {
				tok.append(std::string(1, c));
				if (on_last_char) {
					cut_off_tok = true;
				} else {
					if (allowed_exposed_chars.find(next_c) == allowed_exposed_chars.end()) {
						cut_off_tok = true;
                        // This may be wrong. It should probably throw an error instead.
                        // Otherwise something like (+ 3#%^3 1) would lex to ( + 3 3 1 )
					}
				}
			}
			if (operator_chars.find(c) != operator_chars.end()) {
				tok.append(std::string(1, c));
				cut_off_tok = true;
				// this lack of look-forward means that operators can only be 1 char long.
			}

			if (c == '\n' or c == ' ') {
				// Do nothing. Whitespace is thus ignored by the lexer.
			}
		}


		if (cut_off_tok) {
			toks.push_back(tok);
			tok = "";
		}

	}

	return toks;
}
