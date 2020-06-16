CC=g++
CXXFLAGS= -Wall -Wvla -Wextra -Werror -g -std=c++17
LDFLAGS= -lm
HEADERS= Matrix.h Activation.h Dense.h MlpNetwork.h Digit.h
OBJS= Matrix.o Activation.o Dense.o MlpNetwork.o

%.o : %.c

all: mlpnetwork matrix_valid matrix_invalid simple_main

mlpnetwork: $(OBJS) main.o
	$(CC) $(LDFLAGS) -o $@ $^

simple_main: $(OBJS) simple_main.o
	$(CC) $(LDFLAGS) -o $@ $^

matrix_valid: $(OBJS) t_matrix_valid.o
	$(CC) $(LDFLAGS) -o $@ $^

matrix_invalid: $(OBJS) t_matrix_invalid.o
	$(CC) $(LDFLAGS) -o $@ $^


$(OBJS) : $(HEADERS)

.PHONY: clean
clean:
	rm -rf *.o
	rm -rf mlpnetwork
	rm -rf simple_main
	rm -rf matrix_valid
	rm -rf matrix_invalid




