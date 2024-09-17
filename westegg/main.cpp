#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>

#include "utils.h"

#define QUOTE_CHAR '\"'
#define OPENING_BRACKET_CHAR '('
#define CLOSING_BRACKET_CHAR ')'
#define LINE_SEPARATOR_CHAR ';'


std::vector<std::string> lex(std::string line);


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
        for (int i = 0; i < splitted.size(); i++) {
                splitted[i] = strip_leading_and_trailing_whitespace(splitted[i]);
        }        

        for (auto line : splitted) {
                std::cout << "Line: " << line << "\n";
                lex(line);
        }


        return 0;
}


std::vector<std::string> lex(std::string line)
{
        bool in_quotes = false;

        std::vector<std::string> toks;
        std::string tok;  // The current token that is being constructed

        bool cut_off_tok;

        for (auto c : line) {
                cut_off_tok = false;

                if (in_quotes) {
                        if (c == QUOTE_CHAR) {
                                in_quotes = false;
                        }
                } else if (!in_quotes) {
                        switch (c) {
                        case QUOTE_CHAR:
                                in_quotes = true;
                                break;
                        case OPENING_BRACKET_CHAR:
                                tok = c;
                                cut_off_tok = true;

                                break;
                        case CLOSING_BRACKET_CHAR:
                                tok = c;
                                cut_off_tok = true;

                                break;
                        case '\n':
                                break;
                        case ' ':
                                break;
                        }
                }

                if (cut_off_tok) {
                        toks.push_back(tok);
                }

                std::cout << c << "||" << in_quotes << "\n";

        }

        return toks;
}

