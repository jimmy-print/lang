#include <string>

bool is_whitespace(char c)
{
  switch (c) {
  case ' ':
  case '\n':
    return true;
  }
  return false;
}

std::string strip_leading_and_trailing_whitespace(std::string input)
{
  const int UNSET = -100;

  int i = 0;
  int first_non_whitespace_index = UNSET;
  for (char c : input) {
    if (!is_whitespace(c)) {
      first_non_whitespace_index = i;
      break;
    }
    i++;
  }

  int last_non_whitespace_index = UNSET;
  for (int j = input.size() - 1; j>=0; j--) {
    if (!is_whitespace(input[j])) {
      last_non_whitespace_index = j;
      break;
    }
  }

  if (first_non_whitespace_index == UNSET || last_non_whitespace_index == UNSET) {
    assert(first_non_whitespace_index == last_non_whitespace_index);
    //std::cout << "your string is completely empty\n";
    return std::string("");
  }
  
  input.erase(input.begin() + 0, input.begin() + first_non_whitespace_index);
  input.erase(input.begin() + last_non_whitespace_index - first_non_whitespace_index + 1, input.end());

  return input;
}


