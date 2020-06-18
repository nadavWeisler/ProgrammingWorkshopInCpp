cmake_minimum_required(VERSION 3.14)
project(ex1_sol)

set(CMAKE_CXX_STANDARD 14)


add_executable(ex1_sol main.cpp MlpNetwork.cpp MlpNetwork.h Matrix.cpp Matrix.h Digit.h Dense.cpp Dense.h Activation.cpp Activation.h)