CC=g++

all: lang tests

SRCS=main.cpp utils.cpp lexer.cpp parser.cpp
HDRS=utils.h lexer.h parser.h

SRCS_TESTING=tests.cpp utils.cpp lexer.cpp parser.cpp
# The lack of main.cpp in the above is because the main.cpp file should only 
# deal with the entry point, running the interpreter itself.
# Functions that are unit tested should be in other files.

lang: $(SRCS) $(HDRS)
	$(CC) -o lang $(SRCS) -Wall -std=c++17

tests: $(SRCS_TESTING) $(HDRS)
	$(CC) -o tests $(SRCS_TESTING) -Wall -std=c++17 -g
