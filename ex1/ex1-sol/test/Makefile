CC=g++
CXXFLAGS= -Wall -Wvla -Wextra -Werror -g -std=c++17
LDFLAGS= -lm
HEADERS= ../Matrix.h ../Activation.h ../Dense.h ../MlpNetwork.h ../Digit.h
OBJS= ./obj/Matrix.o ./obj/Activation.o ./obj/Dense.o ./obj/MlpNetwork.o ./obj/Dataset.o ./obj/Tester.o
FILES= ../Matrix.h ../Matrix.cpp ../Activation.h ../Activation.cpp ../Dense.h ../Dense.cpp ../MlpNetwork.h ../MlpNetwork.cpp

./obj/%.o: ../%.cpp
	$(CC) $(CXXFLAGS) -c -o $@ $<

./obj/Dataset.o: Dataset.cpp
	$(CC) $(CXXFLAGS) -c -o $@ $<

./obj/Tester.o: Tester.cpp
	$(CC) $(CXXFLAGS) -c -o $@ $<

test: $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^

run:
	make test
	./test

#$(OBJS) : $(HEADERS)

.PHONY: clean
clean:
	rm -rf ./obj/*.o
	rm -rf test
tar:
	tar -cvf cpp_ex4.tar $(FILES)




