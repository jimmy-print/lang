CC=g++

all: lang tests

lang: main.cpp utils.cpp utils.h
	$(CC) -o lang main.cpp utils.cpp -Wall -std=c++20

tests: basic_tests.cpp utils.cpp utils.h
	$(CC) -o tests basic_tests.cpp utils.cpp -Wall -std=c++20
