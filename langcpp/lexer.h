#ifndef LEXER_H
#define LEXER_H

#include <string>
#include <vector>

std::vector<std::string> lex(std::string line);
std::vector<std::string> expand_sigil(std::vector<std::string> toks);

#endif
